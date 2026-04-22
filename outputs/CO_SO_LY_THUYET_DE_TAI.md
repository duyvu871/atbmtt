# CẨM NANG NGƯỜI MỚI: TỪ LÝ THUYẾT ĐẾN THỰC TIỄN DEMO

*(Hướng dẫn đọc hiểu dành cho các bạn mới tiếp cận An toàn Thông tin và Trí tuệ Nhân tạo)*

Tài liệu này không chứa code hay toán học phức tạp. Mục đích của tài liệu là giúp bạn trả lời 3 câu hỏi lớn: **Chúng ta đang giải bài toán gì? Vì sao lại dùng cách này? Và kết quả Demo chứng minh điều gì?**

---

## PHẦN 1: BỨC TRANH TOÀN CẢNH

### 1.1 Rò rỉ dữ liệu (Data Leakage) là gì?
Hãy tưởng tượng hệ thống máy tính của ngân hàng là một **Tòa lâu đài**:
- **Hacker bên ngoài (External Threat):** Là những kẻ cầm vũ khí cố gắng phá cổng lâu đài. Chúng ta dùng Firewall (Tường lửa) để chặn chúng lại. Rất dễ nhận biết.
- **Nội gián (Insider Threat):** Là những nhân viên hợp lệ, đang làm việc bên trong lâu đài và có chìa khóa kho báu. Một ngày nọ, họ lén cho vàng vào túi và ung dung bước ra cửa. 
  
👉 **Rò rỉ dữ liệu (Data Leakage)** nguy hiểm ở chỗ những kẻ ăn cắp dữ liệu *có quyền hợp lệ*, nên hệ thống an ninh bình thường không hề phát ra tiếng còi báo động.

### 1.2 Làm sao để bắt được kẻ nội gián? (NetFlow vs. DPI)
Có 2 cách để kiểm tra những người đi ra khỏi lâu đài:
1. **DPI (Khám xét tận tay):** Bắt tất cả mọi người mở balo ra, kiểm chứng từng tờ giấy. Rất mất thời gian, tốn kém và sẽ bó tay nếu giấy tờ đó đã bị in **Mật mã (Mã hóa HTTPS)**.
2. **NetFlow/IPFIX (Lưu lượng mạng - Cách Demo áp dụng):** Chúng ta không mở balo ra xem. Chúng ta chỉ nhìn vào **Bảng thống kê ngoài vỏ**: 
   - *Anh A đi ra ngoài lúc mấy giờ? Mang theo khối lượng đồ nặng bao nhiêu? Anh A chuyển đồ cho ai bên kia biên giới?*
   
👉 Bằng cách dùng **Lưu lượng Mạng (NetFlow)**, chúng ta không cần giải mã dữ liệu phức tạp. Điểm yếu duy nhất kẻ trộm để lại chính là **"Hành Vi Bất Thường"** (VD: Mang lượng đồ khổng lồ, đi vào lúc 2 giờ sáng).

---

## PHẦN 2: TRÍ TUỆ NHÂN TẠO VÀO CUỘC NHƯ THẾ NÀO?

Hệ thống ghi chép mạng (Netflow) có thể trả về hàng triệu dòng mỗi ngày. Con người không thể nào ngồi đọc từng dòng để tìm ra kẻ trộm. Ta phải nhờ đến **Máy Học (Machine Learning)**. 

### 2.1 Tiền xử lý dữ liệu (Dạy máy tính học cách nhìn)
Máy tính rất ngốc nên nó sẽ học theo kiểu "Học vẹt" nếu ta không dạy đúng cách.
- **Bỏ đi phần Tên/Địa chỉ IP:** Đừng cho máy tính biết tên của người gửi đồ đi. Nếu biết, nó sẽ học vẹt kiểu: *À, cứ là ông Giám Đốc thì là ăn cắp.* Bạn phải ép máy tính phải phán xét dựa trên **Hành động** chứ không phải **Danh tính**.
- **Tỉ lệ Tải lên/Tải xuống (Upload/Download Ratio):** Người đi làm bình thường luôn kéo tài liệu về đọc (Tải xuống nhiều). Nhưng người ăn cắp thì luôn ném dữ liệu đi (Tải lên cực nhiều). Đây là chìa khóa vàng của Demo!
- **Khung giờ (Hour of day):** Máy tính không hiểu thời gian, ta dạy nó rằng từ 1-8 AM và 18-24 PM là những khung giờ "nhạy cảm".

