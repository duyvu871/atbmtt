# BÁO CÁO MÔ HÌNH PHÂN TÍCH RÒ RỈ MẠNG (NETWORK LEAKAGE DETECTION)

**Môn học:** An toàn và Bảo mật Hệ thống Thông tin  
**Trọng tâm Demo:** Phân tích lưu lượng mạng để xây dựng mô hình học máy phát hiện Rò rỉ Dữ liệu (Data Leakage) theo kịch bản Insider Threat. Khai thác dữ liệu tầng luồng (Flow-based network logs).

## 1. Dữ Liệu Demo (Data Preparation)
- **Tổng số bản ghi sinh giả lập:** 5.000 log mạng (flow-level).
- **Phân phối nhãn:** 85% Hành vi bình thường (Normal) / 15% Hành vi lộ lọt dữ liệu (Leakage).
- **Bộ đặc trưng sử dụng (8 features):** `bytes_sent`, `bytes_recv`, `duration`, `hour_of_day`, `is_external_dst`, `dst_port`, `protocol`, `upload_download_ratio`.

---

## 2. Bảng Xếp hạng và So sánh Mô hình (Model Metrics)

Bảng tổng hợp kết quả đánh giá trên tập Kiểm Thử (Test Set) gồm 1.000 bản ghi:

| Mô hình | Accuracy | Precision | Recall | F1-Score | FPR (Tỷ lệ Báo động Giả) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 99.5% | 98.0% | 98.7% | 98.3% | 0.4% |
| **Random Forest** | **99.9%** | **100.0%** | 99.3% | **99.7%** | **0.0%** |
| **Isolation Forest** | 86.1% | 51.9% | **100.0%** | 68.3% | 16.4% |

*(Chú ý: Đối với mô hình Isolation Forest hoàn toàn không gán nhãn, độ phủ Recall đạt 100% chứng tỏ có khả năng nhận biết Zero-day Leak hiệu quả dù tỷ lệ báo động giả còn cao).*

### Biểu đồ So sánh các Chỉ số (Metrics Output)
![Biểu đồ So sánh Metrics](metrics_comparison.png)

---

## 3. Ma trận Nhầm lẫn (Confusion Matrices)

Confusion Matrix cho thấy sự khác biệt về số lượng mẫu đoán trúng/trật giữa các mô hình. Bài toán Rò rỉ dữ liệu cực kỳ ưu tiên làm giảm **False Negative - FN** (đoán là Normal nhưng thực chất đang rò rỉ dữ liệu bỏ sót tội phạm). 

- **Random Forest** gần như đoán trúng tuyệt đối, chỉ có 1 trường hợp False Negative (bỏ sót).
- **Isolation Forest** tóm gọn tất cả các trường hợp Leakage (FN = 0), đổi lại có 139 trường hợp cảnh báo nhầm (False Positive).

![Confusion Matrices của 3 thuật toán](confusion_matrices.png)

---

## 4. Đường cong Khả năng Cảnh báo (ROC Curves)

Thế hiện tương quan giữa mức phát triển chẩn đoán đúng True Positive Rate và báo động giả False Positive Rate đa mức ngưỡng của Classifier. **Random Forest** đạt AUC kịch khung 1.0.

![ROC Curves](roc_curves.png)

---

## 5. Tầm Quan trọng của Đặc trưng (Feature Importance)

Mô hình Random Forest khi phân tách thành các cây quyết định đã tự nhận thức ra các biến quan trọng nhất cấu thành hành vi gửi tin trái phép. Hoàn toàn phù hợp với lý thuyết phân tích bảo mật:
1. **`duration` (0.32)**: Các cuộc truyền dữ liệu lớn có xu hướng chiếm dụng kết nối thời gian dài hơn hẳn bình thường.
2. **`bytes_sent` (0.31)**: Tổng lượng dữ liệu (bytes) bơm ra ngoài mạng trực tiếp phản ánh rò rỉ.
3. **`upload_download_ratio` (0.18)**: Mức độ bất đối xứng (upload nhiều hơn download) là biểu hiện rõ rệt của Insider Threat gửi thông tin từ trong mạng đi.

![Top Đặc Trưng Quan Trọng](feature_importance.png)

---

## 6. Kết luận
Kịch bản mô phỏng Insider Threat đã thành công mỹ mãn. Học máy cho thấy độ chính xác xuất sắc trên hệ thống lưu lượng mạng. Random Forest có thể được deploy dưới dạng Engine phân tích sâu trên các hệ thống DLP/SIEM, trong khi Isolation Forest sẽ đóng vai trò như Guardrail tìm kiếm những biến hóa đứt gãy Zero-day.
