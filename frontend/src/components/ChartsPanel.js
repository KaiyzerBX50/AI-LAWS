import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Bar,
  Line,
  BarChart,
  PieChart,
  Pie,
  Cell,
  Sector,
  RadialBarChart,
  RadialBar,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import { Card } from '@/components/ui/card';
import { useTheme } from '@/lib/ThemeContext';
import { AnimatedNumber } from '@/components/AnimatedNumber';
import { TrendingUp, Layers, Compass, Activity, Landmark } from 'lucide-react';

const reveal = {
  initial: { opacity: 0, y: 24 },
  animate: { opacity: 1, y: 0 },
};

// Theme-aware cosmic palette
const useColors = () => {
  const { isDark } = useTheme();
  return {
    isDark,
    glow: isDark ? '#67E8F9' : '#0E8BA8',
    glow2: isDark ? '#34E5B0' : '#1AA179',
    axis: isDark ? '#8FA3B8' : '#64748B',
    grid: isDark ? 'rgba(255,255,255,0.06)' : 'rgba(15,23,42,0.07)',
    ring: isDark ? '#67E8F9' : '#1F7A8C',
    palette: isDark
      ? ['#67E8F9', '#34D399', '#60A5FA', '#A78BFA', '#FBBF24', '#2DD4BF', '#38BDF8', '#FB7185']
      : ['#0891B2', '#059669', '#2563EB', '#7C3AED', '#D97706', '#0D9488', '#0369A1', '#E11D48'],
    track: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(15,23,42,0.06)',
    status: {
      Enacted: isDark ? '#34E5B0' : '#0D9488',
      Proposed: isDark ? '#F6C065' : '#E9A23B',
      Draft: isDark ? '#7DD3FC' : '#0891B2',
      Superseded: isDark ? '#94A3B8' : '#94A3B8',
    },
  };
};

const GlassTooltip = ({ active, payload, label, suffix = '' }) => {
  if (!active || !payload || !payload.length) return null;
  return (
    <div className="glass-strong rounded-lg border border-border/60 px-3 py-2 text-xs shadow-xl">
      {label !== undefined && (
        <p className="mb-1 font-display font-semibold text-foreground">{label}</p>
      )}
      {payload.map((p) => (
        <p key={p.name} className="flex items-center gap-2 text-muted-foreground">
          <span className="h-2 w-2 rounded-full" style={{ background: p.color || p.fill }} />
          <span className="text-foreground/90">{p.name}</span>
          <span className="ml-auto font-mono font-semibold text-foreground">
            {p.value}
            {suffix}
          </span>
        </p>
      ))}
    </div>
  );
};

const ActiveShape = (props) => {
  const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, fill } = props;
  return (
    <Sector
      cx={cx}
      cy={cy}
      innerRadius={innerRadius}
      outerRadius={outerRadius + 8}
      startAngle={startAngle}
      endAngle={endAngle}
      fill={fill}
      style={{ filter: `drop-shadow(0 0 10px ${fill})` }}
    />
  );
};

