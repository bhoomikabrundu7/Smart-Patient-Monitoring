from flask import Flask,request,jsonify
import os
from datetime import datetime
from .data_handler import save_sensor_data
from .alerts import check_patient_status

app=Flask(__name__)
latest_data={"temperature":0,"heart_rate":0,"spo2":0,"fall":False,"mode":"WAITING","status":"WAITING","alerts":[],"timestamp":""}
live_history=[]
MAX_HISTORY=100

@app.route("/")
def home(): return "CareMatrix Smart Patient Monitoring Backend is Running"

@app.route("/sensor-data",methods=["POST"])
def receive_sensor_data():
    global latest_data
    data=request.get_json(silent=True)
    if not isinstance(data,dict): return jsonify({"status":"error","message":"Invalid JSON"}),400
    try:
        temperature=float(data.get("temperature",0)); heart_rate=int(data.get("heart_rate",0)); spo2=int(data.get("spo2",0))
        fall=data.get("fall",False)
        fall=fall.strip().lower()=="true" if isinstance(fall,str) else bool(fall)
    except (ValueError,TypeError): return jsonify({"status":"error","message":"Invalid sensor values"}),400
    mode=str(data.get("mode","NORMAL")).upper()
    if mode not in ("NORMAL","ABNORMAL"): mode="NORMAL"
    result=check_patient_status(temperature,heart_rate,spo2,fall)
    alerts=result["alerts"]
    status="ABNORMAL" if mode=="ABNORMAL" or alerts or fall else "NORMAL"
    reading={"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"temperature":temperature,"heart_rate":heart_rate,"spo2":spo2,"fall":fall,"mode":mode,"status":status,"alerts":alerts}
    latest_data=reading.copy(); live_history.append(reading.copy())
    if len(live_history)>MAX_HISTORY: live_history.pop(0)
    save_sensor_data(temperature,heart_rate,spo2,fall,mode)
    print("\n========== CAREMATRIX SENSOR DATA =========="); print(reading); print("============================================")
    return jsonify({"status":"success","message":"Sensor data received","mode":mode,"patient_status":status,"alerts":alerts}),200

@app.route("/latest")
def latest(): return jsonify(latest_data)

@app.route("/history")
def history(): return jsonify(live_history)

@app.route("/health")
def health(): return jsonify({"status":"ok","service":"CareMatrix Backend","live_readings":len(live_history)})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
