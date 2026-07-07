import React from 'react';
import { AnimatePresence } from 'framer-motion';
import { LawCard } from '@/components/LawCard';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { SearchX, Plus, Loader2 } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const BrowseGrid = ({ laws, loading, loadingMore, hasMore, onOpen, onReset, onLoadMore }) => {
  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-48 w-full rounded-2xl" />
        ))}
      </div>
    );
  }

  if (!laws || laws.length === 0) {
    return (
      <div className="glass flex flex-col items-center justify-center gap-3 rounded-2xl py-16 text-center">
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
    <div className="space-y-6">
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

      {hasMore && (
        <div className="flex justify-center">
          <Button
            variant="outline"
            onClick={onLoadMore}
            disabled={loadingMore}
            data-testid={TRACKER.loadMore}
            className="gap-2 glass border-border/60"
          >
            {loadingMore ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" /> Loading…
              </>
            ) : (
              <>
                <Plus className="h-4 w-4" /> Load more
              </>
            )}
          </Button>
        </div>
      )}
    </div>
  );
};
