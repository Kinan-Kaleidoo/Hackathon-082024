// src/pages/Chat/ChatPage.js
import React, { useState } from 'react';
import './ChatPage.css';
import SearchComponent from '../../components/SearchComponent';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I help you today?' },
    { id: 2, text: 'I need assistance with my account.' },
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { id: messages.length + 1, text: input }]);
      setInput('');
    }
  };

  return (
    <div className="chat-page">
      <SearchComponent />
      <div className="chat-container">
        <div className="chat-header">
          <h1>Chat</h1>
        </div>
        <div className="chat-messages">
          {messages.map((msg) => (
            <div key={msg.id} className="message">
              <p>{msg.text}</p>
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message"
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
