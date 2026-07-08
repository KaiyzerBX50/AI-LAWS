import React, { useEffect, useRef } from 'react';

// Fixed, GPU-friendly cosmic backdrop with layered motion:
//  - drifting aurora blobs
//  - twinkling multi-layer starfield with pointer parallax
//  - periodic shooting stars
//  - slow rotating nebula sweep
//  - floating luminous orbs
// Adapts to day/night via CSS variables (stars/nebula intensify in dark mode).
export const CosmicBackground = () => {
  const rootRef = useRef(null);

  // Subtle pointer parallax — nudges star layers a few pixels for depth.
  useEffect(() => {
    const el = rootRef.current;
    if (!el) return;
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;
    let raf = 0;
    const onMove = (e) => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const x = (e.clientX / window.innerWidth - 0.5) * 2;
        const y = (e.clientY / window.innerHeight - 0.5) * 2;
        el.style.setProperty('--px', String(x));
        el.style.setProperty('--py', String(y));
      });
    };
    window.addEventListener('pointermove', onMove, { passive: true });
    return () => {
      window.removeEventListener('pointermove', onMove);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div className="cosmic-bg" aria-hidden="true" ref={rootRef}>
      <div className="nebula" />
      <div className="starfield star-far" />
      <div className="starfield star-near" />
      <div className="aurora-blob aurora-1" />
      <div className="aurora-blob aurora-2" />
      <div className="aurora-blob aurora-3" />

      {/* floating luminous orbs */}
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />
      <div className="orb orb-4" />

      {/* shooting stars */}
      <div className="shooting-star shoot-1" />
      <div className="shooting-star shoot-2" />
      <div className="shooting-star shoot-3" />
    </div>
  );
};
