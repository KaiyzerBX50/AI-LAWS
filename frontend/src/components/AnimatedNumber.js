import React, { useEffect, useRef, useState } from 'react';

// Smoothly counts up to `value` when it first mounts / changes.
export const AnimatedNumber = ({ value = 0, duration = 1100, className = '' }) => {
  const [display, setDisplay] = useState(0);
  const raf = useRef(null);
  const from = useRef(0);

  useEffect(() => {
    const start = performance.now();
    const startVal = from.current;
    const delta = value - startVal;
    const ease = (t) => 1 - Math.pow(1 - t, 3); // easeOutCubic

    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      setDisplay(Math.round(startVal + delta * ease(p)));
      if (p < 1) raf.current = requestAnimationFrame(tick);
      else from.current = value;
    };
    raf.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf.current);
  }, [value, duration]);

  return <span className={className}>{display.toLocaleString()}</span>;
};
