# KỊCH BẢN DEMO: PHÁT HIỆN RÒ RỈ DỮ LIỆU QUA PHÂN TÍCH HÀNH VI MẠNG
*(Dành cho phiên demo kỹ thuật, tiếp nối sau phần trình bày kiến trúc)*

---

## BƯỚC 1: LỜI MỞ ĐẦU & CHUYỂN GIAO (1 Phút)
*(Mở sẵn file `demo_notebook.ipynb` trên màn hình, hoặc chuẩn bị chạy script `run_demo.py`)*

> 🎤 **Thoại:** 
> *"Cảm ơn [Tên người thuyết trình trước] đã tổng kết phần kiến trúc hệ thống. Tiếp theo, mình sẽ đi vào phần demo trực tiếp để chứng minh cách hệ thống áp dụng Học máy (Machine Learning) vào bài toán phân tích hành vi mạng, cụ thể là ứng dụng trong việc phòng chống rò rỉ dữ liệu (Data Exfiltration/Data Leakage)."*

---

## BƯỚC 2: KHAI THÁC & XEM XÉT DỮ LIỆU ĐẦU VÀO (1.5 Phút)
*(Hiển thị dữ liệu thô `network_logs.csv` hoặc kết quả của lệnh `df.head()` trong notebook)*

> 🎤 **Thoại:** 
> *"Như các bạn thấy trên màn hình, đây là tập dữ liệu mô phỏng log mạng thô. Các đặc trưng (features) ban đầu bao gồm `bytes_sent`, `bytes_recv`, `duration`, `protocol`, v.v.*
> 
> *Trong mạng doanh nghiệp, kẻ tấn công thường vượt qua các hệ thống DLP (Data Loss Prevention) kiểu truyền thống bằng cách mã hóa dữ liệu hoặc lợi dụng các giao thức hợp lệ (ví dụ như upload file lên Cloud qua HTTPS). Các thiết bị IDS/IPS dựa trên chữ ký (signature-based) gần như vô hiệu trong trường hợp này. Do đó, logic cốt lõi của giải pháp là phải tập trung vào 'hành vi' (behavior) thay vì kiểm tra 'nội dung' (payload) gói tin."*

---

## BƯỚC 3: TIỀN XỬ LÝ & CHẾ TÁC ĐẶC TRƯNG (1.5 Phút)
*(Chạy cell Preprocessing trong Notebook)*

> 🎤 **Thoại:** 
> *"Hệ thống đang chạy qua luồng tiền xử lý dữ liệu. Điểm mấu chốt ở bước này chính là quá trình **Feature Engineering** (chế tác đặc trưng).\n\n*
> *Ngoài việc xử lý dữ liệu khuyết thiếu, hệ thống tự động tính toán thêm một đặc trưng mới là `upload_download_ratio` (tỉ lệ Tải lên/Tải xuống). Chỉ số này đặc biệt quan trọng: Lưu lượng mạng thông thường sẽ có lượng dữ liệu tải xuống (inbound) áp đảo dữ liệu tải lên (outbound). Nhưng khi quá trình Data Exfiltration diễn ra, tỉ lệ tải lên sẽ tăng vọt một cách bất thường. Đây là đặc trưng mang tính quyết định giúp mô hình ML phát hiện ra các điểm dị thường (anomaly)."*

---

## BƯỚC 4: THIẾT LẬP PHÒNG THỦ ĐA LỚP & HUẤN LUYỆN (2.5 Phút)
*(Chạy cell Training, quá trình huấn luyện sẽ mất vài giây)*

