# Grafik Tasarım MCP Server

Bu proje, grafik tasarım görsellerini analiz eden bir MCP (Model Context Protocol) server'ıdır. OpenAI GPT-4o kullanarak görsel tasarımları analiz eder ve detaylı puanlama yapar.

## Özellikler

- 🎨 Grafik tasarım analizi
- 📊 5 kategoride puanlama
- 🔍 UI/UX uzmanı perspektifi
- 🚀 Cursor IDE entegrasyonu

## Kurulum

### Cursor MCP ile kullanım:

`~/.cursor/mcp.json` dosyanıza ekleyin:

```json
{
  "mcpServers": {
    "Grafik Tasarim MCP": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/mcanince/grafik-tasarim-mcp",
        "grafik-tasarim-mcp"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key-here"
      }
    }
  }
}
```

## Analiz Kategorileri

1. **Görsel Uyum** - Renkler, tipografi, düzen
2. **Netlik** - Bilgi aktarımı kalitesi  
3. **Kullanıcı Dostu** - Kullanım kolaylığı
4. **Etkileşim** - Navigasyon ve butonlar
5. **Yaratıcılık** - Özgünlük ve benzersizlik

## Gereksinimler

- Python 3.8+
- OpenAI API Key
- Internet bağlantısı 