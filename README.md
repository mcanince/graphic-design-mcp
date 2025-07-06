# 🎨 Graphic Design MCP Tools

**4 farklı MCP (Model Context Protocol) aracı ile profesyonel grafik tasarım analizi**

OpenAI GPT-4o Vision kullanarak tasarım görsellerinizi analiz eden, marka tutarlılığını kontrol eden ve metin önerileri sunan güçlü araçlar koleksiyonu.

## 🚀 Özellikler

### 🎨 **1. Graphic Design Analyzer**
- **Genel tasarım analizi** (5 kategori puanlaması)
- Görsel uyum, netlik, kullanıcı dostu olma değerlendirmesi
- Etkileşim ve yaratıcılık analizi
- 10 üzerinden detaylı puanlama

### 🏷️ **2. Brand Consistency Checker**
- **Marka tutarlılığı analizi** (Tasarım + Website karşılaştırması)
- Website'deki renk paletini otomatik çıkarma
- Marka renkleriyle tasarım uyumu kontrolü
- Logo, tipografi ve görsel dil tutarlılığı

### 📐 **3. Spacing Consistency Analyzer**
- **Boşluk ve hizalama tutarlılığı analizi**
- Grid sistemi değerlendirmesi
- Margin, padding, whitespace analizi
- Pixel/rem değer önerileri

### ✍️ **4. Text Content Generator**
- **7 farklı metin tipi** (başlık, açıklama, CTA, sosyal medya, email, slogan)
- **4 dil desteği** (Türkçe, İngilizce, Almanca, Fransızca)
- Her tip için 6 alternatif öneri
- A/B test metinleri

## 🛠️ Kurulum

### Gereksinimler
- Python 3.8+
- OpenAI API anahtarı

### 1. Proje Kurulumu
```bash
pip install -r requirements.txt
```

### 2. MCP Sunucularını Çalıştırma
Her tool ayrı MCP sunucusu olarak çalışır:

```bash
# Genel tasarım analizi
python mcp_graphic_design.py

# Marka tutarlılığı
python mcp_brand_consistency.py

# Spacing analizi
python mcp_spacing_consistency.py

# Metin üretimi
python mcp_text_generator.py
```

### 3. MCP JSON Konfigürasyonu

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
    },
    "brand_consistency_mcp": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/mcanince/graphic-design-mcp",
        "brand-consistency-mcp"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    },
    "spacing_consistency_mcp": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/mcanince/graphic-design-mcp",
        "spacing-consistency-mcp"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    },
    "text_generator_mcp": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/mcanince/graphic-design-mcp",
        "text-generator-mcp"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    }
  }
}
```

## 📖 Kullanım Kılavuzu

### 🎨 Genel Tasarım Analizi
```bash
@analyze_design url:https://example.com/design.jpg
```

**Çıktı:**
- Görsel uyum: 8/10
- Netlik: 9/10
- Kullanıcı dostu olma: 7/10
- Etkileşim: 6/10
- Yaratıcılık: 8/10

### 🏷️ Marka Tutarlılığı Kontrolü
```bash
@brand_consistency design_url:https://example.com/design.jpg website_url:https://company.com
```

**Çıktı:**
- Renk tutarlılığı: ✅ Uygun
- Logo kullanımı: ⚠️ Kısmen Uygun
- Tipografi: ✅ Uygun
- Görsel dil: ✅ Uygun
- Mesaj tutarlılığı: ❌ Uygun Değil

### 📐 Spacing Analizi
```bash
@check_spacing_consistency url:https://example.com/design.jpg
```

**Çıktı:**
- Margin tutarlılığı: 📐 7/10
- Padding tutarlılığı: 📐 8/10
- Element hizalaması: 📐 6/10
- Grid sistemi: 📐 5/10
- Whitespace kullanımı: 📐 9/10

### ✍️ Metin Üretimi
```bash
# Genel metin
@generate_text_for_design url:https://example.com/design.jpg

# Başlık önerileri
@generate_text_for_design url:https://example.com/design.jpg content_type:başlık

