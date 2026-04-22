# Demo Chương 5: Mô hình Phân tích Rò rỉ Mạng (Network Leakage Analysis)

Dự án demo môn học **An toàn và Bảo mật Hệ thống Thông tin**. Trọng tâm chính của bản Demo này là xây dựng và đánh giá hệ thống học máy phân tích dữ liệu mạng để phát hiện hành vi rò rỉ dữ liệu (Chương 5 của Bài tập lớn).

---

## 1. Hướng dẫn xây dựng và chạy Demo

Dự án quản lý và chạy môi trường bằng `uv` để đảm bảo tính nhất quán của các thư viện.

### Yêu cầu hệ thống
- Đã cài đặt [Python](https://www.python.org/downloads/) (>= 3.10)
- Đã cài đặt [uv](https://github.com/astral-sh/uv) (có thể cài qua lệnh `curl -LsSf https://astral.sh/uv/install.sh | sh` trên Linux/macOS hoặc `pip install uv`)

### Các bước triển khai

**Bước 1: Khởi tạo và đồng bộ môi trường (Cài đặt dependencies)**
```bash
uv lock
```

**Bước 2: Tạo Jupyter Notebook (Tự động hóa)**
Lệnh này sẽ tự động sinh file `demo_notebook.ipynb` chứa toàn bộ code và giải thích Markdown:
```bash
uv run --with nbformat create_notebook.py
```

**Bước 3: Chạy nhanh toàn bộ Pipeline (Tùy chọn)**
Nếu bạn chỉ muốn chạy file script Python để sinh model và ảnh biểu đồ mà không cần mở Notebook:
```bash
uv run run_demo.py
```

**Bước 4: Trình diễn (Show Demo)**
Mở và chạy file Notebook đã tạo thông qua Jupyter:
```bash
uv run jupyter notebook demo_notebook.ipynb
```
Hoặc bạn có thể mở trực tiếp file `demo_notebook.ipynb` trong VSCode/Cursor.

---

## 2. Nội dung sẽ Show vào Báo cáo Demo

Khi chạy Demo trước lớp/giảng viên, đây là các nội dung chính cần được trình diễn theo đúng format của BTL (Chương 5):

### A. Kịch bản giả lập (Scenario)
- **Bài toán:** Phân loại nhị phân (Binary Classification) phát hiện hành vi điểm dị thường.
- **Tình huống:** *Insider Threat* — Mô phỏng một nhân viên nội bộ cố tình truyền lượng lớn dữ liệu nhạy cảm ra bên ngoài tổ chức ngoài giờ làm việc thông thường.

### B. Chuẩn bị dữ liệu (Data Preparation)
- **Tập dữ liệu:** 5,000 bản ghi log mạng (tự sinh).
- **Phân phối:** 4,250 bản ghi bình thường (Normal - 85%) và 750 bản ghi bất thường (Leakage - 15%).
- **Trường dữ liệu quan trọng:** `bytes_sent`, `is_external_dst`, `hour_of_day`, `dst_port`.

### C. Quy trình Tiền xử lý (Preprocessing Pipeline)
- **Làm sạch:** Loại bỏ IP, Timestamp (tránh data leakage trong model).
- **Đặc trưng dẫn xuất:** Tạo biến `upload_download_ratio` mấu chốt để nhận diện hành vi gửi file đi.
- **Tiêu chuẩn hóa:** Label Encoding cho giao thức, MinMaxScaler đưa các dữ liệu số về phân phối [0,1].

### D. Các Mô hình Đánh giá
Demo sẽ so sánh đối chiếu giữa 3 thuật toán:
1. **Logistic Regression (Baseline):** Cho tốc độ siêu tốc và khả năng diễn giải tuyệt đối.
2. **Random Forest (Mô hình chính):** Thuật toán Supervised Learning, vượt trội nhất khi xử lý các nhãn bất cân bằng nhờ `class_weight='balanced'`.
3. **Isolation Forest:** Thuật toán Unsupervised Learning để minh họa việc phát hiện zero-day leak khi không có dữ liệu nhãn.

### E. Kết quả và Trực quan hóa (Evaluation & Visualization)
Thay vì những con số khô khan, Demo sẽ show các biểu đồ đẹp mắt đã tự động lưu trong `outputs/`:
- **Bảng so sánh đa chiều:** So sánh Accuracy, Precision, Recall, F1-Score (F1 của Random Forest đạt cực kỳ cao).
- **Confusion Matrices:** Hiển thị trực quan tỷ lệ False Positive và False Negative (giải thích tại sao Recall là quan trọng nhất trong bảo mật).
- **ROC Curves:** Biểu đồ AOC đong đếm tính hiệu quả phân loại.
- **Feature Importance:** Bằng chứng thuyết phục nhất - Chứng minh cho người nghe thấy mô hình ML hoạt động đúng logic khi tự học được rằng `duration`, `bytes_sent` và `upload_download_ratio` là những chỉ báo lớn nhất của rò rỉ dữ liệu.
