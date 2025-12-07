import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Overview',
      collapsible: false,
      items: ['intro'],
    },
    {
      type: 'category',
      label: 'Chapters',
      items: [
        'chapters/physical-ai',
        'chapters/humanoid-basics',
        'chapters/ros2-fundamentals',
        'chapters/digital-twin',
        'chapters/vision-language-action',
        'chapters/capstone',
      ],
    },
    {
      type: 'category',
      label: 'Content Ops',
      items: ['content-ops/spec-kit-plus'],
    },
  ],
};

export default sidebars;
