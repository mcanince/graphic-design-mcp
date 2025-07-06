# 🎨 Graphic Design MCP Tool

**OpenAI GPT-4o Vision ile profesyonel grafik tasarım analizi**

Tek tool ile tasarım görsellerinizi 5 kategoride analiz eder ve detaylı geri bildirim sunar.

## 🚀 Özellikler

### 🎨 **Design Analyzer**
- **5 kategori puanlaması** (Visual Harmony, Clarity, User Friendliness, Interactivity, Creativity)
- Her kategori için 10 üzerinden puanlama
- Detaylı açıklamalar ve öneriler
- OpenAI GPT-4o Vision powered analiz

## 🛠️ Kurulum

### MCP JSON Konfigürasyonu

`~/.cursor/mcp.json` dosyanıza şunu ekleyin:

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

## 📖 Kullanım

### 🎨 Tasarım Analizi
```bash
@analyze_design url:https://example.com/design.jpg
```

**Örnek Çıktı:**
- Visual Harmony: 8/10
- Clarity: 9/10  
- User Friendliness: 7/10
- Interactivity: 6/10
- Creativity: 8/10
- **Overall Score: 7.6/10**

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