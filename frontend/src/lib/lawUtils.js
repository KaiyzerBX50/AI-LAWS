import { CheckCircle2, Clock, FileText, Archive } from 'lucide-react';

// Status -> styling + icon (works in light & dark via semantic classes)
export const STATUS_META = {
  Enacted: {
    label: 'Enacted',
    icon: CheckCircle2,
    className:
      'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800',
  },
  Proposed: {
    label: 'Proposed',
    icon: Clock,
    className:
      'bg-amber-100 text-amber-900 border-amber-300 dark:bg-amber-950/50 dark:text-amber-300 dark:border-amber-800',
  },
  Draft: {
    label: 'Draft',
    icon: FileText,
    className:
      'bg-slate-200 text-slate-800 border-slate-300 dark:bg-slate-800/70 dark:text-slate-200 dark:border-slate-700',
  },
  Superseded: {
    label: 'Superseded',
    icon: Archive,
    className:
      'bg-zinc-200 text-zinc-600 border-zinc-300 dark:bg-zinc-800/70 dark:text-zinc-400 dark:border-zinc-700 line-through decoration-1',
  },
};

export const getStatusMeta = (status) => STATUS_META[status] || STATUS_META.Draft;

// Map maturity bins (0-4) fill colors for light & dark surfaces
export const MATURITY_BINS = [
  { key: 0, label: 'No tracked AI law', light: '#E7EDF3', dark: '#1B2633' },
  { key: 1, label: 'Emerging signals', light: '#CFE6F2', dark: '#1E3A4A' },
  { key: 2, label: 'Developing framework', light: '#9FD3E6', dark: '#1F5566' },
  { key: 3, label: 'Established regulation', light: '#4FB6C8', dark: '#2A7F8E' },
  { key: 4, label: 'Comprehensive / multi-act', light: '#1F7A8C', dark: '#6FD6D1' },
];

export const maturityFill = (level, isDark) => {
  const bin = MATURITY_BINS[level] || MATURITY_BINS[0];
  return isDark ? bin.dark : bin.light;
};

// Status-based map fill (for the 'status' map mode)
export const statusFill = (counts, isDark) => {
  if (!counts) return isDark ? '#1B2633' : '#E7EDF3';
  if (counts.Enacted > 0) return isDark ? '#2A7F8E' : '#1F7A8C';
  if (counts.Proposed > 0) return isDark ? '#7c5a1e' : '#F0B454';
  if (counts.Draft > 0) return isDark ? '#334155' : '#94A3B8';
  return isDark ? '#1B2633' : '#E7EDF3';
};

export const REGION_COLORS = {
  Europe: '#1F7A8C',
  'North America': '#4FB6C8',
  Asia: '#0E7490',
  'South America': '#2A9D8F',
  'Middle East': '#E9A23B',
  Africa: '#8AB17D',
  Oceania: '#457B9D',
};
