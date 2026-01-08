import React, { useEffect, useRef } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

// Module data with icons and colors
const modules = [
  {
    id: 1,
    title: 'ROS 2 Nervous System',
    subtitle: 'Module 1',
    description: 'Master the Robot Operating System 2 - the neural backbone of modern robotics. Learn nodes, topics, services, and real-time communication.',
    icon: '🧠',
    color: '#3b82f6',
    link: '/docs/module-1-ros',
    topics: ['Nodes & Topics', 'Services & Actions', 'Launch Files', 'Navigation Stack'],
  },
  {
    id: 2,
    title: 'Digital Twin',
    subtitle: 'Module 2',
    description: 'Build virtual replicas with Gazebo and Unity. Simulate physics, sensors, and environments before deploying to real hardware.',
    icon: '🌐',
    color: '#8b5cf6',
    link: '/docs/module-2-digital-twin',
    topics: ['Gazebo Simulation', 'Unity Integration', 'Sensor Modeling', 'Physics Engine'],
  },
  {
    id: 3,
    title: 'NVIDIA Isaac AI Brain',
    subtitle: 'Module 3',
    description: 'Harness GPU-accelerated AI for perception, planning, and control. Deploy neural networks that think in milliseconds.',
    icon: '⚡',
    color: '#76b900',
    link: '/docs/module-3-isaac-ai',
    topics: ['Isaac Sim', 'Perception AI', 'Motion Planning', 'Reinforcement Learning'],
  },
  {
    id: 4,
    title: 'Vision-Language-Action',
    subtitle: 'Module 4',
    description: 'Unite vision, language, and action in humanoid robots. Build systems that see, understand, and interact with the world.',
    icon: '🤖',
    color: '#ec4899',
    link: '/docs/module-4-vision-action',
    topics: ['VLA Models', 'Humanoid Control', 'Multi-modal AI', 'Capstone Project'],
  },
];

// Stats data
const stats = [
  { value: '4', label: 'Modules' },
  { value: '20+', label: 'Chapters' },
  { value: '50+', label: 'Code Examples' },
  { value: '∞', label: 'Possibilities' },
];

// Animated counter hook
function useCountUp(end, duration = 2000) {
  const [count, setCount] = React.useState(0);
  const countRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          let start = 0;
          const increment = end / (duration / 16);
          const timer = setInterval(() => {
            start += increment;
            if (start >= end) {
              setCount(end);
              clearInterval(timer);
            } else {
              setCount(Math.floor(start));
            }
          }, 16);
          observer.disconnect();
        }
      },
      { threshold: 0.5 }
    );

    if (countRef.current) {
      observer.observe(countRef.current);
    }

    return () => observer.disconnect();
  }, [end, duration]);

  return [count, countRef];
}

// Hero Section
function HeroSection() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <header className={styles.hero}>
      <div className={styles.heroBackground}>
        <div className={styles.heroGrid}></div>
        <div className={styles.heroGlow}></div>
      </div>
      <div className={styles.heroContent}>
        <div className={styles.heroLabel}>
          <span>Open Source Textbook</span>
        </div>
        <Heading as="h1" className={styles.heroTitle}>
          Physical AI &<br />
          <span className={styles.heroTitleGradient}>Humanoid Robotics</span>
        </Heading>
        <p className={styles.heroSubtitle}>
          A comprehensive journey from ROS 2 fundamentals to building intelligent
          humanoid robots. Master the technologies shaping the future of robotics.
        </p>
        <div className={styles.heroButtons}>
          <Link className={styles.primaryButton} to="/docs/intro">
            Start Learning
            <span className={styles.buttonIcon}>→</span>
          </Link>
          <Link className={styles.secondaryButton} to="/docs/module-1-ros">
            Explore Modules
          </Link>
        </div>
        <div className={styles.heroStats}>
          {stats.map((stat, idx) => (
            <div key={idx} className={styles.statItem}>
              <span className={styles.statValue}>{stat.value}</span>
              <span className={styles.statLabel}>{stat.label}</span>
            </div>
          ))}
        </div>
      </div>
    </header>
  );
}

