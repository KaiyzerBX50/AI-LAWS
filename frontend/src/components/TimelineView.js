import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { getLaws } from '@/lib/api';
import { StatusBadge } from '@/components/StatusBadge';
import { Skeleton } from '@/components/ui/skeleton';
import { MapPin } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const TimelineView = ({ onOpenLaw }) => {
  const [laws, setLaws] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLaws({ sort: 'newest', limit: 1000 })
      .then((d) => setLaws(d.laws))
      .finally(() => setLoading(false));
  }, []);

  const grouped = laws.reduce((acc, law) => {
    (acc[law.year] = acc[law.year] || []).push(law);
    return acc;
  }, {});
  const years = Object.keys(grouped).sort((a, b) => b - a);

  if (loading) {
    return (
      <div className="space-y-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-24 w-full rounded-xl" />
        ))}
      </div>
    );
  }

  return (
    <div data-testid={TRACKER.timelineView} className="relative">
      <div className="absolute left-[19px] top-2 bottom-2 w-px bg-border sm:left-[27px]" />
      <div className="space-y-8">
        {years.map((year) => (
          <div key={year} className="relative">
            <div className="mb-4 flex items-center gap-3">
              <div className="z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border-2 border-primary bg-card font-display text-xs font-bold text-primary sm:h-14 sm:w-14 sm:text-sm">
                {year}
              </div>
              <span className="text-sm text-muted-foreground">
                {grouped[year].length} {grouped[year].length === 1 ? 'development' : 'developments'}
              </span>
            </div>
            <div className="ml-14 grid grid-cols-1 gap-3 sm:ml-20 lg:grid-cols-2">
              {grouped[year].map((law) => (
                <motion.button
                  key={law.id}
                  initial={{ opacity: 0, x: 8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.2 }}
                  onClick={() => onOpenLaw(law.id)}
                  className="rounded-lg glass p-3 text-left transition-shadow duration-200 hover:shadow-md hover:border-primary/40"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
                      <MapPin className="h-3 w-3 text-accent" />
                      {law.country}
                    </span>
                    <StatusBadge status={law.status} />
                  </div>
                  <h4 className="mt-2 font-display text-sm font-semibold leading-snug text-foreground">
                    {law.title}
                  </h4>
                </motion.button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
