# Tóm Gọn Kiến Thức Cốt Lõi Về Hệ Thống Phát Hiện Rò Rỉ Dữ Liệu
*(Góc nhìn theo hệ thống mạng và an toàn thông tin - Bỏ qua kỹ thuật AI cốt lõi)*

Tài liệu này tóm gọn lại bản chất của hệ thống đang được demo, giúp bạn hiểu rõ hệ thống hoạt động để làm gì, tại sao nó lại được thiết kế như vậy dưới góc nhìn của một Kỹ sư Mạng/Bảo mật (Network/Security Engineer).

---

## 1. Bài toán: Kẻ thù từ bên trong (Insider Threat & Data Exfiltration)

Hệ thống này được sinh ra để giải quyết một bài toán cực kỳ đau đầu trong ngành an toàn thông tin: **Nhân viên nội bộ lén lút ăn cắp và tuồn dữ liệu của công ty ra bên ngoài.**

*   **Tại sao Firewall hoặc Antivirus thông thường thất bại?** 
    Firewall và Antivirus rất giỏi chặn kẻ lạ mặt (hacker từ ngoài Internet) cố gắng phá cửa vào công ty. Nhưng với một nhân viên nòng cốt, họ CÓ SẴN chìa khóa (tài khoản hợp lệ), họ ngồi TRONG công ty, chặn họ bằng rào chắn ngoài là điều không thể.
*   **Tại sao dùng Luật (Rule-based) cũng thất bại?** 
    Nếu bạn đặt luật *"Cấm tải lên file quá 1GB"*, kẻ gian sẽ nén file đó thành 10 file 100MB và tải lên trong 10 ngày. Bạn không thể viết tay mọi luật lệ cho vô vần mánh khóe của kẻ gian.
*   **Giải pháp của hệ thống này:** Đứng đằng sau theo dõi **hành vi** của dòng chảy dữ liệu. Khi thấy "Cách cư xử" của dữ liệu di chuyển có mùi bất thường, hệ thống sẽ giăng lưới.

---

## 2. Kiến trúc Luồng Dữ liệu (Dòng chảy mạng)

Hãy tưởng tượng hệ thống như một trạm kiểm soát không lưu. Luồng dữ liệu đi qua 4 trạm:

### Trạm 1: Con mắt thu thập (Data Collection/Sensors)
Hệ thống không can thiệp lấy nội dung (đọc lén file) vì lý do mã hóa HTTPS và quyền riêng tư. Thay vào đó, nó lấy các **Log mạng (Mô hình Netflow)** từ Switch Core hoặc Router. Nó chỉ cần biết: Ai, Gửi cho ai, Dung lượng bao nhiêu, Vào giờ nào.

### Trạm 2: Rây lọc Hành vi thay vì Danh tính (Data Cleaning)
Trong thực tế, địa chỉ IP thay đổi liên tục (do DHCP). Hacker cũng có thể dùng xài VPN hoặc Fake IP. 
👉 **Mấu chốt hệ thống:** Lập trình viên quy định hệ thống **BỎ QUA** đánh giá qua Tên tuổi/Địa chỉ IP (`src_ip`, `dst_ip`). Hệ thống chỉ nhắm vào hành vi hoạt động để đánh giá.

### Trạm 3: Lắp ráp Vũ khí (Feature Engineering)
Nhân viên bình thường truy cập web, xem YouTube thì luồng mạng sẽ là: **Tải xuống nội dung lớn, Tải lên yêu cầu rất nhỏ**.
Kẻ cắp tuồn dữ liệu lên Cloud (Google Drive cá nhân): **Tải xuống gần như bằng 0, Tải lên dữ liệu cực kỳ khổng lồ**.
👉 **Mấu chốt hệ thống:** Tạo ra cột phép tính `Tỉ lệ Tải lên/Tải xuống (Upload/Download Ratio)`. Thuộc tính này là vũ khí chết người bắt thóp hành vi đẩy dữ liệu trái phép ra ngoài mạng nội bộ.

### Trạm 4: Trạm Phân Tích Hành Vi Tập Trung (Central Anomaly Analysis Engine)
Bản chất cỗ máy đằng sau (dù là thuật toán hồi quy, cây quyết định hay chọc lọc điểm mù) đều làm chung một nhiệm vụ: Đối chiếu hành vi của Data ném vào Trạm 3, so sánh với hàng chục triệu bản ghi thói quen hằng ngày của toàn bộ tổ chức, từ đó bắn tín hiệu Có hay Không.

---

## 3. Tâm lý Cảnh báo hệ thống (Alert metrics trong ATTT)

Ngành An toàn thông tin có một sự đánh đổi khốc liệt khi nhận cảnh báo hệ thống:

*   **Tâm lý 1: Ác mộng BỎ LỌT ("False Negative")** 
    Là khi có data đang bị chép trộm đi thật, nhưng trạm thu phát im ắng cho đi qua. Hậu quả: Thất thoát dữ liệu khách hàng, rò rỉ mã nguồn, công ty đền bù hàng triệu đô la.
*   **Tâm lý 2: Hội chứng CẢNH BÁO GIẢ ("False Positive" - Alert Fatigue)** 
    Là khi ông phó giám đốc đang upload lại cái Video dự án cực nạng lên Server đối tác. Máy kêu inh ỏi hú còi cách ly. Đội IT (SOC) lật đật chạy tới kiểm tra và phát hiện nhầm. Nếu hệ thống nhầm vài nghìn lần một ngày, IT sẽ chán nản, mệt mỏi (Fatigue) và rốt cuộc sẽ phớt lờ, tắt cảnh báo của hệ thống.

👉 **Triết lý của hệ thống trong demo:**
Trong bảo mật hiện tại người ta thà tốn công kiểm tra sai (Tâm lý 2), còn hơn là để mất mạng (Tâm lý 1). Nên hệ thống được cấu trúc để tối ưu hóa **Chỉ số Vua (Recall)** - đảm bảo bắt được tối đa 100% số ca mạng khả nghi dù phải hi sinh một chút độ chính xác bắt đúng. 

## 4. Bố cục Triển khai (Hệ thống này nằm ở đâu trong công ty?)

Hệ thống Network Behavior Anomaly Detection (như cái chúng ta đang mô phỏng) thường được thiết lập rẽ nhánh qua một **Cổng Mirror (SPAN Port)** trên lõi mạng Switch Core. 
Nó đứng "Out-of-band" có nghĩa là người dùng thậm chí **không biết** đến sự tồn tại của hệ thống này, nó tàng hình thu log song song, và báo động thẳng về phòng chiến dịch (SOC/NOC Monitoring Dashboard). Tránh việc làm giảm tốc độ băng thông của nhân viên nhưng lại vẫn rào soát được 100% luồng mạng.
