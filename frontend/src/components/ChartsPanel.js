import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import { Card } from '@/components/ui/card';
import { useTheme } from '@/lib/ThemeContext';

const PIE_COLORS = ['#1F7A8C', '#4FB6C8', '#0E7490', '#2A9D8F', '#E9A23B', '#8AB17D', '#457B9D', '#9FD3E6'];

export const ChartsPanel = ({ stats }) => {
  const { isDark } = useTheme();
  if (!stats) return null;

  const axis = isDark ? '#94A3B8' : '#64748B';
  const grid = isDark ? '#243244' : '#E2E8F0';
  const tooltipStyle = {
    background: isDark ? 'hsl(222 35% 10%)' : '#fff',
    border: `1px solid ${grid}`,
    borderRadius: 8,
    fontSize: 12,
    color: isDark ? '#E2E8F0' : '#0f172a',
  };

  const categoryData = Object.entries(stats.by_category).map(([name, value]) => ({ name, value }));

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
      <Card className="rounded-xl border bg-card p-4 shadow-sm lg:col-span-2">
        <h3 className="mb-3 font-display text-sm font-semibold text-foreground">
          Cumulative AI laws over time
        </h3>
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={stats.timeline} margin={{ top: 5, right: 10, left: -18, bottom: 0 }}>
            <defs>
              <linearGradient id="cum" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#1F7A8C" stopOpacity={0.5} />
                <stop offset="95%" stopColor="#1F7A8C" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke={grid} vertical={false} />
            <XAxis dataKey="year" stroke={axis} fontSize={11} tickLine={false} />
            <YAxis stroke={axis} fontSize={11} tickLine={false} axisLine={false} />
            <Tooltip contentStyle={tooltipStyle} />
            <Area type="monotone" dataKey="cumulative" name="Total tracked" stroke="#1F7A8C"
              strokeWidth={2} fill="url(#cum)" />
          </AreaChart>
        </ResponsiveContainer>
      </Card>

      <Card className="rounded-xl border bg-card p-4 shadow-sm">
        <h3 className="mb-3 font-display text-sm font-semibold text-foreground">By category</h3>
        <ResponsiveContainer width="100%" height={220}>
          <PieChart>
            <Pie data={categoryData} dataKey="value" nameKey="name" cx="50%" cy="50%"
              innerRadius={45} outerRadius={75} paddingAngle={2}>
              {categoryData.map((entry, i) => (
                <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} stroke="none" />
              ))}
            </Pie>
            <Tooltip contentStyle={tooltipStyle} />
          </PieChart>
        </ResponsiveContainer>
      </Card>

      <Card className="rounded-xl border bg-card p-4 shadow-sm lg:col-span-3">
        <h3 className="mb-3 font-display text-sm font-semibold text-foreground">
          Regulatory status by region
        </h3>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={stats.region_status} margin={{ top: 5, right: 10, left: -18, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke={grid} vertical={false} />
            <XAxis dataKey="region" stroke={axis} fontSize={11} tickLine={false} />
            <YAxis stroke={axis} fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
            <Tooltip contentStyle={tooltipStyle} cursor={{ fill: isDark ? '#ffffff10' : '#00000008' }} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="Enacted" stackId="a" fill="#1F7A8C" radius={[0, 0, 0, 0]} />
            <Bar dataKey="Proposed" stackId="a" fill="#E9A23B" />
            <Bar dataKey="Draft" stackId="a" fill="#64748B" />
            <Bar dataKey="Superseded" stackId="a" fill="#94A3B8" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );
};
