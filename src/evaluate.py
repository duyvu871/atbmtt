"""
Chương 5 - Đánh giá và Trực quan hóa (Evaluation & Visualization)
==================================================================
- Confusion Matrix (heatmap) cho từng mô hình
- Bảng so sánh metrics: Accuracy, Precision, Recall, F1, FPR
- Feature Importance bar chart (Random Forest)
- ROC Curve
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
)

matplotlib.rcParams["font.size"] = 12
matplotlib.rcParams["figure.dpi"] = 120

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")


def predict_isolation_forest(model, X):
    """Chuyển kết quả Isolation Forest (1/-1) sang nhãn (0/1)."""
    raw = model.predict(X)
    # Isolation Forest: 1 = normal, -1 = anomaly
    return np.where(raw == -1, 1, 0)


def compute_metrics(y_true, y_pred, model_name: str) -> dict:
    """Tính các chỉ số đánh giá."""
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    metrics = {
        "Mô hình": model_name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1-Score": f1_score(y_true, y_pred, zero_division=0),
        "FPR": fp / (fp + tn) if (fp + tn) > 0 else 0,
        "TP": tp, "TN": tn, "FP": fp, "FN": fn,
    }

    return metrics


def plot_confusion_matrix(y_true, y_pred, model_name: str, ax=None):
    """Vẽ Confusion Matrix heatmap."""
    cm = confusion_matrix(y_true, y_pred)
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 4))

    labels = np.array([
        [f"TN = {cm[0,0]}\n({cm[0,0]/cm.sum()*100:.1f}%)",
         f"FP = {cm[0,1]}\n({cm[0,1]/cm.sum()*100:.1f}%)"],
        [f"FN = {cm[1,0]}\n({cm[1,0]/cm.sum()*100:.1f}%)",
         f"TP = {cm[1,1]}\n({cm[1,1]/cm.sum()*100:.1f}%)"],
    ])

    sns.heatmap(
        cm, annot=labels, fmt="", cmap="Blues",
        xticklabels=["Normal", "Leakage"],
        yticklabels=["Normal", "Leakage"],
        ax=ax, cbar=True,
        annot_kws={"fontsize": 11},
    )
    ax.set_xlabel("Dự đoán")
    ax.set_ylabel("Thực tế")
    ax.set_title(f"Confusion Matrix — {model_name}")


def plot_all_confusion_matrices(results: list[dict], y_true, predictions: dict):
    """Vẽ 3 confusion matrix cạnh nhau."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("So sánh Confusion Matrix các mô hình", fontsize=16, fontweight="bold")

    for ax, result in zip(axes, results):
        name = result["Mô hình"]
        plot_confusion_matrix(y_true, predictions[name], name, ax=ax)

    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "confusion_matrices.png")
    fig.savefig(path, bbox_inches="tight")
    print(f"  [✓] Lưu confusion matrices → {path}")
    plt.close()


def plot_metrics_comparison(results: list[dict]):
    """Vẽ bảng so sánh metrics dạng bar chart."""
    df = pd.DataFrame(results)
    metrics_cols = ["Accuracy", "Precision", "Recall", "F1-Score"]

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(metrics_cols))
    width = 0.25
    colors = ["#4A90D9", "#2ECC71", "#E74C3C"]

    for i, row in df.iterrows():
        values = [row[m] for m in metrics_cols]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, values, width, label=row["Mô hình"], color=colors[i], alpha=0.85)
        # Ghi giá trị trên bar
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f"{val:.1%}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_ylabel("Giá trị (%)")
    ax.set_title("So sánh Metrics các mô hình\n\n", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_cols)
    ax.set_ylim(0, 1.15)
    
    # Đưa legend ra ngoài hoặc lên trên để không che data
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=False)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "metrics_comparison.png")
    fig.savefig(path, bbox_inches="tight")
    print(f"  [✓] Lưu metrics comparison → {path}")
    plt.close()


