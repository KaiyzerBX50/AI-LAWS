import React, { useEffect, useState } from 'react';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { StatusBadge } from '@/components/StatusBadge';
import { getUsStateDetail } from '@/lib/api';
import { ArrowRight } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const StatePanel = ({ stateName, open, onOpenChange, onOpenLaw }) => {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open && stateName) {
      setLoading(true);
      getUsStateDetail(stateName)
        .then(setDetail)
        .catch(() => setDetail(null))
        .finally(() => setLoading(false));
    }
  }, [open, stateName]);

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent data-testid={TRACKER.statePanel} className="w-full overflow-hidden p-0 sm:max-w-md">
        <ScrollArea className="h-full">
          <div className="p-6">
            <SheetHeader className="text-left">
              <SheetTitle className="font-display text-2xl">{stateName}</SheetTitle>
              <SheetDescription className="sr-only">AI laws for {stateName}</SheetDescription>
            </SheetHeader>
            {loading ? (
              <p className="mt-4 text-sm text-muted-foreground">Loading…</p>
            ) : !detail ? (
              <p className="mt-4 text-sm text-muted-foreground">No tracked AI laws for this state.</p>
            ) : (
              <>
                <p className="mt-2 text-sm text-muted-foreground">
                  {detail.total} tracked {detail.total === 1 ? 'law' : 'laws'}
                </p>
                <div className="mt-5 space-y-3">
                  {detail.laws.map((law) => (
                    <button key={law.id} onClick={() => onOpenLaw(law.id)}
                      className="group w-full rounded-lg border border-border bg-card p-3 text-left transition-shadow duration-200 hover:shadow-md hover:border-primary/40">
                      <div className="flex items-center justify-between gap-2">
                        <StatusBadge status={law.status} />
                        <span className="font-mono text-xs text-muted-foreground">{law.year}</span>
                      </div>
                      <h4 className="mt-2 font-display text-sm font-semibold leading-snug text-foreground">{law.title}</h4>
                      <p className="mt-1 line-clamp-2 text-xs text-muted-foreground">{law.summary}</p>
                      <span className="mt-2 inline-flex items-center gap-1 text-xs text-primary opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                        View details <ArrowRight className="h-3 w-3" />
                      </span>
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
};
