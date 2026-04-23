# NHẬP MÔN HỌC MÁY (MACHINE LEARNING) CHO NGƯỜI MỚI BẮT ĐẦU
*Tài liệu này được soạn dành riêng để giúp bạn đi từ "trang giấy trắng" đến việc hiểu cặn kẽ bản chất công nghệ đằng sau Demo rò rỉ dữ liệu này.*

---

## 1. Bản chất của Học Máy (Machine Learning - ML) là gì?

Lập trình truyền thống (ví dụ: Viết App, Viết Web) hoạt động theo kiểu **"Có nguyên tắc sẵn"**:
> *Kỹ sư tạo ra LUẬT (Luật: Nếu điểm >= 5 -> Đậu). Đưa DỮ LIỆU (Điểm 7) vào -> Máy tính nhổ ra KẾT QUẢ (Bạn đậu).*

Nhưng trên đời có những thứ không thể viết bằng LUẬT, ví dụ như *"Làm sao biết người này mang dáng đi của một tên trộm?"*. Khi đó **Học Máy** ra đời. Nó làm ngược lại:
> *Kỹ sư đưa cho máy DỮ LIỆU (Video 1.000 tên trộm) + KẾT QUẢ kèm theo (Đây là hình ảnh của vụ trộm). Máy tính sẽ ngậm nhấm xào nấu để tự đẻ ra **LUẬT**.*

Ở Demo này cũng vậy, chúng ta không dạy máy tính "Kẻ cắp cấu hình mạng trông thế nào". Ta quăng cho nó file Excel 5.000 dòng log mạng và bảo: *"Này, 750 dòng cuối là vết tích của kẻ trộm rò rỉ dữ liệu đấy, mày tự tìm điểm chung của chúng nó đi"*. Mọi thứ còn lại máy tính tự lo!

---

## 2. Hai Trường Phái Học Máy Có Mặt Trong Demo

Trong thế giới Học Máy có nhiều trường phái, nhưng bài Demo sử dụng 2 trường phái kinh điển nhất:

### A. Học Có Giám Sát (Supervised Learning)
👉 *Giống như "Đi thi có đáp án sẵn".*
Bạn cung cấp dữ liệu và nói rõ cho máy: "*Dòng 1 là Bình Thường (Label 0), Dòng 2 là Kẻ Trộm (Label 1)*". Quá trình học này tạo ra bài toán **Phân Loại Nhị Phân (Binary Classification)** - Bắt máy tính sau khi học xong phải nhìn vào một dữ liệu mới và bốc thuốc nó là Bình thường (0) hay Trộm (1). 

*Trong Demo: Áp dụng qua mô hình **Logistic Regression** và **Random Forest**.*

### B. Học Không Giám Sát (Unsupervised Learning)
👉 *Giống như "Thả bạn vào một lớp sinh viên quốc tế mà bạn không biết ai tên gì".*
Bạn đưa dữ liệu cho máy tính và **KHÔNG** hề cho nó biết ai là kẻ trộm. Bạn chỉ bảo: *"Đây là sinh hoạt hàng ngày của nhóm người tốt, mày tự tìm hiểu đi"*. Sau đó vào một ngày đẹp trời, có kẻ gửi file dung lượng cực lớn lúc 2 giờ sáng ra nước ngoài (Khác bọt hoàn toàn với thói quen của người tốt). Máy tính thốt lên: *"Tôi không biết anh là ai, nhưng anh quá Dị Biệt (Anomaly), tôi sẽ gắn cờ anh!"*

*Trong Demo: Áp dụng qua mô hình **Isolation Forest**.*

---

## 3. Ba Phép Thuật (Thuật toán) Sử dụng trong Demo

Thay vì gọi là thuật toán khô khan, hãy coi chúng là 3 chuyên gia an ninh:

1. **Anh lính "Logistic Regression" (Hồi quy):**
   - Anh này sẽ cố gắng **kẻ một đường thẳng** trên tấm bản đồ dữ liệu để chia đôi: "Bên trái đường kẻ là Hiền, bên phải đường kẻ là Trộm".
   - **Ưu / Nhược:** Chạy cực kỳ nhanh (vẽ 1 nét là xong), nhưng đời không như mơ, tội phạm mạng rất tinh vi và thường di chuyển ziczac, nên kẻ đường thẳng thường dễ bị sai sót bắt trượt. Do đó đây chỉ dùng làm hệ tham chiếu (Baseline).

