import React from 'react';
import { Button, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="home-page">
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
    </div>
  );
};

export default HomePage;
