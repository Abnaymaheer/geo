import os
import threading
import asyncio
import json
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import websockets

# --- أمر إجبار Replit على فتح الـ Webview ---
# المنفذ 8080 هو المنفذ الرسمي الذي يبحث عنه Replit
os.system("python3 -m http.server 8080 &")

USER_FILE = "users.json"
HTTP_PORT = 8000 # منفذ الخريطة
WS_PORT = 9000   # منفذ استقبال البيانات (غيرناه لضمان العمل)

def load_users():
    try:
        with open(USER_FILE,'r',encoding='utf-8') as f:
            return json.load(f)
    except: return []

def save_user(user):
    users = load_users()
    users.append(user)
    with open(USER_FILE,'w',encoding='utf-8') as f :
        json.dump(users,f,indent=2)

async def ws_handler(ws):
    try:
        data = await ws.recv()
        user = json.loads(data)
        user["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        save_user(user)
        print('\n[+] DONE! Target Found!')
    except: pass

async def start_ws():
    # الاستماع على المنفذ 9000
    async with websockets.serve(ws_handler,"0.0.0.0",WS_PORT):
        await asyncio.Future()

def start_http():
    server = HTTPServer(("0.0.0.0", HTTP_PORT), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    print("\n" + "="*40)
    print("🚀 LIVE NOW! LOOK AT THE WEBVIEW TAB")
    print("="*40)
    threading.Thread(target=start_http, daemon=True).start()
    asyncio.run(start_ws())
