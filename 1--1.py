import os
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

# إعدادات السيرفر
PORT = 8000

def run_server():
    server = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    print(f"[*] Local Server started on port {PORT}")
    server.serve_forever()

def start_tunnel():
    time.sleep(2) # انتظار تشغيل السيرفر
    print("[*] Opening Public Link...")
    # فتح الرابط العام باستخدام localtunnel
    os.system(f"lt --port {PORT}")

if __name__ == "__main__":
    # تشغيل السيرفر في خلفية البرنامج
    threading.Thread(target=run_server, daemon=True).start()
    
    print("\n" + "="*40)
    print("🚀 GEOLOCATION SYSTEM IS STARTING...")
    print("="*40)
    
    # تشغيل الرابط العام
    start_tunnel()
