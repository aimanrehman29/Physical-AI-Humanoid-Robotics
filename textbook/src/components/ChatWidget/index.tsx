import React, {useEffect, useMemo, useState} from 'react';
import clsx from 'clsx';
import styles from './chat-widget.module.css';

type Message = {
  id: number;
  from: 'user' | 'bot';
  text: string;
  citations?: {url: string; label: string}[];
};

const presetPrompts = [
  'What is Physical AI?',
  'Explain ROS 2 topics vs services.',
  'How do I simulate a robot in Gazebo?',
  'What is the VLA loop?',
];

const API_BASE =
  (typeof process !== 'undefined' ? process.env?.CHAT_API_URL : undefined) ?? 'http://127.0.0.1:8000';

export default function ChatWidget(): React.ReactNode {
  const [mounted, setMounted] = useState(false);
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [hasInteracted, setHasInteracted] = useState(false);
  const [messages, setMessages] = useState<Message[]>(() => [
    {
      id: 1,
      from: 'bot',
      text: 'Hi! I answer strictly from the textbook. Ask a question to query the RAG backend.',
    },
  ]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  const addMessage = (msg: Message) => setMessages((prev) => [...prev, msg]);

  const send = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    setHasInteracted(true);
    const userMsg: Message = {id: Date.now(), from: 'user', text: trimmed};
    addMessage(userMsg);
    setInput('');
    setBusy(true);
    setError(null);

    try {
      const resp = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question: trimmed}),
      });
      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}`);
      }
      const data = await resp.json();
      const answerText = data.answer || 'No answer returned.';
      const citations =
        (data.citations || []).map((c: any, idx: number) => ({
          url: c.url || '#',
          label: c.url ? `Source ${idx + 1}` : '',
        })) || [];
      addMessage({
        id: Date.now() + 1,
        from: 'bot',
        text: answerText,
        citations,
      });
    } catch (err: any) {
      setError('Backend not reachable or returned an error.');
      addMessage({
        id: Date.now() + 2,
        from: 'bot',
        text: 'I could not reach the backend right now.',
      });
    } finally {
      setBusy(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    void send(input);
  };

  const history = useMemo(
    () =>
      messages.map((m) => (
        <div
          key={m.id}
          className={clsx(styles.bubble, m.from === 'user' ? styles.fromUser : styles.fromBot)}>
          <div>{m.text}</div>
          {m.citations && m.citations.length > 0 && (
            <div className={styles.citations}>
              {m.citations.map((c, idx) => (
                <a key={idx} href={c.url} target="_blank" rel="noreferrer">
                  {c.label || `Source ${idx + 1}`}
                </a>
              ))}
            </div>
          )}
        </div>
      )),
    [messages],
  );

  if (!mounted) return null;

  return (
    <>
      <button
        type="button"
        className={styles.chatLauncher}
        aria-label="Open chat"
        onClick={() => setOpen((v) => !v)}>
        <span role="img" aria-hidden="true">🤖</span>
        Chat
      </button>
      {open && (
        <div className={styles.chatPanel}>
          <div className={styles.chatHeader}>
            <div>
              <div className={styles.chatTitle}>Textbook Chat</div>
              <div className={styles.chatSubtitle}>Grounded answers from the local RAG backend</div>
            </div>
            <button
              type="button"
              aria-label="Close chat"
              className={styles.closeButton}
              onClick={() => setOpen(false)}>
              ×
            </button>
          </div>
          <div className={styles.statusBar}>
            <span className={styles.statusDot} />
            <span>RAG chatbot · uses textbook embeddings</span>
          </div>
          {!input.trim() && !hasInteracted && (
            <div className={styles.chips}>
              {presetPrompts.map((p) => (
                <button
                  key={p}
                  className={styles.chip}
                  type="button"
                  onClick={() => send(p)}>
                  {p}
                </button>
              ))}
            </div>
          )}
          {error && <div className={styles.error}>{error}</div>}
          <div className={styles.chatMessages}>{history}</div>
          <form className={styles.chatInputRow} onSubmit={handleSubmit}>
            <input
              className={styles.textInput}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about the book..."
              aria-label="Chat input"
            />
            <button className={styles.sendButton} type="submit" disabled={busy || !input.trim()}>
              {busy ? '...' : 'Send'}
            </button>
          </form>
        </div>
      )}
    </>
  );
}
