---
title: "فزیکل اے آئی اور انسان نما روبوٹکس"
description: "فزیکل اے آئی، ROS 2، سمیولیشن اور ویژن-لینگوئج-ایکشن سسٹمز کا جامع اردو نصاب"
---

import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

export default function HomeUrdu() {
  return (
    <Layout
      title="فزیکل اے آئی اور انسان نما روبوٹکس"
      description="فزیکل اے آئی کی بنیادیں، ROS 2، سمیولیشن، اور ویژن-لینگوئج-ایکشن سسٹمز">
      <header className={`hero hero--primary ${styles.heroBanner || ''}`}>
        <div className="container">
          <Heading as="h1" className="hero__title">
            فزیکل اے آئی اور انسان نما روبوٹکس
          </Heading>
          <p className="hero__subtitle">
            فزیکل اے آئی، ROS 2، سمیولیشن، اور ویژن-لینگوئج-ایکشن سسٹمز کو اردو میں سیکھیں۔
          </p>
          <div className={styles.buttons || ''}>
            <Link className="button button--secondary button--lg" to="/docs/chapters/physical-ai">
              آغاز کریں
            </Link>
          </div>
        </div>
      </header>
      <main>
        <div className="container">
          <p style={{textAlign: 'center', marginTop: '1.5rem'}}>
            مکمل نصاب: فزیکل اے آئی تعارف، انسان نما روبوٹکس، ROS 2، ڈیجیٹل ٹوئن، وژن-لینگوئج-ایکشن، اور کیپ اسٹون منصوبہ۔
          </p>
        </div>
      </main>
    </Layout>
  );
}
