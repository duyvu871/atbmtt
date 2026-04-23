# 10 Câu Hỏi Tiềm Năng Của Giảng Viên ATTT Về Demo Học Máy

Dựa vào bối cảnh của một hệ thống Machine Learning dùng để phát hiện Rò rỉ dữ liệu (Data Leakage / Insider Threat) và Phân tích dị thường mạng, các giảng viên ngành An toàn thông tin (ATTT) thường sẽ không chỉ hỏi về code mà họ sẽ xoáy sâu vào **sự kết hợp giữa tư duy bảo mật và độ hiệu quả của AI**. 

Dưới đây là 10 câu hỏi "hóc búa" và tiềm năng nhất mà giảng viên có thể hỏi trong lúc bạn demo, kèm theo gợi ý trả lời để bạn chuẩn bị:

### Nhóm 1: Sự kết nối giữa các chỉ số AI và Hậu quả Bảo mật

**1. Tại sao trong bài toán phát hiện rò rỉ dữ liệu này, em lại ưu tiên chỉ số Recall hơn là Precision hay Accuracy?**
> **Gợi ý trả lời:** Trong bảo mật, giá phải trả cho **False Negative** (có kẻ trộm rò rỉ dữ liệu nhưng máy tính bỏ lọt, phớt lờ) là cực kỳ lớn, có thể gây mất dữ liệu nhạy cảm của công ty. Trong khi đó, **False Positive** (một nhân viên bình thường tải nhầm file bị AI hiểu nhầm là kẻ trộm - tương ứng Precision thấp) thì chỉ tốn thời gian kiểm tra lại của Admin. Do đó thà bắt nhầm còn hơn bỏ sót, hệ thống bắt buộc phải cấu hình tối đa hóa Recall. Accuracy không đo đếm được điều này, nhất là khi dữ liệu bị mất cân bằng (imbalanced).

**2. Nếu mô hình Random Forest của em đạt Accuracy là 99%, có chắc chắn hệ thống này đã an toàn chưa?**
> **Gợi ý trả lời:** Thưa thầy cô là **Chưa chắc chắn**. Trong mạng lưới, 99.9% lưu lượng là bình thường, chỉ 0.1% là lưu lượng của cuộc tấn công/rò rỉ. Nếu mô hình cứ auto đoán tất cả mọi gói tin đều là "Bình thường" (Label 0), nó vẫn đạt Accuracy 99.9%, nhưng hệ thống thực ra vô dụng vì hoàn toàn bỏ lọt 0.1% cuộc tấn công kia. Đó là nghịch lý mất cân bằng dữ liệu (Accuracy Paradox).

### Nhóm 2: Lựa chọn Thuật toán dưới góc nhìn ATTT

**3. Isolation Forest trong demo là học không giám sát (Unsupervised). Vậy trong thực tế ATTT, thuật toán này giúp giải quyết kịch bản tấn công nguy hiểm nào nhất?**
> **Gợi ý trả lời:** Nó chuyên trị các cuộc tấn công **Zero-Day** (các biến thể tấn công mới hoặc các hành vi rò rỉ dữ liệu chưa từng có trong lịch sử). Vì học có giám sát (Supervised như Random Forest) phải có mẫu (nhãn) từ trước mới nhận diện được, còn Isolation Forest không cần biết trước kẻ xấu trông như thế nào, nó chỉ tìm ra "dị biệt" bất thường so với hành vi thông thường hàng ngày để cảnh báo.

**4. Tại sao lại dùng Logistic Regression làm Baseline (hệ quy chiếu) mà không dùng nó làm mô hình chính để phòng thủ mạng?**
> **Gợi ý trả lời:** Mạng máy tính và dữ liệu bị rò rỉ có pattern (dấu vết) rất phức tạp, phi tuyến tính (tội phạm che giấu bằng cách tản mạn dữ liệu, gửi ra lúc nửa đêm, chia nhỏ file). Logistic Regression chỉ cố gắng giải quyết bằng phương pháp đường thẳng (tuyến tính) nên nó sẽ bị "bắt bài" hoặc Underfitting. Nó được dùng để làm mốc chứng minh rằng "Các mô hình phức tạp như Random Forest thực sự làm tốt hơn các phương pháp thống kê cơ bản".

**5. Random Forest là "rừng cây quyết định". Sự ngẫu nhiên (Random) trong thuật toán này đem lại lợi ích bảo mật nào?**
> **Gợi ý trả lời:** Sự ngẫu nhiên giúp Random Forest không bị **Overfitting (Học vẹt)**. Thay vì tin tưởng vào 1 cây quyết định duy nhất có thể bị kẻ tấn công thao túng dữ liệu (Data Poisoning) làm lệch hướng, nó sử dụng nhiều cây, mỗi cây dùng một phần dữ liệu và thuộc tính (features) ngẫu nhiên. Nhờ biểu quyết số đông, kẻ tấn công rất khó qua mặt được toàn bộ "rừng" cảnh sát.

