import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { Link } from 'react-router-dom'; // Import Link
import ChatIcon from '@mui/icons-material/Chat';
import PhotoLibraryIcon from '@mui/icons-material/PhotoLibrary';
import DescriptionIcon from '@mui/icons-material/Description';
import { Home, Media, Description, Audiotrack } from '@mui/icons-material'; // Add the Audiotrack icon
import './Sidebar.css';

const Sidebar = ({ open, onClose }) => {
  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      onClose={onClose}
      className="sidebar"
      sx={{ '& .MuiDrawer-paper': { width: 240, boxSizing: 'border-box' } }}
    >
      <List className="list">
        <ListItem button component={Link} to="/chat" onClick={onClose}>
          <ListItemIcon><ChatIcon /></ListItemIcon>
          <ListItemText primary="Chat" />
        </ListItem>
        <ListItem button component={Link} to="/media" onClick={onClose}>
          <ListItemIcon><PhotoLibraryIcon /></ListItemIcon>
          <ListItemText primary="Media" />
        </ListItem>
        <ListItem button component={Link} to="/documents" onClick={onClose}>
          <ListItemIcon><DescriptionIcon /></ListItemIcon>
          <ListItemText primary="Documents" />
        </ListItem>
        <ListItem button component={Link} to="/audio">
          <ListItemIcon><Audiotrack /></ListItemIcon>
          <ListItemText primary="Audio" />
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Sidebar;
