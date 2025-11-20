# test_serial.py
import serial
import json

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

print("시리얼 포트 연결됨. 데이터 대기 중...")

while True:
    line = ser.readline().decode().strip()
    if line:
        print(f"받은 데이터: {line}")
        try:
            data = json.loads(line)
            print(f"JSON 파싱 성공: {data}")
        except Exception as e:
            print(f"JSON 파싱 실패: {e}")