import React from 'react';
import Typography from '@mui/material/Typography';
import './Footer.css';

const Footer = (props) => {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      Kaleidoo <b />
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
};

export default Footer;
