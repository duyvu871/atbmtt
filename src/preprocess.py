"""
Chương 5 - Tiền xử lý dữ liệu (Preprocessing Pipeline)
=========================================================
Pipeline 4 bước:
  1. Làm sạch dữ liệu (xử lý missing, trùng lặp, loại bỏ cột không cần)
  2. Mã hóa biến phân loại (Label Encoding cho protocol)
  3. Feature Engineering (upload_download_ratio)
  4. Chuẩn hóa dữ liệu số (MinMaxScaler — fit trên train, transform test)

Chia dữ liệu: 80/20 Stratified Split
Xử lý mất cân bằng: class_weight='balanced' (trong mô hình, không ở đây)
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
INPUT_FILE = os.path.join(DATA_DIR, "network_logs.csv")

# Các cột cần chuẩn hóa
NUMERIC_COLS = ["bytes_sent", "bytes_recv", "duration"]
# Các cột sẽ được sử dụng làm đặc trưng
FEATURE_COLS = [
    "bytes_sent", "bytes_recv", "duration",
    "hour_of_day", "is_external_dst", "dst_port",
    "protocol", "upload_download_ratio",
]
TARGET_COL = "label"


def load_data() -> pd.DataFrame:
    """Đọc dữ liệu từ CSV."""
    df = pd.read_csv(INPUT_FILE)
    print(f"[*] Đọc dữ liệu: {len(df)} bản ghi, {df.shape[1]} cột")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Bước 1: Làm sạch dữ liệu."""
    print("\n── Bước 1: Làm sạch dữ liệu ──")

    # Kiểm tra missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"  [!] Có {missing.sum()} giá trị thiếu — điền median cho cột số")
        for col in NUMERIC_COLS:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
    else:
        print("  [✓] Không có giá trị thiếu")

    # Loại bỏ bản ghi trùng lặp
    n_before = len(df)
    df = df.drop_duplicates()
    n_dup = n_before - len(df)
    print(f"  [✓] Loại bỏ {n_dup} bản ghi trùng lặp → còn {len(df)} bản ghi")

    # Loại bỏ các cột không dùng trực tiếp
    cols_to_drop = ["timestamp", "src_ip", "dst_ip"]
    df = df.drop(columns=cols_to_drop, errors="ignore")
    print(f"  [✓] Loại bỏ các cột: {cols_to_drop}")

    return df


def encode_categorical(df: pd.DataFrame) -> tuple[pd.DataFrame, LabelEncoder]:
    """Bước 2: Mã hóa biến phân loại — Label Encoding cho protocol."""
    print("\n── Bước 2: Mã hóa biến phân loại ──")

    le = LabelEncoder()
    df["protocol"] = le.fit_transform(df["protocol"])

    mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    print(f"  [✓] Label Encoding protocol: {mapping}")

    return df, le


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Bước 3: Tạo đặc trưng dẫn xuất."""
    print("\n── Bước 3: Feature Engineering ──")

    # upload_download_ratio = bytes_sent / bytes_recv
    # Tránh chia cho 0
    df["upload_download_ratio"] = df["bytes_sent"] / df["bytes_recv"].replace(0, 0.01)
    df["upload_download_ratio"] = df["upload_download_ratio"].round(4)

    print(f"  [✓] Tạo upload_download_ratio = bytes_sent / bytes_recv")
    print(f"      Min: {df['upload_download_ratio'].min():.4f}, "
          f"Max: {df['upload_download_ratio'].max():.4f}, "
          f"Mean: {df['upload_download_ratio'].mean():.4f}")

    return df


def split_data(df: pd.DataFrame) -> tuple:
    """Chia dữ liệu 80/20 Stratified Split."""
    print("\n── Chia dữ liệu (80/20 Stratified) ──")

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"  [✓] Train: {len(X_train)} bản ghi "
          f"(Normal: {(y_train == 0).sum()}, Leakage: {(y_train == 1).sum()})")
    print(f"  [✓] Test : {len(X_test)} bản ghi "
          f"(Normal: {(y_test == 0).sum()}, Leakage: {(y_test == 1).sum()})")

    return X_train, X_test, y_train, y_test


def scale_features(
    X_train: pd.DataFrame, X_test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, MinMaxScaler]:
    """Bước 4: Chuẩn hóa dữ liệu số bằng MinMaxScaler."""
    print("\n── Bước 4: Chuẩn hóa dữ liệu số (MinMaxScaler) ──")

    scaler = MinMaxScaler()

    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    # Fit trên train, transform cả train và test
    X_train_scaled[NUMERIC_COLS] = scaler.fit_transform(X_train[NUMERIC_COLS])
    X_test_scaled[NUMERIC_COLS] = scaler.transform(X_test[NUMERIC_COLS])

    print(f"  [✓] Chuẩn hóa cột: {NUMERIC_COLS}")
    print(f"      (fit trên train → transform trên cả train & test để tránh data leakage)")

    return X_train_scaled, X_test_scaled, scaler


def run_preprocessing_pipeline():
    """Chạy toàn bộ pipeline tiền xử lý."""
    print("=" * 60)
    print("  QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU")
    print("=" * 60)

    # 1. Đọc dữ liệu
    df = load_data()

    # 2. Làm sạch
    df = clean_data(df)

    # 3. Label Encoding
    df, label_encoder = encode_categorical(df)

    # 4. Feature Engineering
    df = feature_engineering(df)

    # 5. Chia dữ liệu
    X_train, X_test, y_train, y_test = split_data(df)

    # 6. Chuẩn hóa
    X_train, X_test, scaler = scale_features(X_train, X_test)

    print("\n" + "=" * 60)
    print("  [✓] TIỀN XỬ LÝ HOÀN TẤT")
    print(f"  Đặc trưng sử dụng ({len(FEATURE_COLS)}): {FEATURE_COLS}")
    print("=" * 60)

    return X_train, X_test, y_train, y_test, scaler, label_encoder


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler, le = run_preprocessing_pipeline()
    print(f"\nX_train shape: {X_train.shape}")
    print(f"X_test shape : {X_test.shape}")
    print(f"\nX_train sample:")
    print(X_train.head().to_string())
