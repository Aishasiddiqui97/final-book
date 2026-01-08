// @ts-check

/**
 * Physical AI & Humanoid Robotics Textbook Sidebar
 * Organized by modules with clear hierarchy
 *
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 Nervous System',
      collapsed: false,
      collapsible: true,
      link: {
        type: 'doc',
        id: 'module-1-ros/index',
      },
      items: [
        'module-1-ros/introduction-to-physical-ai',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin',
      collapsed: true,
      collapsible: true,
      link: {
        type: 'doc',
        id: 'module-2-digital-twin/index',
      },
      items: [],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac AI',
      collapsed: true,
      collapsible: true,
      link: {
        type: 'doc',
        id: 'module-3-isaac-ai/index',
      },
      items: [],
    },
    {
      type: 'category',
      label: 'Module 4: VLA & Humanoid',
      collapsed: true,
      collapsible: true,
      link: {
        type: 'doc',
        id: 'module-4-vision-action/index',
      },
      items: [],
    },
  ],
};

export default sidebars;
