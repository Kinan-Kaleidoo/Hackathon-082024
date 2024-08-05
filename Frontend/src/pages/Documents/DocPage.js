import React, { useState } from 'react';
import DocumentGallery from './DocGallery';
import { Container, Typography, Paper, Button, TextField } from '@mui/material';
import SearchComponent from '../../components/SearchComponent';
import axios from 'axios';

import './DocPage.css';

const DocPage = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file to upload');
      return;
    }

    const formData = new FormData();
    console.log(file)
    formData.append('file', file);

    try {
      await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('File uploaded successfully');
      // Optionally, you can refresh or update the DocumentGallery component here
    } catch (error) {
      alert('Error uploading file');
    }
  };

  return (
    <Container className="document-page">
      <Paper className="paper">
        <Typography variant="h4" gutterBottom>
          Document Gallery
        </Typography>
        <DocumentGallery />
      </Paper>
      <SearchComponent />

      <Paper className="upload-paper">
        <Typography variant="h6" gutterBottom>
          Upload PDF
        </Typography>
        <TextField
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          variant="outlined"
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
        >
          Upload
        </Button>
      </Paper>
    </Container>
  );
};

export default DocPage;
