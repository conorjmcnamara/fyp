import React from 'react';
import './App.css';
import { fetchMessage } from './services/messageService';

const App: React.FC = () => {
  const handleClick = async () => {
    try {
      const data = await fetchMessage();
      alert(data.message);
    } catch (error) {
      console.error('Error fetching message:', error);
    }
  };
  
  return (
    <div className="App">
      <h1>Hello</h1>
      <button onClick={handleClick}>Get message</button>
    </div>
  );
};

export default App;