### 2.2 Sân khấu của hai "Bộ Não" Học Máy

**A. Mô hình Random Forest (Học CÓ giám sát)**
- **Giống như:** Cảnh sát trưởng dày dạn kinh nghiệm.
- **Cách học:** Bạn đưa ra lịch sử 1.000 vụ ăn cắp trước đây và bảo *“Nhìn này, đây là mặt mũi của tội phạm”*. Từ đó Cảnh sát trưởng tạo ra vô số các Cây suy luận (VD: Hễ ai ra ngoài giờ hành chính + Tải lên > 500MB + Gửi ra địa chỉ Lạ => Chắc chắn ăn cắp).
- **Kết quả Demo:** Chính xác tuyệt đối (99.9%). Tóm gọn toàn bộ kịch bản lỗi lọt đã biết. Thuật toán này dùng làm tấm khiên chắn chính.

**B. Mô hình Isolation Forest (Học KHÔNG giám sát)**
- **Giống như:** Một nhà Trinh thám nghi ngờ mọi thứ.
- **Cách học:** Bạn không cần đưa lịch sử người xấu. Bạn chỉ cho ông ta xem *“Đây là thói quen sống hàng ngày của những công dân tốt”*. Khi ai đó có hành động lệc chuẩn (Lệch cực đoan), ông ta khoanh vùng tách biệt người đó ra ngay lập tức.
- **Kết quả Demo:** Cho phép bắt **Nạn Rò Rỉ Chưa Từng Có Tiền Lệ (Zero-day Data Leak)**. Bù lại có thể bắt oan vài người tốt có thói quen dị biệt (False Positive), nhưng trong bảo mật "Thà giết lầm còn hơn bỏ sót".

---

## PHẦN 3: KẾT QUẢ DEMO THỰC TẾ CHỨNG MINH ĐIỀU GÌ?

Khi bạn chạy bản Demo, nó sẽ tung ra 4 loại Bảng biểu. Nếu bạn là một "Lính Mới", đây là cách đọc hiểu:

1. **Top Đặc Trưng (Feature Importance):**
   - Đập ngay vào mắt là `bytes_sent` (Lượng dữ liệu gửi đi) và `upload_download_ratio` (Mức độ gửi/nhận). Demo chứng minh rằng thuật toán Random Forest hoàn toàn hiểu đúng tư duy của bảo mật - kẻ cắp phải bộc lộ qua lượng Data tung ra ngoài.
2. **False Negative (Tội phạm trốn thoát):**
   - Nhìn vào Bảng Confusion Matrix, FN (số người xấu bị mô hình bỏ lọt) gần như bằng `0` ở mọi mô hình. Lý luận: Kĩ sư bảo mật đã gài trọng số `class_weight='balanced'` để ép AI "Sợ sệt hơn, bắt căng hơn".
3. **Mô hình AI đang vận hành thay kĩ sư an ninh mạng:**
   - Với độ cảnh báo gần như 100% tỷ lệ bắt trúng, chỉ cần đem mô hình của Demo này nhúng (Deploy) vào Tường Lửa hoặc Phần mềm SIEM của công ty, cứ mỗi luồng mạng chạy qua, máy tính sẽ trả về còi cảnh báo trong chưa tới 1 mili-giây.

**⭐ Lời khuyên cuối:** Hãy đọc bản báo cáo này tự nhiên như một câu chuyện. Đừng quá cố ghi nhớ các công thức toán học, hãy ghi nhớ "Máy tính đang cố gắng bắt bệnh kẻ xấu qua những hành vi nhỏ nhất" - đó chính là cốt lõi của môn học An Toàn Hệ Thống.
