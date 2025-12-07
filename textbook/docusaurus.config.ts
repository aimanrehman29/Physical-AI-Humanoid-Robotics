import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Learn Physical AI foundations, ROS 2, simulation, and vision-language-action.',
  favicon: 'img/logo1.png',

  future: {
    v4: true,
  },

  url: 'https://ai-driven-dev.example.com',
  baseUrl: '/',

  organizationName: 'ai-driven-dev',
  projectName: 'textbook',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: undefined,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Humanoid Robotics & Physical AI',
      logo: {
        alt: 'Humanoid Robotics logo',
        src: 'img/logo1.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          type: 'doc',
          docId: 'content-ops/spec-kit-plus',
          position: 'left',
          label: 'Content Ops',
        },
        {
          href: 'https://github.com/aimanrehman29',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Overview',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Content',
          items: [
            {
              label: 'Chapters',
              to: '/docs/chapters/physical-ai',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/aimanrehman29',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Humanoid Robotics & Physical AI.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
