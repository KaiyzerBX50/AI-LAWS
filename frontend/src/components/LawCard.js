import React from 'react';
import { motion } from 'framer-motion';
import { StatusBadge } from '@/components/StatusBadge';
import { MapPin, ArrowUpRight, Calendar } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const LawCard = ({ law, onOpen }) => {
  const place = law.jurisdiction || law.country;
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.22 }}
    >
      <div
        data-testid={TRACKER.lawCard}
        onClick={() => onOpen(law)}
        className="group glass hover-lift flex h-full cursor-pointer flex-col gap-3 rounded-2xl p-5"
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-1.5 text-sm font-medium text-muted-foreground">
            <MapPin className="h-3.5 w-3.5 text-accent" />
            {place}
          </div>
          <StatusBadge status={law.status} />
        </div>

        <h3 className="font-display text-base font-semibold leading-snug tracking-tight text-foreground">
          {law.title}
        </h3>

        <p className="line-clamp-3 text-sm leading-relaxed text-muted-foreground">
          {law.summary}
        </p>

        <div className="mt-auto flex items-center justify-between pt-2">
          <div className="flex items-center gap-2 text-xs">
            <span className="max-w-[150px] truncate rounded-md border border-border/60 bg-secondary/60 px-2 py-0.5 text-muted-foreground">
              {law.category}
            </span>
            <span className="flex items-center gap-1 font-mono text-muted-foreground">
              <Calendar className="h-3 w-3" />
              {law.year}
            </span>
          </div>
          <span
            data-testid={TRACKER.lawCardOpen}
            className="flex items-center gap-1 text-xs font-medium text-primary opacity-0 transition-opacity duration-200 group-hover:opacity-100"
          >
            Details <ArrowUpRight className="h-3 w-3" />
          </span>
        </div>
      </div>
    </motion.div>
  );
};
