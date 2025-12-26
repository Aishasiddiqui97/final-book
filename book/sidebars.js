// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Modules',
      items: [
        {
          type: 'category',
          label: 'Module 1: ROS 2 Nervous System',
          items: [
            'module-1-ros/index',
            'module-1-ros/introduction-to-physical-ai'
          ],
        },
        {
          type: 'category',
          label: 'Module 2: Digital Twin (Gazebo/Unity)',
          items: [
            'module-2-digital-twin/index'
          ],
        },
        {
          type: 'category',
          label: 'Module 3: NVIDIA Isaac AI-Robot Brain',
          items: [
            'module-3-isaac-ai/index'
          ],
        },
        {
          type: 'category',
          label: 'Module 4: Vision-Language-Action & Humanoid Capstone',
          items: [
            'module-4-vision-action/index'
          ],
        }
      ],
    },
  ],
};

export default sidebars;
