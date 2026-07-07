import React, { useEffect, useState } from 'react';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { StatusBadge } from '@/components/StatusBadge';
import { getCountryDetail } from '@/lib/api';
import { MATURITY_BINS } from '@/lib/lawUtils';
import { useTheme } from '@/lib/ThemeContext';
import { ArrowRight } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const CountryPanel = ({ countryName, open, onOpenChange, onOpenLaw }) => {
  const { isDark } = useTheme();
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open && countryName) {
      setLoading(true);
      getCountryDetail(countryName)
        .then(setDetail)
        .catch(() => setDetail(null))
        .finally(() => setLoading(false));
    }
  }, [open, countryName]);

  const bin = detail ? MATURITY_BINS[detail.maturity] : MATURITY_BINS[0];

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        data-testid={TRACKER.countryPanel}
        className="w-full overflow-hidden p-0 sm:max-w-md"
      >
        <ScrollArea className="h-full">
          <div className="p-6">
            <SheetHeader className="text-left">
              <SheetTitle className="font-display text-2xl">{countryName}</SheetTitle>
              <SheetDescription className="sr-only">
                Tracked AI laws, acts and regulations for {countryName}
              </SheetDescription>
            </SheetHeader>

            {loading ? (
              <p className="mt-4 text-sm text-muted-foreground">Loading…</p>
            ) : !detail ? (
              <p className="mt-4 text-sm text-muted-foreground">
                No tracked AI laws for this country yet.
              </p>
            ) : (
              <>
                <div className="mt-3 flex items-center gap-2">
                  <span
                    className="h-3 w-3 rounded-sm"
                    style={{ background: isDark ? bin.dark : bin.light }}
                  />
                  <span className="text-sm font-medium text-foreground">
                    {detail.maturity_label}
                  </span>
                  <span className="text-sm text-muted-foreground">
                    · {detail.total} {detail.total === 1 ? 'entry' : 'entries'}
                  </span>
                </div>

                <div className="mt-5 space-y-3">
                  {detail.laws.map((law) => (
                    <button
                      key={law.id}
                      onClick={() => onOpenLaw(law.id)}
                      className="group w-full rounded-lg border border-border bg-card p-3 text-left transition-shadow duration-200 hover:shadow-md hover:border-primary/40"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <StatusBadge status={law.status} />
                        <span className="font-mono text-xs text-muted-foreground">{law.year}</span>
                      </div>
                      <h4 className="mt-2 font-display text-sm font-semibold leading-snug text-foreground">
                        {law.title}
                      </h4>
                      <p className="mt-1 line-clamp-2 text-xs text-muted-foreground">
                        {law.summary}
                      </p>
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
