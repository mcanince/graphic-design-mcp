#!/usr/bin/env python3
"""
Google Link Converter - Demonstration Script
Converts Google Slides, Drive, Docs, and Sheets sharing links to direct download/analysis URLs
"""

import re
from typing import Dict, Any

def convert_google_links_to_direct_urls(url: str) -> Dict[str, Any]:
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

def display_conversion_results(url: str):
    """Display conversion results in a formatted way"""
    print("=" * 80)
    print("🔄 GOOGLE LINK CONVERTER - DEMONSTRATION")
    print("=" * 80)
    
    results = convert_google_links_to_direct_urls(url)
    
    print(f"\n📁 **Original URL:** {results['original_url']}")
    
    if "error" in results:
        print(f"❌ **Error:** {results['error']}")
        return
    
    print(f"📋 **File Type:** {results['file_type'].replace('_', ' ').title()}")
    print(f"🔗 **File ID:** {results['file_id']}")
    
    print(f"\n📎 **Available Analysis URLs:**")
    for i, url_info in enumerate(results['analysis_urls'], 1):
        print(f"{i}. **{url_info['format'].upper()}:**")
        print(f"   URL: {url_info['url']}")
        print(f"   Use: {url_info['description']}")
        print()

if __name__ == "__main__":
    # Test with the provided URLs
    test_urls = [
        "https://docs.google.com/presentation/d/1Vw4XhzY6YYQcA4-QmBUsYo9pJtCKkmoz/edit?usp=sharing&ouid=113648061257082139362&rtpof=true&sd=true",
        "https://drive.google.com/file/d/1iR-FW2QsoL4gUoK3d8yH2MDcAWmAh-hU/view?usp=sharing"
    ]
    
    for url in test_urls:
        display_conversion_results(url)
        print("\n" + "🔄" * 40 + "\n")
    
    print("✅ **ÖZET/SUMMARY:**")
    print("Bu script, Google dosya paylaşım bağlantılarını analiz edilebilir formatlara dönüştürür.")
    print("This script converts Google file sharing links to analyzable formats.")
    print("\n📚 **Desteklenen Formatlar/Supported Formats:**")
    print("• Google Slides → PDF/PPTX")
    print("• Google Drive Files → Direct Download")
    print("• Google Docs → PDF/DOCX")
    print("• Google Sheets → PDF/XLSX") 