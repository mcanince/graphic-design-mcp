# Graphic Design MCP v4.0.0 🎨

MCP (Model Context Protocol) tool for graphic design analysis and **Google file integration**. Analyzes designs in detail using OpenAI GPT-4 Vision and creates visual reports. **NEW: Direct Google Slides, Drive, Docs, and Sheets analysis!**

## ✨ Features

### 🎯 Analysis Types
- **🎨 Design Analysis** - Visual Harmony, Clarity, User Friendliness, Interactivity, Creativity
- **✍️ Copywriting Analysis** - Clarity, Persuasiveness, Emotional Appeal, Call-to-Action, Brand Voice
- **🌐 Website Design Analysis** - Layout, Navigation, Visual Hierarchy, Branding, Responsiveness
- **📐 Layout & Alignment Analysis** - Spacing, Alignment, Grid System, Balance, Symmetry Issues
- **📊 PDF Presentation Analysis** - Slide Design, Content Organization, Typography, Visual Elements
- **🏗️ Architectural Design Analysis** - Composition, Spatial Design, Structural Elements, Materials
- **🔗 Google File Analysis** - Direct analysis of Google Slides, Drive, Docs, and Sheets sharing links

### 🚀 Google Integration (NEW!)
- **📊 Google Slides** → Automatic PDF conversion and presentation analysis
- **💾 Google Drive** → Direct file download and analysis
- **📄 Google Docs** → PDF/DOCX export and document analysis
- **📈 Google Sheets** → PDF/XLSX export and data visualization analysis
- **🔄 Smart URL Conversion** - Automatically converts sharing links to analysis-ready formats

### 📊 Visual Reports
- **📸 Direct Chat Display** - PNG reports embedded in chat via base64
- **🔗 GitHub Auto-Commit** - Reports automatically committed to GitHub
- **📱 Shareable Links** - Easy sharing with GitHub raw URLs
- **💾 Local Storage** - Reports saved to `reports/` folder

### 🚀 Ease of Use
- **❌ No API Key Required** - Only OpenAI API key needed
- **⚡ Automatic Upload** - No manual upload process
- **🎨 Professional Reports** - Colorful charts and scores
- **📊 Detailed Analysis** - Specific feedback for each category
- **🔗 One-Click Google Analysis** - Just paste Google sharing links!

## 📋 Installation

### Cursor MCP Settings
Add to `~/.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "graphic_design_mcp": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/mcanince/graphic-design-mcp",
        "graphic-design-mcp"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    }
  }
}
```

## 🛠️ Usage

### 🔗 Google File Analysis (NEW!)

#### Google Slides Analysis
```
analyze_google_file_link url:https://docs.google.com/presentation/d/FILE_ID/edit?usp=sharing analysis_type:presentation
```

#### Google Drive File Analysis  
```
analyze_google_file_link url:https://drive.google.com/file/d/FILE_ID/view?usp=sharing analysis_type:design
```

#### Google Docs Analysis
```
analyze_google_file_link url:https://docs.google.com/document/d/FILE_ID/edit analysis_type:copywriting
```

#### Google Sheets Analysis
```
analyze_google_file_link url:https://docs.google.com/spreadsheets/d/FILE_ID/edit analysis_type:layout
```

### 🎨 Traditional Analysis Tools

#### 1. Design Analysis
```
analyze_design url:https://example.com/design.jpg
```

#### 2. Copywriting Analysis
```
analyze_copywriting url:https://example.com/ad.jpg
```

#### 3. Website Design Analysis
```
analyze_website_design url:https://example.com
```

#### 4. Layout & Alignment Analysis
```
analyze_layout_alignment url:https://example.com/layout.jpg
```

#### 5. PDF Presentation Analysis
```
analyze_pdf_presentation url:https://example.com/presentation.pdf
```

#### 6. Architectural Design Analysis
```
analyze_architectural_design url:https://example.com/architecture.jpg
```

## 🔄 Google URL Conversion Examples

The tool automatically converts Google sharing URLs:

### Google Slides
```
FROM: https://docs.google.com/presentation/d/1ABC.../edit?usp=sharing
TO:   https://docs.google.com/presentation/d/1ABC.../export/pdf
```

### Google Drive
```
FROM: https://drive.google.com/file/d/1ABC.../view?usp=sharing
TO:   https://drive.google.com/u/0/uc?id=1ABC...&export=download
```

### Google Docs
```
FROM: https://docs.google.com/document/d/1ABC.../edit
TO:   https://docs.google.com/document/d/1ABC.../export?format=pdf
```

### Google Sheets
```
FROM: https://docs.google.com/spreadsheets/d/1ABC.../edit
TO:   https://docs.google.com/spreadsheets/d/1ABC.../export?format=pdf
```

## 📊 Sample Output

🔄 **GOOGLE FILE LINK CONVERSION**

📁 **Original URL:** https://docs.google.com/presentation/d/1ABC.../edit?usp=sharing
📋 **File Type:** Google Slides
🔗 **File ID:** 1ABC...

📎 **Available Analysis URLs:**
• **PDF:** https://docs.google.com/presentation/d/1ABC.../export/pdf
  _PDF version for presentation analysis_
• **PPTX:** https://docs.google.com/presentation/d/1ABC.../export/pptx  
  _PowerPoint version for download_

🎯 **Using for Analysis:** https://docs.google.com/presentation/d/1ABC.../export/pdf

📊 **PDF PRESENTATION ANALYSIS REPORT**

📋 **ANALYSIS RESULTS:**
- Visual Design & Layout: 8/10
- Content Organization: 9/10  
- Typography & Readability: 8/10
- Color Scheme & Consistency: 7/10
- Information Hierarchy: 8/10
- Slide Flow & Structure: 9/10
- Visual Elements Usage: 7/10
- Professional Appearance: 8/10

