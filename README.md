# AI assistant for SVUIT-MMTT

## Front end

### 1. Khởi tạo Widget

- Sự kiện: Người dùng truy cập trang web svuit.org/mmtt/.
- Hành động:
    + Widget xuất hiện ở một vị trí cố định góc dưới bên phải.
    + Hiển thị một icon chat và dòng chữ Ask AI.

### 2. Người Dùng Khởi Đầu Cuộc Trò Chuyện

- Sự kiện: Người dùng click vào widget.
- Hành động:
    + hiển thị khung chat và chú thích về tác dụng của chatbot.
    + Các nội dung bên ngoài khung chat được làm mờ đi.
      
### 3. Người Dùng Nhập Tin Nhắn

- Sự kiện: Người dùng nhập văn bản vào ô chat.
- Hành động:
  + Tin nhắn của người dùng được gửi đi (Hiển thị phía bên phải khung chat).
  + Bot xử lý tin nhắn và trả lời phù hợp (Hiển thị phía bên trái khung chat).

### 4. Bot Trả Lời

- Sự kiện: Bot đã xử lý xong tin nhắn của người dùng.
- Hành động:
  + Bot gửi tin nhắn trả lời, có thể bao gồm:
    + Văn bản: Câu trả lời trực tiếp cho câu hỏi của người dùng.
    + Markdown: Hiển thị thông tin dưới dạng file Markdown.
    + Nút:
    	+ Copy: để người dùng sao chép câu trả lời từ bot.
    	+ Refresh: để người dùng muốn bot trả lời lại câu hỏi đã hỏi trước đó.
    
### 5. Các Tương Tác Khác

- Người dùng xem lại lịch sử chat: Cho phép người dùng xem lại các cuộc trò chuyện trước đó bằng cách cuộn lên trên.

### 6. Kết Thúc Cuộc Trò Chuyện

- Sự kiện: Người dùng đóng tab.
- Hành động:
  + Widget thu nhỏ lại về trạng thái ban đầu và xóa toàn bộ nội dung chat trước đó.



## Back end

- Language: python
- Dependencies: langchain, langchain_google_vertexai, langchain_community, unstructured, unstructured[pdf], unstructured[docx].
- Custom gemini dựa trên gemini model và framework llm langchain. Model tạo các retriever từ text và text_summaries và lưu trữ trên chromadb.
- Dựng api generate response bằng flask. Khi cung cấp prompt, api sẽ generate response và trả về ở định dạng json. Nội dung của response sẽ ở dạng md.

## Infra
