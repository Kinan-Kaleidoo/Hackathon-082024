import React, { useState } from 'react';
import DocumentGallery from './DocGallery';
import { Container, Typography, Paper, Button, Input } from '@mui/material';
import './DocPage.css';

const DocPage = () => {
  const [documents, setDocuments] = useState([
    { id: 1, file_name: 'Document 1', content: 'This is the first document' },
    { id: 2, file_name: 'Document 2', content: 'This is the second document' },
    // Add more demo documents if needed
  ]);
  const [fileName, setFileName] = useState('');

  const handleFileChange = (event) => {
    setFileName(event.target.files[0]?.name || '');
  };

  const handleUpload = () => {
    if (fileName) {
      const newDocument = {
        id: documents.length + 1,
        file_name: fileName,
        content: 'This is a newly uploaded document' // Replace with actual content if needed
      };
      setDocuments([...documents, newDocument]);
      setFileName('');
    }
  };

  return (
    <Container className="document-page">
      <Paper className="paper">
        <Typography variant="h4" gutterBottom>
          Document Gallery
        </Typography>
        <div className="upload-section">
          <Input type="file" onChange={handleFileChange} />
          <Button variant="contained" color="primary" onClick={handleUpload}>
            Upload Document
          </Button>
        </div>
        <DocumentGallery documents={documents} />
      </Paper>
    </Container>
  );
};

export default DocPage;