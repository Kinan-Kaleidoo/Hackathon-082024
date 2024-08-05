import React from 'react';
import MediaGallery from './MediaGallery';
import { Container, Typography, Paper } from '@mui/material';
import './MediaPage.css';

const MediaPage = () => {
  return (
    <Container className="media-page">
      <Paper className="paper">
        <Typography variant="h4" gutterBottom>
          Media Gallery
        </Typography>
        <MediaGallery />
      </Paper>
    </Container>
  );
};

export default MediaPage;
