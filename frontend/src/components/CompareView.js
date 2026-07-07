import React, { useEffect, useState } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { StatusBadge } from '@/components/StatusBadge';
import { getMeta, getLaws } from '@/lib/api';
import { X, Plus, GitCompareArrows } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const CompareView = ({ onOpenLaw }) => {
  const [countries, setCountries] = useState([]);
  const [selected, setSelected] = useState([]);
  const [dataByCountry, setDataByCountry] = useState({});
  const [pick, setPick] = useState('');

  useEffect(() => {
    getMeta().then((m) => setCountries(m.countries || []));
  }, []);

  const addCountry = (name) => {
    if (!name || selected.includes(name) || selected.length >= 3) return;
    setSelected((s) => [...s, name]);
    setPick('');
    if (!dataByCountry[name]) {
      getLaws({ country: name, sort: 'newest', limit: 500 }).then((d) =>
        setDataByCountry((prev) => ({ ...prev, [name]: d.laws }))
      );
    }
  };

  const removeCountry = (name) =>
    setSelected((s) => s.filter((c) => c !== name));

  const available = countries.filter((c) => !selected.includes(c));

  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-3 rounded-xl border border-border bg-card p-4 shadow-sm sm:flex-row sm:items-center">
        <div className="flex items-center gap-2 text-sm font-medium text-foreground">
          <GitCompareArrows className="h-4 w-4 text-accent" />
          Compare jurisdictions
          <span className="text-muted-foreground">(up to 3)</span>
        </div>
        <div className="flex flex-1 items-center gap-2">
          <Select value={pick} onValueChange={addCountry} disabled={selected.length >= 3}>
            <SelectTrigger data-testid={TRACKER.compareSelect} className="w-full sm:max-w-xs">
              <SelectValue placeholder="Add a country…" />
            </SelectTrigger>
            <SelectContent>
              {available.map((c) => (
                <SelectItem key={c} value={c}>{c}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {selected.length === 0 ? (
        <div className="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-border bg-card py-16 text-center">
          <Plus className="h-8 w-8 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            Select two or three countries to compare their AI regulatory approaches.
          </p>
        </div>
      ) : (
        <div
          data-testid={TRACKER.compareTable}
          className="grid gap-4"
          style={{ gridTemplateColumns: `repeat(${selected.length}, minmax(0, 1fr))` }}
        >
          {selected.map((name) => {
            const laws = dataByCountry[name] || [];
            const enacted = laws.filter((l) => l.status === 'Enacted').length;
            const proposed = laws.filter((l) => ['Proposed', 'Draft'].includes(l.status)).length;
            return (
              <Card key={name} className="flex flex-col rounded-xl border bg-card p-4 shadow-sm">
                <div className="flex items-start justify-between gap-2">
                  <h3 className="font-display text-base font-semibold text-foreground">{name}</h3>
                  <Button variant="ghost" size="icon" className="h-6 w-6"
                    onClick={() => removeCountry(name)} aria-label={`Remove ${name}`}>
                    <X className="h-4 w-4" />
                  </Button>
                </div>
                <div className="mt-2 flex gap-4 text-xs text-muted-foreground">
                  <span><b className="text-foreground">{enacted}</b> enacted</span>
                  <span><b className="text-foreground">{proposed}</b> proposed</span>
                </div>
                <div className="mt-3 space-y-2">
                  {laws.map((law) => (
                    <button
                      key={law.id}
                      onClick={() => onOpenLaw(law.id)}
                      className="w-full rounded-md border border-border bg-secondary/40 p-2 text-left transition-colors duration-200 hover:bg-secondary"
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-mono text-[11px] text-muted-foreground">{law.year}</span>
                        <StatusBadge status={law.status} />
                      </div>
                      <p className="mt-1 text-xs font-medium leading-snug text-foreground">{law.title}</p>
                    </button>
                  ))}
                  {laws.length === 0 && (
                    <p className="text-xs text-muted-foreground">Loading…</p>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
