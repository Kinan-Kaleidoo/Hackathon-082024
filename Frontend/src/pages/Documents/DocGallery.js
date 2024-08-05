import React from 'react';
import DocItem from './DocItem';

const documents = [
  { id: 1, name: 'Document 1', content: 'This is the first document' },
  { id: 2, name: 'Document 2', content: 'This is the second document' },
  // Add more documents here
];

const DocGallery = () => {
  return (
    <div className="doc-gallery">
      {documents.map(doc => (
        <DocItem key={doc.id} document={doc} />
      ))}
    </div>
  );
};

export default DocGallery;
