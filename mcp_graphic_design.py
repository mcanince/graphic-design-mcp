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
import subprocess
import json
from typing import Any, Dict, List, Tuple, Optional
from openai import OpenAI
from fastmcp import FastMCP
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime
import re

# Initialize FastMCP server
mcp = FastMCP("Graphic Design MCP")

def commit_to_github(filename: str, file_path: str) -> Optional[str]:
    """
    Commit the PNG file to GitHub and return the raw file URL.
    
    Args:
        filename: Name of the file
        file_path: Local path to the file
        
    Returns:
        GitHub raw URL of the file or None if failed
    """
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            return None
            
        # Get the current branch and remote info
        branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                     capture_output=True, text=True)
        if branch_result.returncode != 0:
            return None
        branch = branch_result.stdout.strip()
        
        # Get remote URL
        remote_result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                     capture_output=True, text=True)
        if remote_result.returncode != 0:
            return None
        remote_url = remote_result.stdout.strip()
        
        # Extract GitHub username and repo name
        if 'github.com' in remote_url:
            if remote_url.startswith('https://github.com/'):
                repo_info = remote_url.replace('https://github.com/', '').replace('.git', '')
            elif remote_url.startswith('git@github.com:'):
                repo_info = remote_url.replace('git@github.com:', '').replace('.git', '')
            else:
                return None
                
            username, repo_name = repo_info.split('/')
            
            # Add file to git
            subprocess.run(['git', 'add', file_path], check=True)
            
            # Commit file
            commit_message = f"Add analysis report: {filename}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Push to GitHub
            subprocess.run(['git', 'push', 'origin', branch], check=True)
            
            # Return raw GitHub URL
            github_url = f"https://raw.githubusercontent.com/{username}/{repo_name}/{branch}/{filename}"
            return github_url
            
    except Exception as e:
        print(f"Error committing to GitHub: {e}")
        return None
    
    return None