def plot_feature_importance(model, feature_names: list[str]):
    """Vẽ Feature Importance từ Random Forest."""
    fi = pd.DataFrame({
        "Đặc trưng": feature_names,
        "Importance": model.feature_importances_,
    }).sort_values("Importance", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(fi)))[::-1]

    bars = ax.barh(fi["Đặc trưng"], fi["Importance"], color=colors, edgecolor="gray", alpha=0.9)

    for bar, val in zip(bars, fi["Importance"]):
        ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", fontsize=10, fontweight="bold")

    ax.set_xlabel("Importance Score")
    ax.set_title("Feature Importance — Random Forest", fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "feature_importance.png")
    fig.savefig(path, bbox_inches="tight")
    print(f"  [✓] Lưu feature importance → {path}")
    plt.close()


def plot_roc_curves(y_true, models: dict, X_test):
    """Vẽ ROC Curve cho các mô hình supervised."""
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = {"Logistic Regression": "#4A90D9", "Random Forest": "#2ECC71"}

    for name, model in models.items():
        if name == "Isolation Forest":
            continue  # Không có predict_proba
        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_true, y_score)
            roc_auc = auc(fpr, tpr)
            ax.plot(fpr, tpr, color=colors.get(name, "gray"), lw=2,
                    label=f"{name} (AUC = {roc_auc:.3f})")

    ax.plot([0, 1], [0, 1], "k--", alpha=0.4, label="Random (AUC = 0.500)")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "roc_curves.png")
    fig.savefig(path, bbox_inches="tight")
    print(f"  [✓] Lưu ROC curves → {path}")
    plt.close()


def evaluate_all(models: dict, X_test, y_test, feature_names: list[str] = None):
    """Đánh giá tất cả mô hình."""
    print("=" * 60)
    print("  ĐÁNH GIÁ MÔ HÌNH TRÊN TẬP TEST")
    print("=" * 60)
    print(f"  Tập test: {len(y_test)} bản ghi "
          f"(Normal: {(y_test == 0).sum()}, Leakage: {(y_test == 1).sum()})")

    results = []
    predictions = {}

    model_names = {
        "logistic_regression": "Logistic Regression",
        "random_forest": "Random Forest",
        "isolation_forest": "Isolation Forest",
    }

    for key, model in models.items():
        name = model_names.get(key, key)
        if key == "isolation_forest":
            y_pred = predict_isolation_forest(model, X_test)
        else:
            y_pred = model.predict(X_test)

        result = compute_metrics(y_test, y_pred, name)
        results.append(result)
        predictions[name] = y_pred

        print(f"\n  ── {name} ──")
        print(f"    Accuracy  : {result['Accuracy']:.1%}")
        print(f"    Precision : {result['Precision']:.1%}")
        print(f"    Recall    : {result['Recall']:.1%}")
        print(f"    F1-Score  : {result['F1-Score']:.1%}")
        print(f"    FPR       : {result['FPR']:.1%}")
        print(f"    (TP={result['TP']}, TN={result['TN']}, FP={result['FP']}, FN={result['FN']})")

    # ── Bảng tổng hợp ──
    print("\n" + "=" * 60)
    print("  BẢNG TỔNG HỢP KẾT QUẢ")
    print("=" * 60)
    df_results = pd.DataFrame(results)[["Mô hình", "Accuracy", "Precision", "Recall", "F1-Score", "FPR"]]
    for col in ["Accuracy", "Precision", "Recall", "F1-Score", "FPR"]:
        df_results[col] = df_results[col].apply(lambda x: f"{x:.1%}")
    print(df_results.to_string(index=False))

    # ── Visualizations ──
    print("\n── Tạo biểu đồ ──")
    plot_all_confusion_matrices(results, y_test, predictions)
    plot_metrics_comparison(results)
    plot_roc_curves(y_test, {
        "Logistic Regression": models["logistic_regression"],
        "Random Forest": models["random_forest"],
    }, X_test)

    if "random_forest" in models and feature_names:
        plot_feature_importance(models["random_forest"], feature_names)

    print("\n" + "=" * 60)
    print("  [✓] ĐÁNH GIÁ HOÀN TẤT — Kết quả tại outputs/")
    print("=" * 60)

    return results


if __name__ == "__main__":
    from preprocess import run_preprocessing_pipeline
    from train_models import train_all_models

    X_train, X_test, y_train, y_test, scaler, le = run_preprocessing_pipeline()
    models = train_all_models(X_train, y_train)
    results = evaluate_all(models, X_test, y_test, feature_names=list(X_test.columns))
