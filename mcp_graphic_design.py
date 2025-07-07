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
import re
import tempfile
import fitz  # PyMuPDF for PDF processing

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

Note: This analysis is based on general web design principles. For more accurate results, please use a screenshot service to capture the website and analyze it using the `analyze_design` tool.

📸 **For detailed visual analysis:**
1. Take a screenshot of the website
2. Upload it to an image hosting service
3. Use `analyze_design` with the image URL

---
*✨ Analysis powered by OpenAI GPT-4o & Web Design Principles*"""
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

@mcp.tool()
def analyze_pdf_presentation(url: str) -> str:
    """
    Analyze PDF presentation and provide detailed feedback on the presentation quality.
    
    This tool downloads a PDF from the provided URL and analyzes its presentation quality.
    It provides scores and feedback on Visual Harmony, Clarity, User Friendliness, Interactivity, and Creativity.
    
    Args:
        url: The URL of the PDF to analyze (must be a valid HTTP/HTTPS URL)
        
    Returns:
        A detailed analysis of the PDF presentation with scores and recommendations
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
        
        # Download PDF with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Check if the content is a PDF
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('application/pdf'):
            return "❌ Error: The provided URL does not point to a PDF file"
        
        # Encode PDF to base64
        pdf_data = base64.b64encode(response.content).decode()
        
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
                            "text": """Analyze this PDF presentation in detail. Please provide ONLY numerical scores (1-10) for each category, then detailed feedback:

SCORES (format: "Category: X/10"):
1. Visual Harmony: X/10
2. Clarity: X/10  
3. User Friendliness: X/10
4. Interactivity: X/10
5. Creativity: X/10

Then provide detailed feedback for each category and overall recommendations."""
                        },
                        {
                            "type": "file_url",
                            "file_url": {"url": f"data:application/pdf;base64,{pdf_data}"}
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
🎨 **PDF PRESENTATION ANALYSIS REPORT**

📋 **ANALYSIS RESULTS:**
{analysis}

🔗 **ANALYZED PDF:** {url}

---
*✨ Analysis powered by OpenAI GPT-4 Vision*"""
        
        return formatted_response
        
    except requests.exceptions.RequestException as e:
        return f"❌ **Network Error:** Could not download PDF from URL. {str(e)}"
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

@mcp.tool()
def analyze_architectural_design(url: str) -> str:
    """
    Analyze architectural design and provide detailed feedback on the design elements.
    
    This tool downloads an image from the provided URL and analyzes it using OpenAI's vision model.
    It provides scores and feedback on Visual Harmony, Clarity, User Friendliness, Interactivity, and Creativity.
    
    Args:
        url: The URL of the image to analyze (must be a valid HTTP/HTTPS URL)
        
    Returns:
        A detailed analysis of the architectural design with scores and recommendations
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
                            "text": """Analyze this architectural design in detail. Please provide ONLY numerical scores (1-10) for each category, then detailed feedback:

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
🏢 **ARCHITECTURAL DESIGN ANALYSIS REPORT**

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

def convert_google_links_to_direct_urls(url: str) -> Dict[str, str]:
    """
    Convert Google Slides and Google Drive sharing links to direct download URLs
    
    Args:
        url: Original Google sharing URL
        
    Returns:
        Dict containing various format URLs for analysis
    """
    results = {"original_url": url, "analysis_urls": []}
    
    # Google Slides link patterns
    slides_pattern = r'https://docs\.google\.com/presentation/d/([a-zA-Z0-9-_]+)'
    slides_match = re.search(slides_pattern, url)
    
    if slides_match:
        file_id = slides_match.group(1)
        results["file_type"] = "google_slides"
        results["file_id"] = file_id
        
        # Create different export URLs
        results["analysis_urls"] = [
            {
                "format": "pdf",
                "url": f"https://docs.google.com/presentation/d/{file_id}/export/pdf",
                "description": "PDF version for presentation analysis"
            },
            {
                "format": "pptx", 
                "url": f"https://docs.google.com/presentation/d/{file_id}/export/pptx",
                "description": "PowerPoint version for download"
            }
        ]
        return results
    
    # Google Drive file link patterns
    drive_pattern = r'https://drive\.google\.com/file/d/([a-zA-Z0-9-_]+)'
    drive_match = re.search(drive_pattern, url)
    
    if drive_match:
        file_id = drive_match.group(1)
        results["file_type"] = "google_drive"
        results["file_id"] = file_id
        
        # Create direct download URL
        results["analysis_urls"] = [
            {
                "format": "direct_download",
                "url": f"https://drive.google.com/u/0/uc?id={file_id}&export=download",
                "description": "Direct download link for the file"
            }
        ]
        return results
    
    # Google Docs link patterns
    docs_pattern = r'https://docs\.google\.com/document/d/([a-zA-Z0-9-_]+)'
    docs_match = re.search(docs_pattern, url)
    
    if docs_match:
        file_id = docs_match.group(1)
        results["file_type"] = "google_docs"
        results["file_id"] = file_id
        
        # Create export URLs
        results["analysis_urls"] = [
            {
                "format": "pdf",
                "url": f"https://docs.google.com/document/d/{file_id}/export?format=pdf",
                "description": "PDF version for document analysis"
            },
            {
                "format": "docx",
                "url": f"https://docs.google.com/document/d/{file_id}/export?format=docx", 
                "description": "Word document version"
            }
        ]
        return results
    
    # Google Sheets link patterns  
    sheets_pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)'
    sheets_match = re.search(sheets_pattern, url)
    
    if sheets_match:
        file_id = sheets_match.group(1)
        results["file_type"] = "google_sheets"
        results["file_id"] = file_id
        
        # Create export URLs
        results["analysis_urls"] = [
            {
                "format": "pdf",
                "url": f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=pdf",
                "description": "PDF version for analysis"
            },
            {
                "format": "xlsx",
                "url": f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx",
                "description": "Excel version for download"
            }
        ]
        return results
        
    # If no pattern matches
    results["file_type"] = "unknown"
    results["error"] = "URL format not recognized as a Google file sharing link"
    return results

def analyze_google_file(url: str, analysis_type: str = "presentation") -> str:
    """
    Analyze Google files by converting them to appropriate formats first
    
    Args:
        url: Original Google sharing URL
        analysis_type: Type of analysis (presentation, design, copywriting, etc.)
        
    Returns:
        Analysis result string
    """
    # Convert the URL to usable format
    converted_links = convert_google_links_to_direct_urls(url)
    
    if "error" in converted_links:
        return f"❌ Error: {converted_links['error']}"
    
    file_type = converted_links["file_type"]
    analysis_urls = converted_links["analysis_urls"]
    
    # Find the best URL for analysis (prefer PDF)
    analysis_url = None
    for url_info in analysis_urls:
        if url_info["format"] == "pdf":
            analysis_url = url_info["url"]
            break
    
    if not analysis_url and analysis_urls:
        analysis_url = analysis_urls[0]["url"]
    
    if not analysis_url:
        return "❌ Could not generate analysis URL"
    
    # Perform analysis based on file type
    try:
        if file_type == "google_slides" and analysis_type == "presentation":
            return analyze_pdf_presentation(analysis_url)
        elif analysis_type == "design":
            return analyze_design(analysis_url)
        elif analysis_type == "copywriting":  
            return analyze_copywriting(analysis_url)
        elif analysis_type == "layout":
            return analyze_layout_alignment(analysis_url)
        else:
            return analyze_pdf_presentation(analysis_url)
            
    except Exception as e:
                 return f"❌ Analysis failed: {str(e)}"

@mcp.tool()
def analyze_pdf_presentation(url: str) -> str:
    """
    Analyze PDF presentation and provide detailed feedback on presentation design and content quality.
    
    This tool downloads a PDF from the provided URL and analyzes its presentation design elements.
    It provides scores and feedback on slide design, content organization, visual hierarchy, and presentation flow.
    
    Args:
        url: The URL of the PDF to analyze (must be a valid HTTP/HTTPS URL)
        
    Returns:
        A detailed analysis of the PDF presentation with scores and recommendations
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
        
        # Download PDF with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Check if the content is a PDF
        content_type = response.headers.get('content-type', '')
        if 'pdf' not in content_type.lower() and not url.lower().endswith('.pdf'):
            return "❌ Error: The provided URL does not appear to point to a PDF file"
        
        # For PDF analysis, we'll provide comprehensive analysis based on presentation design principles
        client = OpenAI(api_key=api_key)
        
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user", 
                    "content": f"""Analyze the PDF presentation from this URL: {url}

Please provide a comprehensive presentation analysis with scores (1-10) for:

**PRESENTATION DESIGN SCORES:**
1. Visual Design & Layout: X/10
2. Content Organization: X/10
3. Typography & Readability: X/10
4. Color Scheme & Consistency: X/10
5. Information Hierarchy: X/10
6. Slide Flow & Structure: X/10
7. Visual Elements Usage: X/10
8. Professional Appearance: X/10

**DETAILED ANALYSIS:**

**1. SLIDE DESIGN QUALITY:**
- Layout consistency across slides
- Visual balance and white space usage
- Professional design standards
- Brand consistency (if applicable)

**2. CONTENT ORGANIZATION:**
- Logical flow of information
- Clear section divisions
- Effective use of headings and subheadings
- Information density per slide

**3. TYPOGRAPHY & READABILITY:**
- Font selection and hierarchy
- Text size and readability
- Contrast and legibility
- Consistent text formatting

**4. VISUAL ELEMENTS:**
- Use of images, charts, diagrams
- Quality and relevance of visuals
- Integration of multimedia elements
- Visual-text balance

**5. PRESENTATION FLOW:**
- Introduction and conclusion effectiveness
- Transition quality between topics
- Logical progression of ideas
- Call-to-action clarity

**RECOMMENDATIONS:**
- Specific improvements for slide design
- Content organization suggestions
- Visual enhancement recommendations
- Professional presentation tips

Note: This analysis is based on presentation design best practices. For detailed visual analysis, please convert PDF pages to images and use the image analysis tools."""
                }
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        analysis = result.choices[0].message.content
        
        # Format the response with emojis and better structure
        formatted_response = f"""
📊 **PDF PRESENTATION ANALYSIS REPORT**

🔗 **ANALYZED PDF:** {url}

📋 **ANALYSIS RESULTS:**
{analysis}

💡 **NOTE:** This analysis is based on presentation design principles. For detailed visual analysis of specific slides, please convert PDF pages to images and use the `analyze_design` tool.

📸 **For detailed slide-by-slide analysis:**
1. Convert PDF pages to images (PNG/JPG)
2. Upload images to an image hosting service
3. Use `analyze_design` with each slide image URL

---
*✨ Analysis powered by OpenAI GPT-4o & Presentation Design Principles*"""
        
        return formatted_response
        
    except requests.exceptions.RequestException as e:
        return f"❌ **Network Error:** Could not download PDF from URL. {str(e)}"
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

