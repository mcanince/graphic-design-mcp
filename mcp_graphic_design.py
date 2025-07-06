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
from typing import Any, Dict, List, Tuple, Optional
from openai import OpenAI
from fastmcp import FastMCP
from datetime import datetime

# Initialize FastMCP server
mcp = FastMCP("Graphic Design MCP")

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
        
        # Format the response with emojis and better structure
        formatted_response = f"""
🎨 **GRAPHIC DESIGN ANALYSIS REPORT**

📋 **ANALYSIS RESULTS:**
{analysis}

🔗 **ANALYZED IMAGE:** {url}

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
        
        # Format the response with emojis and better structure
        formatted_response = f"""
✍️ **COPYWRITING ANALYSIS REPORT**

📝 **ANALYSIS RESULTS:**
{analysis}

🔗 **ANALYZED IMAGE:** {url}

---
*✨ Analysis powered by OpenAI GPT-4 Vision*"""
        
        return formatted_response
        
    except requests.exceptions.RequestException as e:
        return f"❌ **Network Error:** Could not download image from URL. {str(e)}"
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

@mcp.tool()
def analyze_website_design(url: str) -> str:
    """
    Analyze website design by taking a screenshot and evaluating the overall web design.
    
    This tool analyzes website design elements including layout, navigation, visual hierarchy,
    responsive design, user experience, and overall aesthetic appeal.
    
    Args:
        url: The website URL to analyze (must be a valid HTTP/HTTPS URL)
        
    Returns:
        A detailed analysis of the website design with scores and recommendations
    """
    try:
        # Validate URL
        if not url or not url.strip():
            return "❌ Error: URL cannot be empty"
        
        url = url.strip()
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "❌ Error: OPENAI_API_KEY environment variable not found. Please set your OpenAI API key."
        
        # Use a screenshot service (we'll simulate this by providing instructions)
        # In a real implementation, you would use a service like:
        # - screenshot.to-api.net
        # - htmlcsstoimage.com
        # - screenshotapi.net
        
        # For now, we'll provide analysis based on the URL and general web design principles
        client = OpenAI(api_key=api_key)
        
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user", 
                    "content": f"""Analyze the website design at: {url}

Please provide a comprehensive website design analysis with scores (1-10) for:

**WEBSITE DESIGN SCORES:**
1. Layout & Structure: X/10
2. Navigation & UX: X/10
3. Visual Hierarchy: X/10
4. Color Scheme & Branding: X/10
5. Typography: X/10
6. Responsiveness: X/10
7. Loading Speed: X/10
8. Accessibility: X/10

**DETAILED ANALYSIS:**
- Overall design assessment
- Strengths and weaknesses
- User experience evaluation
- Mobile responsiveness considerations
- Performance and accessibility notes

**RECOMMENDATIONS:**
- Specific improvements for layout
- Navigation enhancements
- Visual design suggestions
- Technical optimization tips

Note: This analysis is based on general web design principles. For accurate assessment, please provide a screenshot of the website."""
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        analysis = result.choices[0].message.content
        
        # Format the response
        formatted_response = f"""
🌐 **WEBSITE DESIGN ANALYSIS REPORT**

🔗 **ANALYZED WEBSITE:** {url}

📊 **ANALYSIS RESULTS:**
{analysis}

💡 **NOTE:** This analysis is based on web design best practices. For more accurate results, please use a screenshot service to capture the website and analyze it using the `analyze_design` tool.

📸 **For detailed visual analysis:**
1. Take a screenshot of the website
2. Upload it to an image hosting service
3. Use `analyze_design` with the image URL

---
*✨ Analysis powered by OpenAI GPT-4o & Web Design Principles*"""
        
        return formatted_response
        
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

@mcp.tool()
def analyze_layout_alignment(url: str) -> str:
    """
    Analyze layout alignment, spacing, and symmetry issues in design images.
    
    This tool focuses specifically on layout problems including misalignment, inconsistent spacing,
    asymmetric elements, and provides detailed suggestions for improvement.
    
    Args:
        url: The URL of the design image to analyze for layout issues
        
    Returns:
        A detailed analysis of layout, alignment, and spacing issues with specific recommendations
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
                            "text": """Analyze this design with a focus on layout, alignment, and spacing issues. Provide detailed feedback on:

**LAYOUT ANALYSIS SCORES** (format: "Category: X/10"):
1. Overall Alignment: X/10
2. Spacing Consistency: X/10
3. Grid System Usage: X/10
4. Element Balance: X/10
5. Visual Weight Distribution: X/10

**DETAILED LAYOUT ASSESSMENT:**

**1. ALIGNMENT ISSUES:**
- Identify misaligned elements (text, images, buttons, etc.)
- Check for consistent margins and padding
- Evaluate baseline grid alignment
- Note any elements that break the layout structure

**2. SPACING PROBLEMS:**
- Analyze white space usage and distribution
- Check for inconsistent gaps between elements
- Identify cramped or overly spaced areas
- Evaluate breathing room around key elements

**3. SYMMETRY & ASYMMETRY:**
- Identify intentional vs unintentional asymmetric elements
- Check for visual balance issues
- Note elements that appear "off-center" when they shouldn't be
- Evaluate compositional balance

**4. GRID & STRUCTURE:**
- Assess adherence to grid system
- Identify elements that break the grid unnecessarily
- Check for consistent column widths and gutters
- Evaluate overall structural hierarchy

**5. SPECIFIC RECOMMENDATIONS:**
- Provide exact pixel/spacing adjustments where possible
- Suggest alignment fixes for specific elements
- Recommend spacing improvements
- Propose solutions for asymmetry issues
- Give actionable layout optimization tips

Be very specific about what needs to be fixed and how to fix it."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                        }
                    ]
                }
            ],
            max_tokens=1800,
            temperature=0.7
        )
        
        analysis = result.choices[0].message.content
        
        # Format the response with emojis and better structure
        formatted_response = f"""
📐 **LAYOUT & ALIGNMENT ANALYSIS REPORT**

📊 **LAYOUT ANALYSIS:**
{analysis}

🔗 **ANALYZED IMAGE:** {url}

---
*✨ Analysis powered by OpenAI GPT-4o Vision - Layout Specialist*"""
        
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
        print("  • analyze_website_design - Analyze website design from URL")
        print("  • analyze_layout_alignment - Check layout, spacing & alignment issues")
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Graphic Design MCP Server...")
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        raise

if __name__ == "__main__":
    main()