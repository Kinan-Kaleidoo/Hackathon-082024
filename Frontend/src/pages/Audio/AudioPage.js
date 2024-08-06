import React, { useState } from 'react';
import AudioUpload from './AudioUpload';
import AudioPlayer from './AudioPlayer';
import Search from '../../components/SearchComponent';

import './AudioPage.css';

const AudioPage = () => {
  const [audioSrc, setAudioSrc] = useState(null);

  const handleAudioUpload = (file) => {
    const audioUrl = URL.createObjectURL(file);
    setAudioSrc(audioUrl);
  };

  return (
    <div className="audio-page">
      <h1>Audio Page</h1>
      <AudioUpload onAudioUpload={handleAudioUpload} />
      {audioSrc && <AudioPlayer src={audioSrc} />}
      <Search />
    </div>
  );
};

export default AudioPage;
