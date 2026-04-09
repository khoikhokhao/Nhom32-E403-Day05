import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load API Key từ file .env
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Khởi tạo Client OpenAI
client = OpenAI(api_key=API_KEY)

# 2. Cấu hình giao diện trang Web
st.set_page_config(page_title="VinFast AI Copilot", page_icon="🚗")
st.title("🚗 VinFast AI Copilot")
st.caption("Trợ lý ảo tư vấn mua xe & bảo dưỡng (Powered by GPT-4o-mini)")

# 3. SYSTEM PROMPT: Định hình não bộ của AI
SYSTEM_PROMPT = """
Bạn là Trợ lý ảo tư vấn cao cấp của VinFast. Nhiệm vụ của bạn là:
1. Tư vấn mua xe: Dựa vào ngân sách và nhu cầu (quãng đường, nơi ở) để gợi ý dòng xe VinFast phù hợp (VF3, VF5, VF6, VF7, VF8, VF9).
2. Hỗ trợ bảo dưỡng: Giải đáp mốc bảo dưỡng, chi phí dự kiến.

[RÀNG BUỘC QUAN TRỌNG - THIẾT KẾ CHO SỰ KHÔNG CHẮC CHẮN]:
- Luôn trả lời bằng tiếng Việt, ngắn gọn, dùng Markdown (in đậm, bullet point) cho dễ đọc.
- Nếu người dùng báo LỖI KỸ THUẬT NGUY HIỂM (liên quan đến phanh, pin, cảnh báo đỏ trên màn hình, lỗi con rùa): TUYỆT ĐỐI KHÔNG tự chẩn đoán. Phải yêu cầu họ tấp vào lề và cung cấp ngay số Hotline (1900 23 23 89) để gặp Kỹ thuật viên thật (Human-Handoff).
- Nếu người dùng hỏi các hãng xe khác hoặc kiến thức không liên quan: Từ chối lịch sự và lái câu chuyện về xe VinFast.
"""

# 4. Quản lý lịch sử Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào! Mình là Trợ lý AI của VinFast. Mình có thể giúp bạn tìm chiếc xe ưng ý hoặc đặt lịch bảo dưỡng hôm nay?"}
    ]

# Hiển thị lại lịch sử
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Xử lý khi người dùng nhập tin nhắn mới
if prompt := st.chat_input("Nhập câu hỏi của bạn (VD: Tìm xe tầm 700 triệu...)"):
    
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Đưa System Prompt lên đầu danh sách tin nhắn để GPT hiểu vai trò
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    # Gọi API GPT-4o-mini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0.2 # Ngăn AI "ảo giác" (Hallucination)
            )
            
            # Trích xuất câu trả lời và hiển thị
            answer = response.choices[0].message.content
            message_placeholder.markdown(answer)
            
            # Lưu vào bộ nhớ
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            message_placeholder.error(f"Lỗi kết nối OpenAI: {str(e)}\nVui lòng kiểm tra lại API Key trong file .env")