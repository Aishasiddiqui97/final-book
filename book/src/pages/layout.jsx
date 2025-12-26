import React from 'react';
import Layout from '@theme/Layout';
import RagChatbot from '@site/src/components/RagChatbot';

function LayoutWrapper(props) {
  return (
    <Layout {...props}>
      {props.children}
      <RagChatbot />
    </Layout>
  );
}

export default LayoutWrapper;