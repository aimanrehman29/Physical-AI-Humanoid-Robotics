import React, {useState} from 'react';
import Layout from '@theme/Layout';

export default function SignIn(): JSX.Element {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('Demo-only form. Wire this to your Better Auth signin endpoint.');
  };

  return (
    <Layout title="Sign in">
      <main className="container margin-vert--lg">
        <h1>Sign in</h1>
        <p>Use your credentials to access personalized content.</p>
        <form onSubmit={handleSubmit} style={{maxWidth: 420}}>
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
          <button className="button button--primary" type="submit">
            Sign in
          </button>
        </form>
        {status && <p className="margin-top--md">{status}</p>}
      </main>
    </Layout>
  );
}
