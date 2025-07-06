#!/usr/bin/env python3
import os, sys, json, base64, requests
from openai import OpenAI

def get_openai_key_from_cursor_config():
    try:
        cursor_config_path = os.path.expanduser("~/.cursor/mcp.json")
        with open(cursor_config_path, 'r') as f:
            config = json.load(f)
        
        env_vars = config["mcpServers"]["Grafik Tasarim MCP"]["env"]
        api_key = env_vars.get("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OpenAI API key Cursor MCP konfigürasyonunda bulunamadı")
        return api_key
    except Exception as e:
        raise Exception(f"API key alınırken hata: {e}")

def initialize_server(request_id):
    """MCP sunucusunu başlatır"""
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "logging": {},
                "prompts": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "Grafik Tasarım MCP",
                "version": "1.0.0"
            }
        }
    }
    return response

def list_tools(request_id):
    """MCP tools listesini döner"""
    tools = [
        {
            "name": "analyze_design",
            "description": "Grafik tasarım görselini analiz eder ve puanlama yapar",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Analiz edilecek görselin URL'si"
                    }
                },
                "required": ["url"]
            }
        }
    ]
    
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": tools
        }
    }
    
    return response

def fetch_image_base64(url):
    """URL'den görseli indirir ve base64'e çevirir"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Görsel indirilemedi. HTTP {response.status_code}")
        return base64.b64encode(response.content).decode()
    except Exception as e:
        raise Exception(f"Görsel indirme hatası: {e}")

def analyze_image_with_openai(b64img):
    """OpenAI GPT-4o ile görsel analizi yapar"""
    try:
        api_key = get_openai_key_from_cursor_config()
        client = OpenAI(api_key=api_key)
        
        prompt = """
        Sen profesyonel bir UI/UX tasarım uzmanısın.
        Verilen tasarım görselini şu kategorilerde analiz et:

        1. **Görsel Uyum** (renkler, tipografi, düzen tutarlılığı)
        2. **Netlik** (bilginin ne kadar açık aktarıldığı)
        3. **Kullanıcı Dostu Olma** (kullanım kolaylığı, sezgisel akış)
        4. **Etkileşim** (navigasyon, buton netliği, etkileşim ipuçları)
        5. **Yaratıcılık** (özgünlük ve tasarım benzersizliği)

        Her kategori için:
        - 10 üzerinden puan ver
        - Kısa açıklama yap

        Sonunda genel bir puan ver (10 üzerinden ortalama).
        """
        
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
                                "url": f"data:image/png;base64,{b64img}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"OpenAI analiz hatası: {e}")

def call_tool(request_id, tool_name, arguments):
    """MCP tool çağrısını işler"""
    try:
        if tool_name == "analyze_design":
            url = arguments.get("url")
            if not url:
                raise Exception("URL parametresi gerekli")
            
            # URL temizle (@ işareti varsa kaldır)
            url = url.lstrip('@').strip()
            
            # Görseli indir ve analiz et
            b64_img = fetch_image_base64(url)
            analysis = analyze_image_with_openai(b64_img)
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"🎨 **Grafik Tasarım Analizi**\n\n{analysis}"
                        }
                    ]
                }
            }
            return response
        else:
            raise Exception(f"Bilinmeyen tool: {tool_name}")
            
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }

def main():
    """Ana MCP handler fonksiyonu"""
    try:
        # stdin'den JSON oku
        input_data = sys.stdin.read()
        if not input_data.strip():
            return
            
        payload = json.loads(input_data)
        method = payload.get("method")
        request_id = payload.get("id")
        params = payload.get("params", {})
        
        if method == "initialize":
            response = initialize_server(request_id)
            print(json.dumps(response))
        elif method == "tools/list":
            response = list_tools(request_id)
            print(json.dumps(response))
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            response = call_tool(request_id, tool_name, arguments)
            print(json.dumps(response))
        else:
            error_response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
            print(json.dumps(error_response))
            
    except json.JSONDecodeError as e:
        error_response = {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32700,
                "message": f"Parse error: {str(e)}"
            }
        }
        print(json.dumps(error_response))
    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "id": request_id if 'request_id' in locals() else None,
            "error": {
                "code": -32000,
                "message": f"Internal error: {str(e)}"
            }
        }
        print(json.dumps(error_response))

if __name__ == "__main__":
    main()