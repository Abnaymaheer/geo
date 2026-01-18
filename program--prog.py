import requests
import json
import asyncio
import websockets

# ⚠️ ضع رابط Replit الخاص بك هنا بين العلامات (بدون أي كلمات إضافية)
RAW_URL = "انسخ_الرابط_هنا" 

# تنظيف الرابط تلقائياً لضمان عدم حدوث خطأ الـ URI
CLEAN_URL = RAW_URL.strip().replace("https://", "").replace("http://", "").split('/')[0]
SERVER_WS = f"wss://{CLEAN_URL}"

def get_ip_info():
   try:
       r = requests.get("https://ipinfo.io/json", timeout=5)
       return r.json()
   except: return None

async def send(datainfo):
    # الاتصال بالرابط المنظف
    async with websockets.connect(SERVER_WS) as ws:
        await ws.send(json.dumps(datainfo))
        print("[+] Data Sent Successfully!")

def main():
    info = get_ip_info()
    if not info: return

    lat, lon = map(float, info["loc"].split(","))
    datainfo = {
        "country": info.get("country"),
        "city": info.get("city"),
        "org": info.get("org"),
        "lat": lat,
        "lon": lon
    }
    
    try:
        asyncio.run(send(datainfo))
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
