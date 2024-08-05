import React from 'react';

const MediaItem = ({ media }) => {
  return (
    <div className="media-item">
      {media.type === 'image' ? (
        <img src={media.src} alt={`media-${media.id}`} />
      ) : (
        <video src={media.src} controls />
      )}
    </div>
  );
};

export default MediaItem;