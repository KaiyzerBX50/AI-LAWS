import React, { useEffect, useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { StatusBadge } from '@/components/StatusBadge';
import { getLawById } from '@/lib/api';
import { MapPin, ExternalLink, Building2, Calendar, Layers, Link2 } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const LawDetailDialog = ({ lawId, open, onOpenChange, onSelectRelated }) => {
  const [law, setLaw] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open && lawId) {
      setLoading(true);
      getLawById(lawId)
        .then(setLaw)
        .catch(() => setLaw(null))
        .finally(() => setLoading(false));
    }
  }, [open, lawId]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        data-testid={TRACKER.lawDetailDialog}
        className="max-h-[88vh] max-w-2xl overflow-hidden p-0"
      >
        {loading || !law ? (
          <div className="p-8 text-sm text-muted-foreground">Loading law details…</div>
        ) : (
          <ScrollArea className="max-h-[88vh]">
            <div className="p-6">
              <DialogHeader className="space-y-3 text-left">
                <div className="flex flex-wrap items-center gap-2">
                  <StatusBadge status={law.status} />
                  <span className="rounded-md border border-border bg-secondary px-2 py-0.5 text-xs text-muted-foreground">
                    {law.category}
                  </span>
                </div>
                <DialogTitle className="font-display text-xl leading-snug">
                  {law.title}
                </DialogTitle>
                <DialogDescription className="sr-only">
                  Details, key provisions and sources for {law.title} ({law.country})
                </DialogDescription>
              </DialogHeader>

              <div className="mt-4 grid grid-cols-1 gap-2 rounded-lg border border-border bg-secondary/50 p-3 text-sm sm:grid-cols-2">
                <Meta icon={MapPin} label="Jurisdiction" value={law.country} />
                <Meta icon={Calendar} label="Year" value={law.year} />
                <Meta icon={Layers} label="Region" value={law.region} />
                <Meta icon={Building2} label="Authority" value={law.authority} />
              </div>

              <Section title="Overview">
                <p className="text-sm leading-relaxed text-foreground/90">{law.summary}</p>
              </Section>

              {law.key_provisions?.length > 0 && (
                <Section title="Key provisions">
                  <ul className="space-y-2">
                    {law.key_provisions.map((p, i) => (
                      <li key={i} className="flex gap-2 text-sm leading-relaxed">
                        <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
                        <span className="text-foreground/90">{p}</span>
                      </li>
                    ))}
                  </ul>
                </Section>
              )}

              {law.sources?.length > 0 && (
                <Section title="Official sources">
                  <div className="space-y-2" data-testid={TRACKER.lawSourceLinks}>
                    {law.sources.map((s, i) => (
                      <a
                        key={i}
                        href={s.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 rounded-md border border-border bg-card px-3 py-2 text-sm text-primary transition-colors duration-200 hover:bg-secondary"
                      >
                        <Link2 className="h-3.5 w-3.5 shrink-0" />
                        <span className="flex-1 truncate">{s.title}</span>
                        <ExternalLink className="h-3.5 w-3.5 shrink-0 opacity-60" />
                      </a>
                    ))}
                  </div>
                </Section>
              )}

              {law.related?.length > 0 && (
                <Section title="Related laws">
                  <div className="flex flex-wrap gap-2">
                    {law.related.map((r) => (
                      <button
                        key={r.id}
                        onClick={() => onSelectRelated && onSelectRelated(r.id)}
                        className="rounded-full border border-border bg-secondary px-3 py-1 text-xs text-foreground transition-colors duration-200 hover:border-primary/50 hover:text-primary"
                      >
                        {r.country}: {r.title.length > 40 ? r.title.slice(0, 40) + '…' : r.title}
                      </button>
                    ))}
                  </div>
                </Section>
              )}
            </div>
          </ScrollArea>
        )}
      </DialogContent>
    </Dialog>
  );
};

const Meta = ({ icon: Icon, label, value }) => (
  <div className="flex items-center gap-2">
    <Icon className="h-3.5 w-3.5 text-accent" />
    <span className="text-muted-foreground">{label}:</span>
    <span className="font-medium text-foreground">{value}</span>
  </div>
);

const Section = ({ title, children }) => (
  <div className="mt-5">
    <Separator className="mb-4" />
    <h4 className="mb-2 font-display text-sm font-semibold uppercase tracking-wide text-muted-foreground">
      {title}
    </h4>
    {children}
  </div>
);
