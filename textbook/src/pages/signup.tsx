import React, {useState} from 'react';
import Layout from '@theme/Layout';

export default function SignUp(): JSX.Element {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [software, setSoftware] = useState('');
  const [hardware, setHardware] = useState('');
  const [experience, setExperience] = useState('beginner');
  const [lang, setLang] = useState('en');
  const [status, setStatus] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('Demo-only form. Wire this to your Better Auth signup endpoint.');
  };

  return (
    <Layout title="Sign up">
      <main className="container margin-vert--lg">
        <h1>Sign up</h1>
        <p>Create an account and tell us about your background to personalize content.</p>
        <form onSubmit={handleSubmit} style={{maxWidth: 520}}>
          <label className="margin-bottom--sm" style={{display: 'block'}}>
            Email
            <input
              className="margin-top--xs"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{width: '100%'}}
            />
          </label>
          <label className="margin-bottom--sm" style={{display: 'block'}}>
            Password
            <input
              className="margin-top--xs"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{width: '100%'}}
            />
          </label>
          <label className="margin-bottom--sm" style={{display: 'block'}}>
            Software background (languages/frameworks)
            <textarea
              className="margin-top--xs"
              value={software}
              onChange={(e) => setSoftware(e.target.value)}
              placeholder="e.g., Python, ROS 2, React"
              style={{width: '100%'}}
            />
          </label>
          <label className="margin-bottom--sm" style={{display: 'block'}}>
            Hardware/robotics background
            <textarea
              className="margin-top--xs"
              value={hardware}
              onChange={(e) => setHardware(e.target.value)}
              placeholder="e.g., Arduino, sensors, embedded systems, ROS hardware"
              style={{width: '100%'}}
            />
          </label>
          <label className="margin-bottom--sm" style={{display: 'block'}}>
            Experience level
            <select
              className="margin-top--xs"
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              style={{width: '100%'}}>
              <option value="beginner">Beginner</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>
          <label className="margin-bottom--sm" style={{display: 'block'}}>
            Preferred language
            <select
              className="margin-top--xs"
              value={lang}
              onChange={(e) => setLang(e.target.value)}
              style={{width: '100%'}}>
              <option value="en">English</option>
              <option value="ur">اردو</option>
            </select>
          </label>
          <button className="button button--primary" type="submit">
            Sign up
          </button>
        </form>
        {status && <p className="margin-top--md">{status}</p>}
      </main>
    </Layout>
  );
}
