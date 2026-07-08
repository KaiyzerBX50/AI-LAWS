import React from 'react';
import { Volume2, VolumeX } from 'lucide-react';
import { useSound } from '@/lib/SoundContext';

export const SoundToggle = () => {
  const { enabled, toggle, play } = useSound();
  return (
    <button
      type="button"
      onClick={() => {
        // play a confirmation only when turning sound ON
        if (!enabled) play('toggle');
        toggle();
      }}
      data-testid="sound-toggle"
      data-sound="toggle"
      aria-label={enabled ? 'Mute interface sounds' : 'Enable interface sounds'}
      aria-pressed={enabled}
      title={enabled ? 'Sound on' : 'Sound off'}
      className="relative inline-flex h-9 w-9 items-center justify-center rounded-lg border border-border/60 bg-background/40 text-muted-foreground transition-colors duration-200 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
    >
      {enabled ? (
        <Volume2 className="h-4 w-4 text-primary" />
      ) : (
        <VolumeX className="h-4 w-4" />
      )}
    </button>
  );
};
