#!/usr/bin/env python3
"""
MCP Server for Graphic Design Analysis
Provides tools for analyzing graphic design images using OpenAI's vision model
"""

import asyncio
import os
import base64
import requests
from typing import Any, Dict, List
from openai import OpenAI
from fastmcp import FastMCP

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
                            "text": """Analyze this graphic design in detail. Please provide:

1. **Visual Harmony** (Score: /10) - How well do colors, typography, and layout work together?
2. **Clarity** (Score: /10) - How clear and readable is the design?
3. **User Friendliness** (Score: /10) - How intuitive and accessible is the design?
4. **Interactivity** (Score: /10) - How well does the design guide user interaction?
5. **Creativity** (Score: /10) - How original and innovative is the design?

For each category, provide the score and 2-3 sentences of specific feedback. End with overall recommendations for improvement."""
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
        return f"🎨 **Graphic Design Analysis**\n\n{analysis}\n\n---\n*Analysis powered by OpenAI GPT-4 Vision*"
        
    except requests.exceptions.RequestException as e:
        return f"❌ Network Error: Could not download image from URL. {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

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

**2. COPYWRITING ANALYSIS** (if text exists)
- **Clarity** (Score: /10) - How clear and understandable is the message?
- **Persuasiveness** (Score: /10) - How convincing and compelling is the copy?
- **Emotional Appeal** (Score: /10) - How well does it connect emotionally?
- **Call-to-Action** (Score: /10) - How effective is the CTA (if present)?
- **Brand Voice** (Score: /10) - How consistent is the tone and voice?

**3. ALTERNATIVE COPYWRITING SUGGESTIONS**
- Provide 3-5 alternative copywriting options that could improve the message
- Include different approaches: emotional, logical, urgent, benefit-focused
- Suggest improved headlines, taglines, or CTAs

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
        return f"✍️ **Copywriting Analysis**\n\n{analysis}\n\n---\n*Analysis powered by OpenAI GPT-4 Vision*"
        
    except requests.exceptions.RequestException as e:
        return f"❌ Network Error: Could not download image from URL. {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Main entry point for the MCP server"""
    try:
        print("🎨 Starting Graphic Design MCP Server...")
        print("✅ Server is ready to analyze graphic designs and copywriting!")
        print("📋 Available tools:")
        print("  • analyze_design - Analyze visual design elements")
        print("  • analyze_copywriting - Analyze text/copywriting content")
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Graphic Design MCP Server...")
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        raise

if __name__ == "__main__":
    main()