import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatPage from '../Chat/ChatPage';
import MediaPage from '../Media/MediaPage';
import DocumentPage from '../Documents/DocPage';
import Header from '../../components/Common/Header';
import Footer from '../../components/Common/Footer';
import Sidebar from '../../components/Common/Sidebar';
import AudioPage from '../Audio/AudioPage'; // Import the AudioPage
import SignIn from '../Auto/signIn'
import SignUp from '../Auto/signUp';

// import './HomePage.css';

const HomePage = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(prev => !prev);
  };

  return (
    <Router>
      <div style={{ display: 'flex' }}>
        <Sidebar open={sidebarOpen} onClose={toggleSidebar} />
        <div style={{ flexGrow: 1 }}>
          <Header onMenuClick={toggleSidebar} />
          <main>
            <Routes>
              <Route path="/signIn" element={<SignIn/>}/> 
              <Route path="/signUp" element={<SignUp/>}/> 
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/media" element={<MediaPage />} />
              <Route path="/documents" element={<DocumentPage />} />
              <Route path="/audio" element={<AudioPage />} /> {/* Add route here */}
              <Route path="/" element={<ChatPage />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </div>
    </Router>
  );
};

export default HomePage;
