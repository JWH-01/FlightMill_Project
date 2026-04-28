import serial
import time
import os
from datetime import datetime

PORT = 'COM5'
BAUD = 9600

# ▶ 바탕화면 > Flight_Data 폴더
desktop = os.path.join(os.path.expanduser("~"), "Desktop", "Flight_Data")

# ▶ 폴더 없으면 자동 생성 (안전장치)
os.makedirs(desktop, exist_ok=True)

# ▶ 파일 이름
filename = f"flight_mill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
filepath = os.path.join(desktop, filename)

ser = serial.Serial(PORT, BAUD)
time.sleep(2)

print(f"저장 경로: {filepath}")

# ▶ 시작 신호 (필요하면)
ser.write(b's\n')

with open(filepath, "w", buffering=1) as f:
    f.write("rotation,interval_ms,time_ms,speed_cm_s\n")

    while True:
        try:
            line = ser.readline().decode().strip()

            if line and line[0].isdigit():
                print(line)
                f.write(line + "\n")
                f.flush()   # 핵심

            if "[최종 요약 데이터]" in line:
                print("측정 종료 → 저장 완료")
                break

        except KeyboardInterrupt:
            break

ser.close()