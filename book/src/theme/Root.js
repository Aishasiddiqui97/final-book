import React from 'react';
import RagChatbot from '@site/src/components/RagChatbot';

// Default implementation, that you can customize
function Root({ children }) {
  return (
    <>
      {children}
      <RagChatbot />
    </>
  );
}

export default Root;