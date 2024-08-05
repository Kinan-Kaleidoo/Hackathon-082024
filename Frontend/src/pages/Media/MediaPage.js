import React, { useState, useEffect } from 'react';
import { Container, Typography, Paper, Button, Box, Input } from '@mui/material';
import axios from 'axios';
import MediaGallery from './MediaGallery';
import { Container, Typography, Paper } from '@mui/material';
import SearchComponent from '../../components/SearchComponent';

import './MediaPage.css';

const MediaPage = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  
  // Cleanup URLs on component unmount
  useEffect(() => {
    return () => {
      selectedFiles.forEach((file) => {
        URL.revokeObjectURL(URL.createObjectURL(file));
      });
    };
  }, [selectedFiles]);

  // Handle file selection
  const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(files);
  };

  // Handle file upload
  const handleFileUpload = async () => {
    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      };
      await axios.post('http://localhost:4000/addCards', formData, config);
      alert("Files uploaded successfully");
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  // Render file previews
  const renderPreview = () => {
    return selectedFiles.map((file, index) => {
      const fileURL = URL.createObjectURL(file);

      return (
        <Box key={index} sx={{ margin: '10px', display: 'inline-block' }}>
          {file.type.startsWith('image/') ? (
            <img
              src={fileURL}
              alt={`preview-${index}`}
              style={{ width: '100px', height: '100px' }}
            />
          ) : file.type.startsWith('audio/') ? (
            <audio controls style={{ display: 'block', margin: '10px' }}>
              <source src={fileURL} />
              Your browser does not support the audio element.
            </audio>
          ) : (
            <Typography variant="body2" color="textSecondary">
              Unsupported file type
            </Typography>
          )}
        </Box>
      );
    });
  };

  return (
    <Container className="media-page">
      <Box sx={{ padding: 2 }}>
        <Typography variant="h6" gutterBottom>
          Upload Files
        </Typography>
        <Input
          type="file"
          multiple
          onChange={handleFileChange}
          sx={{ mb: 2 }}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleFileUpload}
        >
          Upload
        </Button>
        <Box sx={{ mt: 2 }}>
          {renderPreview()}
        </Box>
      </Box>

      <Paper className="paper">
        <Typography variant="h4" gutterBottom>
          Media Gallery
        </Typography>
        <MediaGallery />
      </Paper>
      <SearchComponent />

    </Container>
  );
};

export default MediaPage;
