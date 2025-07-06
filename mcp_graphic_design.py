#!/usr/bin/env python3
"""
MCP Server for Graphic Design Analysis
"""

import os
import base64
import requests
from openai import OpenAI
from fastmcp import FastMCP

# Create FastMCP instance
mcp = FastMCP("Graphic Design MCP")

@mcp.tool
def analyze_design(url: str) -> str:
    """
    Analyze graphic design and provide detailed feedback.
    
    Args:
        url: URL of the image to analyze
        
    Returns:
        Design analysis results
    """
    try:
        # Clean URL
        url = url.strip().lstrip('@')
        
        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "❌ Error: OPENAI_API_KEY not found"
        
        # Download image
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        image_data = base64.b64encode(response.content).decode()
        
        # Analyze with OpenAI
        client = OpenAI(api_key=api_key)
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text", 
                            "text": "Analyze this design in 5 categories (Visual Harmony, Clarity, User Friendliness, Interactivity, Creativity). Give scores out of 10 for each."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        analysis = result.choices[0].message.content
        return f"🎨 **Design Analysis**\n\n{analysis}"
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Entry point for the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()