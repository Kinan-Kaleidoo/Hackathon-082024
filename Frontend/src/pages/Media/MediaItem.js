import React from 'react';
import { useLocation } from 'react-router-dom';

const MediaItem = () => {
  const location = useLocation();
  const { item } = location.state;

  return (
    <div className="media-item">
      <h1>{item.title}</h1>
      <img src={item.img} alt={item.title} style={{ width: '100%' }} />
    </div>
  );
};

export default MediaItem;
