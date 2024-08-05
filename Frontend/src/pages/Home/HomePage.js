import React, { useState } from 'react';
import { Button, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../../components/Common/Sidebar';
import Header from '../../components/Common/Header';
import Footer from '../../components/Common/Footer';
// import './HomePage.css'; // Ensure this CSS file exists and contains styling

const HomePage = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  const toggleSidebar = () => {
    setSidebarOpen(prev => !prev);
  };

  return (
    <div className="home-page">
      <Sidebar open={sidebarOpen} onClose={toggleSidebar} />
      <div className={`main-content ${sidebarOpen ? 'shrink' : ''}`}>
        <Header onMenuClick={toggleSidebar} />
        <main>
          <h1>Welcome to the Chat App</h1>
          <Grid container spacing={3} justifyContent="center" alignItems="center">
            <Grid item xs={12} sm={6} md={3}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={() => handleNavigate('/chat')}
              >
                Chat
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                variant="contained"
                color="secondary"
                fullWidth
                onClick={() => handleNavigate('/media')}
              >
                Media
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                variant="contained"
                color="success"
                fullWidth
                onClick={() => handleNavigate('/doc')}
              >
                Documents
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                variant="contained"
                color="error"
                fullWidth
                onClick={() => handleNavigate('/audio')}
              >
                Audio
              </Button>
            </Grid>
          </Grid>
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default HomePage;
