import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, IconButton } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import MenuIcon from '@mui/icons-material/Menu';
import './Header.css'; // Ensure this path is correct

const Header = ({ onMenuClick }) => {
  return (
    <AppBar position="static" className="header">
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="menu" onClick={onMenuClick}>
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" className="title">
          <Link to="/" className="MuiLink-root">
            Home
          </Link>
        </Typography>
        <IconButton color="inherit" component={Link} to="/" className="MuiIconButton-root">
          <HomeIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
