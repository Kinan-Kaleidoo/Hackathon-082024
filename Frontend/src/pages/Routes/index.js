import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatPage from '../Chat/ChatPage';
import MediaPage from '../Media/MediaPage';
import MediaItem from '../Media/MediaItem';
import DocPage from '../Documents/DocPage';
import Header from '../../components/Common/Header';
import Footer from '../../components/Common/Footer';
import Sidebar from '../../components/Common/Sidebar';
// import HomePage from '../Home/HomePage'; // Import the HomePage
import AudioPage from '../Audio/AudioPage'; // Import the AudioPage
import SignIn from '../Auto/signIn';
import SignUp from '../Auto/signUp';

// Rename this component to avoid conflict
const App = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(prev => !prev);
  };

  return (
    <Router>
      <div className="app-container">
        <Sidebar open={sidebarOpen} onClose={toggleSidebar} />
        <div className={`main-content ${sidebarOpen ? '' : 'shrink'}`}>
          <Header onMenuClick={toggleSidebar} />
          <main>
            <Routes>
              {/* <Route path="/" element={<HomePage />} />  */}
              <Route path="/signIn" element={<SignIn />} />
              <Route path="/signUp" element={<SignUp />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/media" element={<MediaPage />} />
              <Route path="/media/:title" element={<MediaItem />} />
              <Route path="/" element={<ChatPage />} />
              <Route path="/doc" element={<DocPage />} />
              <Route path="/audio" element={<AudioPage />} />
            </Routes>
          </main>
          <Footer sx={{ mt: 8, mb: 4 }}/>
        </div>
      </div>
    </Router>
  );
};

export default App;


