import React, { useState } from 'react';
import { Button, Input } from '@mui/material';
import './AudioUpload.css';

const AudioUpload = ({ onAudioUpload }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type.startsWith('audio/')) {
      setFile(selectedFile);
    } else {
      alert('Please select a valid audio file');
    }
  };

  const handleUpload = () => {
    if (file) {
      onAudioUpload(file);
      setFile(null);
    }
  };

  return (
    <div className="audio-upload">
      <Input
        type="file"
        accept="audio/*"
        onChange={handleFileChange}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={!file}
      >
        Upload Audio
      </Button>
    </div>
  );
};

export default AudioUpload;
