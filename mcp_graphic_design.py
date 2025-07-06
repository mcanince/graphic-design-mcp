#!/usr/bin/env python3
import os, sys, json, base64, requests, logging
from openai import OpenAI
from datetime import datetime

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/mcp_graphic_design.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

def get_openai_api_key():
    """Environment variable'dan OpenAI API anahtarını alır"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable bulunamadı")
    return api_key

def initialize_server(request_id):
    """MCP sunucusunu başlatır"""
    logger.info(f"Initialize server called with request_id: {request_id}")
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "tools": {"listChanged": True},
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
    logger.info(f"Initialize response: {json.dumps(response)}")
    return response

def list_tools(request_id):
    """MCP tools listesini döner"""
    logger.info(f"List tools called with request_id: {request_id}")
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
    logger.info(f"List tools response: {json.dumps(response)}")
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
        api_key = get_openai_api_key()
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
    logger.info("MCP Server starting...")
    logger.info("Environment variables available:")
    logger.info(f"OPENAI_API_KEY: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
    
    # Multiple requests için loop
    while True:
        try:
            # stdin'den tek satır JSON oku
            logger.info("Reading single line from stdin...")
            input_data = sys.stdin.readline()
            logger.info(f"Received input: {repr(input_data)}")
            
            if not input_data.strip():
                logger.warning("Empty input received - breaking loop")
                break
                
            payload = json.loads(input_data)
            method = payload.get("method")
            request_id = payload.get("id")
            params = payload.get("params", {})
            
            logger.info(f"Method: {method}, Request ID: {request_id}, Params: {params}")
            
            if method == "initialize":
                response = initialize_server(request_id)
                print(json.dumps(response))
                sys.stdout.flush()
            elif method == "tools/list":
                response = list_tools(request_id)
                print(json.dumps(response))
                sys.stdout.flush()
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                logger.info(f"Tool call: {tool_name}, Arguments: {arguments}")
                response = call_tool(request_id, tool_name, arguments)
                print(json.dumps(response))
                sys.stdout.flush()
            else:
                logger.warning(f"Unknown method: {method}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
        except EOFError:
            logger.info("EOF reached - stopping server")
            break
        except Exception as e:
            logger.error(f"General error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": request_id if 'request_id' in locals() else None,
                "error": {
                    "code": -32000,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
    
    logger.info("MCP Server finished processing all requests")

if __name__ == "__main__":
    main()