# AI assistant for SVUIT-MMTT

## Front end

### 1. Initialize Widget

- Event: User visits website svuit.org/mmtt/.
- Action:
    + Widget appears in a fixed position in the lower right corner.
    + Display a chat icon and the text Ask AI.

### 2. User Initiates Conversation

- Event: User clicks on widget.
- Action:
    + displays the chat frame and notes about the chatbot's effects.
    + Content outside the chat frame is blurred.
      
### 3. User Enters Message

- Event: User enters text into the chat box.
- Action:
  + User's message is sent (Displayed on the right side of the chat frame).
  + Bot processes messages and responds appropriately (Displayed on the left side of the chat frame).

### 4. Reply Bot

- Event: The bot has finished processing the user's message.
- Action:
  + Bot sends reply messages, which can include:
    + Text: Direct answers to user questions.
    + Markdown: Display information as Markdown file.
    + Button:
    	+ Copy: let users copy the answer from the bot.
    	+ Refresh: so that the user wants the bot to answer the previously asked question again.
    
### 5. Other Interactions

- Users review chat history: Allows users to review previous conversations by scrolling up.

### 6. End the Conversation

- Event: User closes the tab.
- Action:
  + Widget shrinks back to its original state and deletes all previous chat content.

## Back end

- Language: python
- Dependencies: langchain, langchain_google_vertexai, langchain_community, unstructured, unstructured[pdf], unstructured[docx].
- Custom gemini dựa trên gemini model và framework llm langchain. Model tạo các retriever từ text và text_summaries và lưu trữ trên chromadb.
- Dựng api generate response bằng flask. Khi cung cấp prompt, api sẽ generate response và trả về ở định dạng json. Nội dung của response sẽ ở dạng md.

## Infra
