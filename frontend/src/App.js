import React, { useEffect, useState, useCallback, useRef } from 'react';
import '@/App.css';
import { ThemeProvider } from '@/lib/ThemeContext';
import { ThemeToggle } from '@/components/ThemeToggle';
import { WorldMap } from '@/components/WorldMap';
import { CountryPanel } from '@/components/CountryPanel';
import { LawDetailDialog } from '@/components/LawDetailDialog';
import { StatsRow } from '@/components/StatsRow';
import { ChartsPanel } from '@/components/ChartsPanel';
import { FiltersBar } from '@/components/FiltersBar';
import { BrowseGrid } from '@/components/BrowseGrid';
import { TimelineView } from '@/components/TimelineView';
import { CompareView } from '@/components/CompareView';
import { AIAssistant } from '@/components/AIAssistant';
import { getMeta, getStats, getCountries, getLaws } from '@/lib/api';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Scale, Map, LayoutGrid, Clock, GitCompareArrows, Sparkle, ScrollText } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

const DEFAULT_FILTERS = { search: '', region: 'all', status: 'all', category: 'all', sort: 'newest' };

function Tracker() {
  const [meta, setMeta] = useState(null);
  const [stats, setStats] = useState(null);
  const [countries, setCountries] = useState(null);
  const [mapMode, setMapMode] = useState('maturity');
  const [tab, setTab] = useState('explore');

  // shared dialogs
  const [lawId, setLawId] = useState(null);
  const [lawOpen, setLawOpen] = useState(false);
  const [country, setCountry] = useState(null);
  const [countryOpen, setCountryOpen] = useState(false);

  // browse
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [laws, setLaws] = useState([]);
  const [lawsLoading, setLawsLoading] = useState(true);
  const debounceRef = useRef(null);

  useEffect(() => {
    getMeta().then(setMeta).catch(() => {});
    getStats().then(setStats).catch(() => {});
    getCountries().then(setCountries).catch(() => {});
  }, []);

  useEffect(() => {
    setLawsLoading(true);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      getLaws(filters)
        .then((d) => setLaws(d.laws))
        .finally(() => setLawsLoading(false));
    }, 250);
    return () => clearTimeout(debounceRef.current);
  }, [filters]);

  const openLaw = useCallback((law) => {
    const id = typeof law === 'string' ? law : law.id;
    setLawId(id);
    setLawOpen(true);
  }, []);

  const openCountry = useCallback((name) => {
    setCountry(name);
    setCountryOpen(true);
  }, []);

  const openLawFromPanel = (id) => {
    setCountryOpen(false);
    setTimeout(() => openLaw(id), 150);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur supports-[backdrop-filter]:bg-background/70">
        <div className="mx-auto flex max-w-[1200px] items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Scale className="h-5 w-5" />
            </div>
            <div>
              <h1 className="font-display text-base font-semibold leading-none tracking-tight text-foreground sm:text-lg">
                Global AI Law Tracker
              </h1>
              <p className="mt-0.5 text-xs text-muted-foreground">
                Worldwide AI laws, acts &amp; regulations
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span
              data-testid={TRACKER.dataFreshnessBadge}
              className="hidden items-center gap-1.5 rounded-full border border-border bg-secondary px-2.5 py-1 text-xs text-muted-foreground sm:inline-flex"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              {stats ? `${stats.total_laws} entries tracked` : 'Loading…'}
            </span>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="hero-gradient-light dark:hero-gradient-dark border-b border-border">
        <div className="mx-auto max-w-[1200px] px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
          <div className="max-w-2xl">
            <h2 className="font-display text-3xl font-semibold tracking-tight text-foreground sm:text-4xl lg:text-5xl">
              Track AI regulation across the world
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-muted-foreground sm:text-base">
              Explore an interactive map of AI laws, acts and governance frameworks — from the
              EU AI Act to national strategies — filter by status and region, follow the timeline,
              and ask the AI assistant.
            </p>
          </div>
          <div className="mt-6">
            <StatsRow stats={stats} />
          </div>
        </div>
      </section>

      {/* Main */}
      <main className="mx-auto max-w-[1200px] px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <Tabs value={tab} onValueChange={setTab} className="space-y-6">
          <TabsList className="flex h-auto w-full flex-wrap justify-start gap-1 bg-secondary p-1">
            <TabsTrigger value="explore" data-testid={TRACKER.navMap} className="gap-1.5">
              <Map className="h-4 w-4" /> Explore
            </TabsTrigger>
            <TabsTrigger value="browse" data-testid={TRACKER.navBrowse} className="gap-1.5">
              <LayoutGrid className="h-4 w-4" /> Browse
            </TabsTrigger>
            <TabsTrigger value="timeline" data-testid={TRACKER.navTimeline} className="gap-1.5">
              <Clock className="h-4 w-4" /> Timeline
            </TabsTrigger>
            <TabsTrigger value="compare" data-testid={TRACKER.navCompare} className="gap-1.5">
              <GitCompareArrows className="h-4 w-4" /> Compare
            </TabsTrigger>
            <TabsTrigger value="assistant" data-testid={TRACKER.navAssistant} className="gap-1.5">
              <Sparkle className="h-4 w-4" /> Assistant
            </TabsTrigger>
          </TabsList>

          {/* Explore: map + charts */}
          <TabsContent value="explore" className="space-y-6">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-display text-lg font-semibold tracking-tight text-foreground">
                World map
              </h3>
              <ToggleGroup
                type="single"
                value={mapMode}
                onValueChange={(v) => v && setMapMode(v)}
                data-testid={TRACKER.mapModeToggle}
                className="rounded-lg border border-border bg-card p-0.5"
              >
                <ToggleGroupItem value="maturity" className="h-7 px-3 text-xs">
                  Maturity
                </ToggleGroupItem>
                <ToggleGroupItem value="status" className="h-7 px-3 text-xs">
                  Status
                </ToggleGroupItem>
              </ToggleGroup>
            </div>
            <WorldMap countries={countries} mode={mapMode} onSelectCountry={openCountry} />
            <ChartsPanel stats={stats} />
          </TabsContent>

          {/* Browse */}
          <TabsContent value="browse" className="space-y-5">
            <FiltersBar
              meta={meta}
              filters={filters}
              setFilters={setFilters}
              onReset={() => setFilters(DEFAULT_FILTERS)}
            />
            <div className="flex items-center justify-between">
              <p className="text-sm text-muted-foreground">
                {lawsLoading ? 'Searching…' : `${laws.length} ${laws.length === 1 ? 'result' : 'results'}`}
              </p>
            </div>
            <BrowseGrid
              laws={laws}
              loading={lawsLoading}
              onOpen={openLaw}
              onReset={() => setFilters(DEFAULT_FILTERS)}
            />
          </TabsContent>

          {/* Timeline */}
          <TabsContent value="timeline">
            <div className="mb-5 flex items-center gap-2">
              <ScrollText className="h-5 w-5 text-accent" />
              <h3 className="font-display text-lg font-semibold tracking-tight text-foreground">
                Timeline of AI regulation
              </h3>
            </div>
            <TimelineView onOpenLaw={openLaw} />
          </TabsContent>

          {/* Compare */}
          <TabsContent value="compare">
            <CompareView onOpenLaw={openLaw} />
          </TabsContent>

          {/* Assistant */}
          <TabsContent value="assistant">
            <AIAssistant />
          </TabsContent>
        </Tabs>
      </main>

      <footer className="border-t border-border py-6">
        <div className="mx-auto max-w-[1200px] px-4 text-center text-xs text-muted-foreground sm:px-6 lg:px-8">
          Data is curated from official sources for reference only and is not legal advice.
          Always verify with primary sources linked in each entry.
        </div>
      </footer>

      {/* Shared overlays */}
      <LawDetailDialog
        lawId={lawId}
        open={lawOpen}
        onOpenChange={setLawOpen}
        onSelectRelated={(id) => setLawId(id)}
      />
      <CountryPanel
        countryName={country}
        open={countryOpen}
        onOpenChange={setCountryOpen}
        onOpenLaw={openLawFromPanel}
      />
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <Tracker />
    </ThemeProvider>
  );
}

export default App;
