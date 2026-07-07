import React from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '@/lib/ThemeContext';
import { TRACKER } from '@/constants/testIds';

export const ThemeToggle = () => {
  const { isDark, toggle } = useTheme();
  return (
    <button
      type="button"
      onClick={toggle}
      data-testid={TRACKER.themeToggle}
      aria-label={isDark ? 'Switch to day mode' : 'Switch to night mode'}
      className="relative inline-flex h-9 w-16 items-center rounded-full border border-border bg-secondary transition-colors duration-200 hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
    >
      <span
        className={`inline-flex h-7 w-7 transform items-center justify-center rounded-full bg-card shadow-sm transition-transform duration-300 ${
          isDark ? 'translate-x-8' : 'translate-x-1'
        }`}
      >
        {isDark ? (
          <Moon className="h-4 w-4 text-primary" />
        ) : (
          <Sun className="h-4 w-4 text-amber-500" />
        )}
      </span>
    </button>
  );
};
