#!/usr/bin/env python3
"""
Chương 5 - Chạy toàn bộ pipeline demo
======================================
Từ sinh dữ liệu → tiền xử lý → huấn luyện → đánh giá
"""

import sys
import os

# Thêm src/ vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from generate_data import generate_dataset
from preprocess import run_preprocessing_pipeline
from train_models import train_all_models
from evaluate import evaluate_all


def main():
    print("╔" + "═" * 58 + "╗")
    print("║  DEMO CHƯƠNG 5: PHÁT HIỆN RÒ RỈ DỮ LIỆU BẰNG HỌC MÁY  ║")
    print("║  Bài toán: Phân loại nhị phân — Insider Threat            ║")
    print("╚" + "═" * 58 + "╝")

    # 1. Sinh dữ liệu
    print("\n" + "▶" * 20 + " BƯỚC 1: SINH DỮ LIỆU " + "◀" * 20)
    generate_dataset()

    # 2. Tiền xử lý
    print("\n" + "▶" * 20 + " BƯỚC 2: TIỀN XỬ LÝ " + "◀" * 20)
    X_train, X_test, y_train, y_test, scaler, le = run_preprocessing_pipeline()

    # 3. Huấn luyện
    print("\n" + "▶" * 20 + " BƯỚC 3: HUẤN LUYỆN " + "◀" * 20)
    models = train_all_models(X_train, y_train)

    # 4. Đánh giá
    print("\n" + "▶" * 20 + " BƯỚC 4: ĐÁNH GIÁ " + "◀" * 20)
    results = evaluate_all(models, X_test, y_test, feature_names=list(X_test.columns))

    print("\n" + "═" * 60)
    print("  ✅ DEMO HOÀN TẤT!")
    print("  📊 Biểu đồ: outputs/")
    print("  📁 Dữ liệu: data/network_logs.csv")
    print("═" * 60)


if __name__ == "__main__":
    main()
