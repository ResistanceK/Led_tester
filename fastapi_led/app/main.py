from fastapi import FastAPI
import serial, json, threading, requests

app = FastAPI()

# -------------------------------
# 1️⃣ 아두이노 연결 (포트 이름은 필요에 따라 수정)
# -------------------------------
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# -------------------------------
# 2️⃣ FastAPI 서버의 /api/measure 주소
# -------------------------------
@app.post("/api/measure")
def receive_data(data: dict):
    print("✅ 받은 데이터:", data)
    return {"status": "ok", "data": data}

# -------------------------------
# 3️⃣ 아두이노에서 JSON 받아서 FastAPI로 보내기
# -------------------------------
def read_from_arduino():
    while True:
        line = ser.readline().decode().strip()  # 한 줄 읽기
        if not line:
            continue  # 빈 줄이면 무시

        try:
            data = json.loads(line)  # JSON 문자열 → 파이썬 딕셔너리
            print("📩 아두이노 데이터:", data)

            # FastAPI 서버로 전송
            requests.post("http://localhost:8000/api/measure", json=data)

        except:
            print("⚠️ JSON 해석 실패:", line)

# -------------------------------
# 4️⃣ 별도 스레드로 시리얼 읽기 실행
# -------------------------------
thread = threading.Thread(target=read_from_arduino)
thread.daemon = True
thread.start()
