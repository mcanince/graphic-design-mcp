# Graphic Design MCP v3.0.0 🎨

MCP (Model Context Protocol) tool for graphic design analysis. Analyzes designs in detail using OpenAI GPT-4 Vision and creates visual reports.

## ✨ Features

### 🎯 Analysis Types
- **🎨 Design Analysis** - Visual Harmony, Clarity, User Friendliness, Interactivity, Creativity
- **✍️ Copywriting Analysis** - Clarity, Persuasiveness, Emotional Appeal, Call-to-Action, Brand Voice

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

### 1. Design Analysis
```
analyze_design url:https://example.com/design.jpg
```

### 2. Copywriting Analysis
```
analyze_copywriting url:https://example.com/ad.jpg
```

## 📊 Sample Output

🎨 **GRAPHIC DESIGN ANALYSIS REPORT**

📋 **ANALYSIS RESULTS:**
- Visual Harmony: 8/10
- Clarity: 9/10  
- User Friendliness: 8/10
- Interactivity: 7/10
- Creativity: 7/10

📸 **VISUAL REPORT IMAGE:**
![Analysis Report](data:image/png;base64,...)

🔗 **Shareable Link:** https://raw.githubusercontent.com/username/repo/main/reports/...

📊 **QUICK SUMMARY:** 👍 **GOOD** - Overall Score: 7.8/10

## 🔧 Technical Details

### Dependencies
- `fastmcp>=0.1.0`
- `requests>=2.31.0`
- `openai>=1.0.0`
- `Pillow>=9.0.0`

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

- **v3.0.0** - Base64 embedding + GitHub auto-commit
- **v2.0.1** - PNG generation bug fixes
- **v2.0.0** - Visual PNG reports added
- **v1.2.0** - Copywriting analysis tool
- **v1.1.0** - Design analysis tool
- **v1.0.0** - Initial release

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/mcanince/graphic-design-mcp)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [OpenAI API](https://openai.com/api/)

---

✨ **Powered by OpenAI GPT-4o & Model Context Protocol**

## 🎯 Use Cases

### 📊 Website Design
```bash
@analyze_design url:https://example.com/homepage-mockup.jpg
```

### 🎪 Social Media Post
```bash
@analyze_design url:https://example.com/instagram-post.jpg
```

### 🏢 Presentation Slide
```bash
@analyze_design url:https://example.com/presentation-slide.jpg
```

### 📱 Mobile App UI
```bash
@analyze_design url:https://example.com/mobile-app-screen.jpg
```

## 🚨 Troubleshooting

### Common Issues

**1. OpenAI API Key Error**
```bash
❌ OPENAI_API_KEY not found
```
**Solution:** Make sure you have correctly defined the API key in your MCP configuration.

**2. Image Download Error**
```bash
❌ Failed to download image: HTTP 404
```
**Solution:** Ensure the URL is valid and accessible.

**3. MCP Connection Error**
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
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## 🔧 Local Testing

```bash
git clone https://github.com/mcanince/graphic-design-mcp
cd graphic-design-mcp
pip install -r requirements.txt
python mcp_graphic_design.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request



## 📧 Contact

- GitHub: [@mcanince](https://github.com/mcanince)
- Email: mcanince@hotmail.com

---

⭐ If you like this project, don't forget to give it a star!

## 📈 Version History

### v1.0.0 (2024-01-15)
- 🎨 Design analysis tool
- 📊 5-category scoring system
- 🔧 Clean and stable code structure
- ✅ Working FastMCP implementation 