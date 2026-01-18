import requests
import json
import asyncio
import websockets

# العنوان مأخوذ من الصورة التي أرسلتها (عنوان التابلت السيرفر)
SERVER_WS = "ws://192.168.1.3:8765"

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
    asyncio.run(send(datainfo))
    print("[+] sended")

if __name__ == "__main__":
    main()
