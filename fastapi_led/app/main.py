from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import serial, json, threading, requests
from typing import List
from datetime import datetime

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델
class MeasureData(BaseModel):
    supply_voltage: float
    reference_voltage: float
    led_voltage: float
    current: float
    resistor: float

# 측정값 저장소
measurements: List[dict] = []

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def read_from_arduino():
    while True:
        line = ser.readline().decode().strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            print(f"Arduino 데이터 수신: {data}")  # 디버깅
            requests.post("http://localhost:8000/api/measure", json=data)
        except Exception as e:
            print(f"오류: {e}, 데이터: {line}")

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI LED Tester ready!"}

@app.post("/api/measure")
def receive_measure(data: MeasureData):
    measurement = data.dict()
    measurement["timestamp"] = datetime.now().isoformat()
    measurements.append(measurement)
    
    # 최근 100개만 유지
    if len(measurements) > 100:
        measurements.pop(0)
    
    print(f"측정값 저장됨: {measurement}")  # 디버깅
    return {"status": "success", "data": measurement}

@app.get("/api/latest")
def get_latest():
    if not measurements:
        raise HTTPException(status_code=404, detail="No data available yet")
    return measurements[-1]

@app.get("/api/all")
def get_all():
    return {"count": len(measurements), "data": measurements}


