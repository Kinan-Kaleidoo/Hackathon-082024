import React from 'react';
import DocumentGallery from './DocGallery';
import { Container, Typography, Paper } from '@mui/material';
import './DocPage.css';

const DocPage = () => {
  return (
    <Container className="document-page">
      <Paper className="paper">
        <Typography variant="h4" gutterBottom>
          Document Gallery
        </Typography>
        <DocumentGallery />
      </Paper>
    </Container>
  );
};

export default DocPage;