def create_png_report(analysis_type: str, scores: dict, analysis_text: str, image_url: str = None) -> Tuple[str, str, str]:
    """
    Create a visual PNG report of the analysis results and upload it.
    
    Args:
        analysis_type: Type of analysis (design or copywriting)
        scores: Dictionary of scores and feedback
        analysis_text: Full analysis text
        image_url: Original image URL (optional)
        
    Returns:
        Tuple of (base64_image, filename, github_url)
    """
    try:
        # Create a large canvas for the report
        width, height = 1200, 1600
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts (fallback to default if not available)
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
            header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
            text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        except:
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 42)
                header_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 28)
                text_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
                small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
            except:
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
        
        # Colors
        primary_color = '#1e40af'
        secondary_color = '#64748b'
        accent_color = '#10b981'
        bg_color = '#f8fafc'
        
        # Background gradient effect
        draw.rectangle([(0, 0), (width, 200)], fill=bg_color)
        
        y = 40
        
        # Title with emoji
        if analysis_type.lower() == "design":
            title = "🎨 GRAPHIC DESIGN ANALYSIS REPORT"
        else:
            title = "✍️ COPYWRITING ANALYSIS REPORT"
            
        # Center the title
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        draw.text((title_x, y), title, fill=primary_color, font=title_font)
        y += 80
        
        # Draw separator line
        draw.line([(80, y), (width-80, y)], fill=secondary_color, width=3)
        y += 40
        
        # Helper function to draw rounded rectangle for older Pillow versions
        def draw_rounded_rectangle(draw, coords, radius, fill, outline=None):
            try:
                # Try the newer method first
                draw.rounded_rectangle(coords, radius=radius, fill=fill, outline=outline)
            except AttributeError:
                # Fallback for older versions
                x1, y1, x2, y2 = coords
                draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline)
                draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline)
                draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill, outline=outline)
                draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill, outline=outline)
                draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill, outline=outline)
                draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill, outline=outline)
        
        # Overall score calculation and display
        if scores:
            total_score = sum(scores.values()) / len(scores)
            
            # Score color based on performance
            if total_score >= 8:
                score_color = '#10b981'  # Green
                score_emoji = "🌟"
                score_text = "EXCELLENT"
            elif total_score >= 6:
                score_color = '#3b82f6'  # Blue
                score_emoji = "👍"
                score_text = "GOOD"
            elif total_score >= 4:
                score_color = '#f59e0b'  # Yellow
                score_emoji = "⚠️"
                score_text = "NEEDS IMPROVEMENT"
            else:
                score_color = '#ef4444'  # Red
                score_emoji = "❌"
                score_text = "POOR"
            
            # Overall score box
            score_box_height = 120
            draw_rounded_rectangle(draw, (80, y, width-80, y+score_box_height), 
                                 radius=20, fill=score_color, outline=score_color)
            
            # Overall score text
            overall_text = f"{score_emoji} {score_text}"
            score_number = f"{total_score:.1f}/10"
            
            # Center the overall score text
            overall_bbox = draw.textbbox((0, 0), overall_text, font=header_font)
            overall_width = overall_bbox[2] - overall_bbox[0]
            overall_x = (width - overall_width) // 2
            
            draw.text((overall_x, y+20), overall_text, fill='white', font=header_font)
            
            # Center the score number
            score_bbox = draw.textbbox((0, 0), score_number, font=title_font)
            score_width = score_bbox[2] - score_bbox[0]
            score_x = (width - score_width) // 2
            
            draw.text((score_x, y+55), score_number, fill='white', font=title_font)
            y += score_box_height + 60
            
            # Individual scores section
            draw.text((80, y), "📊 DETAILED SCORES", fill=primary_color, font=header_font)
            y += 50
            
            # Individual scores with bars
            for category, score in scores.items():
                # Category name
                draw.text((100, y), f"• {category}", fill=secondary_color, font=text_font)
                
                # Score number
                score_text = f"{score}/10"
                draw.text((width-200, y), score_text, fill=secondary_color, font=text_font)
                
                # Score bar background
                bar_y = y + 30
                bar_width = width - 200
                bar_height = 20
                draw_rounded_rectangle(draw, (100, bar_y, bar_width, bar_y+bar_height), 
                                     radius=10, fill='#e5e7eb', outline='#e5e7eb')
                
                # Score bar fill
                fill_width = int((score / 10) * (bar_width - 100))
                if fill_width > 0:
                    draw_rounded_rectangle(draw, (100, bar_y, 100+fill_width, bar_y+bar_height), 
                                         radius=10, fill=score_color, outline=score_color)
                
                y += 70
        
        # Add source image info if provided
        if image_url:
            y += 30
            draw.text((80, y), "🔗 ANALYZED IMAGE:", fill=primary_color, font=header_font)
            y += 35
            
            # Wrap URL text
            url_text = image_url
            if len(url_text) > 80:
                url_text = url_text[:77] + "..."
            draw.text((100, y), url_text, fill=secondary_color, font=small_font)
            y += 40
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((80, height-80), f"📅 Generated: {timestamp}", fill=secondary_color, font=small_font)
        draw.text((80, height-50), "✨ Powered by OpenAI GPT-4 Vision", fill=secondary_color, font=small_font)
        
        # Create filename
        timestamp_str = str(int(datetime.now().timestamp()))
        filename = f"reports/{analysis_type}_analysis_report_{timestamp_str}.png"
        
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        
        # Save the image locally
        img.save(filename, format='PNG', quality=95)
        
        # Convert to base64 for embedding
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Try to commit to GitHub
        github_url = commit_to_github(filename, filename)
        
        return image_base64, filename, github_url
        
    except Exception as e:
        return None, f"Error creating report: {str(e)}", None

