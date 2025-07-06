#!/usr/bin/env python3
"""
MCP Server for Graphic Design Analysis
Provides tools for analyzing graphic design images using OpenAI's vision model
"""

import asyncio
import os
import base64
import requests
import io
from typing import Any, Dict, List
from openai import OpenAI
from fastmcp import FastMCP
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Initialize FastMCP server
mcp = FastMCP("Graphic Design MCP")

def create_analysis_report(analysis_type: str, scores: dict, image_url: str = None) -> str:
    """
    Create a visual PNG report of the analysis results.
    
    Args:
        analysis_type: Type of analysis (design or copywriting)
        scores: Dictionary of scores and feedback
        image_url: Original image URL (optional)
        
    Returns:
        Base64 encoded PNG image
    """
    try:
        # Create a large canvas for the report
        width, height = 800, 1000
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to load a font (fallback to default if not available)
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
            header_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
            text_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Colors
        primary_color = '#2563eb'
        secondary_color = '#64748b'
        accent_color = '#10b981'
        
        y = 30
        
        # Title
        title = f"🎨 {analysis_type.upper()} ANALYSIS REPORT"
        draw.text((50, y), title, fill=primary_color, font=title_font)
        y += 60
        
        # Draw a line
        draw.line([(50, y), (750, y)], fill=secondary_color, width=2)
        y += 30
        
        # Overall score calculation
        if scores:
            total_score = sum(scores.values()) / len(scores)
            score_color = accent_color if total_score >= 7 else '#f59e0b' if total_score >= 5 else '#ef4444'
            
            # Overall score box
            draw.rectangle([(50, y), (750, y+60)], fill=score_color, outline=score_color)
            draw.text((60, y+15), f"📊 OVERALL SCORE: {total_score:.1f}/10", 
                     fill='white', font=header_font)
            y += 80
            
            # Individual scores
            for category, score in scores.items():
                score_text = f"• {category}: {score}/10"
                draw.text((60, y), score_text, fill=secondary_color, font=text_font)
                
                # Score bar
                bar_width = int((score / 10) * 200)
                draw.rectangle([(300, y+5), (500, y+15)], fill='#e5e7eb', outline='#e5e7eb')
                draw.rectangle([(300, y+5), (300+bar_width, y+15)], fill=score_color, outline=score_color)
                y += 35
        
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((50, height-40), f"Generated: {timestamp}", fill=secondary_color, font=text_font)
        
        # Save to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Save to file as well
        filename = f"{analysis_type}_report_{int(datetime.now().timestamp())}.png"
        img.save(filename)
        
        return base64.b64encode(buffer.getvalue()).decode(), filename
        
    except Exception as e:
        return None, f"Error creating report: {str(e)}"

@mcp.tool()
def analyze_design(url: str) -> str:
    """
    Analyze graphic design and provide detailed feedback on visual elements.
    
    This tool downloads an image from the provided URL and analyzes it using OpenAI's vision model.
    It provides scores and feedback on Visual Harmony, Clarity, User Friendliness, Interactivity, and Creativity.
    
    Args:
        url: The URL of the image to analyze (must be a valid HTTP/HTTPS URL)
        
    Returns:
        A detailed analysis of the graphic design with scores and recommendations
    """
    try:
        # Validate and clean URL
        if not url or not url.strip():
            return "❌ Error: URL cannot be empty"
        
        url = url.strip().lstrip('@')
        
        if not url.startswith(('http://', 'https://')):
            return "❌ Error: Please provide a valid HTTP/HTTPS URL"
        
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "❌ Error: OPENAI_API_KEY environment variable not found. Please set your OpenAI API key."
        
        # Download image with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Check if the content is an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            return "❌ Error: The provided URL does not point to an image file"
        
        # Encode image to base64
        image_data = base64.b64encode(response.content).decode()
        
        # Create OpenAI client and analyze
        client = OpenAI(api_key=api_key)
        
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text", 
                            "text": """Analyze this graphic design in detail. Please provide ONLY numerical scores (1-10) for each category, then detailed feedback:

SCORES (format: "Category: X/10"):
1. Visual Harmony: X/10
2. Clarity: X/10  
3. User Friendliness: X/10
4. Interactivity: X/10
5. Creativity: X/10

Then provide detailed feedback for each category and overall recommendations."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                        }
                    ]
                }
            ],
            max_tokens=1200,
            temperature=0.7
        )
        
        analysis = result.choices[0].message.content
        
        # Extract scores for PNG generation
        scores = {}
        lines = analysis.split('\n')
        for line in lines:
            if any(category in line for category in ['Visual Harmony', 'Clarity', 'User Friendliness', 'Interactivity', 'Creativity']):
                if '/10' in line:
                    try:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            category = parts[0].strip().replace('*', '').replace('#', '').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').strip()
                            score_part = parts[1].strip()
                            score = float(score_part.split('/')[0].strip())
                            scores[category] = score
                    except:
                        continue
        
        # Generate PNG report
        report_image, filename = create_analysis_report("Design", scores, url)
        
        # Format the response with emojis and better structure
        formatted_response = f"""
🎨 **GRAPHIC DESIGN ANALYSIS REPORT**

📋 **ANALYSIS RESULTS:**
{analysis}

🖼️ **VISUAL REPORT:** 
✅ PNG report generated: `{filename}`

🔗 **ANALYZED IMAGE:** {url}

