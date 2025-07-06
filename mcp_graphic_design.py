#!/usr/bin/env python3
"""
MCP Server for Graphic Design Analysis
"""

import asyncio
import os
import base64
import requests
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

# Create FastMCP instance
mcp = FastMCP("Graphic Design MCP")

def get_openai_api_key():
    """Get OpenAI API key from environment variable"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable not found")
    return api_key

def download_image_as_base64(url):
    """Download image from URL and convert to base64"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return base64.b64encode(response.content).decode()
    except Exception as e:
        raise Exception(f"Failed to download image: {e}")

@mcp.tool()
def analyze_design(url: str) -> str:
    """
    Analyze graphic design and provide scores in 5 categories.
    
    Args:
        url: URL of the image to analyze
        
    Returns:
        Detailed design analysis and scoring
    """
    try:
        # Clean URL
        url = url.strip().lstrip('@')
        
        # Get OpenAI client
        client = OpenAI(api_key=get_openai_api_key())
        
        # Download and encode image
        image_b64 = download_image_as_base64(url)
        
        # Create analysis prompt
        prompt = """
        You are a professional UI/UX design expert.
        Analyze the given design image in these 5 categories:

        1. **Visual Harmony** (colors, typography, layout consistency)
        2. **Clarity** (how clearly information is communicated)
        3. **User Friendliness** (ease of use, intuitive flow)
        4. **Interactivity** (navigation, button clarity, interaction cues)
        5. **Creativity** (originality and design uniqueness)

        For each category:
        - Give a score out of 10
        - Provide a brief explanation

        Finally, give an overall score (average of the 5 categories).
        """
        
        # Call GPT-4 Vision
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        analysis = response.choices[0].message.content
        return f"🎨 **Design Analysis**\n\n{analysis}"
        
    except Exception as e:
        return f"❌ Analysis Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()