import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  Sector,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import { Card } from '@/components/ui/card';
import { useTheme } from '@/lib/ThemeContext';

const PIE_COLORS = ['#1F7A8C', '#4FB6C8', '#0E7490', '#2A9D8F', '#E9A23B', '#8AB17D', '#457B9D', '#9FD3E6'];

const reveal = {
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, amount: 0.2 },
};

// Enlarged, glowing active sector for the donut
const ActiveShape = (props) => {
  const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, fill } = props;
  return (
    <g>
      <Sector cx={cx} cy={cy} innerRadius={innerRadius} outerRadius={outerRadius + 7}
        startAngle={startAngle} endAngle={endAngle} fill={fill}
        style={{ filter: `drop-shadow(0 0 8px ${fill})` }} />
    </g>
  );
};

export const ChartsPanel = ({ stats }) => {
  const { isDark } = useTheme();
  const [active, setActive] = useState(null);
  if (!stats) return null;

  const axis = isDark ? '#94A3B8' : '#64748B';
  const grid = isDark ? '#243244' : '#E2E8F0';
  const tooltipStyle = {
    background: isDark ? 'hsl(222 40% 9%)' : '#fff',
    border: `1px solid ${grid}`,
    borderRadius: 10,
    fontSize: 12,
    boxShadow: '0 8px 30px -12px rgba(0,0,0,0.4)',
    color: isDark ? '#E2E8F0' : '#0f172a',
  };

  const categoryData = Object.entries(stats.by_category)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value);
  const catTotal = categoryData.reduce((s, d) => s + d.value, 0);
  const activeCat = active != null ? categoryData[active] : null;

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
      {/* Timeline */}
      <motion.div {...reveal} transition={{ duration: 0.5 }} className="lg:col-span-2">
        <Card className="glass rounded-2xl p-4 h-full">
          <h3 className="mb-3 font-display text-sm font-semibold text-foreground">
            Cumulative AI laws over time
          </h3>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={stats.timeline} margin={{ top: 5, right: 10, left: -18, bottom: 0 }}>
              <defs>
                <linearGradient id="cum" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={isDark ? '#67E8F9' : '#1F7A8C'} stopOpacity={0.55} />
                  <stop offset="95%" stopColor={isDark ? '#67E8F9' : '#1F7A8C'} stopOpacity={0.04} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke={grid} vertical={false} />
              <XAxis dataKey="year" stroke={axis} fontSize={11} tickLine={false} />
              <YAxis stroke={axis} fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Area type="monotone" dataKey="cumulative" name="Total tracked"
                stroke={isDark ? '#67E8F9' : '#1F7A8C'} strokeWidth={2.5} fill="url(#cum)"
                animationDuration={1400} dot={{ r: 2.5, strokeWidth: 0, fill: isDark ? '#67E8F9' : '#1F7A8C' }}
                activeDot={{ r: 5 }} />
            </AreaChart>
          </ResponsiveContainer>
        </Card>
      </motion.div>

      {/* Category donut + custom legend */}
      <motion.div {...reveal} transition={{ duration: 0.5, delay: 0.08 }}>
        <Card className="glass rounded-2xl p-4 h-full">
          <h3 className="mb-1 font-display text-sm font-semibold text-foreground">Top categories</h3>
          <p className="mb-2 text-xs text-muted-foreground">Share of tracked laws by focus area</p>
          <div className="relative">
            <ResponsiveContainer width="100%" height={190}>
              <PieChart>
                <defs>
                  {PIE_COLORS.map((c, i) => (
                    <radialGradient key={i} id={`pie-${i}`} cx="50%" cy="50%" r="75%">
                      <stop offset="0%" stopColor={c} stopOpacity={0.85} />
                      <stop offset="100%" stopColor={c} stopOpacity={1} />
                    </radialGradient>
                  ))}
                </defs>
                <Pie
                  data={categoryData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={52}
                  outerRadius={80}
                  paddingAngle={3}
                  cornerRadius={4}
                  stroke="none"
                  activeIndex={active ?? undefined}
                  activeShape={ActiveShape}
                  onMouseEnter={(_, i) => setActive(i)}
                  onMouseLeave={() => setActive(null)}
                  animationDuration={900}
                >
                  {categoryData.map((entry, i) => (
                    <Cell key={i} fill={`url(#pie-${i % PIE_COLORS.length})`} />
                  ))}
                </Pie>
                <Tooltip contentStyle={tooltipStyle} />
              </PieChart>
            </ResponsiveContainer>
            {/* center label */}
            <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
              <span className="font-display text-2xl font-bold tabular-nums text-foreground">
                {activeCat ? activeCat.value : catTotal}
              </span>
              <span className="max-w-[110px] truncate text-center text-[10px] text-muted-foreground">
                {activeCat ? activeCat.name : 'across categories'}
              </span>
            </div>
          </div>

          {/* interactive legend */}
          <div className="mt-3 space-y-1.5">
            {categoryData.map((entry, i) => {
              const pct = Math.round((entry.value / catTotal) * 100);
              return (
                <button
                  key={entry.name}
                  onMouseEnter={() => setActive(i)}
                  onMouseLeave={() => setActive(null)}
                  className={`flex w-full items-center gap-2 rounded-md px-2 py-1 text-left text-xs transition-colors ${
                    active === i ? 'bg-secondary' : 'hover:bg-secondary/60'
                  }`}
                >
                  <span className="h-2.5 w-2.5 shrink-0 rounded-full"
                    style={{ background: PIE_COLORS[i % PIE_COLORS.length] }} />
                  <span className="flex-1 truncate text-foreground/90">{entry.name}</span>
                  <span className="font-mono text-muted-foreground">{entry.value}</span>
                  <span className="w-8 text-right font-mono text-[10px] text-muted-foreground/70">{pct}%</span>
                </button>
              );
            })}
          </div>
        </Card>
      </motion.div>

      {/* Region status stacked bar */}
      <motion.div {...reveal} transition={{ duration: 0.5, delay: 0.12 }} className="lg:col-span-3">
        <Card className="glass rounded-2xl p-4">
          <h3 className="mb-3 font-display text-sm font-semibold text-foreground">
            Regulatory status by region
          </h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={stats.region_status} margin={{ top: 5, right: 10, left: -18, bottom: 0 }}>
              <defs>
                <linearGradient id="bEnacted" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={isDark ? '#67E8F9' : '#2AA0B3'} />
                  <stop offset="100%" stopColor="#1F7A8C" />
                </linearGradient>
                <linearGradient id="bProposed" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#F6C065" />
                  <stop offset="100%" stopColor="#E9A23B" />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke={grid} vertical={false} />
              <XAxis dataKey="region" stroke={axis} fontSize={11} tickLine={false} />
              <YAxis stroke={axis} fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
              <Tooltip contentStyle={tooltipStyle} cursor={{ fill: isDark ? '#ffffff10' : '#00000008' }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="Enacted" stackId="a" fill="url(#bEnacted)" animationDuration={1100} />
              <Bar dataKey="Proposed" stackId="a" fill="url(#bProposed)" animationDuration={1100} />
              <Bar dataKey="Draft" stackId="a" fill="#64748B" animationDuration={1100} />
              <Bar dataKey="Superseded" stackId="a" fill="#94A3B8" radius={[5, 5, 0, 0]} animationDuration={1100} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </motion.div>
    </div>
  );
};
