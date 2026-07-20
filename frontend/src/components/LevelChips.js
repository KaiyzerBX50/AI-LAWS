import React from 'react';
import { LayoutGrid, Landmark, Building2, Building, Flag, Globe2 } from 'lucide-react';

const LEVELS = [
  { key: 'all', label: 'All', icon: LayoutGrid },
  { key: 'Federal', label: 'Federal', icon: Landmark },
  { key: 'State', label: 'State', icon: Building2 },
  { key: 'City', label: 'City', icon: Building },
  { key: 'National', label: 'National', icon: Flag },
  { key: 'International', label: 'International', icon: Globe2 },
];

// One-click governance-level filter chips with live counts.
export const LevelChips = ({ byLevel = {}, total = 0, value = 'all', onChange }) => {
  const countFor = (k) => (k === 'all' ? total : byLevel[k] || 0);
  const chips = LEVELS.filter((l) => l.key === 'all' || (byLevel[l.key] || 0) > 0);

  return (
    <div className="flex flex-wrap items-center gap-2" data-testid="level-chips">
      {chips.map(({ key, label, icon: Icon }) => {
        const active = value === key;
        return (
          <button
            key={key}
            type="button"
            onClick={() => onChange(key)}
            data-testid={`level-chip-${key.toLowerCase()}`}
            aria-pressed={active}
            className={`group inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-medium transition-colors duration-200 ${
              active
                ? 'border-transparent bg-gradient-to-br from-primary to-accent text-primary-foreground shadow-md'
                : 'border-border/60 bg-background/40 text-muted-foreground hover:text-foreground hover:border-border'
            }`}
          >
            <Icon className="h-3.5 w-3.5" />
            {label}
            <span
              className={`ml-0.5 rounded-full px-1.5 py-px font-mono text-[10px] ${
                active ? 'bg-white/20 text-primary-foreground' : 'bg-secondary text-muted-foreground'
              }`}
            >
              {countFor(key)}
            </span>
          </button>
        );
      })}
    </div>
  );
};
