// import React, { useState } from 'react';
// import axios from 'axios';
// import './App.css';

// function App() {
//   const [input, setInput] = useState('');
//   const [chat, setChat] = useState([]);

//   const handleSend = async () => {
//     if (!input.trim()) return;

//     setChat([...chat, { sender: 'user', message: input }]);

//     try {
//       const response = await axios.post('http://localhost:8000/chat', { message: input });
//       setChat([...chat, 
//         { sender: 'user', message: input }, 
//         { sender: 'bot', message: response.data.reply }
//       ]);
//     } catch (err) {
//       setChat([...chat, { sender: 'bot', message: "Error talking to Gemini." }]);
//     }

//     setInput('');
//   };

//   return (
//     <div className="chat-container">
//       <div className="chat-box">
//         {chat.map((msg, index) => (
//           <div key={index} className={`message ${msg.sender}`}>
//             <span>{msg.message}</span>
//           </div>
//         ))}
//       </div>
//       <div className="input-box">
//         <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} />
//         <button onClick={handleSend}>Send</button>
//       </div>
//     </div>
//   );
// }

// export default App;
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [chat, setChat] = useState([]);
  const chatBoxRef = useRef(null);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', message: input };
    setChat(prev => [...prev, userMessage]);

    try {
      const response = await axios.post('http://localhost:8000/chat', { message: input });
      const botMessage = {
        sender: 'bot',
        message: response.data.reply,
      };
      setChat(prev => [...prev, botMessage]);
    } catch (err) {
      setChat(prev => [
        ...prev,
        { sender: 'bot', message: 'Error talking to Gemini.' },
      ]);
    }

    setInput('');
  };

  // 🔽 Scroll to bottom when chat updates
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [chat]);

  return (
    <div className="chat-container">
      <h1 id="abc">GEMNI  CHATBOT</h1>
      <div className="chat-box" ref={chatBoxRef}>
        {chat.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.sender === 'bot' ? (
              <span dangerouslySetInnerHTML={{ __html: msg.message }} />
            ) : (
              <span>{msg.message}</span>
            )}
          </div>
        ))}
      </div>
      <div className="input-box">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask me anything..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default App;

