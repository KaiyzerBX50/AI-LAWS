import React from 'react';
import { Volume2, VolumeX, Radio, Sparkles } from 'lucide-react';
import { useSound } from '@/lib/SoundContext';
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';

export const SoundToggle = () => {
  const { enabled, toggle, ambient, toggleAmbient, play } = useSound();
  const anyOn = enabled || ambient;

  return (
    <Popover>
      <PopoverTrigger asChild>
        <button
          type="button"
          data-testid="sound-toggle"
          aria-label="Sound settings"
          title="Sound settings"
          className="relative inline-flex h-9 w-9 items-center justify-center rounded-lg border border-border/60 bg-background/40 text-muted-foreground transition-colors duration-200 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          {anyOn ? (
            <Volume2 className="h-4 w-4 text-primary" />
          ) : (
            <VolumeX className="h-4 w-4" />
          )}
          {ambient && (
            <span className="absolute -right-0.5 -top-0.5 h-2 w-2 animate-pulse rounded-full bg-accent shadow-[0_0_8px_hsl(var(--accent))]" />
          )}
        </button>
      </PopoverTrigger>
      <PopoverContent
        align="end"
        className="glass-strong w-64 rounded-xl border-border/60 p-3"
        data-testid="sound-settings-popover"
      >
        <p className="mb-3 px-1 font-display text-sm font-semibold text-foreground">Sound</p>

        <label
          htmlFor="ui-sound-switch"
          className="flex cursor-pointer items-center gap-3 rounded-lg px-2 py-2 transition-colors hover:bg-secondary/60"
        >
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/15 text-primary">
            <Radio className="h-4 w-4" />
          </span>
          <span className="flex-1">
            <span className="block text-sm font-medium text-foreground">Interface sounds</span>
            <span className="block text-xs text-muted-foreground">Clicks, hovers &amp; cues</span>
          </span>
          <Switch
            id="ui-sound-switch"
            checked={enabled}
            onCheckedChange={() => {
              if (!enabled) play('toggle');
              toggle();
            }}
            data-testid="ui-sound-switch"
          />
        </label>

        <label
          htmlFor="ambient-switch"
          className="flex cursor-pointer items-center gap-3 rounded-lg px-2 py-2 transition-colors hover:bg-secondary/60"
        >
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent/15 text-accent">
            <Sparkles className="h-4 w-4" />
          </span>
          <span className="flex-1">
            <span className="block text-sm font-medium text-foreground">Ambient space</span>
            <span className="block text-xs text-muted-foreground">Evolving cosmic soundscape</span>
          </span>
          <Switch
            id="ambient-switch"
            checked={ambient}
            onCheckedChange={toggleAmbient}
            data-testid="ambient-switch"
          />
        </label>

        <Label className="mt-1 block px-2 pt-1 text-[11px] leading-relaxed text-muted-foreground/80">
          Audio starts after your first interaction.
        </Label>
      </PopoverContent>
    </Popover>
  );
};
