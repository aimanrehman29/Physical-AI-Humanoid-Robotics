import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg?: React.ComponentType<React.ComponentProps<'svg'>>;
  imgSrc?: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Humanoid basics',
    imgSrc: '/img/humaniod-robbot.png',
    description: (
      <>
        Understand sensors, actuators, and safe human interaction with clear
        sketches and checklists.
      </>
    ),
  },
  {
    title: 'ROS 2 ready',
    imgSrc: '/img/ROS 2 ready.png',
    description: (
      <>
        Minimal publisher/subscriber and launch examples to get nodes, topics,
        and services running quickly.
      </>
    ),
  },
  {
    title: 'Sim-first pipeline',
    imgSrc: '/img/Sim-first_pipeline.png',
    description: (
      <>
        Build and test in Gazebo/Isaac, then connect vision-language-action for
        a safe capstone demo.
      </>
    ),
  },
];

function Feature({title, Svg, imgSrc, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className={clsx('text--center', styles.featureCard)}>
        {Svg ? (
          <Svg className={styles.featureSvg} role="img" />
        ) : (
          imgSrc && <img src={imgSrc} alt={title} className={styles.featureSvg} />
        )}
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