def create_png_report_with_image(analysis_type: str, scores: dict, analysis_text: str, original_image_url: str) -> Tuple[str, str, str]:
    """
    Create a comprehensive PNG report that includes the original image and analysis results.
    
    Args:
        analysis_type: Type of analysis (design or copywriting)
        scores: Dictionary of scores and feedback
        analysis_text: Full analysis text
        original_image_url: URL of the original analyzed image
        
    Returns:
        Tuple of (base64_image, filename, github_url)
    """
    try:
        # Download the original image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(original_image_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Load original image
        original_img = Image.open(io.BytesIO(response.content))
        
        # Create a large canvas for the combined report (1600x1200)
        canvas_width, canvas_height = 1600, 1200
        canvas = Image.new('RGB', (canvas_width, canvas_height), color='white')
        draw = ImageDraw.Draw(canvas)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        except:
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 36)
                header_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                text_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
                small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
            except:
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
        
        # Colors
        primary_color = '#1e40af'
        secondary_color = '#64748b'
        accent_color = '#10b981'
        bg_color = '#f8fafc'
        
        # Background
        draw.rectangle([(0, 0), (canvas_width, 80)], fill=bg_color)
        
        # Title
        if analysis_type.lower() == "design":
            title = "🎨 DESIGN ANALYSIS REPORT"
        else:
            title = "✍️ COPYWRITING ANALYSIS REPORT"
            
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (canvas_width - title_width) // 2
        draw.text((title_x, 20), title, fill=primary_color, font=title_font)
        
        # Resize and place original image on the left side
        img_area_width = 700
        img_area_height = 900
        img_x = 50
        img_y = 120
        
        # Calculate scaling to fit image in the designated area
        img_w, img_h = original_img.size
        scale_w = img_area_width / img_w
        scale_h = img_area_height / img_h
        scale = min(scale_w, scale_h)
        
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        
        # Resize and paste original image
        resized_img = original_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        paste_x = img_x + (img_area_width - new_w) // 2
        paste_y = img_y + (img_area_height - new_h) // 2
        canvas.paste(resized_img, (paste_x, paste_y))
        
        # Draw border around image
        draw.rectangle([(img_x, img_y), (img_x + img_area_width, img_y + img_area_height)], outline=secondary_color, width=2)
        
        # Analysis results on the right side
        results_x = 800
        y = 120
        
        # Helper function for rounded rectangles
        def draw_rounded_rectangle(draw, coords, radius, fill, outline=None):
            try:
                draw.rounded_rectangle(coords, radius=radius, fill=fill, outline=outline)
            except AttributeError:
                x1, y1, x2, y2 = coords
                draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline)
                draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline)
                draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill, outline=outline)
                draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill, outline=outline)
                draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill, outline=outline)
                draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill, outline=outline)
        
        # Overall score
        if scores:
            total_score = sum(scores.values()) / len(scores)
            
            # Score color based on performance
            if total_score >= 8:
                score_color = '#10b981'
                score_emoji = "🌟"
                score_text = "EXCELLENT"
            elif total_score >= 6:
                score_color = '#3b82f6'
                score_emoji = "👍"
                score_text = "GOOD"
            elif total_score >= 4:
                score_color = '#f59e0b'
                score_emoji = "⚠️"
                score_text = "NEEDS IMPROVEMENT"
            else:
                score_color = '#ef4444'
                score_emoji = "❌"
                score_text = "POOR"
            
            # Overall score box
            score_box_height = 100
            draw_rounded_rectangle(draw, (results_x, y, canvas_width - 50, y + score_box_height), 
                                 radius=15, fill=score_color, outline=score_color)
            
            # Overall score text
            overall_text = f"{score_emoji} {score_text}"
            score_number = f"{total_score:.1f}/10"
            
            draw.text((results_x + 20, y + 15), overall_text, fill='white', font=header_font)
            draw.text((results_x + 20, y + 50), score_number, fill='white', font=title_font)
            y += score_box_height + 40
            
            # Individual scores
            draw.text((results_x, y), "📊 DETAILED SCORES", fill=primary_color, font=header_font)
            y += 40
            
            bar_width = canvas_width - results_x - 100
            for category, score in scores.items():
                # Category name and score
                category_text = f"• {category}: {score}/10"
                draw.text((results_x, y), category_text, fill=secondary_color, font=text_font)
                
                # Score bar background
                bar_y = y + 25
                bar_height = 15
                draw_rounded_rectangle(draw, (results_x, bar_y, results_x + bar_width, bar_y + bar_height), 
                                     radius=8, fill='#e5e7eb', outline='#e5e7eb')
                
                # Score bar fill
                fill_width = int((score / 10) * bar_width)
                if fill_width > 0:
                    draw_rounded_rectangle(draw, (results_x, bar_y, results_x + fill_width, bar_y + bar_height), 
                                         radius=8, fill=score_color, outline=score_color)
                
                y += 50
        
        # Add URL and timestamp at bottom
        y = canvas_height - 100
        draw.text((50, y), "🔗 ANALYZED IMAGE:", fill=primary_color, font=header_font)
        y += 30
        
        # Wrap URL if too long
        url_text = original_image_url
        if len(url_text) > 100:
            url_text = url_text[:97] + "..."
        draw.text((50, y), url_text, fill=secondary_color, font=small_font)
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((50, canvas_height - 40), f"📅 Generated: {timestamp}", fill=secondary_color, font=small_font)
        draw.text((50, canvas_height - 20), "✨ Powered by OpenAI GPT-4 Vision", fill=secondary_color, font=small_font)
        
        # Create filename
        timestamp_str = str(int(datetime.now().timestamp()))
        filename = f"reports/{analysis_type}_comprehensive_report_{timestamp_str}.png"
        
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        
        # Save the image locally
        canvas.save(filename, format='PNG', quality=95)
        
        # Convert to base64 for embedding
        buffer = io.BytesIO()
        canvas.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Try to commit to GitHub
        github_url = commit_to_github(filename, filename)
        
        return image_base64, filename, github_url
        
    except Exception as e:
        return None, f"Error creating comprehensive report: {str(e)}", None

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
        
        # Extract scores for future PNG generation
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
        
        # Save analysis data for PNG generation
        analysis_data = {
            "type": "design",
            "url": url,
            "scores": scores,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to temporary file for generate_report tool
        with open("last_analysis.json", "w") as f:
            json.dump(analysis_data, f)
        
        # Format the response with emojis and better structure
        formatted_response = f"""
🎨 **GRAPHIC DESIGN ANALYSIS REPORT**

📋 **ANALYSIS RESULTS:**
{analysis}

🔗 **ANALYZED IMAGE:** {url}

📊 **QUICK SUMMARY:**"""
        
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
        
        formatted_response += """

📸 **Want a visual PNG report?** Use the `generate_report` tool to create a beautiful infographic with charts and colors!

---
*✨ Analysis powered by OpenAI GPT-4 Vision*"""
        
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
        
        # Save analysis data for PNG generation
        analysis_data = {
            "type": "copywriting",
            "url": url,
            "scores": scores,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to temporary file for generate_report tool
        with open("last_analysis.json", "w") as f:
            json.dump(analysis_data, f)
        
        # Format the response with emojis and better structure
        formatted_response = f"""
✍️ **COPYWRITING ANALYSIS REPORT**

📝 **ANALYSIS RESULTS:**
{analysis}

🔗 **ANALYZED IMAGE:** {url}

📊 **QUICK SUMMARY:**"""
        
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
        
        formatted_response += """

📸 **Want a visual PNG report?** Use the `generate_report` tool to create a beautiful infographic with charts and colors!

---
*✨ Analysis powered by OpenAI GPT-4 Vision*"""
        
        return formatted_response
        
    except requests.exceptions.RequestException as e:
        return f"❌ **Network Error:** Could not download image from URL. {str(e)}"
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

@mcp.tool()
def generate_report(original_image_url: str, analysis_result: str) -> str:
    """
    Generate a visual PNG report from provided analysis results and original image.
    
    This tool creates a beautiful PNG infographic with charts, colors, and visual elements
    based on the provided analysis results and original image URL. The PNG includes the 
    original analyzed image alongside the analysis results and is displayed in chat and 
    optionally uploaded to GitHub if available.
    
    Args:
        original_image_url: URL of the original image that was analyzed
        analysis_result: JSON string containing the analysis results
    
    Returns:
        Status of PNG generation with embedded image or error message
    """
    try:
        import json
        
        # Parse the analysis result
        try:
            analysis_data = json.loads(analysis_result)
        except json.JSONDecodeError:
            # If it's not JSON, treat as plain text and extract scores
            analysis_text = analysis_result
            analysis_data = {
                "analysis_type": "design",
                "analysis_text": analysis_text,
                "scores": extract_scores_from_text(analysis_text),
                "original_image_url": original_image_url
            }
        
        # Create comprehensive PNG report with original image
        base64_image, filename, github_url = create_png_report_with_image(
            analysis_data.get("analysis_type", "design"),
            analysis_data.get("scores", {}),
            analysis_data.get("analysis_text", analysis_result),
            original_image_url
        )
        
        # Prepare response with embedded PNG
        response = f"""
🎨 **PNG REPORT GENERATED SUCCESSFULLY!**

📸 **VISUAL REPORT:**
![Analysis Report](data:image/png;base64,{base64_image})

💾 **Local File:** {filename}

🔗 **Shareable Link:** {github_url if github_url else "Not available (not in a git repository or no push access)"}

📊 **Report Summary:**
- **Analysis Type:** {analysis_data.get("analysis_type", "Design").title()}
- **Original Image:** {original_image_url}
- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*✨ Visual report powered by Pillow & OpenAI GPT-4 Vision*"""

        return response
        
    except Exception as e:
        return f"❌ **Error generating PNG report:** {str(e)}"

def extract_scores_from_text(text: str) -> dict:
    """
    Extract scores from analysis text using regex patterns.
    
    Args:
        text: Analysis text containing scores
        
    Returns:
        Dictionary of extracted scores
    """
    scores = {}
    
    # Common score patterns
    patterns = [
        r'Visual Harmony[:\s]*(\d+)/10',
        r'Clarity[:\s]*(\d+)/10', 
        r'User Friendliness[:\s]*(\d+)/10',
        r'Interactivity[:\s]*(\d+)/10',
        r'Creativity[:\s]*(\d+)/10',
        r'(\w+)[:\s]*(\d+)/10'  # Generic pattern
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match.groups()) == 2:  # Generic pattern
                category = match.group(1).strip()
                score = int(match.group(2))
                if category.lower() not in [k.lower() for k in scores.keys()]:
                    scores[category] = score
            else:  # Specific patterns
                score = int(match.group(1))
                if 'harmony' in pattern.lower():
                    scores['Visual Harmony'] = score
                elif 'clarity' in pattern.lower():
                    scores['Clarity'] = score
                elif 'friendliness' in pattern.lower():
                    scores['User Friendliness'] = score
                elif 'interactivity' in pattern.lower():
                    scores['Interactivity'] = score
                elif 'creativity' in pattern.lower():
                    scores['Creativity'] = score
    
    return scores

def main():
    """Main entry point for the MCP server"""
    try:
        print("🎨 Starting Graphic Design MCP Server...")
        print("✅ Server is ready to analyze graphic designs and copywriting!")
        print("📋 Available tools:")
        print("  • analyze_design - Analyze visual design elements")
        print("  • analyze_copywriting - Analyze text/copywriting content")
        print("  • generate_report - Create PNG infographic from last analysis")
        print("📸 PNG reports embedded directly in chat!")
        print("🔗 Auto-upload to GitHub if available!")
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Graphic Design MCP Server...")
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        raise

if __name__ == "__main__":
    main()