import React from 'react';
import MediaItem from './MediaItem';

const mediaItems = [
  { id: 1, src: 'path/to/image1.jpg', type: 'image' },
  { id: 2, src: 'path/to/video1.mp4', type: 'video' },
  // Add more media items here
];

const MediaGallery = () => {
  return (
    <div className="media-gallery">
      {mediaItems.map(item => (
        <MediaItem key={item.id} media={item} />
      ))}
    </div>
  );
};

export default MediaGallery;
