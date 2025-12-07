import React, {useMemo, useState} from 'react';
import clsx from 'clsx';
import styles from './chat-widget.module.css';

type Message = {
  id: number;
  from: 'user' | 'bot';
  text: string;
};

const presetPrompts = [
  'What is Physical AI?',
  'Explain ROS 2 topics vs services.',
  'How do I simulate a robot in Gazebo?',
  'What is the VLA loop?',
];

const mockAnswers: Record<string, string> = {
  'what is physical ai?':
    'Physical AI blends sensing, perception, planning, and control so a robot can safely act in the real world. It follows a sense → think → act loop with safety anchors like E-stop and force/speed limits.',
  'explain ros 2 topics vs services.':
    'In ROS 2, topics are pub/sub streams (e.g., /camera) while services are request/response calls (e.g., /reset_pose). Nodes publish or subscribe to topics and call or serve services.',
  'how do i simulate a robot in gazebo?':
    'Install gazebo_ros packages, launch Gazebo, and spawn your model via /spawn_entity using an SDF/URDF. Use ROS 2 bridge to publish simulated sensors and test trajectories before hardware.',
  'what is the vla loop?':
    'Vision-Language-Action: see (detect/caption), understand (intent schema), decide (plan), and act (controller). Always confirm targets and enforce force/speed limits.',
};

const defaultMockAnswer =
  'This is a UI mock. The chatbot will answer from the textbook when the backend is connected.';

export default function ChatWidget(): React.ReactNode {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>(() => [
    {
      id: 1,
      from: 'bot',
      text: 'Hi! I will answer strictly from the Physical AI & Humanoid Robotics textbook. Backend hookup coming soon.',
    },
  ]);
  const [busy, setBusy] = useState(false);

  const addMessage = (msg: Message) => setMessages((prev) => [...prev, msg]);

  const send = (text: string) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    const userMsg: Message = {id: Date.now(), from: 'user', text: trimmed};
    addMessage(userMsg);
    setInput('');
    setBusy(true);
    // Mock bot reply based on simple matching
    setTimeout(() => {
      const key = trimmed.toLowerCase();
      addMessage({
        id: Date.now() + 1,
        from: 'bot',
        text: mockAnswers[key] ?? defaultMockAnswer,
      });
      setBusy(false);
    }, 400);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    send(input);
  };

  const history = useMemo(
    () =>
      messages.map((m) => (
        <div
          key={m.id}
          className={clsx(styles.bubble, m.from === 'user' ? styles.fromUser : styles.fromBot)}>
          {m.text}
        </div>
      )),
    [messages],
  );

  return (
    <>
      <button
        type="button"
        className={styles.chatLauncher}
        aria-label="Open chat"
        onClick={() => setOpen((v) => !v)}>
        💬 Chat
      </button>
      {open && (
        <div className={styles.chatPanel}>
          <div className={styles.chatHeader}>
            <div>
              <div className={styles.chatTitle}>Textbook Chat (mock)</div>
              <div className={styles.chatSubtitle}>Grounded answers; backend coming soon</div>
            </div>
            <button
              type="button"
              aria-label="Close chat"
              className={styles.closeButton}
              onClick={() => setOpen(false)}>
              ✕
            </button>
          </div>
          <div className={styles.chips}>
            {presetPrompts.map((p) => (
              <button key={p} className={styles.chip} type="button" onClick={() => send(p)}>
                {p}
              </button>
            ))}
          </div>
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
