import nbformat as nbf

nb = nbf.v4.new_notebook()

nb.cells = [
    nbf.v4.new_markdown_cell("# Demo Chương 5: Phân tích Rò rỉ Mạng qua Mô hình Học máy\n\n**Môn học:** An toàn và Bảo mật Hệ thống Thông tin\n**Trọng tâm Demo:** Xây dựng mô hình phân tích lưu lượng mạng để phát hiện Rò rỉ Dữ liệu (Data Leakage)\n\nTrong bài thực hành này, chúng ta tập trung phân tích các luồng kết nối (network flow) nhằm phát hiện kịch bản nội gián (insider threat) - một nhân viên cố tình truyền dữ liệu ra ngoài mạng vượt thẩm quyền ngoài giờ làm việc."),
    
    nbf.v4.new_markdown_cell("## 1. Sinh dữ liệu giả lập (Data Generation)\n\nTạo 5,000 bản ghi dữ liệu mạng dạng flow với tỉ lệ 85% bình thường (Normal) và 15% rò rỉ dữ liệu (Leakage)."),
    nbf.v4.new_code_cell("import sys; sys.path.append('src')\nfrom generate_data import generate_dataset\n\ndf = generate_dataset()\ndf.head()"),
    
    nbf.v4.new_markdown_cell("## 2. Tiền xử lý dữ liệu (Preprocessing)\n\nQuy trình tiền xử lý bao gồm:\n- Làm sạch dữ liệu và loại bỏ các cột không sử dụng (IP, Timestamp).\n- Mã hóa các biến phân loại (`protocol`).\n- Thay đổi đặc trưng dẫn xuất: `upload_download_ratio = bytes_sent / bytes_recv`.\n- Chuẩn hóa các biến liên tục MinMaxScaler (khoảng [0,1]).\n- Chia tập huấn luyện/kiểm tra 80:20."),
    nbf.v4.new_code_cell("from preprocess import run_preprocessing_pipeline\n\nX_train, X_test, y_train, y_test, scaler, le = run_preprocessing_pipeline()\nprint('Training set size:', X_train.shape)\nprint('Testing set size:', X_test.shape)\nX_train.head()"),
    
    nbf.v4.new_markdown_cell("## 3. Huấn luyện Mô hình\n\n- **Logistic Regression (Baseline):** Mô hình phân loại tuyến tính cơ bản.\n- **Random Forest (Chính):** Mô hình Decision Tree Ensemble.\n- **Isolation Forest:** Mô hình phát hiện bất thường Unsupervised (Không giám sát - chỉ sử dụng nhãn Normal khi train)."),
    nbf.v4.new_code_cell("from train_models import train_all_models\n\nmodels = train_all_models(X_train, y_train)"),

    nbf.v4.new_markdown_cell("## 4. Đánh giá Kết quả (Evaluation)\n\nSử dụng các chỉ số: **Accuracy**, **Precision**, **Recall**, **F1-Score**, **FPR** và biểu đồ **Confusion Matrix**."),
    nbf.v4.new_code_cell("from evaluate import evaluate_all\nimport matplotlib.pyplot as plt\n%matplotlib inline\n\nresults = evaluate_all(models, X_test, y_test, feature_names=list(X_test.columns))"),
    
    nbf.v4.new_markdown_cell("## 5. Kết luận \& Trực quan hóa\n\nCác biểu đồ kết quả trực quan được xuất ra thư mục `outputs/`:"),
    nbf.v4.new_markdown_cell("### So sánh Metrics\n![](outputs/metrics_comparison.png)"),
    nbf.v4.new_markdown_cell("### Confusion Matrices\n![](outputs/confusion_matrices.png)"),
    nbf.v4.new_markdown_cell("### ROC Curves\n![](outputs/roc_curves.png)"),
    nbf.v4.new_markdown_cell("### Feature Importance (Random Forest)\n![](outputs/feature_importance.png)"),

    nbf.v4.new_markdown_cell("- **Random Forest** cho kết quả tốt nhất khi có dữ liệu gán nhãn, nhận thức rõ nhất các đặc trưng `bytes_sent` và `upload_download_ratio`.\n- Mô hình phát hiện rò rỉ dữ liệu nhận biệt rõ được hành vi truyền dữ liệu trái phép thông qua các đặc trưng ngữ cảnh (cổng giao tiếp, giờ giấc, tỉ lệ truy xuất ngoài).")
]

with open('demo_notebook.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print('Notebook demo_notebook.ipynb đã được tạo thành công!')