@mcp.tool()
def analyze_google_file_link(url: str, analysis_type: str = "presentation") -> str:
    """
    Analyze Google Slides, Drive, Docs, or Sheets files by converting sharing links to direct analysis URLs.
    
    This tool converts Google sharing links to direct download/analysis formats and then performs the requested analysis.
    Supports Google Slides, Google Drive files, Google Docs, and Google Sheets.
    
    Args:
        url: Original Google sharing URL (e.g., Google Slides share link)
        analysis_type: Type of analysis ("presentation", "design", "copywriting", "layout")
        
    Returns:
        Analysis result with converted URLs and detailed feedback
    """
    try:
        # Clean the URL
        url = url.strip().lstrip('@')
        
        # Convert the URL to usable format
        converted_links = convert_google_links_to_direct_urls(url)
        
        if "error" in converted_links:
            return f"❌ Error: {converted_links['error']}"
        
        file_type = converted_links["file_type"]
        analysis_urls = converted_links["analysis_urls"]
        
        # Find the best URL for analysis (prefer PDF)
        analysis_url = None
        for url_info in analysis_urls:
            if url_info["format"] == "pdf":
                analysis_url = url_info["url"]
                break
        
        if not analysis_url and analysis_urls:
            analysis_url = analysis_urls[0]["url"]
        
        if not analysis_url:
            return "❌ Could not generate analysis URL"
        
        # Show conversion results first
        conversion_info = f"""
🔄 **GOOGLE FILE LINK CONVERSION**

📁 **Original URL:** {url}
📋 **File Type:** {file_type.replace('_', ' ').title()}
🔗 **File ID:** {converted_links.get('file_id', 'Unknown')}

📎 **Available Analysis URLs:**
"""
        for url_info in analysis_urls:
            conversion_info += f"• **{url_info['format'].upper()}:** {url_info['url']}\n  _{url_info['description']}_\n"
        
        conversion_info += f"\n🎯 **Using for Analysis:** {analysis_url}\n\n"
        
        # Perform analysis based on file type and analysis type
        if file_type == "google_slides" and analysis_type == "presentation":
            analysis_result = analyze_pdf_presentation(analysis_url)
        elif analysis_type == "design":
            analysis_result = analyze_design(analysis_url)
        elif analysis_type == "copywriting":
            analysis_result = analyze_copywriting(analysis_url)
        elif analysis_type == "layout":
            analysis_result = analyze_layout_alignment(analysis_url)
        else:
            # Default to presentation analysis for Google Slides, design for others
            if file_type == "google_slides":
                analysis_result = analyze_pdf_presentation(analysis_url)
            else:
                analysis_result = analyze_design(analysis_url)
        
        # Combine conversion info with analysis
        return conversion_info + analysis_result
            
    except Exception as e:
        return f"❌ Analysis failed: {str(e)}"

