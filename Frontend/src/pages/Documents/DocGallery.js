import React from 'react';
import DocItem from './DocItem';

const DocGallery = ({ documents }) => {
  return (
    <div className="doc-gallery">
      {documents.map(doc => (
        <DocItem key={doc.id} document={doc} />
      ))}
    </div>
  );
};

export default DocGallery;
