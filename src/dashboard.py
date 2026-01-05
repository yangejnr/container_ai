from flask import Flask, render_template_string, request, jsonify
import easyocr
import cv2
import numpy as np
import sqlite3
import os
import base64
import threading
import time
from datetime import datetime
import requests  # Mock NCS API

app = Flask(__name__)
reader = easyocr.Reader(['en'], gpu=False)
DB_PATH = '/app/data/containers.db'

# Mock NCS Database
NCS_DB = {
    'CSQU3054383': {'departure': 'Lagos', 'datetime': '2026-01-05 14:00', 'status': 'Cleared', 'goods': 'Electronics'},
    'TCLU1234567': {'departure': 'Apapa', 'datetime': '2026-01-05 12:30', 'status': 'Pending', 'goods': 'Textiles'},
    'MEDU9876543': {'departure': 'Tin Can', 'datetime': '2026-01-04 09:15', 'status': 'Held', 'goods': 'Machinery'}
}

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scans 
                 (id INTEGER PRIMARY KEY, code TEXT, departure TEXT, 
                  datetime TEXT, status TEXT, goods TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return '''
<!DOCTYPE html>
<html><head><title>🚢 NCS Container Scanner</title>
<style>body{font-family:Arial;max-width:900px;margin:50px auto;padding:20px;background:#f5f5f5;}
video{width:100%;max-width:640px;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.1);}
input,button{padding:15px;font-size:18px;border:none;border-radius:8px;cursor:pointer;}
#code{width:300px;background:#fff;box-shadow:0 2px 4px rgba(0,0,0,0.1);}
#scan{background:#4CAF50;color:white;font-size:20px;width:150px;}
#result{font-size:28px;padding:20px;border-radius:10px;margin:20px 0;}
.valid{background:#d4edda;color:#155724;border:1px solid #c3e6cb;}
.invalid{background:#f8d7da;color:#721c24;border:1px solid #f5c6cb;}
.info{background:#d1ecf1;color:#0c5460;border:1px solid #bee5eb;padding:15px;}
#history{background:white;padding:20px;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.1);}
.scan-item{padding:10px;border-bottom:1px solid #eee;}
h1{text-align:center;color:#333;}
.status-badge{padding:5px 12px;border-radius:20px;font-size:14px;}
.cleared{background:#d4edda;color:#155724;}
.pending{background:#fff3cd;color:#856404;}
.held{background:#f8d7da;color:#721c24;}
</style></head>
<body>
<h1>🚢 Nigeria Customs Container Scanner</h1>
<img src="/video_feed" style="width:100%;max-width:640px;border-radius:10px;">
<br><br>
<input id="code" placeholder="Hold container code to Svpro..." readonly>
<button id="scan" onclick="autoScan()">🔍 AUTO SCAN</button>
<div id="result"></div>
<h3>📊 Scan History</h3>
<div id="history"></div>

<script>
let scanning = false;
async function autoScan(){
  if(scanning) return;
  scanning = true;
  document.getElementById("scan").innerHTML = "⏳ Scanning NCS DB...";
  
  const res = await fetch("/scan", {method:"POST"});
  const data = await res.json();
  
  document.getElementById("code").value = data.code;
  let resultDiv = document.getElementById("result");
  
  if(data.found){
    resultDiv.innerHTML = `
      <div class="info">
        ✅ <strong>${data.code}</strong> FOUND IN NCS DB<br>
        Departure: ${data.departure} | ${data.datetime}<br>
        Status: <span class="status-badge ${data.status.toLowerCase()}">${data.status}</span><br>
        Goods: ${data.goods}
      </div>`;
  } else {
    resultDiv.innerHTML = `<div class="invalid">❌ ${data.code} - Not in NCS Database</div>`;
  }
  
  loadHistory();
  scanning = false;
  document.getElementById("scan").innerHTML = "🔍 AUTO SCAN";
}

async function loadHistory(){
  const res = await fetch("/history");
  const scans = await res.json();
  document.getElementById("history").innerHTML = scans.map(s=>`
    <div class="scan-item">
      <strong>${s.code}</strong> 
      <span class="status-badge ${s.status.toLowerCase()}">${s.status}</span><br>
      <small>${s.datetime} from ${s.departure} - ${s.goods}</small>
    </div>
  `).join("");
}
loadHistory(); setInterval(loadHistory, 5000);
</script>
</body></html>'''

@app.route('/video_feed')
def video_feed():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
    cap.release()
    return Response(frame, mimetype='image/jpeg')

@app.route("/scan", methods=["POST"])
def scan():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return jsonify({"code": "No camera", "found": False})
    
    # OCR Svpro frame
    results = reader.readtext(frame)
    codes = []
    for (bbox, text, conf) in results:
        if conf > 0.5 and len(text.strip()) >= 8:
            code = ''.join(c for c in text.strip().upper() if c.isalnum())
            if len(code) >= 10:
                codes.append(code)
    
    code = codes[0] if codes else "No code detected"
    
    # NCS DB lookup
    container = NCS_DB.get(code[:11], None)
    if container:
        status = "Cleared" if "Cleared" in container['status'] else "Pending" if "Pending" in container['status'] else "Held"
        data = {
            "code": code, "found": True, "departure": container['departure'],
            "datetime": container['datetime'], "status": status,
            "goods": container['goods']
        }
        # Save to local DB
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO scans VALUES (NULL, ?, ?, ?, ?, ?, ?)", 
                  (code, container['departure'], container['datetime'], 
                   status, container['goods'], datetime.now().isoformat()))
        conn.commit()
        conn.close()
    else:
        data = {"code": code, "found": False}
    
    return jsonify(data)

@app.route("/history")
def history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT code, departure, datetime, status, goods FROM scans ORDER BY id DESC LIMIT 20")
    scans = [{"code": row[0], "departure": row[1], "datetime": row[2], 
              "status": row[3], "goods": row[4]} for row in c.fetchall()]
    conn.close()
    return jsonify(scans)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
