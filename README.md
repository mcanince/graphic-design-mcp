# Graphic Design MCP v3.0.0 🎨

Grafik tasarım analizi için MCP (Model Context Protocol) aracı. OpenAI GPT-4 Vision kullanarak tasarımları detaylı analiz eder ve görsel raporlar oluşturur.

## ✨ Özellikler

### 🎯 Analiz Türleri
- **🎨 Tasarım Analizi** - Visual Harmony, Clarity, User Friendliness, Interactivity, Creativity
- **✍️ Copywriting Analizi** - Clarity, Persuasiveness, Emotional Appeal, Call-to-Action, Brand Voice

### 📊 Görsel Raporlar
- **📸 Chat'te Direkt Gösterim** - PNG raporları base64 ile chat'e embed edilir
- **🔗 GitHub Auto-Commit** - Raporlar otomatik olarak GitHub'a commit edilir
- **📱 Paylaşılabilir Linkler** - GitHub raw URL'leri ile kolay paylaşım
- **💾 Yerel Kayıt** - Raporlar `reports/` klasörüne kaydedilir

### 🚀 Kullanım Kolaylığı
- **❌ API Key Gerektirmez** - Sadece OpenAI API key'i gerekli
- **⚡ Otomatik Upload** - Manuel upload işlemi yok
- **🎨 Profesyonel Raporlar** - Renkli çizelgeler ve skorlar
- **📊 Detaylı Analiz** - Her kategori için özel geri bildirim

## 📋 Kurulum

### Cursor MCP Ayarları
`~/.cursor/mcp.json` dosyasına ekleyin:

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

## 🛠️ Kullanım

### 1. Tasarım Analizi
```
analyze_design url:https://example.com/design.jpg
```

### 2. Copywriting Analizi
```
analyze_copywriting url:https://example.com/ad.jpg
```

## 📊 Örnek Çıktı

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

## 🔧 Teknik Detaylar

### Bağımlılıklar
- `fastmcp>=0.1.0`
- `requests>=2.31.0`
- `openai>=1.0.0`
- `Pillow>=9.0.0`

### Raporlar
- PNG formatında 1200x1600 piksel
- Base64 olarak chat'e embed
- GitHub'a otomatik commit
- Yerel `reports/` klasörüne kayıt

### GitHub Entegrasyonu
- Otomatik git add, commit, push
- Raw URL'ler ile paylaşım
- `reports/` klasörü organizasyonu

## �� Versiyon Geçmişi

- **v3.0.0** - Base64 embedding + GitHub auto-commit
- **v2.0.1** - PNG generation bug fixes
- **v2.0.0** - Visual PNG reports added
- **v1.2.0** - Copywriting analysis tool
- **v1.1.0** - Design analysis tool
- **v1.0.0** - Initial release

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🔗 Links

- [GitHub Repository](https://github.com/mcanince/graphic-design-mcp)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [OpenAI API](https://openai.com/api/)

---

✨ **Powered by OpenAI GPT-4 Vision & Model Context Protocol**

## 🎯 Kullanım Senaryoları

### 📊 Website Tasarımı
```bash
@analyze_design url:https://example.com/homepage-mockup.jpg
```

### 🎪 Sosyal Medya Post'u
```bash
@analyze_design url:https://example.com/instagram-post.jpg
```

### 🏢 Sunum Slide'ı
```bash
@analyze_design url:https://example.com/presentation-slide.jpg
```

### 📱 Mobil App UI
```bash
@analyze_design url:https://example.com/mobile-app-screen.jpg
```

## 🚨 Hata Giderme

### Yaygın Sorunlar

**1. OpenAI API Anahtarı Hatası**
```bash
❌ OPENAI_API_KEY not found
```
**Çözüm:** MCP konfigürasyonunda API anahtarını doğru tanımladığınızdan emin olun.

**2. Görsel İndirme Hatası**
```bash
❌ Failed to download image: HTTP 404
```
**Çözüm:** URL'nin geçerli ve erişilebilir olduğundan emin olun.

**3. MCP Bağlantı Hatası**
```bash
❌ 0 tools enabled
```
**Çözüm:** 
- Cursor'da `Cmd+Shift+P` → `MCP: Restart All Connections`
- `mcp.json` konfigürasyonunu kontrol edin

## 📁 Dosya Yapısı

```
graphic-design-mcp/
├── mcp_graphic_design.py      # Ana MCP tool
├── requirements.txt           # Python bağımlılıkları
├── pyproject.toml            # Proje konfigürasyonu
└── README.md                 # Bu dosya
```

## 🔧 Yerel Test

```bash
git clone https://github.com/mcanince/graphic-design-mcp
cd graphic-design-mcp
pip install -r requirements.txt
python mcp_graphic_design.py
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/NewFeature`)
3. Commit'leyin (`git commit -m 'Add NewFeature'`)
4. Push edin (`git push origin feature/NewFeature`)
5. Pull Request açın

## 📜 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.

## 🙏 Teşekkürler

- OpenAI GPT-4o Vision API
- FastMCP framework
- Cursor IDE MCP desteği

## 📧 İletişim

- GitHub: [@mcanince](https://github.com/mcanince)
- Email: mcanince@example.com

---

⭐ Bu projeyi beğendiyseniz star vermeyi unutmayın!

## 📈 Versiyon Geçmişi

### v1.0.0 (2024-01-15)
- 🎨 Tasarım analizi tool'u
- 📊 5 kategori puanlama sistemi
- 🔧 Temiz ve stabil kod yapısı
- ✅ Çalışan FastMCP implementasyonu 