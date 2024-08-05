import React from 'react';
import { IconButton, Toolbar, AppBar, Typography } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import './Header.css';

const Header = ({ onMenuClick }) => {
  return (
    <AppBar position="static" className="header">
      <Toolbar className="toolbar">
        <IconButton edge="start" color="inherit" aria-label="menu" onClick={onMenuClick}>
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" className="title">
          Chat Application
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