# İngilizce CTA metinleri
@generate_text_for_design url:https://example.com/design.jpg content_type:cta language:ingilizce
```

**Desteklenen İçerik Tipleri:**
- `genel` - Genel metin önerileri
- `başlık` - Çekici başlık önerileri
- `açıklama` - Açıklayıcı paragraflar
- `cta` - Eylem çağrısı (Call-to-Action)
- `sosyal_medya` - Sosyal medya paylaşım metinleri
- `email` - Email pazarlama metinleri
- `slogan` - Marka slogan önerileri

**Desteklenen Diller:**
- `türkçe` - Türkçe metinler
- `ingilizce` - İngilizce metinler
- `almanca` - Almanca metinler
- `fransızca` - Fransızca metinler

## 🎯 Kullanım Senaryoları

### 📊 E-ticaret Sitesi Tasarımı
```bash
# 1. Genel tasarım kalitesini değerlendir
@analyze_design url:https://example.com/homepage-design.jpg

# 2. Mevcut website ile tutarlılığı kontrol et
@brand_consistency design_url:https://example.com/homepage-design.jpg website_url:https://mystore.com

# 3. Spacing problemlerini tespit et
@check_spacing_consistency url:https://example.com/homepage-design.jpg

# 4. Ürün açıklama metinleri üret
@generate_text_for_design url:https://example.com/product-card.jpg content_type:açıklama
```

### 🎪 Sosyal Medya Kampanyası
```bash
# 1. Tasarım etkisini analiz et
@analyze_design url:https://example.com/instagram-post.jpg

# 2. Sosyal medya metinleri üret
@generate_text_for_design url:https://example.com/instagram-post.jpg content_type:sosyal_medya

# 3. İngilizce versiyonu için metin üret
@generate_text_for_design url:https://example.com/instagram-post.jpg content_type:sosyal_medya language:ingilizce
```

### 🏢 Kurumsal Sunum
```bash
# 1. Profesyonellik seviyesini ölç
@analyze_design url:https://example.com/presentation-slide.jpg

# 2. Kurumsal website ile uyumunu kontrol et
@brand_consistency design_url:https://example.com/presentation-slide.jpg website_url:https://company.com

# 3. Başlık önerileri al
@generate_text_for_design url:https://example.com/presentation-slide.jpg content_type:başlık
```

## 📁 Dosya Yapısı

```
graphic-design-mcp/
├── mcp_graphic_design.py      # Genel tasarım analizi
├── mcp_brand_consistency.py   # Marka tutarlılığı
├── mcp_spacing_consistency.py # Spacing analizi
├── mcp_text_generator.py      # Metin üretimi
├── requirements.txt           # Python bağımlılıkları
├── pyproject.toml            # Proje konfigürasyonu
└── README.md                 # Bu dosya
```

## 🔧 Geliştirme

### Yeni Özellik Ekleme
Her MCP tool'u ayrı dosyada bulunur. Yeni özellikler eklemek için:

1. İlgili `.py` dosyasını düzenleyin
2. `@mcp.tool()` decorator'u ile yeni fonksiyon tanımlayın
3. `requirements.txt` ve `pyproject.toml` dosyalarını güncelleyin

### Test Etme
```bash
# Tek bir tool'u test et
python mcp_graphic_design.py

# Tüm tool'ları test et
python -m pytest tests/
```

## 🚨 Hata Giderme

### Yaygın Sorunlar

**1. OpenAI API Anahtarı Hatası**
```bash
❌ OPENAI_API_KEY environment variable bulunamadı
```
**Çözüm:** `.env` dosyasında veya sistem değişkenlerinde API anahtarını tanımlayın.

**2. Görsel İndirme Hatası**
```bash
❌ Görsel indirilemedi. HTTP 404
```
**Çözüm:** URL'nin geçerli ve erişilebilir olduğundan emin olun.

**3. MCP Bağlantı Hatası**
```bash
❌ MCP sunucusuna bağlanılamadı
```
**Çözüm:** `mcp.json` konfigürasyonunu kontrol edin ve API anahtarının doğru olduğundan emin olun.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit'leyin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📜 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. Detaylar için `LICENSE` dosyasını inceleyin.

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

### v0.1.0 (2024-01-15)
- 🎨 Genel tasarım analizi eklendi
- 🏷️ Marka tutarlılığı kontrolü eklendi
- 📐 Spacing analizi eklendi
- ✍️ Metin üretimi eklendi
- 🌍 Çoklu dil desteği eklendi
- 📦 4 ayrı MCP tool'u olarak yapılandırıldı 