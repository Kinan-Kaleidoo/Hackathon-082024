import React from 'react';

const DocItem = ({ document }) => {
  return (
    <div className="doc-item">
      <h3>{document.file_name}</h3>
      <p>{document.content}</p>
    </div>
  );
};

export default DocItem;
