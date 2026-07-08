import React, { createContext, useContext, useEffect, useMemo, useRef, useState } from 'react';

/**
 * SoundContext — a tiny, dependency-free spatial UI sound engine built on the
 * Web Audio API. All sounds are synthesised at runtime (no audio assets), so
 * there is zero network cost. A single AudioContext is created lazily on the
 * first user gesture to satisfy browser autoplay policies.
 *
 * It also installs delegated pointer listeners so that *every* interactive
 * element (buttons, tabs, links) emits subtle "liquid glass" feedback without
 * having to wire handlers into each component.
 */

const SoundContext = createContext({
  enabled: true,
  toggle: () => {},
  play: () => {},
});

const STORAGE_KEY = 'sound-enabled';

export const SoundProvider = ({ children }) => {
  const [enabled, setEnabled] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved === null ? true : saved === 'true';
  });

  const ctxRef = useRef(null);
  const masterRef = useRef(null);
  const enabledRef = useRef(enabled);
  const lastHoverRef = useRef(0);
  const lastPlayRef = useRef({});

  useEffect(() => {
    enabledRef.current = enabled;
    localStorage.setItem(STORAGE_KEY, String(enabled));
  }, [enabled]);

  // Lazily create / resume the AudioContext.
  const ensureCtx = () => {
    if (typeof window === 'undefined') return null;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return null;
    if (!ctxRef.current) {
      const ctx = new AudioCtx();
      const master = ctx.createGain();
      master.gain.value = 0.5;
      master.connect(ctx.destination);
      ctxRef.current = ctx;
      masterRef.current = master;
    }
    if (ctxRef.current.state === 'suspended') {
      ctxRef.current.resume().catch(() => {});
    }
    return ctxRef.current;
  };

  // Core voice: a short shaped oscillator with soft attack/decay + optional
  // gentle low-pass to keep everything glassy and non-fatiguing.
  const voice = (ctx, {
    type = 'sine',
    freq = 660,
    to = null,
    dur = 0.12,
    gain = 0.06,
    attack = 0.006,
    filter = null,
    detune = 0,
    delay = 0,
  }) => {
    const t0 = ctx.currentTime + delay;
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, t0);
    if (detune) osc.detune.setValueAtTime(detune, t0);
    if (to) osc.frequency.exponentialRampToValueAtTime(Math.max(1, to), t0 + dur);

    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(gain, t0 + attack);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);

    let node = osc;
    if (filter) {
      const lp = ctx.createBiquadFilter();
      lp.type = filter.type || 'lowpass';
      lp.frequency.value = filter.freq || 2200;
      if (filter.q) lp.Q.value = filter.q;
      node.connect(lp);
      lp.connect(g);
    } else {
      node.connect(g);
    }
    g.connect(masterRef.current);
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
  };

  const play = (kind = 'click') => {
    if (!enabledRef.current) return;
    const ctx = ensureCtx();
    if (!ctx) return;

    // throttle identical sounds so rapid events don't stack harshly
    const now = performance.now();
    const minGap = kind === 'hover' ? 55 : 24;
    if (now - (lastPlayRef.current[kind] || 0) < minGap) return;
    lastPlayRef.current[kind] = now;

    switch (kind) {
      case 'hover':
        voice(ctx, { type: 'sine', freq: 1180, dur: 0.055, gain: 0.018, filter: { freq: 3200 } });
        break;
      case 'click':
        voice(ctx, { type: 'triangle', freq: 520, to: 760, dur: 0.09, gain: 0.05, filter: { freq: 2600 } });
        break;
      case 'tab':
        voice(ctx, { type: 'sine', freq: 620, dur: 0.11, gain: 0.045, filter: { freq: 2800 } });
        voice(ctx, { type: 'sine', freq: 930, dur: 0.13, gain: 0.03, delay: 0.04, filter: { freq: 3200 } });
        break;
      case 'toggle':
        voice(ctx, { type: 'sine', freq: 440, to: 880, dur: 0.16, gain: 0.045, filter: { freq: 3000 } });
        break;
      case 'open':
        voice(ctx, { type: 'sine', freq: 380, to: 720, dur: 0.2, gain: 0.05, filter: { freq: 2600 } });
        voice(ctx, { type: 'sine', freq: 760, to: 1140, dur: 0.22, gain: 0.025, delay: 0.05 });
        break;
      case 'close':
        voice(ctx, { type: 'sine', freq: 720, to: 340, dur: 0.18, gain: 0.045, filter: { freq: 2400 } });
        break;
      case 'success': {
        // gentle ascending arpeggio (C5 · E5 · G5)
        [523.25, 659.25, 783.99].forEach((f, i) =>
          voice(ctx, { type: 'sine', freq: f, dur: 0.28, gain: 0.045, delay: i * 0.07, filter: { freq: 3400 } })
        );
        break;
      }
      default:
        voice(ctx, { type: 'sine', freq: 600, dur: 0.09, gain: 0.04 });
    }
  };

  // Global delegated feedback for hover + click on interactive elements.
  useEffect(() => {
    const isInteractive = (el) =>
      el && el.closest && el.closest(
        'button, [role="tab"], a[href], [role="switch"], [data-sound-hover], .hover-lift'
      );

    const onOver = (e) => {
      if (!enabledRef.current) return;
      const now = performance.now();
      if (now - lastHoverRef.current < 45) return;
      const target = isInteractive(e.target);
      if (!target || target.hasAttribute('disabled') || target.getAttribute('aria-disabled') === 'true') return;
      lastHoverRef.current = now;
      play('hover');
    };

    const onClick = (e) => {
      if (!enabledRef.current) return;
      const target = isInteractive(e.target);
      if (!target || target.hasAttribute('disabled') || target.getAttribute('aria-disabled') === 'true') return;
      // let dedicated component handlers own richer sounds via data-sound
      const custom = target.getAttribute && target.getAttribute('data-sound');
      play(custom || 'click');
    };

    document.addEventListener('pointerover', onOver, { passive: true });
    document.addEventListener('click', onClick, { passive: true });
    return () => {
      document.removeEventListener('pointerover', onOver);
      document.removeEventListener('click', onClick);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const value = useMemo(
    () => ({ enabled, toggle: () => setEnabled((v) => !v), play }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [enabled]
  );

  return <SoundContext.Provider value={value}>{children}</SoundContext.Provider>;
};

export const useSound = () => useContext(SoundContext);
