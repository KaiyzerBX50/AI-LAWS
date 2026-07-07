import React from 'react';
import { AnimatePresence } from 'framer-motion';
import { LawCard } from '@/components/LawCard';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { SearchX } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const BrowseGrid = ({ laws, loading, onOpen, onReset }) => {
  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-48 w-full rounded-xl" />
        ))}
      </div>
    );
  }

  if (!laws || laws.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 rounded-xl border border-dashed border-border bg-card py-16 text-center">
        <SearchX className="h-10 w-10 text-muted-foreground" />
        <p className="text-sm text-muted-foreground">
          No laws match your filters. Try broadening your search.
        </p>
        <Button variant="outline" size="sm" onClick={onReset}>
          Reset filters
        </Button>
      </div>
    );
  }

  return (
    <div
      data-testid={TRACKER.lawGrid}
      className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3"
    >
      <AnimatePresence mode="popLayout">
        {laws.map((law) => (
          <LawCard key={law.id} law={law} onOpen={onOpen} />
        ))}
      </AnimatePresence>
    </div>
  );
};
