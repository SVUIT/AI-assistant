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

- Idea: Building a chatbot using the Gemini base model and the LangChain LLM framework.  
- Language: python
-  Training data: content from courses of University of Information Technology, Viet Nam National University , Ho Chi Minh City. 
- Steps:
	+  Using DirectoryLoader of langchain_community to load data 
		+ LangChain's DirectoryLoader provides functionality for reading various file types from disk into LangChain Document objects. In this project, the data includes three types: pdf, docx, md.
	+ Split documents into chunks using RecursiveCharacterTextSplitter.
	+ Using model embedding-001 to embed the contents of each document  and insert these embeddings into the Chroma vector store.
	+ Creating a vector retriever from a vectorstore.
	+ Create a retriever from vector retriever and chat history.
	+ Build the prompt for the question and answer.
	+ Create a chain using the retriever, prompt, and the gemini-1.5-flash model.
	+ Build an API with Flask to generate answers.

## Infra
