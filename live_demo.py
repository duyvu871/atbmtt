#!/usr/bin/env python3
"""
KỊCH BẢN DEMO LIVE: BẮT LOG THỜI GIAN THỰC
==========================================
Script này mô phỏng luồng đẩy dữ liệu thật (như Kafka hoặc Firehose).
Dữ liệu mạng đi vào, được trích xuất đặc trưng (Feature Engineering)
và được phán xử bởi 3 mô hình cùng lúc.
"""

import sys
import os
import time
import pandas as pd
import numpy as np
import warnings

# Tắt các warning để console sạch sẽ
warnings.filterwarnings('ignore')

# Thêm đường dẫn src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from preprocess import run_preprocessing_pipeline, NUMERIC_COLS, FEATURE_COLS
from train_models import train_all_models

# Colors for terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== {text} ==={Colors.RESET}")

def simulate_realtime_detection():
    print(f"{Colors.YELLOW}[*] Đang khởi động hệ thống Core Engine...{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Nạp dữ liệu lịch sử và huấn luyện mô hình màng lọc...{Colors.RESET}\n")
    
    # Bước 1: Huấn luyện nhanh màng lọc
    X_train, X_test, y_train, y_test, scaler, le = run_preprocessing_pipeline()
    models = train_all_models(X_train, y_train)
    
    # Xoá màn hình để làm demo thật
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.BLUE}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}║   HỆ THỐNG GIÁM SÁT RÒ RỈ DỮ LIỆU ĐA LỚP SOC (THỜI GIAN THỰC)  ║{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}╚════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    print(f"Trạng thái: {Colors.GREEN}ONLINE{Colors.RESET} | Chờ kết nối mạng...")
    time.sleep(1.5)

    # Dữ liệu mô phỏng chạy qua mạng
    live_logs = [
        {
            "desc": "Nhân viên làm việc bình thường (Gửi email nhỏ)",
            "timestamp": "2025-10-15 14:30:00",
            "src_ip": "192.168.1.50", "dst_ip": "203.0.113.10", "dst_port": 443,
            "protocol": "TCP", "bytes_sent": 25.5, "bytes_recv": 120.0,
            "duration": 40.0, "hour_of_day": 14, "is_external_dst": 1
        },
        {
            "desc": "[BÌNH THƯỜNG] Nhân viên tải ảnh 4MB lên Facebook/Google Drive",
            "timestamp": "2025-10-15 11:15:00",
            "src_ip": "192.168.2.15", "dst_ip": "31.13.71.36", "dst_port": 443,
            "protocol": "TCP", "bytes_sent": 4000.0, "bytes_recv": 80.0,
            "duration": 12.0, "hour_of_day": 11, "is_external_dst": 1
        },
        {
            "desc": "[BÌNH THƯỜNG] Nhân viên xem Youtube giờ nghỉ trưa (Tải xuống 50MB)",
            "timestamp": "2025-10-15 12:30:00",
            "src_ip": "10.0.1.66", "dst_ip": "142.250.207.46", "dst_port": 443,
            "protocol": "TCP", "bytes_sent": 1500.0, "bytes_recv": 50000.0,
            "duration": 600.0, "hour_of_day": 12, "is_external_dst": 1
        },
        {
            "desc": "[EDGE CASE 1] NV Marketing upload ảnh sản phẩm 4MB lên Drive (giờ HC)",
            "timestamp": "2025-10-15 15:00:00",
            "src_ip": "192.168.1.55", "dst_ip": "203.0.113.88", "dst_port": 443,
            "protocol": "TCP", "bytes_sent": 4000.0, "bytes_recv": 80.0,
            "duration": 15.0, "hour_of_day": 15, "is_external_dst": 1
        },
        {
            "desc": "[EDGE CASE 2] NV Kỹ thuật upload bản vẽ CAD 65MB lúc tăng ca tối",
            "timestamp": "2025-10-15 20:00:00",
            "src_ip": "192.168.1.55", "dst_ip": "203.0.113.88", "dst_port": 443,
            "protocol": "TCP", "bytes_sent": 65000.0, "bytes_recv": 200.0,
            "duration": 450.0, "hour_of_day": 20, "is_external_dst": 1
        },
        {
            "desc": "Tấn công rò rỉ dữ liệu ồ ạt (Hacker kinh điển)",
            "timestamp": "2025-10-16 02:45:00",
            "src_ip": "10.0.1.20", "dst_ip": "45.33.32.99", "dst_port": 443,
            "protocol": "TCP", "bytes_sent": 250000.0, "bytes_recv": 15.0,
            "duration": 500.0, "hour_of_day": 2, "is_external_dst": 1
        },
        {
            "desc": "[EDGE CASE 2] Kẻ cắp tuồn nhỏ giọt (Drip Leakage)",
            "timestamp": "2025-10-17 03:15:00",
            "src_ip": "192.168.2.110", "dst_ip": "185.220.101.5", "dst_port": 443,
            "protocol": "TCP", "bytes_sent": 120.0, "bytes_recv": 2.0,
            "duration": 800.0, "hour_of_day": 3, "is_external_dst": 1
        },
        {
            "desc": "[EDGE CASE 3] Tuồn ngầm qua cổng DNS UDP (DNS Tunneling)",
            "timestamp": "2025-10-17 10:30:00",
            "src_ip": "10.0.2.14", "dst_ip": "8.8.8.8", "dst_port": 53,
            "protocol": "UDP", "bytes_sent": 2500.0, "bytes_recv": 15.0, # DNS gửi 2.5MB là phi lý
            "duration": 60.0, "hour_of_day": 10, "is_external_dst": 1
        },
        {
            "desc": "[EDGE CASE 4] NV IT Backup Code lên Server Nội bộ vào nửa đêm",
            "timestamp": "2025-10-18 23:30:00",
            "src_ip": "192.168.1.200", "dst_ip": "10.0.1.250", "dst_port": 22,
            "protocol": "TCP", "bytes_sent": 45000.0, "bytes_recv": 300.0,
            "duration": 500.0, "hour_of_day": 23, "is_external_dst": 0 # Rất lưu ý: External = 0
        }
    ]

    for log in live_logs:
        # In Log thô ra màn hình
        print(f"\n{Colors.BOLD}[*] BẮT ĐƯỢC KẾT NỐI MỚI (Syslog) lúc {log['timestamp']} {Colors.RESET}")
        print(f"    {Colors.YELLOW}Source: {log['src_ip']} -> Dest: {log['dst_ip']}:{log['dst_port']}{Colors.RESET}")
        print(f"    Payload : Upload {log['bytes_sent']} KB, Download {log['bytes_recv']} KB | Port: {log['dst_port']} (Giao thức SSL/TLS chuẩn)")
        time.sleep(1)
        
        # Tiền xử lý bản ghi này y như lúc train
        df_raw = pd.DataFrame([log])
        df_feat = df_raw.copy()
        
        print(f"    {Colors.BOLD}>> [ENGINE] Phân tích đặc trưng hành vi...{Colors.RESET}")
        time.sleep(1)
        
        # Đặc trưng 1: Encode protocol
        df_feat['protocol'] = le.transform(df_feat['protocol'])
        
        # Đặc trưng 2: Feature Engineering (Upload/Download Ratio) - TRỌNG ĐIỂM
        ratio = df_feat['bytes_sent'] / df_feat['bytes_recv'].replace(0, 0.01)
        df_feat['upload_download_ratio'] = ratio.round(4)
        print(f"    {Colors.BLUE}>> [X-RAY] Bóc tách: Tỉ lệ Upload/Download = {df_feat['upload_download_ratio'].iloc[0]:.2f}{Colors.RESET}")
        time.sleep(1)

        # Trích các cột cần và scale
        X_live = df_feat[FEATURE_COLS].copy()
        X_live[NUMERIC_COLS] = scaler.transform(X_live[NUMERIC_COLS])
        
        print(f"    {Colors.BOLD}>> [SOC] Chuyển tiếp tới Tòa án AI (3 Mô hình):{Colors.RESET}")
        time.sleep(1)

        # Logistic Regression
        lr_pred = models['logistic_regression'].predict(X_live)[0]
        # Random Forest
        rf_pred = models['random_forest'].predict(X_live)[0]
        # Isolation Forest (-1 là dị thường, 1 là bình thường)
        if_pred_raw = models['isolation_forest'].predict(X_live)[0]
        if_pred = 1 if if_pred_raw == -1 else 0

        # Top 3 đặc trưng quan trọng nhất (dùng feature_importances_ của RF)
        fi = models['random_forest'].feature_importances_
        raw_vals = df_feat[FEATURE_COLS].iloc[0]
        ranked = sorted(zip(FEATURE_COLS, fi, raw_vals), key=lambda x: x[1], reverse=True)[:3]

        # In kết quả của Logistic
        if lr_pred == 1:
            print(f"       => Logistic Reg (Baseline): {Colors.RED} Phát hiện Rò rỉ!{Colors.RESET}")
        else:
            print(f"       => Logistic Reg (Baseline): {Colors.GREEN} Bình thường (Bỏ lọt nếu tinh vi){Colors.RESET}")
        time.sleep(0.5)

        # In kết quả của Random Forest
        if rf_pred == 1:
            print(f"       => Random Forest (Chính)  : {Colors.RED} Phát hiện Rò rỉ!{Colors.RESET}")
        else:
            print(f"       => Random Forest (Chính)  : {Colors.GREEN} Bình thường{Colors.RESET}")
        time.sleep(0.5)

        # In kết quả của Isolation Forest
        if if_pred == 1:
            print(f"       => Isolation Forest (Unsup): {Colors.YELLOW}⚠ Hành vi dị thường (Outlier){Colors.RESET}")
        else:
            print(f"       => Isolation Forest (Unsup): {Colors.GREEN}✓ Phù hợp với thói quen công ty{Colors.RESET}")
        time.sleep(1.2)

        # ── Phán quyết 3 tầng ──────────────────────────────────────────────
        # AUTO-BLOCK : RF=1 VÀ IF=1 → bằng chứng rõ ràng
        # IF-WARNING : chỉ IF=1 đơn độc → cần SOC Analyst xem xét thủ công
        # ALLOW      : tất cả sạch
        print("-" * 70)
        if rf_pred == 1 and if_pred == 1:
            print(f"    {Colors.RED}{Colors.BOLD}[🚨 AUTO-BLOCK] Cắt mạng Source: {log['src_ip']} — RF + IF đồng thuận!{Colors.RESET}")
            print(f"    Lý do: Bằng chứng kép rõ ràng.")
            print(f"    Phân tích: {log['desc']}")
        elif if_pred == 1 and rf_pred == 0:
            print(f"    {Colors.YELLOW}{Colors.BOLD}[⚠ IF-WARNING] Tạo ticket SOC — IF phát hiện Outlier nhưng RF chưa đủ bằng chứng.{Colors.RESET}")
            print(f"    Lý do: Hành vi lạ, cần SOC Analyst xem xét thủ công trước khi Block.")
            print(f"    Phân tích: {log['desc']}")
        elif rf_pred == 1 and if_pred == 0:
            print(f"    {Colors.RED}{Colors.BOLD}[🚨 AUTO-BLOCK] Cắt mạng Source: {log['src_ip']} — RF xác nhận pattern tội phạm!{Colors.RESET}")
            print(f"    Lý do: RF nhận diện được pattern rò rỉ đã học.")
            print(f"    Phân tích: {log['desc']}")
        else:
            print(f"    {Colors.GREEN}{Colors.BOLD}[✅ ALLOW] Kết nối hợp lệ. Cho phép tiếp tục luồng dữ liệu.{Colors.RESET}")
            print(f"    Phân tích: {log['desc']}")

        # ── XAI: Giải thích quyết định (Explainable AI) ──────────────────
        print(f"\n    {Colors.BLUE}∙ [XAI] Top-3 đặc trưng quyết định (Random Forest):{Colors.RESET}")
        for feat, importance, raw in ranked:
            bar = "█" * int(importance * 40)
            print(f"       {feat:25s} = {raw:<14.2f} w={importance:.3f} {bar}")
        print("=" * 70)
        time.sleep(3)
        

if __name__ == "__main__":
    simulate_realtime_detection()
