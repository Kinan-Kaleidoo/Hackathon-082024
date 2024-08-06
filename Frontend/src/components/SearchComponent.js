// src/components/SearchComponent.js
import React from 'react';
import { TextField, Button } from '@mui/material';
import './SearchComponent.css';

const SearchComponent = () => {
  return (
    <div className="search-container">
      <TextField
        label="Search"
        variant="outlined"
        className="search-input"
      />
      <Button variant="contained" color="primary">Search</Button>
    </div>
  );
};

export default SearchComponent;