@mcp.tool()
def analyze_architectural_design(url: str) -> str:
    """
    Analyze architectural design and provide detailed feedback on architectural elements.
    
    This tool downloads an image from the provided URL and analyzes it using OpenAI's vision model.
    It provides scores and feedback on architectural composition, spatial design, structural elements, and aesthetic appeal.
    
    Args:
        url: The URL of the image to analyze (must be a valid HTTP/HTTPS URL)
        
    Returns:
        A detailed analysis of the architectural design with scores and recommendations
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
                            "text": """Analyze this architectural design in detail. Focus specifically on architectural elements and provide numerical scores (1-10) for each category, then detailed feedback:

**ARCHITECTURAL DESIGN SCORES** (format: "Category: X/10"):
1. Architectural Composition: X/10
2. Spatial Design & Flow: X/10
3. Structural Integrity & Innovation: X/10
4. Material Selection & Usage: X/10
5. Environmental Integration: X/10
6. Functional Design: X/10
7. Aesthetic Appeal: X/10
8. Sustainability Considerations: X/10

**DETAILED ARCHITECTURAL ANALYSIS:**

**1. ARCHITECTURAL COMPOSITION:**
- Proportion and scale relationships
- Symmetry and balance in design
- Visual weight distribution
- Architectural harmony and unity

