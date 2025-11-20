from fastapi import FastAPI
import serial, json, threading, requests

app = FastAPI()

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def read_from_arduino():
    while True:
        line = ser.readline().decode().strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            requests.post("http://localhost:8000/api/measure", json=data)
        except:
            print("JSON 오류:", line)

# FastAPI 서버가 시작될 때 스레드 시작
@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()