> 🎤 **Thoại:** 
> *"Tiếp theo, bộ dữ liệu sau khi chuẩn hóa sẽ được nạp vào module phân tích lõi (Core Detection Engine). Ở đây, nhóm không lựa chọn thuật toán một cách ngẫu nhiên mà chủ đích thiết lập 3 mô hình phân loại (classifiers) theo chiến thuật phòng thủ đa lớp (Defense-in-depth):*
> 
> *Đầu tiên, **Logistic Regression** làm thước đo cơ sở (Baseline) để chứng minh các phương pháp tuyến tính truyền thống đã hụt hơi. Nhược điểm chí mạng của nó là chỉ nhìn nhận mọi đặc trưng (Feature) một cách hoàn toàn độc lập và cộng dồn.*
> 
> *Chủ lực thứ hai làm nhiệm vụ khắc phục khiếm khuyết đó là **Random Forest** (Học có giám sát). Thưa thầy/cô, "ngụy trang tinh vi" trong rò rỉ dữ liệu thực chất là sự tương tác chéo (Interaction) của nhiều yếu tố. Ví dụ: Nhân viên Admin tải 1GB dữ liệu lúc 2 giờ chiều là Bình thường. Một thực tập sinh tải 10MB lúc 2 giờ sáng cũng Bình thường. NHƯNG nếu **(Nhân sự = Thực tập) AND (Giờ = 2h sáng) AND (Dung lượng = 1GB)** thì hệ thống phải báo động Đỏ. Logistic Regression gần như bất lực cực kỳ khó bắt được chuỗi logic này. Ngược lại, cấu trúc rẽ nhánh đan chéo của Random Forest sinh ra chính là để xử lý các logic "AND" lồng nhau như vậy. Chưa kể, cấu trúc Rừng cây còn cho phép truy xuất rành mạch nguyên nhân (Explainable AI) giúp Kỹ sư bảo mật có bằng chứng vững chắc.*
> 
> *Tuy nhiên, Random Forest có một tử huyệt: Nó là mô hình **Học có giám sát**, nghĩa là nó chỉ bắt được những kiểu ăn cắp mà nó TỪNG ĐƯỢC DẠY trong quá khứ. Giả sử ngày mai hacker dùng một thủ đoạn tuồn dữ liệu hoàn toàn mới (ví dụ nhét log vào DNS) thì Random Forest sẽ mù hoàn toàn vì nó đối chiếu không thấy khớp với nhãn tội phạm nào cả.*
> 
> *Đó là lý do ta cần chốt chặn dự phòng cuối cùng: **Isolation Forest** (Học không giám sát). Nó không cần biết tội phạm trông như thế nào, nó chỉ học thuộc "thói quen bình thường" của toàn công ty. Bất kỳ đường truyền nào lọt ra khỏi thói quen chung lập tức bị nó cô lập báo động đỏ. Mô hình này làm lưới vớt dị thường để bắt gọn mọi nỗ lực tân công Zero-day mới nhất.*
> 
> *Toàn bộ dữ liệu ở bước này được chia theo tỷ lệ 80/20. Nghĩa là nhóm em cấp 80% dữ liệu (Tập Train) để dạy cho máy học luật chơi, và giấu kín hoàn toàn 20% dữ liệu còn lại (Tập Test) để dùng làm bài thi kiểm tra chéo cuối cùng. Đồng thời bọn em áp dụng phương pháp lấy mẫu phân tầng (Stratified sampling) để đảm bảo dù ở tập Train hay Test thì bộ mặt của bọn tội phạm cũng không bị pha loãng, giúp quá trình huấn luyện sát với thực tế mạng doanh nghiệp nhất."*

---

## BƯỚC 5: PHÂN TÍCH & ĐÁNH GIÁ CHỈ SỐ (3 Phút - Trọng tâm)
*(Hiển thị các biểu đồ đánh giá trong thư mục `outputs/` hoặc trong Notebook)*

**1. Biểu đồ So sánh các Chỉ số (Metrics Comparison):**
> 🎤 **Thoại:** 
> *"Đây là kết quả đánh giá trên tập kiểm thử (Test set). Trong mảng bảo mật, chúng ta không tối ưu mô hình dựa trên độ chính xác tổng thể (Accuracy) vì nghịch lý của tập dữ liệu mất cân bằng. Thay vào đó, hệ thống được thiết kế để tối đa hóa chỉ số **Recall**.* 
> *Lý do là vì hậu quả của việc bỏ lọt tội phạm (False Negative) nghiêm trọng hơn rất nhiều so với việc cảnh báo nhầm (False Positive). Hiện tại mô hình Random Forest đang đạt chỉ số Recall ở mức [X]%, đảm bảo gần như không bỏ sót bất kỳ một hành vi rò rỉ nào."*

**2. Ma trận Nhầm lẫn (Confusion Matrix):**
> 🎤 **Thoại:** 
> *"Nhìn sâu hơn vào Confusion Matrix của Random Forest, với ngưỡng cấu hình hiện tại, số lượng cảnh báo nhầm (False Positive) nằm ở mức chấp nhận được đối với các chuyên viên phân tích (SOC analyst), trong khi số lượng bỏ lọt tội phạm (False Negative) đã được giảm sát về 0."*

**3. Mức độ quan trọng của Đặc trưng (Feature Importance):**
> 🎤 **Thoại:** 
> *"Cuối cùng, để đáp ứng yêu cầu về khả năng giải thích của AI (Explainable AI - XAI), đây là biểu đồ Feature Importance. Mô hình đã vận hành rất chính xác khi đánh giá cao nhất vai trò của `upload_download_ratio` và `bytes_sent`. Kết quả này hoàn toàn khớp với nghiệp vụ và tư duy của một Kỹ sư Bảo mật khi chủ động săn lùng mối đe dọa (threat hunting)."*

---

## BƯỚC 6: KẾT LUẬN & HƯỚNG PHÁT TRIỂN (1 Phút)
> 🎤 **Thoại:** 
> *"Tóm lại, bản demo này đã minh chứng được tính hiệu quả của việc ứng dụng Học máy phân tích log mạng thô để định vị các nguy cơ rò rỉ dữ liệu.*
> 
> *Về mặt triển khai thực tế (Production), luồng xử lý này hoàn toàn có thể được đóng gói container, kết hợp với các nền tảng Streaming như Kafka và sử dụng các mô hình suy luận nhẹ để phát hiện thời gian thực (Real-time detection) ngay tại biên mạng.*
> 
> *Cảm ơn các thầy cô và các bạn đã theo dõi demo. Mình xin kết thúc phần trình bày và sẵn sàng trả lời các câu hỏi ạ!"*
