import requests
import json
import asyncio
import websockets

# ⚠️ ضع هنا الرابط الذي سيظهر لك بعد تشغيل 1.py (مثلاً: https://short-dots-run.loca.lt)
SERVER_URL = "ضع_الرابط_هنا"

# تحويل الرابط تلقائياً ليعمل مع بروتوكول الـ Websocket المشفر (wss)
SERVER_WS = SERVER_URL.replace("https://", "wss://")

def get_ip_info():
   try:
       r = requests.get("https://ipinfo.io/json", timeout=5)
       return r.json()
   except:
       return None

def is_morocco(info):
    return info.get("country") == "MA"

async def send(datainfo):
    # استخدام SERVER_WS الذي تم تجهيزه بالأعلى
    async with websockets.connect(SERVER_WS) as ws:
        await ws.send(json.dumps(datainfo))

def main():
    info = get_ip_info()
    if not info:
        print("[-] Connection Error")
        return

    if not is_morocco(info):
        print('[-] User not in Morocco')
        return

    lat, lon = map(float, info["loc"].split(","))
    datainfo = {
        "country": "MA",
        "city": info.get("city"),
        "org": info.get("org"),
        "lat": lat,
        "lon": lon
    }
    
    try:
        asyncio.run(send(datainfo))
        print("[+] Success! Data sent via Localtunnel.")
    except Exception as e:
        print(f"[-] Failed to send: {e}")

if __name__ == "__main__":
    main()
