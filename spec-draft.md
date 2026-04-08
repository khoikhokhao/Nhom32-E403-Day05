# SPEC Draft - Nhóm 32- Phòng E403

## Track Lựa Chọn: VinFast

## 🎯 Tuyên Bố Vấn Đề (Problem Statement)
**Ai gặp vấn đề gì:** Khách hàng mới muốn mua xe điện và chủ xe VinFast hiện tại thường bị "ngợp" trước lượng thông tin phân tán (giá pin, chính sách sạc, lịch bảo dưỡng), dẫn đến hành trình trải nghiệm bị đứt đoạn và tăng tải cho đội ngũ CSKH. 
**AI giải quyết thế nào:** Một AI Copilot (Trợ lý ảo) được tích hợp sâu vào hệ sinh thái VinFast sẽ đóng vai trò "chuyên gia tư vấn cá nhân", tự động hóa việc tra cứu chính sách, cá nhân hóa gợi ý chọn xe/đặt lịch xưởng, đồng thời liên tục tổng hợp phản hồi của người dùng để cảnh báo sớm các điểm nóng về chất lượng vận hành.

---

## 1. AI Product Canvas

| | Value (Giá trị) | Trust (Niềm tin) | Feasibility (Khả thi) |
|---|---|---|---|
| **Trả lời** | **User:** (1) Khách tìm hiểu xe mới; (2) Chủ xe cần hỗ trợ kỹ thuật/đặt lịch; (3) Khối Dịch vụ & CSKH.<br><br>**Pain points:** Tra cứu chính sách pin/sạc phức tạp; chờ đợi tổng đài lâu; dữ liệu phản hồi bị phân mảnh.<br><br>**AI Solutions:** Trợ lý ảo giải đáp 24/7 tức thì dựa trên Knowledge Base chuẩn; flow đặt lịch nhanh gọn; tự động phân loại và trích xuất "pain points" từ hàng ngàn bình luận để team R&D xử lý. | **Hậu quả khi sai:** Gợi ý sai gói thuê pin gây thiệt hại tài chính; hướng dẫn xử lý cảnh báo lỗi trên xe sai gây nguy hiểm.<br><br>**Xây dựng Trust:** Mọi câu trả lời về kỹ thuật/giá phải có trích dẫn nguồn (Link to policy). Luôn hiển thị nút "Kết nối Kỹ thuật viên".<br><br>**Sửa lỗi:** Tích hợp UI cho phép người dùng thay đổi tham số (ví dụ: đổi dòng xe, đổi mốc km bảo dưỡng) chỉ với 1-Click thay vì gõ lại prompt. | **Tech Stack:** RAG Pipeline (Truy xuất tài liệu nội bộ) + LLM gán nhãn Sentiment.<br><br>**Costs:** Chi phí token API cho LLM và Vector DB lưu trữ tài liệu. Dự kiến ở mức an toàn cho giai đoạn Pilot.<br><br>**Risks chính:** Ảo giác dữ liệu (bịa ra chương trình khuyến mãi đã hết hạn); độ trễ (Latency) khi truy xuất tài liệu nặng. |

**Quyết định: Automation hay Augmentation?** -> **Augmentation (Gợi ý).**
**Lý do:** Mua xe ô tô là quyết định tài chính lớn (High-involvement), và lỗi kỹ thuật xe liên quan đến an toàn tính mạng. AI chỉ đóng vai trò phân tích và đề xuất phương án (Copilot), người dùng hoặc kỹ thuật viên VinFast mới là người đưa ra quyết định chốt hạ.

### Learning Signal (Tín hiệu học tập)

| # | Câu hỏi | Trả lời |
|---|---|---|
| 1 | Dữ liệu sửa lỗi (Correction) đi về đâu? | Đưa vào kho dữ liệu Explicit Feedback. Phân tích các luồng bị user "Reject" để tinh chỉnh lại Chunking trong RAG hoặc bổ sung câu hỏi vào mục FAQ hệ thống. |
| 2 | Signal nào đánh giá sản phẩm tốt lên/tệ đi? | **Quantitative:** Tỉ lệ tự giải quyết xong (Self-service rate); Tỉ lệ chốt lịch lái thử/bảo dưỡng. <br>**Qualitative:** CSAT Score; Tỉ lệ user ấn nút "Chuyển sang Tư vấn viên" (Escalation rate). |
| 3 | Phân loại dữ liệu? | **Domain-specific:** Cẩm nang sử dụng xe VF, chính sách trạm sạc. <br>**User-specific:** Quãng đường ODO hiện tại, dòng xe đang đi. <br>**Real-time:** Slot trống tại xưởng dịch vụ. |

