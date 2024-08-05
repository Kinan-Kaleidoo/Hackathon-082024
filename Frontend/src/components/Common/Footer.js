import React from 'react';
import { useLocation } from 'react-router-dom';
import { TextField, Button } from '@mui/material';
import './Footer.css'; // Ensure you have styles for the footer and search bar


const Footer = () => {
  const location = useLocation();
  const shouldShowSearch = ['/media', '/doc', '/audio'].includes(location.pathname);

  return (
    <footer className="footer">
      <p>© 2024 Multi-Modal Chat App</p>
      {shouldShowSearch && (
        <div className="footer-search">
          <TextField
            variant="outlined"
            placeholder="Search..."
            size="small"
            style={{ marginRight: '8px' }}
          />
          <Button variant="contained" color="primary">Search</Button>
        </div>
      )}
    </footer>
  );
};

export default Footer;


