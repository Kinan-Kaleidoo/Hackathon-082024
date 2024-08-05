import React from 'react';
import { useNavigate } from 'react-router-dom';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';


const itemData = [
  {
    img: 'https://images.unsplash.com/photo-1551963831-b3b1ca40c98e',  
    title: 'Image 1',
    type: 'image',
  },
  {
    img: 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d',
    title: 'Image 2',
    type: 'image',
  },
  {
    img: 'https://images.unsplash.com/photo-1522770179533-24471fcdba45',
    title: 'Image 3',
    type: 'image',
  },
  {
    video: 'https://www.w3schools.com/html/mov_bbb.mp4',
    title: 'Video 1',
    type: 'video',
  },
  // Add more items here
];


const MediaGallery = () => {
  const navigate = useNavigate();

  const handleClick = (item) => {
    navigate(`/media/${encodeURIComponent(item.title)}`, { state: { item } });
  };

  return (
    <ImageList sx={{ width: 500, height: 450 }} cols={3} rowHeight={164}>
      {itemData.map((item) => (
        <ImageListItem key={item.img || item.video} onClick={() => handleClick(item)}>
          {item.type === 'image' ? (
            <img
              srcSet={`${item.img}?w=164&h=164&fit=crop&auto=format&dpr=2 2x`}
              src={`${item.img}?w=164&h=164&fit=crop&auto=format`}
              alt={item.title}
              loading="lazy"
            />
          ) : (
            <video
              src={item.video}
              alt={item.title}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              controls
            />
          )}
        </ImageListItem>
      ))}
    </ImageList>
  );
};

export default MediaGallery;
