from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import serial, json, threading, requests
from typing import List
from datetime import datetime

app = FastAPI()

# CORS 설정 (프론트엔드 연결 시 필요)
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

# 측정값 저장소 (메모리)
measurements: List[dict] = []

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def read_from_arduino():
    while True:
        line = ser.readline().decode().strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            requests.post("http://localhost:8000/api/measure", json=data)
        except Exception as e:
            print("JSON 오류:", line, e)

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

# 루트 엔드포인트
@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI LED Tester ready!"}

# 측정 데이터 수신 엔드포인트 (추가!)
@app.post("/api/measure")
def receive_measure(data: MeasureData):
    measurement = data.dict()
    measurement["timestamp"] = datetime.now().isoformat()
    measurements.append(measurement)
    
    # 최근 100개만 유지
    if len(measurements) > 100:
        measurements.pop(0)
    
    return {"status": "success", "data": measurement}

# 최신 측정값 조회
@app.get("/api/latest")
def get_latest():
    if not measurements:
        return {"status": "no_data"}
    return measurements[-1]

# 전체 측정값 조회
@app.get("/api/all")
def get_all():
    return {"count": len(measurements), "data": measurements}