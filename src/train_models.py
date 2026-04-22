"""
Chương 5 - Huấn luyện mô hình (Model Training)
================================================
3 mô hình:
  1. Logistic Regression (Baseline) — supervised, class_weight='balanced'
  2. Random Forest (Chính)           — supervised, class_weight='balanced'
  3. Isolation Forest (Không giám sát) — unsupervised, chỉ train trên normal
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")


def train_logistic_regression(X_train, y_train):
    """Mô hình 1: Logistic Regression (Baseline)."""
    print("\n┌─────────────────────────────────────────────────┐")
    print("│  MÔ HÌNH 1: LOGISTIC REGRESSION (BASELINE)      │")
    print("└─────────────────────────────────────────────────┘")
    print("  Cấu hình: solver='lbfgs', max_iter=1000, class_weight='balanced'")

    model = LogisticRegression(
        solver="lbfgs",
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
        verbose=1
    )
    model.fit(X_train, y_train)

    print("  [✓] Huấn luyện hoàn tất")

    # Hiển thị hệ số
    if hasattr(X_train, "columns"):
        coef_df = pd.DataFrame({
            "Đặc trưng": X_train.columns,
            "Hệ số": model.coef_[0],
        }).sort_values("Hệ số", ascending=False, key=abs)
        print("\n  Hệ số mô hình (|lớn| = quan trọng):")
        for _, row in coef_df.iterrows():
            bar = "▓" * int(abs(row["Hệ số"]) * 5)
            sign = "+" if row["Hệ số"] > 0 else "-"
            print(f"    {sign} {row['Đặc trưng']:25s} {row['Hệ số']:+.4f}  {bar}")

    return model


def train_random_forest(X_train, y_train):
    """Mô hình 2: Random Forest (Mô hình chính)."""
    print("\n┌─────────────────────────────────────────────────┐")
    print("│  MÔ HÌNH 2: RANDOM FOREST (MÔ HÌNH CHÍNH)       │")
    print("└─────────────────────────────────────────────────┘")
    print("  Cấu hình: n_estimators=100, max_depth=10, class_weight='balanced'")

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    model.fit(X_train, y_train)

    print("  [✓] Huấn luyện hoàn tất")

    # Feature Importance
    if hasattr(X_train, "columns"):
        fi_df = pd.DataFrame({
            "Đặc trưng": X_train.columns,
            "Importance": model.feature_importances_,
        }).sort_values("Importance", ascending=False)
        print("\n  Feature Importance:")
        for rank, (_, row) in enumerate(fi_df.iterrows(), 1):
            bar = "▓" * int(row["Importance"] * 50)
            print(f"    #{rank} {row['Đặc trưng']:25s} {row['Importance']:.4f}  {bar}")

    return model


def train_isolation_forest(X_train, y_train):
    """Mô hình 3: Isolation Forest (Không giám sát)."""
    print("\n┌─────────────────────────────────────────────────┐")
    print("│  MÔ HÌNH 3: ISOLATION FOREST (KHÔNG GIÁM SÁT)   │")
    print("└─────────────────────────────────────────────────┘")
    print("  Cấu hình: n_estimators=100, contamination=0.15")
    print("  Chỉ huấn luyện trên dữ liệu Normal (label=0)")

    # Chỉ lấy dữ liệu normal để train
    X_train_normal = X_train[y_train == 0]
    print(f"  Tập train (chỉ Normal): {len(X_train_normal)} bản ghi")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    model.fit(X_train_normal)

    print("  [✓] Huấn luyện hoàn tất")

    return model


def save_models(models: dict, output_dir: str = OUTPUT_DIR):
    """Lưu models ra file."""
    os.makedirs(output_dir, exist_ok=True)
    for name, model in models.items():
        path = os.path.join(output_dir, f"{name}.pkl")
        with open(path, "wb") as f:
            pickle.dump(model, f)
        print(f"  [✓] Lưu {name} → {path}")


def train_all_models(X_train, y_train):
    """Huấn luyện tất cả 3 mô hình."""
    print("=" * 60)
    print("  HUẤN LUYỆN MÔ HÌNH")
    print("=" * 60)
    print(f"  Tập train: {X_train.shape[0]} bản ghi, {X_train.shape[1]} đặc trưng")

    models = {}
    models["logistic_regression"] = train_logistic_regression(X_train, y_train)
    models["random_forest"] = train_random_forest(X_train, y_train)
    models["isolation_forest"] = train_isolation_forest(X_train, y_train)

    # Lưu models
    print("\n── Lưu mô hình ──")
    save_models(models)

    print("\n" + "=" * 60)
    print("  [✓] HUẤN LUYỆN HOÀN TẤT — 3 mô hình")
    print("=" * 60)

    return models


if __name__ == "__main__":
    # Chạy cần có dữ liệu đã tiền xử lý
    from preprocess import run_preprocessing_pipeline

    X_train, X_test, y_train, y_test, scaler, le = run_preprocessing_pipeline()
    models = train_all_models(X_train, y_train)
