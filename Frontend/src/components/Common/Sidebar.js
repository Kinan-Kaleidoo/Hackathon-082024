import React from 'react';
import { Link } from 'react-router-dom';
import { List, ListItem, ListItemText } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import ChatIcon from '@mui/icons-material/Chat';
import MediaIcon from '@mui/icons-material/PhotoLibrary';
import DocumentIcon from '@mui/icons-material/Description';
import AudioIcon from '@mui/icons-material/Audiotrack';
import './Sidebar.css'; // Import the updated CSS file

const Sidebar = ({ open, onClose }) => {
  return (
    <div className={`sidebar ${open ? '' : 'closed'}`}>
      <List>
        <ListItem button component={Link} to="/" onClick={onClose}>
          <HomeIcon />
          <ListItemText primary="Home" />
        </ListItem>
        <ListItem button component={Link} to="/chat" onClick={onClose}>
          <ChatIcon />
          <ListItemText primary="Chat" />
        </ListItem>
        <ListItem button component={Link} to="/media" onClick={onClose}>
          <MediaIcon />
          <ListItemText primary="Media" />
        </ListItem>
        <ListItem button component={Link} to="/doc" onClick={onClose}>
          <DocumentIcon />
          <ListItemText primary="Documents" />
        </ListItem>
        <ListItem button component={Link} to="/audio" onClick={onClose}>
          <AudioIcon />
          <ListItemText primary="Audio" />
        </ListItem>
      </List>
    </div>
  );
};

export default Sidebar;