📊 **QUICK SUMMARY:**
"""
        
        if scores:
            overall_score = sum(scores.values()) / len(scores)
            if overall_score >= 8:
                formatted_response += f"🌟 **EXCELLENT** - Overall Score: {overall_score:.1f}/10"
            elif overall_score >= 6:
                formatted_response += f"👍 **GOOD** - Overall Score: {overall_score:.1f}/10"
            elif overall_score >= 4:
                formatted_response += f"⚠️ **NEEDS IMPROVEMENT** - Overall Score: {overall_score:.1f}/10"
            else:
                formatted_response += f"❌ **POOR** - Overall Score: {overall_score:.1f}/10"
        
        formatted_response += "\n\n---\n*✨ Analysis powered by OpenAI GPT-4 Vision*"
        
        return formatted_response
        
    except requests.exceptions.RequestException as e:
        return f"❌ **Network Error:** Could not download image from URL. {str(e)}"
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

@mcp.tool()
def analyze_copywriting(url: str) -> str:
    """
    Analyze copywriting in images and provide scoring with alternative suggestions.
    
    This tool downloads an image from the provided URL and analyzes any text/copywriting present.
    It provides scores on effectiveness, clarity, persuasiveness, and offers alternative copywriting suggestions.
    
    Args:
        url: The URL of the image to analyze (must be a valid HTTP/HTTPS URL)
        
    Returns:
        A detailed analysis of the copywriting with scores and alternative suggestions
    """
    try:
        # Validate and clean URL
        if not url or not url.strip():
            return "❌ Error: URL cannot be empty"
        
        url = url.strip().lstrip('@')
        
        if not url.startswith(('http://', 'https://')):
            return "❌ Error: Please provide a valid HTTP/HTTPS URL"
        
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "❌ Error: OPENAI_API_KEY environment variable not found. Please set your OpenAI API key."
        
        # Download image with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Check if the content is an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            return "❌ Error: The provided URL does not point to an image file"
        
        # Encode image to base64
        image_data = base64.b64encode(response.content).decode()
        
        # Create OpenAI client and analyze
        client = OpenAI(api_key=api_key)
        
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text", 
                            "text": """Analyze the copywriting/text content in this image. Please provide:

**1. TEXT EXTRACTION**
- List all visible text/copywriting in the image

**2. COPYWRITING SCORES** (format: "Category: X/10"):
- Clarity: X/10
- Persuasiveness: X/10
- Emotional Appeal: X/10
- Call-to-Action: X/10
- Brand Voice: X/10

**3. ALTERNATIVE COPYWRITING SUGGESTIONS**
- Provide 3-5 alternative copywriting options that could improve the message
- Include different approaches: emotional, logical, urgent, benefit-focused

**4. RECOMMENDATIONS**
- Specific improvements for the existing copy
- Target audience considerations
- Tone and voice adjustments

If no text is visible, indicate that no copywriting was found to analyze."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                        }
                    ]
                }
            ],
            max_tokens=1500,
            temperature=0.8
        )
        
        analysis = result.choices[0].message.content
        
        # Extract scores for PNG generation
        scores = {}
        lines = analysis.split('\n')
        for line in lines:
            if any(category in line for category in ['Clarity', 'Persuasiveness', 'Emotional Appeal', 'Call-to-Action', 'Brand Voice']):
                if '/10' in line:
                    try:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            category = parts[0].strip().replace('*', '').replace('-', '').strip()
                            score_part = parts[1].strip()
                            score = float(score_part.split('/')[0].strip())
                            scores[category] = score
                    except:
                        continue
        
        # Generate PNG report
        report_image, filename = create_analysis_report("Copywriting", scores, url)
        
        # Format the response with emojis and better structure
        formatted_response = f"""
✍️ **COPYWRITING ANALYSIS REPORT**

📝 **ANALYSIS RESULTS:**
{analysis}

🖼️ **VISUAL REPORT:** 
✅ PNG report generated: `{filename}`

🔗 **ANALYZED IMAGE:** {url}

📊 **QUICK SUMMARY:**
"""
        
        if scores:
            overall_score = sum(scores.values()) / len(scores)
            if overall_score >= 8:
                formatted_response += f"🌟 **EXCELLENT COPY** - Overall Score: {overall_score:.1f}/10"
            elif overall_score >= 6:
                formatted_response += f"👍 **GOOD COPY** - Overall Score: {overall_score:.1f}/10"
            elif overall_score >= 4:
                formatted_response += f"⚠️ **NEEDS IMPROVEMENT** - Overall Score: {overall_score:.1f}/10"
            else:
                formatted_response += f"❌ **POOR COPY** - Overall Score: {overall_score:.1f}/10"
        
        formatted_response += "\n\n---\n*✨ Analysis powered by OpenAI GPT-4 Vision*"
        
        return formatted_response
        
    except requests.exceptions.RequestException as e:
        return f"❌ **Network Error:** Could not download image from URL. {str(e)}"
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

def main():
    """Main entry point for the MCP server"""
    try:
        print("🎨 Starting Graphic Design MCP Server...")
        print("✅ Server is ready to analyze graphic designs and copywriting!")
        print("📋 Available tools:")
        print("  • analyze_design - Analyze visual design elements")
        print("  • analyze_copywriting - Analyze text/copywriting content")
        print("🖼️ PNG reports will be generated for each analysis!")
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Graphic Design MCP Server...")
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        raise

if __name__ == "__main__":
    main()