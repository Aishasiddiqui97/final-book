import React, { useState, useEffect, useRef } from 'react';
import './RagChatbot.css';

const RagChatbot = ({ textbookContentPath = '/docs', apiBaseUrl = 'http://localhost:8000' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedMode, setSelectedMode] = useState('full_book'); // 'full_book' or 'selected_text'
  const [selectedText, setSelectedText] = useState('');
  const [isSelectingText, setIsSelectingText] = useState(false);
  const messagesEndRef = useRef(null);
  const chatInputRef = useRef(null);

  // Function to handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
        if (isSelectingText) {
          setIsSelectingText(false);
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, [isSelectingText]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && chatInputRef.current) {
      setTimeout(() => {
        chatInputRef.current.focus();
      }, 100);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request payload
      const requestBody = {
        query: inputValue,
        mode: selectedMode,
      };

      // Include selected text if in selected_text mode
      if (selectedMode === 'selected_text' && selectedText) {
        requestBody.selected_text = selectedText;
      }

      // Call the backend API
      const response = await fetch(`${apiBaseUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        citations: data.citations || [],
        sources: data.sources || [],
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleTextSelectionMode = () => {
    setIsSelectingText(!isSelectingText);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="rag-chatbot">
      {/* Floating button to open chat */}
      {!isOpen && (
        <button className="chat-toggle-button" onClick={toggleChat}>
          <span>📚 Ask Textbook</span>
        </button>
      )}

      {/* Chat window */}
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <div className="chat-title">Textbook Assistant</div>
            <div className="chat-controls">
              <button className="clear-chat-btn" onClick={clearChat} title="Clear chat">
                🗑️
              </button>
              <button className="close-chat-btn" onClick={toggleChat} title="Close">
                ×
              </button>
            </div>
          </div>

          <div className="chat-mode-selector">
            <label>
              <input
                type="radio"
                value="full_book"
                checked={selectedMode === 'full_book'}
                onChange={(e) => setSelectedMode(e.target.value)}
              />
              Full Book
            </label>
            <label>
              <input
                type="radio"
                value="selected_text"
                checked={selectedMode === 'selected_text'}
                onChange={(e) => setSelectedMode(e.target.value)}
              />
              Selected Text
            </label>

            {selectedMode === 'selected_text' && (
              <button
                className={`select-text-btn ${isSelectingText ? 'active' : ''}`}
                onClick={toggleTextSelectionMode}
              >
                {isSelectingText ? '✓ Text Selected' : 'Select Text on Page'}
              </button>
            )}
          </div>

          {selectedMode === 'selected_text' && selectedText && (
            <div className="selected-text-preview">
              <strong>Selected Text:</strong>
              <p>"{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</p>
            </div>
          )}

          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your textbook assistant.</p>
                <p>Ask me anything about the Physical AI & Humanoid Robotics textbook.</p>
                <p>You can ask in <strong>Full Book</strong> mode or <strong>Selected Text</strong> mode.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender}-message`}
                >
                  <div className="message-content">
                    {message.text}
                  </div>
                  {message.citations && message.citations.length > 0 && (
                    <div className="citations">
                      <strong>Citations:</strong>
                      {message.citations.map((citation, idx) => (
                        <span key={idx} className="citation">
                          [{citation.chapter} &gt; {citation.section}]
                        </span>
                      ))}
                    </div>
                  )}
                  <div className="message-timestamp">
                    {message.timestamp}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-content typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-area">
            <textarea
              ref={chatInputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={
                selectedMode === 'selected_text' && !selectedText
                  ? 'Please select text on the page first...'
                  : 'Ask a question about the textbook...'
              }
              disabled={selectedMode === 'selected_text' && !selectedText}
              rows="3"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading || (selectedMode === 'selected_text' && !selectedText)}
              className="send-button"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RagChatbot;