export const ChartsPanel = ({ stats }) => {
  const c = useColors();
  const [activeCatIdx, setActiveCatIdx] = useState(null);
  const [activeStatusIdx, setActiveStatusIdx] = useState(null);
  if (!stats) return null;

  // ---- derive datasets ----
  const timeline = (stats.timeline || []).map((t) => ({
    year: t.year,
    'New laws': t.count,
    Cumulative: t.cumulative,
  }));
  const peak = timeline.reduce((m, t) => (t['New laws'] > (m?.['New laws'] || 0) ? t : m), null);
  const total = stats.total_laws;

  const categoryData = Object.entries(stats.by_category || {})
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);
  const catTotal = categoryData.reduce((s, d) => s + d.value, 0);
  const maxCat = Math.max(...categoryData.map((d) => d.value), 1);
  const radialData = categoryData.map((d, i) => ({
    ...d,
    fill: c.palette[i % c.palette.length],
  }));
  const activeCat = activeCatIdx != null ? categoryData[activeCatIdx] : null;

  const regionData = Object.entries(stats.by_region || {})
    .map(([region, value]) => ({ region, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 7);

  const statusOrder = ['Enacted', 'Proposed', 'Draft', 'Superseded'];
  const statusData = statusOrder
    .filter((s) => stats.by_status?.[s])
    .map((name) => ({ name, value: stats.by_status[name] }));
  const statusTotal = statusData.reduce((s, d) => s + d.value, 0);
  const activeStatus = activeStatusIdx != null ? statusData[activeStatusIdx] : null;

  const levelOrder = ['Federal', 'State', 'City', 'National', 'International'];
  const levelData = (stats.level_status || [])
    .slice()
    .sort((a, b) => levelOrder.indexOf(a.level) - levelOrder.indexOf(b.level))
    .map((d) => ({
      level: d.level,
      Enacted: d.Enacted || 0,
      Proposed: (d.Proposed || 0) + (d.Draft || 0),
      total: (d.Enacted || 0) + (d.Proposed || 0) + (d.Draft || 0) + (d.Superseded || 0),
    }));

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-6">
      {/* ============ HERO: The rise of AI regulation ============ */}
      <motion.div {...reveal} transition={{ duration: 0.5 }} className="lg:col-span-6">
        <Card className="glass glass-interactive relative overflow-hidden rounded-2xl p-5">
          <div className="mb-4 flex flex-wrap items-start justify-between gap-4">
            <div className="flex items-start gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/15 text-primary">
                <TrendingUp className="h-5 w-5" />
              </span>
              <div>
                <h3 className="font-display text-base font-semibold text-foreground">
                  The rise of AI regulation
                </h3>
                <p className="text-xs text-muted-foreground">
                  New laws enacted each year and the cumulative global total
                </p>
              </div>
            </div>
            <div className="flex items-center gap-5">
              <div className="text-right">
                <div className="font-display text-2xl font-bold tabular-nums text-foreground">
                  <AnimatedNumber value={total} />
                </div>
                <div className="text-[11px] uppercase tracking-wide text-muted-foreground">Total tracked</div>
              </div>
              {peak && (
                <div className="hidden text-right sm:block">
                  <div className="font-display text-2xl font-bold tabular-nums text-primary">
                    {peak.year}
                  </div>
                  <div className="text-[11px] uppercase tracking-wide text-muted-foreground">
                    Peak year · {peak['New laws']} laws
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="chart-neon">
            <ResponsiveContainer width="100%" height={280}>
              <ComposedChart data={timeline} margin={{ top: 10, right: 8, left: -16, bottom: 0 }}>
                <defs>
                  <linearGradient id="cumFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={c.glow} stopOpacity={0.5} />
                    <stop offset="100%" stopColor={c.glow} stopOpacity={0.02} />
                  </linearGradient>
                  <linearGradient id="barFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={c.glow2} stopOpacity={0.95} />
                    <stop offset="100%" stopColor={c.glow2} stopOpacity={0.35} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={c.grid} vertical={false} />
                <XAxis dataKey="year" stroke={c.axis} fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke={c.axis} fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
                <Tooltip content={<GlassTooltip />} cursor={{ fill: c.grid }} />
                <Bar
                  dataKey="New laws"
                  barSize={16}
                  radius={[4, 4, 0, 0]}
                  fill="url(#barFill)"
                  isAnimationActive={false}
                />
                <Area
                  type="monotone"
                  dataKey="Cumulative"
                  stroke="none"
                  fill="url(#cumFill)"
                  isAnimationActive={false}
                />
                <Line
                  type="monotone"
                  dataKey="Cumulative"
                  stroke={c.glow}
                  strokeWidth={2.5}
                  dot={false}
                  activeDot={{ r: 5, fill: c.glow, stroke: 'transparent' }}
                  isAnimationActive={false}
                />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </motion.div>

      {/* ============ Category radial bars ============ */}
      <motion.div {...reveal} transition={{ duration: 0.5, delay: 0.06 }} className="lg:col-span-2">
        <Card className="glass glass-interactive h-full rounded-2xl p-5">
          <div className="mb-2 flex items-center gap-2">
            <Layers className="h-4 w-4 text-primary" />
            <h3 className="font-display text-sm font-semibold text-foreground">Top categories</h3>
          </div>
          <div className="relative chart-neon">
            <ResponsiveContainer width="100%" height={200}>
              <RadialBarChart
                data={radialData}
                innerRadius="32%"
                outerRadius="105%"
                startAngle={90}
                endAngle={-270}
                barSize={9}
              >
                <PolarAngleAxis type="number" domain={[0, maxCat]} tick={false} />
                <RadialBar
                  dataKey="value"
                  cornerRadius={6}
                  background={{ fill: c.track }}
                  isAnimationActive={false}
                  onMouseEnter={(_, i) => setActiveCatIdx(i)}
                  onMouseLeave={() => setActiveCatIdx(null)}
                >
                  {radialData.map((entry, i) => (
                    <Cell
                      key={i}
                      fill={entry.fill}
                      opacity={activeCatIdx == null || activeCatIdx === i ? 1 : 0.35}
                    />
                  ))}
                </RadialBar>
                <Tooltip content={<GlassTooltip />} />
              </RadialBarChart>
            </ResponsiveContainer>
            <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
              <span className="font-display text-2xl font-bold tabular-nums text-foreground">
                {activeCat ? activeCat.value : <AnimatedNumber value={catTotal} />}
              </span>
              <span className="max-w-[100px] truncate text-center text-[10px] text-muted-foreground">
                {activeCat ? activeCat.name : 'top 8 areas'}
              </span>
            </div>
          </div>
          <div className="mt-3 space-y-1">
            {categoryData.map((entry, i) => {
              const pct = Math.round((entry.value / catTotal) * 100);
              return (
                <button
                  key={entry.name}
                  onMouseEnter={() => setActiveCatIdx(i)}
                  onMouseLeave={() => setActiveCatIdx(null)}
                  className={`flex w-full items-center gap-2 rounded-md px-2 py-1 text-left text-xs transition-colors ${
                    activeCatIdx === i ? 'bg-secondary' : 'hover:bg-secondary/60'
                  }`}
                >
                  <span
                    className="h-2.5 w-2.5 shrink-0 rounded-full"
                    style={{ background: c.palette[i % c.palette.length] }}
                  />
                  <span className="flex-1 truncate text-foreground/90">{entry.name}</span>
                  <span className="font-mono text-muted-foreground">{entry.value}</span>
                  <span className="w-8 text-right font-mono text-[10px] text-muted-foreground/70">{pct}%</span>
                </button>
              );
            })}
          </div>
        </Card>
      </motion.div>

      {/* ============ Regional footprint radar ============ */}
      <motion.div {...reveal} transition={{ duration: 0.5, delay: 0.12 }} className="lg:col-span-2">
        <Card className="glass glass-interactive h-full rounded-2xl p-5">
          <div className="mb-1 flex items-center gap-2">
            <Compass className="h-4 w-4 text-primary" />
            <h3 className="font-display text-sm font-semibold text-foreground">Regional footprint</h3>
          </div>
          <p className="mb-1 text-xs text-muted-foreground">Laws tracked across world regions</p>
          <div className="chart-neon">
            <ResponsiveContainer width="100%" height={278}>
              <RadarChart data={regionData} outerRadius="72%">
                <defs>
                  <radialGradient id="radarFill" cx="50%" cy="50%" r="65%">
                    <stop offset="0%" stopColor={c.glow} stopOpacity={0.5} />
                    <stop offset="100%" stopColor={c.glow2} stopOpacity={0.15} />
                  </radialGradient>
                </defs>
                <PolarGrid />
                <PolarAngleAxis
                  dataKey="region"
                  tick={{ fill: c.axis, fontSize: 10 }}
                />
                <PolarRadiusAxis tick={false} axisLine={false} />
                <Radar
                  name="Laws"
                  dataKey="value"
                  stroke={c.glow}
                  strokeWidth={2}
                  fill="url(#radarFill)"
                  fillOpacity={1}
                  isAnimationActive={false}
                  dot={{ r: 3, fill: c.glow, stroke: 'transparent' }}
                />
                <Tooltip content={<GlassTooltip />} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </motion.div>

      {/* ============ Status mix donut ============ */}
      <motion.div {...reveal} transition={{ duration: 0.5, delay: 0.18 }} className="lg:col-span-2">
        <Card className="glass glass-interactive h-full rounded-2xl p-5">
          <div className="mb-1 flex items-center gap-2">
            <Activity className="h-4 w-4 text-primary" />
            <h3 className="font-display text-sm font-semibold text-foreground">Status mix</h3>
          </div>
          <p className="mb-1 text-xs text-muted-foreground">Where the world's AI laws stand</p>
          <div className="relative chart-neon">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={statusData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={54}
                  outerRadius={82}
                  paddingAngle={3}
                  cornerRadius={5}
                  stroke="none"
                  activeIndex={activeStatusIdx ?? undefined}
                  activeShape={ActiveShape}
                  onMouseEnter={(_, i) => setActiveStatusIdx(i)}
                  onMouseLeave={() => setActiveStatusIdx(null)}
                  isAnimationActive={false}
                >
                  {statusData.map((entry) => (
                    <Cell key={entry.name} fill={c.status[entry.name] || c.palette[0]} />
                  ))}
                </Pie>
                <Tooltip content={<GlassTooltip />} />
              </PieChart>
            </ResponsiveContainer>
            <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
              <span className="font-display text-2xl font-bold tabular-nums text-foreground">
                {activeStatus ? activeStatus.value : <AnimatedNumber value={statusTotal} />}
              </span>
              <span className="text-[10px] text-muted-foreground">
                {activeStatus ? activeStatus.name : 'total laws'}
              </span>
            </div>
          </div>
          <div className="mt-3 grid grid-cols-2 gap-1.5">
            {statusData.map((entry, i) => {
              const pct = Math.round((entry.value / statusTotal) * 100);
              return (
                <button
                  key={entry.name}
                  onMouseEnter={() => setActiveStatusIdx(i)}
                  onMouseLeave={() => setActiveStatusIdx(null)}
                  className={`flex items-center gap-2 rounded-md px-2 py-1 text-left text-xs transition-colors ${
                    activeStatusIdx === i ? 'bg-secondary' : 'hover:bg-secondary/60'
                  }`}
                >
                  <span
                    className="h-2.5 w-2.5 shrink-0 rounded-full"
                    style={{ background: c.status[entry.name] || c.palette[0] }}
                  />
                  <span className="flex-1 truncate text-foreground/90">{entry.name}</span>
                  <span className="font-mono text-[10px] text-muted-foreground/70">{pct}%</span>
                </button>
              );
            })}
          </div>
        </Card>
      </motion.div>

      {/* ============ Coverage by government level ============ */}
      <motion.div {...reveal} transition={{ duration: 0.5, delay: 0.24 }} className="lg:col-span-6">
        <Card className="glass glass-interactive rounded-2xl p-5">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Landmark className="h-4 w-4 text-primary" />
              <div>
                <h3 className="font-display text-sm font-semibold text-foreground">
                  Coverage by government level
                </h3>
                <p className="text-xs text-muted-foreground">
                  Federal, state, city, national &amp; international — enacted vs. proposed
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4 text-xs">
              <span className="flex items-center gap-1.5 text-muted-foreground">
                <span className="h-2.5 w-2.5 rounded-full" style={{ background: c.status.Enacted }} />
                Enacted
              </span>
              <span className="flex items-center gap-1.5 text-muted-foreground">
                <span className="h-2.5 w-2.5 rounded-full" style={{ background: c.status.Proposed }} />
                Proposed / pending
              </span>
            </div>
          </div>
          <div className="chart-neon">
            <ResponsiveContainer width="100%" height={Math.max(160, levelData.length * 46)}>
              <BarChart
                data={levelData}
                layout="vertical"
                margin={{ top: 0, right: 16, left: 8, bottom: 0 }}
                barCategoryGap={14}
              >
                <CartesianGrid strokeDasharray="3 3" stroke={c.grid} horizontal={false} />
                <XAxis type="number" stroke={c.axis} fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
                <YAxis
                  type="category"
                  dataKey="level"
                  stroke={c.axis}
                  fontSize={12}
                  width={82}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip content={<GlassTooltip />} cursor={{ fill: c.grid }} />
                <Bar dataKey="Enacted" stackId="a" fill={c.status.Enacted} radius={[4, 0, 0, 4]} isAnimationActive={false} barSize={20} />
                <Bar dataKey="Proposed" stackId="a" fill={c.status.Proposed} radius={[0, 4, 4, 0]} isAnimationActive={false} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </motion.div>
    </div>
  );
};