**Lợi thế cạnh tranh (Marginal Value):** Bộ dữ liệu về thói quen sử dụng xe điện, các lỗi thường gặp theo điều kiện khí hậu Việt Nam và lịch sử bảo dưỡng là "tài sản độc quyền" của VinFast. Các hãng xe xăng hoặc đối thủ mới sẽ không thể có sẵn tệp Data Flywheel này để huấn luyện AI.

---

## 2. User Stories - 4 Paths UX (Thiết kế cho sự không chắc chắn)

### Path 1 - Khi AI Đúng (Value Moment)
- **Context:** User nhắn *"Mình có 800 triệu, đi làm trong nội thành Hà Nội, chung cư không có sạc."*
- **Action:** AI tính toán quãng đường, đề xuất VF 6 kèm gói thuê pin (vì không có sạc nhà). Gợi ý bản đồ trạm sạc gần chung cư user nhất.
- **UI/UX:** Hiển thị Card thông tin xe + Nút "Đăng ký lái thử cuối tuần này". Mượt mà, không ma sát.

### Path 2 - Khi AI Không Chắc (Low-Confidence Fallback)
- **Context:** User nhắn *"Xe tự nhiên báo lỗi con rùa màu vàng trên màn hình".*
- **Action:** AI không có quyền tự chẩn đoán bệnh. Nó chặn luồng suy luận tự do (Hallucination).
- **UI/UX:** AI phản hồi: *"Lỗi hình con rùa liên quan đến giới hạn công suất mô-tơ. Để đảm bảo an toàn, AI xin phép kết nối bạn ngay với Chuyên viên Kỹ thuật nhé!"* kèm theo nút Gọi Hotline khẩn cấp.

### Path 3 - Khi AI Sai (Graceful Failure & Correction)
- **Context:** User hỏi *"Bảo dưỡng mốc 12.000km cho VF 5 tốn bao nhiêu?"*. AI trả về báo giá của mốc 24.000km.
- **Action:** User nhận ra giá cao bất thường.
- **UI/UX:** Ngay dưới báo giá có các Chips UI: `[Sửa thành mốc 12.000km]`, `[Xem bảng giá chuẩn]`. User bấm sửa với 1 chạm. Hành động này tạo Explicit Signal báo cáo hệ thống RAG đang truy xuất sai bảng giá.

### Path 4 - Khi User Mất Niềm Tin (Trust Breakdown Exit)
- **Context:** AI liên tục hiểu sai ý định đặt lịch của user 2 lần liên tiếp.
- **Action:** Tránh "The Alexa Effect" (vòng lặp hỏi đáp ngu ngốc).
- **UI/UX:** Tự động kích hoạt tính năng "Human Handoff" (Chuyển giao người thật). Ẩn giao diện chat của AI, chuyển toàn bộ lịch sử đoạn hội thoại sang màn hình của nhân viên CSKH để họ tiếp quản ngay lập tức.

---

## 3. Eval Metrics & Threshold (Đo lường chất lượng)

**Đánh giá độ chính xác của AI (AI Capabilities):**
- **Độ phủ nguồn (Groundedness Score):** $\ge 90\%$ câu trả lời bắt buộc phải lấy thông tin từ kho tài liệu VinFast, không được tự "bịa" chính sách.
- **Chỉ số điều hướng (Routing Accuracy):** $\ge 92\%$ phân loại đúng ý định người dùng (Hỏi mua xe / Hỏi lỗi kỹ thuật / Khiếu nại).
- **Độ chính xác cảm xúc (Sentiment F1-Score):** $\ge 0.85$ trong việc đọc hiểu review của khách hàng (Tích cực / Tiêu cực / Góp ý).

**Đánh giá tác động Kinh doanh (Business Outcomes):**
- Tỉ lệ thành công (Task Completion Rate) cho luồng Đặt lịch: $\ge 40\%$.
- Giảm thời gian xử lý khiếu nại (Time-to-resolution) của team CSKH: giảm $\ge 40\%$ nhờ AI đã tóm tắt sẵn vấn đề.

---

## 4. Failure Modes & Mitigation (Thư viện rủi ro)

1. **Rủi ro:** AI "ảo giác" (Hallucinate) ra một chương trình giảm giá không có thật.
   * **Mitigation:** Áp dụng kỹ thuật Prompt Engineering chặt chẽ: *"Chỉ trả lời dựa trên context được cung cấp. Nếu không có, nói Tôi không biết"*.
