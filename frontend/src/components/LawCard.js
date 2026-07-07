import React from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { StatusBadge } from '@/components/StatusBadge';
import { MapPin, ArrowUpRight, Calendar } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const LawCard = ({ law, onOpen }) => {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
    >
      <Card
        data-testid={TRACKER.lawCard}
        onClick={() => onOpen(law)}
        className="group flex h-full cursor-pointer flex-col gap-3 rounded-xl border bg-card p-5 shadow-sm transition-shadow duration-200 hover:shadow-md hover:border-primary/40"
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-1.5 text-sm font-medium text-muted-foreground">
            <MapPin className="h-3.5 w-3.5 text-accent" />
            {law.country}
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
            <span className="rounded-md border border-border bg-secondary px-2 py-0.5 text-muted-foreground">
              {law.category}
            </span>
            <span className="flex items-center gap-1 font-mono text-muted-foreground">
              <Calendar className="h-3 w-3" />
              {law.year}
            </span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            data-testid={TRACKER.lawCardOpen}
            className="h-7 gap-1 px-2 text-xs text-primary opacity-0 transition-opacity duration-200 group-hover:opacity-100"
            onClick={(e) => {
              e.stopPropagation();
              onOpen(law);
            }}
          >
            Details <ArrowUpRight className="h-3 w-3" />
          </Button>
        </div>
      </Card>
    </motion.div>
  );
};
