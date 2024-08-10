document.addEventListener("DOMContentLoaded", function () {

  var socket = io('http://34.1.143.90:8888/');

    socket.on('connect', function() {
        console.log('Connected to Flask server');
    });

    let latestServerResponse = null;


    socket.on('server_response', function(data) {
    latestServerResponse = data.message;
    hideLoader();
    displayAIMessage(data.message);
  });

    // Create chat icon
  const chatIcon = document.createElement('div');
  chatIcon.id = 'chat-icon';
  chatIcon.style = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 75px;
    height: 78px;
    border-radius: 4px;
    background-color: #523AF0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #fff;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 5px 0; 
    `;

  const iconImage = document.createElement('img');
  iconImage.src = '/assets/images/chatbot.png';
  iconImage.alt = 'AI chat icon';
  iconImage.style = `
    width: 53px; 
    height: 55px; 
    `;

  const iconText = document.createElement('span');
  iconText.innerText = 'Ask AI';
  iconText.style = `
    font-family: Arial, sans-serif;
    font-size: 16px;
    font-weight: bold;
    color: #fff;
    line-height: 1;
    margin-top: -3px; 
  `;

  chatIcon.appendChild(iconImage);
  chatIcon.appendChild(iconText);
  document.body.appendChild(chatIcon);
  
  // Create overlay
  const overlay = document.createElement('div');
  overlay.id = 'overlay';
  overlay.style = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: none;
    z-index: 999;
    `;
  document.body.appendChild(overlay);
  
    // Create chatbox
  const chatbox = document.createElement('div');
  chatbox.id = 'chatbox';
  chatbox.style = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 700px;
    height: 300px;
    max-height: 80vh;
    background-color: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    display: none;
    flex-direction: column;
    border-radius: 5px;
    z-index: 1000;
    overflow: hidden;
    `;
  document.body.appendChild(chatbox);
  
    // Create chatbox header
  const chatHeader = document.createElement('div');
  chatHeader.style = `
    padding: 13px;
    background-color:#523AF0;
    color: #fff;
    text-align: center;
    display: flex;
    align-items: center;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    `;
  
  const headerText = document.createElement('span');
  headerText.innerText = 'SVUIT - MMTT AI CHAT';
  headerText.style = `
    font-family: Arial, sans-serif;
    font-weight: bold;
    font-size: 25px;
    margin-left: 10px;
    `;
  
  const closeButton = document.createElement('button');
  closeButton.innerText = '×';
  closeButton.style = `
    margin-left: auto;
    background-color: transparent;
    border: none;
    border-radius: 5px;
    color: #fff;
    font-size: 25px;
    cursor: pointer;
    display: flex;
    `;
  
  closeButton.addEventListener('click', function () {
    chatbox.style.display = 'none';
    overlay.style.display = 'none';
    resetChatboxHeight();
  });
  
  overlay.addEventListener('click', function () {
    chatbox.style.display = 'none';
    overlay.style.display = 'none';
    resetChatboxHeight();
  });
  
  chatHeader.appendChild(headerText);
  chatHeader.appendChild(closeButton);
  chatbox.appendChild(chatHeader);
  
  // Create chat messages container
  const chatMessages = document.createElement('div');
  chatMessages.style = `
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    z-index: 1000;
    `;
  chatbox.appendChild(chatMessages);
  
  // Add a note to the chatbox
  const note = document.createElement('div');
  note.innerText = 'This is a custom LLM for answering questions about SVUIT - MMTT. Answers are based on the contents of the documentation.';
  note.style = `
    background-color: #FFFFCC;
    color: #000;
    border-radius: 5px;
    padding: 10px;
    font-family: Arial, sans-serif;
    font-size: 14px;
    margin-bottom: 10px;
    width: 100%; 
    text-align: left;
    display: block;
    z-index: 1000;
    `;
  chatMessages.appendChild(note);
  
  // Create chat input wrapper
  const chatInputWrapper = document.createElement('div');
  chatInputWrapper.style = `
    display: flex;
    align-items: center;
    padding: 5px;
    border: 1px solid #523AF0;
    border-radius: 15px;
    margin: 10px;
    z-index: 1000;
    `;
  chatbox.appendChild(chatInputWrapper);
  
  // Create chat input
  const chatInput = document.createElement('textarea');
  chatInput.style = `
    flex: 1;
    padding: 10px;
    height: 20px; /* Allow height to adjust based on content */
    background-color: #fff;
    color: #000;
    border: none;
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    outline: none;
    resize: none;
    overflow: hidden;
    line-height: 16px;
    max-height: 100px; /* Adjust to fit within container */
    box-sizing: border-box;
    z-index: 1000;
    `;
  chatInputWrapper.appendChild(chatInput);
  chatInput.placeholder = 'Ask me a question';
  
  // Create chat button
  const chatButton = document.createElement('button');
  chatButton.innerText = '➙';
  chatButton.style = `
    width: 32px;
    height: 32px;
    background-color: #523AF0;
    color: #fff;
    border: none;
    cursor: pointer;
    border-radius: 8px;
    font-size: 20px;
    margin: 5px;
    `;
  chatInputWrapper.appendChild(chatButton);
  
  chatButton.addEventListener('click', sendMessage);

  chatInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });
  
  chatIcon.addEventListener('click', function () {
    chatbox.style.display = chatbox.style.display === 'none' ? 'flex' : 'none';
    overlay.style.display = chatbox.style.display === 'none' ? 'none' : 'block';
    if (chatbox.style.display === 'flex') {
      resetChatboxHeight();
      setTimeout(() => chatInput.focus(), 0); 
    }
  });

  // Function to show loader
  function showLoader() {
    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.style = `
      display: inline-block;
      text-align: left;
      z-index: 1000;
      display: flex;
      align-items: center;
      margin-bottom: -20px;
      z-index: 1000;
      `;
  
    const loaderImg = document.createElement('img');
    loaderImg.src = '/assets/images/loader.gif';
    loaderImg.style = `
      width: 55px;
      height: 57px;
      `;
  
    loader.appendChild(loaderImg);
    chatMessages.appendChild(loader);
      
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Function to hide loader
  function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
      loader.remove();
    }
  }

  //Function to hide old refresh button
  function hidePreviousRefreshButtons() {
    const allRefreshButtons = chatMessages.querySelectorAll('button i.fa-refresh');
    allRefreshButtons.forEach(button => {
        button.parentElement.style.display = 'none'; // Hide button
        button.parentElement.style.pointerEvents = 'none'; // Prevent interaction
    });
  }
  

  //Function to activate button
  function activateButton(button) {
    const originalBackgroundColor = button.style.backgroundColor;
    const originalColor = button.style.color;
  
    button.style.backgroundColor = '#d3d3d3'; 
    button.style.color = '#000';
  
    setTimeout(() => {
      button.style.backgroundColor = originalBackgroundColor;
      button.style.color = originalColor;
    }, 200);
  }

  // Function to send message
  function sendMessage() {
    const userMessage = chatInput.value;
    if (userMessage.trim()) {
      // Display user's message
      const userMessageElem = document.createElement('div');
      userMessageElem.style = `
        display: inline-block;
        max-width: 90%;
        margin-bottom: 10px;
        padding: 10px;
        color: #fff;
        font-weight: bold;
        background-color: #6B68EE;
        border-radius: 20px;
        word-break: break-word;
        font-size: 14px;
        text-align: left;
        align-self: flex-end;
        z-index: 1000;  
        `;
      userMessageElem.innerText = userMessage;
      chatMessages.appendChild(userMessageElem);
      chatInput.value = '';
  
      chatInput.style.height = '20px';
      adjustChatboxHeight();
      showLoader();
      hidePreviousRefreshButtons();

      // Send message to server
      socket.emit('client_event', { data: userMessage });
    }
  }
    
  //Display AI message
  function displayAIMessage(message) {
    const aiMessageElem = document.createElement('div');
    aiMessageElem.style = `
      display: inline-block;
      max-width: 90%;
      padding: 5px 10px;
      color: #000;
      background-color: #D3D3D3;
      border-radius: 20px;
      font-size: 14px;
      text-align: left;
      word-break: break-word;
      z-index: 1000;
      align-self: flex-start;
      box-sizing: border-box;
      `;
    aiMessageElem.innerHTML = marked.parse(message); 

    const codeBlocks = aiMessageElem.querySelectorAll('code');
    codeBlocks.forEach(block => {
        block.style = `
            display: inline-flex;
            background-color: #222; 
            color: #fff; 
            padding: 5px;
            border-radius: 5px;
            font-family: Consolas, "Courier New", monospace;
            font-size: 13px;
            z-index: 1000;
        `;
    });
    
    chatMessages.appendChild(aiMessageElem);
    
    // Create container for copy and refresh button
    const buttonContainer = document.createElement('div');
    buttonContainer.style = `
      display: flex;
      gap: 1px;
      margin-top: 0px;
      margin-left: 10px;
      z-index: 1000;
      `;
    
    //Create copy button
    const copyButton = document.createElement('button');
    copyButton.innerHTML = '<i class="fa fa-copy"></i>';
    copyButton.style = `
      background-color: #e8e8e8;
      color: #696969;
      border: none;
      cursor: pointer;
      padding: 5px 10px;
      border-radius: 5px;
      margin-top: 5px;
      font-size: 12px;
      font-family: Arial, sans-serif;
      margin-left: 5px;
      `;
    
      copyButton.addEventListener('click', function () {
        activateButton(copyButton);
        const messageToCopy = aiMessageElem.innerText.trim();
      
        const textArea = document.createElement('textarea');
        textArea.value = messageToCopy;
        textArea.style.position = 'fixed';  
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
      
        textArea.select();
      
        try {
            document.execCommand('copy');
        } catch (error) {
            alert('An error occurred while copying. Try again.');
        }
    
        document.body.removeChild(textArea);
      });
      
    
    // Create refresh button
    const refreshButton = document.createElement('button');
    refreshButton.innerHTML = '<i class="fa fa-refresh"></i>';
    refreshButton.style = `
      background-color: #e8e8e8;
      color: #696969;
      border: none;
      cursor: pointer;
      padding: 5px 10px;
      border-radius: 5px;
      margin-top: 5px;
      font-size: 12px;
      font-family: Arial, sans-serif;
      margin-left: 5px;
      `;
    
    refreshButton.addEventListener('click', function () {
      activateButton(refreshButton);
      showLoader();
      socket.emit('repeat');
    });
    
    buttonContainer.appendChild(copyButton);
    buttonContainer.appendChild(refreshButton);
    chatMessages.appendChild(buttonContainer);

   // Thêm separator visibility: hidden;
   const separator = document.createElement('hr');
   separator.style =`
    border: none;
    border-top: 1px solid #333; 
    margin-top: 10px;
    margin-bottom: 0px;
    width: 100%;
    visibility: hidden;
    `;
   chatMessages.appendChild(separator);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;

    hidePreviousRefreshButtons();

    // Display the refresh button for the current message
    refreshButton.style.display = 'inline-block';
    refreshButton.style.pointerEvents = 'auto';
    
    adjustChatboxHeight();
  }
    
  // Custom scrollbar chatbox styling
  const style = document.createElement('style');
  style.innerHTML = `
    #chatbox ::-webkit-scrollbar {
      width: 12px;
    }
    #chatbox ::-webkit-scrollbar-track {
      background: #f1f1f1;
    }
    #chatbox ::-webkit-scrollbar-thumb {
      background: #888;
      border-radius: 10px;
    }
    #chatbox ::-webkit-scrollbar-thumb:hover {
      background: #555;
    }
    #chatbox {
      scrollbar-width: thin;
      scrollbar-color: #888 #f1f1f1;
    }
    `;
  document.head.appendChild(style);
    
  //auto resize
  function adjustChatboxHeight() {
    chatInput.style.height = '20px'; 
    chatInput.style.height = chatInput.scrollHeight + 'px';
  
    const chatContentHeight = chatMessages.scrollHeight;
    const chatInputHeight = chatInput.scrollHeight;
    const chatInputWrapperHeight = chatInputWrapper.offsetHeight;
    const chatHeaderHeight = chatHeader.offsetHeight;
    const minChatboxHeight = 300; 
    const maxChatboxHeight = window.innerHeight * 0.8; 
  
    const newChatboxHeight = Math.min(
      Math.max(minChatboxHeight, chatContentHeight + chatInputWrapperHeight + chatHeaderHeight),
      maxChatboxHeight
    );
  
    chatbox.style.height = newChatboxHeight + 'px';
    chatMessages.style.maxHeight = (newChatboxHeight - chatInputWrapperHeight - chatHeaderHeight) + 'px';
  }

  //Reset size
  function resetChatboxHeight() {
    if (chatMessages.children.length === 1) { // Only the note exists
      chatbox.style.height = '300px'; 
      chatMessages.style.maxHeight = '200px'; 
    }
    chatInput.style.height = '20px';
  }
  
  chatInput.addEventListener('input', function () {
    if (chatInput.value.trim() === '') {
      resetChatboxHeight();
    } else {
      adjustChatboxHeight();
    }
  });

  chatInput.addEventListener('focus', function () {
    adjustChatboxHeight();
  });
});

  