### Nhóm 3: Vòng đời Dữ liệu & Tính thực tiễn triển khai

**6. Trong thực tế, làm thế nào kẻ tấn công (Attacker) có thể qua mặt hệ thống Machine Learning của em?**
> **Gợi ý trả lời:** Bằng phương pháp Evasion Attacks. Hacker sẽ cố gắng mô phỏng lưu lượng của chúng sao cho giống hệt người bình thường nhất (giảm sự dị biệt) để lừa Isolation Forest, hoặc chúng tiêm dữ liệu bẩn vào quá trình học (Data Poisoning) để Random Forest học sai quy luật (ví dụ: gửi dữ liệu rò rỉ nhưng chia ra rải rác mỗi ngày 1KB trong vài năm thay vì gửi cục 1GB một lúc).

**7. Em chia tập Train/Test theo tỉ lệ 80/20. Nếu mô hình bị "Overfitting", thì điều gì sẽ xảy ra khi em gắn nó vào mạng lưới công ty thực (Real-time network)?**
> **Gợi ý trả lời:** Nếu bị tập Train bị Overfitting (Học vẹt thuộc lòng), điểm test có thể cao. Nhưng khi đem ra triển khai thực tế chặn bắt mạng công ty, chỉ cần một dòng log có thêm thông số lạ (ví dụ IP đích thay đổi, browser thay đổi), mô hình sẽ phân cực sai ngay lập tức vì nó không hiểu "Quy luật", nó chỉ nhớ "Dữ liệu cũ". Hậu quả là sinh ra hàng ngàn cảnh báo giả (False Positive Alert Fatigue) làm loạn admin.

**8. Điều gì sẽ xảy ra nếu thói quen của công ty thay đổi (ví dụ: Trước đây không xài Cloud, nay công ty đăng ký xài Google Drive)? Mô hình Unsupervised (Isolation Forest) của em có bắt khối lượng data up lên Google Drive là tấn công không?**
> **Gợi ý trả lời:** Có, nó sẽ nhận diện nhầm đây là Dị biến (Anomaly) vì khác xa thói quen cũ. Hiện tượng này trong ML gọi là **Concept Drift / Data Drift** (Trôi dạt dữ liệu). Vì thế trong thực tế bảo mật, hệ thống không chỉ train 1 lần mà phải được **Retrain (huấn luyện lại) bằng dữ liệu mới** định kỳ để làm quen với các hành vi bình thường mới.

**9. Hiện tại em đang có sẵn tập dữ liệu file excel CSV để cho máy học. Nhưng trong thực tế làm IDS/DLP (Hệ thống chống thất thoát), dữ liệu đầu vào (Features) để tính toán thường được trích xuất từ đâu và gồm những gì?**
> **Gợi ý trả lời:** Trong thực tế, dữ liệu sẽ thu thập từ Netflow, PCAP network traffic hoặc System Logs. Các đặc trưng (Features) bao gồm: Số lượng packets in/out, Tổng số bytes tải lên/tải xuống bất thường, Cổng (Port) đích, Tần suất kết nối trong khung giờ 2AM - 4AM, Quốc gia của IP đích... Các đặc trưng này sau đó sẽ được feature engineering (chuyển đổi) rồi mới cho dự đoán.

**10. Việc chạy Random Forest có độ trễ (latency) không? Nếu anh/chị cần một hệ thống chặn rò rỉ dữ liệu theo thời gian thực (block lập tức gói tin) thì kiến trúc triển khai sẽ phải thay đổi ra sao?**
> **Gợi ý trả lời:** Nếu Random Forest quá nặng, nó sẽ làm chậm băng thông mạng do tốn thời gian predict. Để giải quyết, mô hình cần được xuất ra các file nhẹ hơn (ONNX format) chạy trên thiết bị phần cứng chuyên dụng, hoặc dùng các mô hình cực kỳ nhẹ để chạy ở Tầng Network chặn sơ bộ trước, sau đó mới đẩy về máy chủ phân tích sâu hơn bằng các mô hình cực nặng.

---

> 💡 **Mẹo khi trả lời:** Hãy luôn nhấn mạnh rằng: _"Máy học trong demo là cốt lõi (Core Engine), nhưng để đưa vào ATTT thực tế, nó phải đối phó với việc dữ liệu bị mất cân bằng trầm trọng, hành vi nhân viên thay đổi liên tục, và hacker luôn tìm cách làm nhiễu dữ liệu."_