2. **Rủi ro:** Báo giá cũ, chưa cập nhật chính sách mới.
   * **Mitigation:** Dữ liệu RAG phải được đồng bộ (Sync) mỗi đêm. Câu trả lời của AI luôn đính kèm dòng: *"Cập nhật lúc [Ngày/Giờ] - Áp dụng tại thị trường VN"*.
3. **Rủi ro:** Bỏ sót các phản hồi (Review) chứa cảnh báo nguy hiểm về pin.
   * **Mitigation:** Xây dựng danh sách "Tứ chứng nan y" (Safety Triggers keywords). Nếu review chứa các từ này, tự động bypass AI và cảnh báo đỏ (Alert) cho team Kỹ thuật.

---

## 5. Phân tích ROI - 3 Kịch bản Pilot

**Giả định:** Triển khai thử nghiệm với 15.000 lượt chat/tháng. Chi phí API + Server khoảng 1.000 VNĐ/lượt chat.
**Cost (Chi phí cố định):** ~15.000.000 VNĐ/tháng.

| Kịch bản | Conservative (Kém) | Expected (Đạt kỳ vọng) | Optimistic (Xuất sắc) |
|---|---|---|---|
| **Tỉ lệ chặn (Deflection Rate)** | 15% | 35% | 55% |
| **Giờ CSKH tiết kiệm được** | 100 giờ | 250 giờ | 450 giờ |
| **Giá trị quy đổi (VNĐ)** | 20 Triệu | 50 Triệu | 90 Triệu |
| **Net ROI (Giá trị ròng)** | **+ 5 Triệu** | **+ 35 Triệu** | **+ 75 Triệu** |

**Kill Criteria (Điểm dừng dự án):** Nếu sau 2 tháng triển khai, Net ROI âm (Cost vượt quá giá trị tiết kiệm) HOẶC điểm CSAT của người dùng chat với AI $\le 3.5/5$, dự án sẽ bị tạm ngưng để đánh giá lại luồng dữ liệu RAG.

---

## 6. Mini AI Spec (Thông số kỹ thuật MVP)

### Scope (Phạm vi sản phẩm)
- **Nền tảng:** Widget trên Website VinFast & Zalo OA.
- **Core Features:** (1) Trợ lý mua xe; (2) Trợ lý Hậu mãi (Bảo dưỡng/Sửa chữa); (3) Bảng điều khiển phân tích Review cho nội bộ.

### Input / Output
- **Input:** Câu lệnh Text/Voice của user; Mã VIN của xe (nếu user cung cấp).
- **Output:** Câu trả lời cấu trúc rõ ràng (Markdown); Bảng so sánh; Link điều hướng.

### Tech Flow
1. User nhập câu hỏi.
2. Bộ phân loại (Router LLM) kiểm tra: Nếu là lỗi an toàn -> Chuyển người thật.
3. Nếu là câu hỏi thường -> Sinh Embedding -> Quét qua Vector DB chứa cẩm nang VinFast.
4. LLM tổng hợp Context và trả lời user.
### Phân công thực hiện Hackathon (Đội hình 5 thành viên)
- **Ngô Quang Tăng:** Phụ trách AI Canvas & Thiết kế luồng UX (User Stories - 4 Paths), thiết kế luồng tương tác (UI/UX) của người dùng, **chịu trách nhiệm thiết kế Slide Pitching**.
- **Vũ Đức Minh:** Đảm nhiệm Prompt Engineering, xây dựng logic cho luồng RAG (truy xuất tài liệu VinFast) và thiết lập kịch bản Fallback (chuyển người thật), **xây dựng kịch bản thuyết trình (Pitching content)**.
- **Trần Sỹ Minh Quân:** Xây dựng Eval Framework (bộ dữ liệu test cases), rà soát Failure Modes (Thư viện rủi ro) và thiết kế các phương án Mitigation.
- **Nguyễn Thế Anh:** Phân tích Business/Tài chính (Tính toán ROI 3 kịch bản), xác định các Eval Metrics và chiến lược thu thập Learning Signal (Data Flywheel).
- **Phạm Minh Khôi:** Theo dõi tiến độ dự án , **trực tiếp lập trình tích hợp hệ thống MVP (code giao diện Chatbot kết nối với RAG/LLM)**, tổng hợp tài liệu Mini Spec.

---
