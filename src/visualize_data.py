import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

matplotlib.rcParams["font.size"] = 12
matplotlib.rcParams["figure.dpi"] = 120

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "network_logs.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

def plot_data_scatter():
    """Vẽ scatter plots biểu diễn dữ liệu."""
    if not os.path.exists(DATA_FILE):
        print(f"Không tìm thấy file: {DATA_FILE}")
        return

    df = pd.read_csv(DATA_FILE)
    
    # Tính thêm upload_download_ratio để dễ vẽ
    # Tránh chia cho 0
    df['bytes_recv_safe'] = df['bytes_recv'].replace(0, 0.01)
    df['ratio'] = df['bytes_sent'] / df['bytes_recv_safe']

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    label_map = {0: 'Normal (0)', 1: 'Leakage (1)'}
    df['Label_Text'] = df['label'].map(label_map)
    palette = {'Normal (0)': '#2ecc71', 'Leakage (1)': '#e74c3c'}

    # 1. Plot: Tham số Bytes Upload vs Bytes Download
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=df, 
        x='bytes_recv', y='bytes_sent', 
        hue='Label_Text', palette=palette, 
        alpha=0.6, ax=ax1, s=40
    )
    # Log scale do dữ liệu chênh lệch rất lớn
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("Bytes Download (log scale)")
    ax1.set_ylabel("Bytes Upload (log scale)")
    ax1.set_title("Phân tán dữ liệu: Upload vs Download\n(Log Scale)")
    ax1.grid(True, alpha=0.3)
    ax1.legend(title="Label")
    
    fig1_path = os.path.join(OUTPUT_DIR, "scatter_upload_download.png")
    fig1.savefig(fig1_path, bbox_inches="tight")
    print(f"[✓] Đã lưu scatter plot 1 tại: {fig1_path}")
    plt.close(fig1)

    # 2. Plot: Thời gian trong ngày (Hour) vs Tỷ lệ Ratio
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    # Cộng thêm xíu noise (jitter) vào giờ để các chấm không đè sát lên nhau
    df['hour_jitter'] = df['hour_of_day'] + np.random.normal(0, 0.15, size=len(df))
    
    sns.scatterplot(
        data=df, 
        x='hour_jitter', y='ratio', 
        hue='Label_Text', palette=palette, 
        alpha=0.6, ax=ax2, s=40
    )
    ax2.set_yscale("log")
    ax2.set_xticks(range(0, 24, 2))
    ax2.set_xlabel("Hour of Day")
    ax2.set_ylabel("Upload/Download Ratio (log scale)")
    ax2.set_title("Hành vi rò rỉ: Thời gian hoạt động và Tỷ lệ Upload")
    
    # Vẽ các mốc giờ hành chính (8h sáng - 6h tối) để dễ bề nhận diện hacker làm việc ban đêm
    ax2.axvspan(8, 18, color='gray', alpha=0.1, label='Giờ Hành chính')
    
    # Chỉnh sửa legend
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles, labels, title="Label", loc="upper left", bbox_to_anchor=(1, 1))
    ax2.grid(True, alpha=0.3)

    fig2_path = os.path.join(OUTPUT_DIR, "scatter_hour_ratio.png")
    fig2.savefig(fig2_path, bbox_inches="tight")
    print(f"[✓] Đã lưu scatter plot 2 tại: {fig2_path}")
    plt.close(fig2)

if __name__ == "__main__":
    import numpy as np # Import ở đây do phía trên xài numpy
    print("Đang vẽ biểu đồ trực quan hóa dữ liệu...")
    plot_data_scatter()
    print("HOÀN TẤT!")