📊 **QUICK SUMMARY:** 👍 **EXCELLENT** - Overall Score: 8.1/10

## 🔧 Technical Details

### Dependencies
- `fastmcp>=0.1.0`
- `requests>=2.31.0`
- `openai>=1.0.0`
- `Pillow>=9.0.0`
- `PyMuPDF>=1.23.0` (PDF processing)

### Supported Google File Types
- **Google Slides** (.pptx, .pdf)
- **Google Drive Files** (direct download)
- **Google Docs** (.docx, .pdf)
- **Google Sheets** (.xlsx, .pdf)

### Reports
- PNG format 1200x1600 pixels
- Base64 embedded in chat
- Automatic GitHub commit
- Local save to `reports/` folder

### GitHub Integration
- Automatic git add, commit, push
- Sharing with raw URLs
- `reports/` folder organization

## 📋 Version History

- **v4.0.0** - 🔗 Google File Integration + Smart URL Conversion
- **v3.0.0** - Base64 embedding + GitHub auto-commit
- **v2.0.1** - PNG generation bug fixes
- **v2.0.0** - Visual PNG reports added
- **v1.2.0** - Copywriting analysis tool
- **v1.1.0** - Design analysis tool
- **v1.0.0** - Initial release

## 🎯 Use Cases

### 📊 Google Slides Presentation
```bash
analyze_google_file_link url:https://docs.google.com/presentation/d/1ABC.../edit analysis_type:presentation
```

### 💾 Google Drive PDF Analysis
```bash
analyze_google_file_link url:https://drive.google.com/file/d/1ABC.../view analysis_type:presentation
```

### 📄 Google Docs Copywriting Review
```bash
analyze_google_file_link url:https://docs.google.com/document/d/1ABC.../edit analysis_type:copywriting
```

### 📈 Google Sheets Layout Analysis
```bash
analyze_google_file_link url:https://docs.google.com/spreadsheets/d/1ABC.../edit analysis_type:layout
```

### 🎪 Social Media Post
```bash
analyze_design url:https://example.com/instagram-post.jpg
```

### 🏢 Website Analysis
```bash
analyze_website_design url:https://example.com
```

### 📐 Layout Issues Check
```bash
analyze_layout_alignment url:https://example.com/layout-design.jpg
```

### 🏗️ Architectural Design
```bash
analyze_architectural_design url:https://example.com/building-design.jpg
```

## 🚨 Troubleshooting

### Common Issues

**1. OpenAI API Key Error**
```bash
❌ OPENAI_API_KEY not found
```
**Solution:** Make sure you have correctly defined the API key in your MCP configuration.

**2. Google File Access Error**
```bash
❌ URL format not recognized as a Google file sharing link
```
**Solution:** Ensure the Google file is shared with "Anyone with the link can view" permission.

**3. Image Download Error**
```bash
❌ Failed to download image: HTTP 404
```
**Solution:** Ensure the URL is valid and accessible.

**4. MCP Connection Error**
```bash
❌ 0 tools enabled
```
**Solution:** 
- In Cursor: `Cmd+Shift+P` → `MCP: Restart All Connections`
- Check your `mcp.json` configuration

## 📁 File Structure

```
graphic-design-mcp/
├── mcp_graphic_design.py      # Main MCP tool
├── google_link_converter.py   # Standalone Google link converter
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project configuration
├── reports/                  # Generated analysis reports
└── README.md                 # This file
```

## 🔧 Local Testing

```bash
git clone https://github.com/mcanince/graphic-design-mcp
cd graphic-design-mcp
pip install -r requirements.txt

# Test Google link conversion
python google_link_converter.py

# Run MCP server
python mcp_graphic_design.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## 📜 License

This project is distributed under the MIT License.

## 🙏 Acknowledgments

- OpenAI GPT-4o Vision API
- FastMCP framework
- Cursor IDE MCP support
- Google Workspace APIs
- [Research sources for Google URL conversion methods](https://www.graytechnical.com/blog/how-to-easily-create-google-direct-download-links/)

## 📧 Contact

- GitHub: [@mcanince](https://github.com/mcanince)
- Email: mcanince@example.com

---

⭐ If you like this project, don't forget to give it a star!

## 📈 Version History

### v4.0.0 (2024-01-15) - Google Integration Release 🚀
- 🔗 Google Slides analysis with automatic PDF conversion
- 💾 Google Drive file direct download and analysis
- 📄 Google Docs export and analysis (PDF/DOCX)
- 📈 Google Sheets export and analysis (PDF/XLSX)
- 🔄 Smart URL conversion system
- 🎯 `analyze_google_file_link` tool added
- 📋 Standalone `google_link_converter.py` script
- 🛠️ Enhanced error handling and validation
- 📚 Comprehensive documentation update

### v3.0.0 (2024-01-15)
- 📊 PDF Presentation Analysis tool added
- 🏗️ Architectural Design Analysis tool added
- 🎨 6 analysis modes available
- 🔧 Enhanced analysis categories
- ✅ Comprehensive design evaluation

### v1.0.0 (2024-01-15)
- 🎨 Design analysis tool
- 📊 5-category scoring system
- 🔧 Clean and stable code structure
- ✅ Working FastMCP implementation

---

## 🎉 What's New in v4.0.0

🔗 **Google File Integration** - The biggest update yet! Now you can directly analyze:
- Google Slides presentations
- Google Drive files  
- Google Docs documents
- Google Sheets spreadsheets

Just paste the sharing link and let the tool handle the rest! No more manual downloads or conversions needed.

✨ **Powered by OpenAI GPT-4o & Model Context Protocol** 