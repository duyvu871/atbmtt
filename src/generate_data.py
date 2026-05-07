"""
Chương 5 - Sinh dữ liệu giả lập (Simulated Data Generation)
=============================================================
Tạo 5.000 bản ghi log mạng dạng flow mô phỏng kịch bản insider threat:
nhân viên nội bộ truyền lượng lớn dữ liệu ra ngoài tổ chức ngoài giờ làm việc.

Quy tắc gán nhãn leakage (đồng thời thỏa mãn):
  1. bytes_sent > 5000 KB
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
TOTAL_RECORDS = 100000  # Tăng từ 5000 lên 15000
LEAKAGE_RATIO = 0.12  # Hạ xuống 12% để tạo sự khác biệt
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "network_logs.csv")

# Các tham số mạng — mở rộng với nhiều subnet hơn
INTERNAL_SUBNETS = [
    "192.168.1", "192.168.2", "192.168.3",
    "10.0.1", "10.0.2", "10.0.3", "10.0.4",
    "172.16.0", "172.17.0", "172.18.0",
]
EXTERNAL_SUBNETS = [
    "203.0.113", "198.51.100", "185.220.101", "45.33.32", "104.16.85",
    "8.8.8.8", "1.1.1.1", "208.67.222.222",  # Public DNS, CDN
    "13.107.42", "52.84.214",  # Cloud providers
    "195.154.0", "212.71.0",  # ISP ranges
]
# Mở rộng port list
NORMAL_PORTS = [
    22, 53, 80, 443, 3306, 5432, 8080, 8443, 3389, 25, 110, 143,  # Original
    465, 587, 993, 995,  # Mail ports
    5900, 5901, 5902,  # VNC
    3000, 3001, 8000, 8001, 8888,  # Dev/Web
    6379, 6380, 27017, 27018,  # NoSQL
    9000, 9001, 9200, 9300,  # Elasticsearch
    11211,  # Memcached
    5673, 5672,  # AMQP
    30000, 30001, 30002, 30003,  # Custom
]
LEAKAGE_PORTS = [
    21, 80, 443, 8080,  # Original
    22, 23,  # SSH, Telnet
    8888, 8000,  # Common proxy
    443, 8443,  # HTTPS variants
    5900,  # Remote access
]
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
        # Giờ làm việc bình thường: phân phối lệch về 8-18h nhưng cũng có ngoài giờ
        if np.random.random() < 0.15:  # 15% ngoài giờ bình thường
            hour = int(np.random.choice(list(range(0, 8)) + list(range(18, 24))))
        else:
            hour = int(np.clip(np.random.normal(13, 3), 0, 23))
        
        timestamp = base_date + timedelta(
            days=np.random.randint(0, 60),  # Mở rộng từ 30 sang 60 ngày
            hours=hour,
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
        )

        src_ip = _random_ip(INTERNAL_SUBNETS)
        is_external = int(np.random.random() < 0.35)  # Tăng từ 30% lên 35%
        dst_ip = _random_ip(EXTERNAL_SUBNETS if is_external else INTERNAL_SUBNETS)
        dst_port = int(np.random.choice(NORMAL_PORTS))
        protocol = np.random.choice(PROTOCOLS, p=PROTOCOL_WEIGHTS_NORMAL)

        duration = float(np.random.exponential(40))

        rand_val = np.random.random()
        # Thêm nhiều hơn các loại patterns
        if rand_val < 0.08:  # 8%: DNS queries
            bytes_sent = float(np.random.uniform(50, 200))
            bytes_recv = float(np.random.uniform(100, 500))
            dst_port = 53
            protocol = "UDP"
        elif rand_val < 0.12:  # 4%: Gửi Video/Ảnh lớn 3-25MB
            bytes_sent = float(np.random.uniform(3000, 25000))
            bytes_recv = float(np.random.uniform(10, 100))
        elif rand_val < 0.20:  # 8%: Xem Youtube/Netflix (Download 10MB - 150MB)
            bytes_sent = float(np.random.uniform(10, 100))
            bytes_recv = float(np.random.uniform(10000, 200000))
            duration = float(np.random.uniform(300, 2000))
        elif rand_val < 0.24:  # 4%: Sync Server Nội bộ (20-80MB)
            is_external = 0
            dst_ip = _random_ip(INTERNAL_SUBNETS)
            bytes_sent = float(np.random.uniform(20000, 80000))
            bytes_recv = float(np.random.uniform(100, 500))
        elif rand_val < 0.28:  # 4%: Database replication
            is_external = 0
            dst_ip = _random_ip(INTERNAL_SUBNETS)
            bytes_sent = float(np.random.uniform(5000, 15000))
            bytes_recv = float(np.random.uniform(5000, 15000))
            duration = float(np.random.uniform(300, 1800))
        elif rand_val < 0.32:  # 4%: FTP/SFTP transfer
            bytes_sent = float(np.random.uniform(500, 5000))
            bytes_recv = float(np.random.uniform(100, 500))
            dst_port = int(np.random.choice([21, 22, 22]))  # SFTP
        elif rand_val < 0.36:  # 4%: API calls (small payload)
            bytes_sent = float(np.random.uniform(100, 1000))
            bytes_recv = float(np.random.uniform(100, 2000))
            dst_port = int(np.random.choice([443, 8443, 8080, 8000]))
        elif rand_val < 0.40:  # 4%: Email
            bytes_sent = float(np.random.uniform(50, 500))
            bytes_recv = float(np.random.uniform(50, 1000))
            dst_port = int(np.random.choice([25, 587, 465]))
            protocol = "TCP"
        else:  # 60%: Regular small connections
            bytes_sent = float(np.random.exponential(30))
            bytes_recv = float(np.random.exponential(150))

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
    noise_count = int(n * 0.35)  # Tăng từ 30% lên 35% noise
    records = []

    for i in range(n):
        is_noisy = i < noise_count

        # Kẻ gian thường tuồn ngoài giờ (18h-8h sáng hôm sau)
        # Nhưng đôi khi lẩn trốn vào giờ hành chính (nhiễu)
        if is_noisy and np.random.random() < 0.7:  # Tăng khả năng lẩn trốn
            hour = int(np.clip(np.random.normal(14, 3), 0, 23)) # Lẻn vào giờ làm
        else:
            hour = np.random.choice(list(range(0, 8)) + list(range(19, 24)))

        timestamp = base_date + timedelta(
            days=np.random.randint(0, 60),  # Mở rộng từ 30 sang 60 ngày
            hours=int(hour),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
        )

        src_ip = _random_ip(INTERNAL_SUBNETS)

        # Leakage đa phần bắn ra ngoài
        if is_noisy and np.random.random() < 0.25:  # Tăng từ 20% lên 25%
            is_external = 0
            dst_ip = _random_ip(INTERNAL_SUBNETS)
        else:
            is_external = 1
            dst_ip = _random_ip(EXTERNAL_SUBNETS)

        # Chọn port với logic đa dạng
        if is_noisy and np.random.random() < 0.3:
            dst_port = int(np.random.choice([22, 53, 3306, 27017, 5432]))  # Lẻn qua các port khác
        else:
            dst_port = int(np.random.choice(LEAKAGE_PORTS))
        
        protocol = np.random.choice(PROTOCOLS, p=PROTOCOL_WEIGHTS_LEAKAGE)

        rand_val = np.random.random()
        if is_noisy and rand_val < 0.2:  # 20%: Nhỏ giọt (Drip Leakage)
            bytes_sent = float(np.random.uniform(50, 500))
            duration = float(np.random.uniform(10, 60))
        elif is_noisy and rand_val < 0.35:  # 15%: Tuồn qua đường ngầm DNS
            protocol = "UDP"
            dst_port = 53
            bytes_sent = float(np.random.uniform(2000, 8000))
            duration = float(np.random.uniform(30, 300))
        elif is_noisy and rand_val < 0.50:  # 15%: HTTPS encryption bypass
            protocol = "TCP"
            dst_port = 443
            bytes_sent = float(np.random.uniform(10000, 50000))
            duration = float(np.random.uniform(60, 500))
        elif is_noisy and rand_val < 0.65:  # 15%: Multiple small transfers (tinh vi)
            bytes_sent = float(np.random.uniform(500, 2000))
            duration = float(np.random.uniform(5, 120))
        elif is_noisy and rand_val < 0.80:  # 15%: SSH tunnel exfiltration
            protocol = "TCP"
            dst_port = 22
            bytes_sent = float(np.random.uniform(5000, 20000))
            duration = float(np.random.uniform(60, 400))
        else:  # 20%: Tuồn ồ ạt tiêu chuẩn
            bytes_sent = float(np.random.uniform(100000, 800000)) # DB Dump/ZIP (100MB - 800MB)
            duration = float(np.random.uniform(300, 1200))

        bytes_recv = float(np.random.exponential(15))  # Hầu như không tải xuống
        
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
