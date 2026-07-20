import React from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { ScrollText, Globe2, CheckCircle2, Clock } from 'lucide-react';
import { AnimatedNumber } from '@/components/AnimatedNumber';
import { TRACKER } from '@/constants/testIds';

const StatCard = ({ icon: Icon, label, value, testId, accent, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 16, scale: 0.98 }}
    animate={{ opacity: 1, y: 0, scale: 1 }}
    transition={{ duration: 0.5, delay, ease: [0.16, 1, 0.3, 1] }}
  >
    <Card
      data-testid={testId}
      className="glass glass-shimmer hover-lift group relative flex items-center gap-4 overflow-hidden rounded-2xl p-4"
    >
      <div className={`flex h-11 w-11 items-center justify-center rounded-lg transition-transform duration-300 group-hover:scale-110 ${accent}`}>
        <Icon className="h-5 w-5" />
      </div>
      <div>
        <div className="font-display text-2xl font-semibold tabular-nums text-foreground">
          <AnimatedNumber value={value} />
        </div>
        <div className="text-xs text-muted-foreground">{label}</div>
      </div>
    </Card>
  </motion.div>
);

export const StatsRow = ({ stats }) => {
  if (!stats) return null;
  return (
    <div
      data-testid={TRACKER.statsDashboard}
      className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4"
    >
      <StatCard
        icon={ScrollText}
        label="Laws & frameworks tracked"
        value={stats.total_laws}
        testId={TRACKER.statTotalLaws}
        accent="bg-primary/10 text-primary"
        delay={0}
      />
      <StatCard
        icon={Globe2}
        label="Jurisdictions covered"
        value={stats.total_jurisdictions}
        testId={TRACKER.statJurisdictions}
        accent="bg-accent/10 text-accent"
        delay={0.05}
      />
      <StatCard
        icon={CheckCircle2}
        label="Enacted / in force"
        value={stats.enacted}
        testId={TRACKER.statEnacted}
        accent="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
        delay={0.1}
      />
      <StatCard
        icon={Clock}
        label="Proposed / draft"
        value={stats.proposed}
        testId={TRACKER.statProposed}
        accent="bg-amber-500/10 text-amber-600 dark:text-amber-400"
        delay={0.15}
      />
    </div>
  );
};
