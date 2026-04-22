"""
Chương 5 - Sinh dữ liệu giả lập (Simulated Data Generation)
=============================================================
Tạo 5.000 bản ghi log mạng dạng flow mô phỏng kịch bản insider threat:
nhân viên nội bộ truyền lượng lớn dữ liệu ra ngoài tổ chức ngoài giờ làm việc.

Quy tắc gán nhãn leakage (đồng thời thỏa mãn):
  1. bytes_sent > 500 KB
  2. is_external_dst = 1
  3. hour_of_day < 8 hoặc > 18
  4. dst_port ∈ {21, 80, 443, 8080}

~20% bản ghi leakage có nhiễu ngẫu nhiên.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ── Config ──────────────────────────────────────────────────────────────────
SEED = 42
TOTAL_RECORDS = 5000
LEAKAGE_RATIO = 0.15  # 15% leakage
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "network_logs.csv")

# Các tham số mạng
INTERNAL_SUBNETS = ["192.168.1", "192.168.2", "10.0.1", "10.0.2"]
EXTERNAL_SUBNETS = ["203.0.113", "198.51.100", "185.220.101", "45.33.32", "104.16.85"]
NORMAL_PORTS = [22, 53, 80, 443, 3306, 5432, 8080, 8443, 3389, 25, 110, 143]
LEAKAGE_PORTS = [21, 80, 443, 8080]
PROTOCOLS = ["TCP", "UDP", "ICMP"]
PROTOCOL_WEIGHTS_NORMAL = [0.70, 0.25, 0.05]
PROTOCOL_WEIGHTS_LEAKAGE = [0.85, 0.10, 0.05]

np.random.seed(SEED)


def _random_ip(subnets: list[str]) -> str:
    """Sinh IP ngẫu nhiên từ danh sách subnet."""
    subnet = np.random.choice(subnets)
    return f"{subnet}.{np.random.randint(1, 255)}"


def _generate_normal_records(n: int) -> pd.DataFrame:
    """Sinh bản ghi hành vi mạng bình thường."""
    base_date = datetime(2025, 10, 1)
    records = []

    for _ in range(n):
        # Giờ làm việc bình thường: phân phối lệch về 8-18h
        hour = int(np.clip(np.random.normal(13, 3), 0, 23))
        timestamp = base_date + timedelta(
            days=np.random.randint(0, 30),
            hours=hour,
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
        )

        src_ip = _random_ip(INTERNAL_SUBNETS)

        # 70% kết nối nội bộ, 30% ra ngoài
        is_external = int(np.random.random() < 0.30)
        dst_ip = _random_ip(EXTERNAL_SUBNETS if is_external else INTERNAL_SUBNETS)

        dst_port = int(np.random.choice(NORMAL_PORTS))
        protocol = np.random.choice(PROTOCOLS, p=PROTOCOL_WEIGHTS_NORMAL)

        # Lưu lượng bình thường: bytes_sent thấp (trung bình ~50 KB)
        bytes_sent = float(np.random.exponential(50))
        bytes_recv = float(np.random.exponential(80))
        duration = float(np.random.exponential(30))  # ~30 giây

        records.append({
            "timestamp": timestamp,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "dst_port": dst_port,
            "protocol": protocol,
            "bytes_sent": round(bytes_sent, 2),
            "bytes_recv": round(bytes_recv, 2),
            "duration": round(duration, 2),
            "hour_of_day": hour,
            "is_external_dst": is_external,
            "label": 0,
        })

    return pd.DataFrame(records)


def _generate_leakage_records(n: int) -> pd.DataFrame:
    """Sinh bản ghi hành vi rò rỉ dữ liệu."""
    base_date = datetime(2025, 10, 1)
    noise_count = int(n * 0.20)  # ~20% có nhiễu
    records = []

    for i in range(n):
        is_noisy = i < noise_count

        # Ngoài giờ hành chính: trước 8h hoặc sau 18h
        if is_noisy and np.random.random() < 0.5:
            hour = int(np.random.normal(13, 3))  # có thể trong giờ
            hour = int(np.clip(hour, 0, 23))
        else:
            hour = np.random.choice(
                list(range(0, 8)) + list(range(19, 24))
            )

        timestamp = base_date + timedelta(
            days=np.random.randint(0, 30),
            hours=int(hour),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
        )

        src_ip = _random_ip(INTERNAL_SUBNETS)

        # Leakage luôn gửi ra ngoài (trừ nhiễu)
        if is_noisy and np.random.random() < 0.3:
            is_external = 0
            dst_ip = _random_ip(INTERNAL_SUBNETS)
        else:
            is_external = 1
            dst_ip = _random_ip(EXTERNAL_SUBNETS)

        # Port phổ biến cho exfiltration
        if is_noisy and np.random.random() < 0.3:
            dst_port = int(np.random.choice([22, 53, 3306, 5432]))
        else:
            dst_port = int(np.random.choice(LEAKAGE_PORTS))

        protocol = np.random.choice(PROTOCOLS, p=PROTOCOL_WEIGHTS_LEAKAGE)

        # Lưu lượng lớn: bytes_sent > 500 KB (trung bình ~1500 KB)
        if is_noisy and np.random.random() < 0.3:
            bytes_sent = float(np.random.exponential(200))  # có thể < 500
        else:
            bytes_sent = float(np.random.uniform(500, 5000))

        bytes_recv = float(np.random.exponential(40))  # nhận ít
        duration = float(np.random.uniform(60, 600))  # phiên dài hơn

        records.append({
            "timestamp": timestamp,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "dst_port": dst_port,
            "protocol": protocol,
            "bytes_sent": round(bytes_sent, 2),
            "bytes_recv": round(bytes_recv, 2),
            "duration": round(duration, 2),
            "hour_of_day": int(hour),
            "is_external_dst": is_external,
            "label": 1,
        })

    return pd.DataFrame(records)


def generate_dataset() -> pd.DataFrame:
    """Sinh toàn bộ dataset và lưu ra CSV."""
    n_leakage = int(TOTAL_RECORDS * LEAKAGE_RATIO)
    n_normal = TOTAL_RECORDS - n_leakage

    print(f"[*] Sinh {n_normal} bản ghi Normal và {n_leakage} bản ghi Leakage...")
    df_normal = _generate_normal_records(n_normal)
    df_leakage = _generate_leakage_records(n_leakage)

    df = pd.concat([df_normal, df_leakage], ignore_index=True)
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)  # Shuffle

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"[✓] Đã lưu dataset tại: {OUTPUT_FILE}")
    print(f"    Tổng bản ghi : {len(df)}")
    print(f"    Normal (0)   : {(df['label'] == 0).sum()} ({(df['label'] == 0).mean():.1%})")
    print(f"    Leakage (1)  : {(df['label'] == 1).sum()} ({(df['label'] == 1).mean():.1%})")
    print(f"\n[*] 5 bản ghi đầu tiên:")
    print(df.head().to_string(index=False))

    return df


if __name__ == "__main__":
    generate_dataset()
