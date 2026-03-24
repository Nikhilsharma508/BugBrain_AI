import { useState } from 'react';

export default function GlassCard({ children, className = '', style = {} }) {
  const [styleState, setStyleState] = useState({});

  function handleMove(e) {
    const rect = e.currentTarget.getBoundingClientRect();

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const midX = rect.width / 2;
    const midY = rect.height / 2;

    const rotateX = ((y - midY) / midY) * 8;
    const rotateY = ((x - midX) / midX) * -8;

    setStyleState({
      transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
      '--mouse-x': `${x}px`,
      '--mouse-y': `${y}px`,
    });
  }

  function handleLeave() {
    setStyleState({
      transform: `rotateX(0deg) rotateY(0deg)`,
    });
  }

  return (
    <div
      className={`glass-card ${className}`}
      style={{ ...style, ...styleState }}
      onMouseMove={handleMove}
      onMouseLeave={handleLeave}
    >
      {children}
    </div>
  );
}