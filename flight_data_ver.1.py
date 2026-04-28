import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

folder = os.path.join(os.path.expanduser("~"), "Desktop", "Flight_Data")

timestamp = input("파일 시간 입력 (예: 20260428_123456) : ")

filepath = None
for file in os.listdir(folder):
    if timestamp in file and file.endswith(".csv"):
        filepath = os.path.join(folder, file)
        break

if filepath is None:
    raise FileNotFoundError("해당 파일을 찾을 수 없음")

print("선택된 파일:", filepath)

df = pd.read_csv(filepath)

# Hz 계산 (필요한 경우)
if "Hz" not in df.columns:
    df["Hz"] = 1000 / df["interval_ms"]

#표

# 시간 변환
df["time_s"] = df["time_ms"] / 1000

# 반지름 (수정 필요!)
r = 0.125

# 속도
df["speed"] = 2 * np.pi * r * df["Hz"]

# 거리 계산
df["dt"] = df["time_s"].diff()
df["distance"] = df["speed"] * df["dt"]

# 가속도
df["acc"] = df["speed"].diff() / df["dt"]

# 요약값
total_time = df["time_s"].iloc[-1] - df["time_s"].iloc[0]
total_distance = df["distance"].sum()
avg_speed = total_distance / total_time
max_speed = df["speed"].max()
max_acc = df["acc"].max()

max_idx = df["acc"].idxmax()
max_acc_interval = f"{max_idx-1} ~ {max_idx}"

# 📊 요약 테이블
summary = pd.DataFrame({
    "Total Time (s)": [total_time],
    "Total Distance (m)": [total_distance],
    "Average Speed (m/s)": [avg_speed],
    "Max Speed (m/s)": [max_speed],
    "Max Acceleration (m/s^2)": [max_acc],
    "Max Acc Interval": [max_acc_interval]
})

print(summary)

# 저장
summary.to_csv(filepath.replace(".csv", "_summary.csv"), index=False)

# 그래프
plt.figure()
plt.plot(df["time_ms"], df["Hz"])

plt.xlabel("Time (ms)")
plt.ylabel("Frequency (Hz)")
plt.title("Flight Mill Frequency vs Time")
plt.grid()
plt.savefig(filepath.replace(".csv", ".png"), dpi=300)
plt.show()