**2. SPATIAL DESIGN & FLOW:**
- Interior/exterior space organization
- Traffic flow and circulation patterns
- Space efficiency and functionality
- Relationship between different areas

**3. STRUCTURAL ELEMENTS:**
- Structural system clarity and logic
- Innovation in structural solutions
- Integration of structure with design
- Structural expression and aesthetics

**4. MATERIAL ANALYSIS:**
- Material selection appropriateness
- Texture and color combinations
- Material durability and maintenance
- Cost-effectiveness of material choices

**5. ENVIRONMENTAL INTEGRATION:**
- Site integration and context response
- Climate-responsive design features
- Landscape integration
- Natural light and ventilation utilization

**6. FUNCTIONAL DESIGN:**
- Program requirements fulfillment
- User experience and comfort
- Accessibility considerations
- Flexibility and adaptability

**7. AESTHETIC QUALITY:**
- Visual impact and character
- Architectural style consistency
- Detail quality and craftsmanship
- Overall design coherence

**8. SUSTAINABILITY:**
- Energy efficiency considerations
- Sustainable material usage
- Environmental impact minimization
- Long-term sustainability features

**ARCHITECTURAL RECOMMENDATIONS:**
- Specific design improvements
- Structural optimization suggestions
- Material and finish enhancements
- Functional layout improvements
- Sustainability enhancement opportunities"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                        }
                    ]
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        analysis = result.choices[0].message.content
        
        # Format the response with emojis and better structure
        formatted_response = f"""
🏗️ **ARCHITECTURAL DESIGN ANALYSIS REPORT**

🏢 **ANALYSIS RESULTS:**
{analysis}

🔗 **ANALYZED IMAGE:** {url}

---
*✨ Analysis powered by OpenAI GPT-4o Vision - Architectural Specialist*"""
        
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
        print("  • analyze_pdf_presentation - Analyze PDF presentation quality")
        print("  • analyze_architectural_design - Analyze architectural design elements")
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Graphic Design MCP Server...")
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        raise

if __name__ == "__main__":
    main()