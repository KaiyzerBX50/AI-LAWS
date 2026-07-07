import React from 'react';

// Fixed, GPU-friendly cosmic backdrop: aurora blobs + starfield + noise.
// Adapts to day/night via CSS variables (stars only show in dark mode).
export const CosmicBackground = () => (
  <div className="cosmic-bg" aria-hidden="true">
    <div className="starfield" />
    <div className="aurora-blob aurora-1" />
    <div className="aurora-blob aurora-2" />
    <div className="aurora-blob aurora-3" />
  </div>
);