// Module Card Component
function ModuleCard({ module, index }) {
  const cardRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add(styles.visible);
          }
        });
      },
      { threshold: 0.1, rootMargin: '50px' }
    );

    if (cardRef.current) {
      observer.observe(cardRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <Link
      to={module.link}
      className={styles.moduleCard}
      ref={cardRef}
      style={{
        '--module-color': module.color,
        '--animation-delay': `${index * 100}ms`,
      }}
    >
      <div className={styles.moduleCardHeader}>
        <span className={styles.moduleIcon}>{module.icon}</span>
        <span className={styles.moduleSubtitle}>{module.subtitle}</span>
      </div>
      <h3 className={styles.moduleTitle}>{module.title}</h3>
      <p className={styles.moduleDescription}>{module.description}</p>
      <div className={styles.moduleTopics}>
        {module.topics.map((topic, idx) => (
          <span key={idx} className={styles.topicTag}>
            {topic}
          </span>
        ))}
      </div>
      <div className={styles.moduleFooter}>
        <span>Start Module</span>
        <span className={styles.moduleArrow}>→</span>
      </div>
    </Link>
  );
}

// Modules Section
function ModulesSection() {
  return (
    <section className={styles.modulesSection}>
      <div className={styles.container}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionLabel}>Curriculum</span>
          <h2 className={styles.sectionTitle}>Learning Modules</h2>
          <p className={styles.sectionDescription}>
            Four comprehensive modules taking you from robotics fundamentals to
            building autonomous humanoid systems.
          </p>
        </div>
        <div className={styles.modulesGrid}>
          {modules.map((module, idx) => (
            <ModuleCard key={module.id} module={module} index={idx} />
          ))}
        </div>
      </div>
    </section>
  );
}

// Features Section
function FeaturesSection() {
  const features = [
    {
      icon: '📚',
      title: 'Structured Learning',
      description: 'Progressive curriculum designed by robotics experts. Each chapter builds on previous concepts.',
    },
    {
      icon: '💻',
      title: 'Hands-on Code',
      description: 'Every concept comes with working code examples. Clone, run, and experiment immediately.',
    },
    {
      icon: '🤖',
      title: 'AI-Powered Assistant',
      description: 'Built-in RAG chatbot answers your questions using textbook content. Zero hallucinations.',
    },
    {
      icon: '🌍',
      title: 'Multi-language',
      description: 'Available in English and Urdu. Making robotics education accessible globally.',
    },
    {
      icon: '🔬',
      title: 'Research-backed',
      description: 'Content based on latest papers and industry practices from NVIDIA, Open Robotics, and more.',
    },
    {
      icon: '🎓',
      title: 'Project-based',
      description: 'Capstone project guides you to build a complete humanoid robot system.',
    },
  ];

  return (
    <section className={styles.featuresSection}>
      <div className={styles.container}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionLabel}>Why This Book</span>
          <h2 className={styles.sectionTitle}>Built for Learners</h2>
        </div>
        <div className={styles.featuresGrid}>
          {features.map((feature, idx) => (
            <div key={idx} className={styles.featureCard}>
              <span className={styles.featureIcon}>{feature.icon}</span>
              <h3 className={styles.featureTitle}>{feature.title}</h3>
              <p className={styles.featureDescription}>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// CTA Section
function CTASection() {
  return (
    <section className={styles.ctaSection}>
      <div className={styles.container}>
        <div className={styles.ctaContent}>
          <h2 className={styles.ctaTitle}>Ready to Build the Future?</h2>
          <p className={styles.ctaDescription}>
            Join thousands of learners mastering Physical AI and Humanoid Robotics.
            Start your journey today.
          </p>
          <div className={styles.ctaButtons}>
            <Link className={styles.primaryButton} to="/docs/intro">
              Get Started Free
              <span className={styles.buttonIcon}>→</span>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

// Main Home Component
export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title="Physical AI & Humanoid Robotics Textbook"
      description="A comprehensive guide to Physical AI and Humanoid Robotics - from ROS 2 to Vision-Language-Action models"
    >
      <HeroSection />
      <main>
        <ModulesSection />
        <FeaturesSection />
        <CTASection />
      </main>
    </Layout>
  );
}