2. **Hội đồng Thẩm phán "Random Forest" (Rừng Cây Quyết Định):**
   - Không cho 1 ông cảnh sát quyết định nữa, ta mời **Hành trăm Cảnh sát độc lập** (Gọi là mảng các Decision Trees). Người thì săm soi *Thời gian*, người săm soi *Giờ giấc*, người soi *Số Megabytes*. Cuối cùng 100 ông này phải... giơ tay biểu quyết (Voting). Nếu > 50 người đồng ý đây là Tội phạm, thì nó là Tội phạm.
   - **Ưu điểm:** Khó bị lừa nhất, độ chính xác gần như 100% trong bài Demo. Đây là vũ khí săn tội phạm mạng chủ chốt của các hãng bảo mật lớn.

3. **Cảnh khuyển "Isolation Forest" (Phát hiện điểm mù):**
   - Mấy con chó nghiệp vụ thường có linh cảm khoanh vùng dị thú. Thuật toán này không quan tâm quá khứ. Nó liên tục đào bới bao vây đống dữ liệu. Nếu một hạt dữ liệu nào quá dễ bị cô lập chỉ bằng một hai đường cắt (vì hạt đó trơ trọi, khác biệt số đông), hạt dữ liệu đó bị đánh giá là Bất Thường. Cực kỳ hiệu quả để chống Virus kiểu mới (Mệnh danh là Zero-day attacks).

---

## 4. Máy tính đi thi thế nào? (Data Split & Epochs)

Trong code, bạn thấy thao tác **Chia dữ liệu 80/20 (Train/Test Split)**. Nghĩa là gì?

- Nếu bạn mua một cuốn sách 1.000 bài tập để học Toán. Nếu bạn giải hết 1.000 bài để học, đến lúc thi cuối kì thầy giáo lấy đúng 1 bài trong cuốn sách đó ra thi. Bạn làm 10 điểm. => Đây gọi là **Học vẹt (Overfitting)**. Bạn được 10 điểm không phải bạn giỏi Toán, mà vì bạn... nhớ đề!
- Để biết máy tính "Giỏi" thật sự không, kỹ sư chỉ đưa 80% (4.000 số liệu) để nó cày cuốc ngày đêm **(Train set)**. Giấu nhẹm 20% (1.000 bài) còn lại đi đi làm Đề Thi. Đến ngày thi, mới bung 1.000 câu hỏi này ra bắt nó làm **(Test set)**.
- Khi đánh giá Accuracy (Độ chính xác) ở trong báo cáo, đó là điểm số máy tính đạt được trên **Tập Đề Thi ẩn 20% kia**, chứng tỏ nó là một chuyên gia bắt rò rỉ dữ liệu thực thụ chứ không hề học vẹt!

---

## 5. Đọc Dịch Bảng Điểm Thi của Máy Tính (Đánh giá chỉ số AI)

Cuối Demo, AI khoe bảng điểm với 4 con số, bạn cần nhớ ý nghĩa sau:

- **Accuracy (Độ chính xác tống thể):** AI làm đúng được bao nhiêu câu trên tổng số. (VD 99%).
- **Precision (Đã bắt là không bắt nhầm):** Nếu AI túm cổ 100 công nhân bảo là Ăn cắp, thì trong đó có bao nhiêu công nhân bị oan (Gọi là **False Positive**). 
- 👑 **Recall (Ông vua trong Ngành Bảo mật):** Nếu có 100 kẻ ăn cắp thật trong mạng, AI tóm được bao nhiêu thằng và vô ý để lọt bao nhiêu thằng đi qua cửa (Gọi là **False Negative**). 

👉 Trong bảo mật mạng, người ta **Sợ nhất là Recall thấp**. Bạn có thể thà tóm nhầm bắt nhân viên giảo trình vì tải nhầm file (Precision thấp xíu không sao), chứ tuyệt đối không được cấu hình máy tính lơ đễnh để tên trộm ung dung cuỗm file khách hàng đi mất (False Negative cực kỳ nguy hiểm). Vì thế trong hệ thống, kỹ sư đã thêm đoạn code để ép Recall phải đạt lớn nhất có thể!

---
*Đọc xong tài liệu này, bạn hãy liếc qua file Notebook Demo một lần nữa. Mọi dòng code rắc rối sẽ bỗng nhiên biến thành những mệnh lệnh cực kỳ logic từ con người gửi xuống cho máy!*
