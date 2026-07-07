import React, { useEffect, useState, useCallback, useRef } from 'react';
import '@/App.css';
import { ThemeProvider } from '@/lib/ThemeContext';
import { ThemeToggle } from '@/components/ThemeToggle';
import { CosmicBackground } from '@/components/CosmicBackground';
import { WorldMap } from '@/components/WorldMap';
import { UsStatesMap } from '@/components/UsStatesMap';
import { CountryPanel } from '@/components/CountryPanel';
import { StatePanel } from '@/components/StatePanel';
import { AdminPanel } from '@/components/AdminPanel';
import { LawDetailDialog } from '@/components/LawDetailDialog';
import { StatsRow } from '@/components/StatsRow';
import { ChartsPanel } from '@/components/ChartsPanel';
import { FiltersBar } from '@/components/FiltersBar';
import { BrowseGrid } from '@/components/BrowseGrid';
import { TimelineView } from '@/components/TimelineView';
import { CompareView } from '@/components/CompareView';
import { AIAssistant } from '@/components/AIAssistant';
import { getMeta, getStats, getCountries, getLaws, buildExportUrl, getUsStates } from '@/lib/api';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';
import { Orbit, Map, LayoutGrid, Clock, GitCompareArrows, Sparkle, ScrollText, Globe2, Shield } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

const DEFAULT_FILTERS = {
  search: '', group: 'all', region: 'all', status: 'all', category: 'all', sort: 'newest',
};
const PAGE = 60;

const readUrl = () => {
  const p = new URLSearchParams(window.location.search);
  const f = { ...DEFAULT_FILTERS };
  ['search', 'group', 'region', 'status', 'category', 'sort'].forEach((k) => {
    if (p.get(k)) f[k] = p.get(k);
  });
  return { filters: f, tab: p.get('tab') || 'explore' };
};

function Tracker() {
  const initial = readUrl();
  const [meta, setMeta] = useState(null);
  const [stats, setStats] = useState(null);
  const [countries, setCountries] = useState(null);
  const [usStates, setUsStates] = useState(null);
  const [mapMode, setMapMode] = useState('maturity');
  const [mapScope, setMapScope] = useState('world');
  const [tab, setTab] = useState(initial.tab);

  const [lawId, setLawId] = useState(null);
  const [lawOpen, setLawOpen] = useState(false);
  const [country, setCountry] = useState(null);
  const [countryOpen, setCountryOpen] = useState(false);
  const [usState, setUsState] = useState(null);
  const [stateOpen, setStateOpen] = useState(false);
  const [adminOpen, setAdminOpen] = useState(false);

  const [filters, setFilters] = useState(initial.filters);
  const [laws, setLaws] = useState([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [lawsLoading, setLawsLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const debounceRef = useRef(null);

  const loadReference = useCallback(() => {
    getMeta().then(setMeta).catch(() => {});
    getStats().then(setStats).catch(() => {});
    getCountries().then(setCountries).catch(() => {});
    getUsStates().then(setUsStates).catch(() => {});
  }, []);

  useEffect(() => { loadReference(); }, [loadReference]);

  // sync URL (shareable state)
  useEffect(() => {
    const p = new URLSearchParams();
    if (tab !== 'explore') p.set('tab', tab);
    Object.entries(filters).forEach(([k, v]) => {
      if (v && v !== 'all' && v !== '') p.set(k, v);
    });
    const qs = p.toString();
    window.history.replaceState(null, '', qs ? `?${qs}` : window.location.pathname);
  }, [filters, tab]);

  // fetch first page whenever filters change
  useEffect(() => {
    setLawsLoading(true);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      getLaws({ ...filters, limit: PAGE, offset: 0 })
        .then((d) => {
          setLaws(d.laws);
          setTotal(d.count);
          setOffset(d.laws.length);
        })
        .finally(() => setLawsLoading(false));
    }, 250);
    return () => clearTimeout(debounceRef.current);
  }, [filters]);

  const loadMore = () => {
    setLoadingMore(true);
    getLaws({ ...filters, limit: PAGE, offset })
      .then((d) => {
        setLaws((prev) => [...prev, ...d.laws]);
        setOffset((o) => o + d.laws.length);
      })
      .finally(() => setLoadingMore(false));
  };

  const openLaw = useCallback((law) => {
    setLawId(typeof law === 'string' ? law : law.id);
    setLawOpen(true);
  }, []);
  const openCountry = useCallback((name) => {
    setCountry(name);
    setCountryOpen(true);
  }, []);
  const openStateView = useCallback((name) => {
    setUsState(name);
    setStateOpen(true);
  }, []);
  const openLawFromPanel = (id) => {
    setCountryOpen(false);
    setStateOpen(false);
    setTimeout(() => openLaw(id), 150);
  };

  const refreshData = useCallback(() => {
    loadReference();
    getLaws({ ...filters, limit: PAGE, offset: 0 }).then((d) => {
      setLaws(d.laws); setTotal(d.count); setOffset(d.laws.length);
    });
  }, [filters, loadReference]);

  const handleExport = () => {
    window.open(buildExportUrl(filters), '_blank');
    toast.success('Exporting filtered results to CSV…');
  };
  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href);
    toast.success('Shareable link copied to clipboard');
  };

  const TABS = [
    { v: 'explore', label: 'Explore', icon: Map, tid: TRACKER.navMap },
    { v: 'browse', label: 'Browse', icon: LayoutGrid, tid: TRACKER.navBrowse },
    { v: 'timeline', label: 'Timeline', icon: Clock, tid: TRACKER.navTimeline },
    { v: 'compare', label: 'Compare', icon: GitCompareArrows, tid: TRACKER.navCompare },
    { v: 'assistant', label: 'Assistant', icon: Sparkle, tid: TRACKER.navAssistant },
  ];

  return (
    <div className="relative min-h-screen">
      <CosmicBackground />
      <Toaster position="top-center" />

      {/* Header */}
      <header className="glass sticky top-0 z-40 border-b border-border/60">
        <div className="mx-auto flex max-w-[1220px] items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-accent text-primary-foreground glow-ring">
              <Orbit className="h-5 w-5" />
            </div>
            <div>
              <h1 className="font-display text-base font-semibold leading-none tracking-tight text-foreground sm:text-lg">
                AI Law Observatory
              </h1>
              <p className="mt-0.5 text-xs text-muted-foreground">
                Worldwide AI laws, acts &amp; regulations
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span
              data-testid={TRACKER.dataFreshnessBadge}
              className="hidden items-center gap-1.5 rounded-full border border-border/60 bg-background/40 px-3 py-1 text-xs text-muted-foreground sm:inline-flex"
            >
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
              {stats ? `${stats.total_laws} entries · ${stats.total_jurisdictions} jurisdictions` : 'Loading…'}
            </span>
            <button
              type="button"
              onClick={() => setAdminOpen(true)}
              data-testid={TRACKER.adminButton}
              aria-label="Open admin panel"
              className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-border/60 bg-background/40 text-muted-foreground transition-colors hover:text-foreground"
            >
              <Shield className="h-4 w-4" />
            </button>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border/50">
        <div className="mx-auto max-w-[1220px] px-4 py-10 sm:px-6 sm:py-14 lg:px-8">
          <div className="max-w-3xl animate-in-up">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-border/60 bg-background/40 px-3 py-1 text-xs font-medium text-muted-foreground backdrop-blur">
              <Globe2 className="h-3.5 w-3.5 text-accent" />
              Tracking {stats ? stats.total_laws : '370+'} laws across {stats ? stats.total_jurisdictions : '80+'} jurisdictions
            </div>
            <h2 className="font-display text-4xl font-semibold leading-[1.05] tracking-tight text-foreground sm:text-5xl lg:text-6xl">
              The global map of{' '}
              <span className="text-gradient">artificial intelligence law</span>
            </h2>
            <p className="mt-4 max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-base">
              An interactive observatory of AI legislation, acts, treaties and governance frameworks —
              from the EU AI Act and US state laws to national strategies worldwide. Explore the map,
              track the timeline, compare jurisdictions, and ask the AI assistant.
            </p>
          </div>
          <div className="mt-8">
            <StatsRow stats={stats} />
          </div>
        </div>
      </section>

      {/* Main */}
      <main className="mx-auto max-w-[1220px] px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
        <Tabs value={tab} onValueChange={setTab} className="space-y-6">
          <TabsList className="glass flex h-auto w-full flex-wrap justify-start gap-1 rounded-2xl p-1.5">
            {TABS.map(({ v, label, icon: Icon, tid }) => (
              <TabsTrigger
                key={v}
                value={v}
                data-testid={tid}
                className="gap-1.5 rounded-xl px-4 py-2 data-[state=active]:bg-gradient-to-br data-[state=active]:from-primary data-[state=active]:to-accent data-[state=active]:text-primary-foreground data-[state=active]:shadow-lg"
              >
                <Icon className="h-4 w-4" /> {label}
              </TabsTrigger>
            ))}
          </TabsList>

          {/* Explore */}
          <TabsContent value="explore" className="space-y-6">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h3 className="font-display text-lg font-semibold tracking-tight text-foreground">
                {mapScope === 'world' ? 'World map' : 'United States map'}
              </h3>
              <div className="flex items-center gap-2">
                <ToggleGroup
                  type="single"
                  value={mapScope}
                  onValueChange={(v) => v && setMapScope(v)}
                  data-testid={TRACKER.mapScopeToggle}
                  className="glass rounded-xl p-0.5"
                >
                  <ToggleGroupItem value="world" className="h-7 px-3 text-xs">World</ToggleGroupItem>
                  <ToggleGroupItem value="us" className="h-7 px-3 text-xs">United States</ToggleGroupItem>
                </ToggleGroup>
                <ToggleGroup
                  type="single"
                  value={mapMode}
                  onValueChange={(v) => v && setMapMode(v)}
                  data-testid={TRACKER.mapModeToggle}
                  className="glass rounded-xl p-0.5"
                >
                  <ToggleGroupItem value="maturity" className="h-7 px-3 text-xs">Maturity</ToggleGroupItem>
                  <ToggleGroupItem value="status" className="h-7 px-3 text-xs">Status</ToggleGroupItem>
                </ToggleGroup>
              </div>
            </div>
            {mapScope === 'world' ? (
              <WorldMap countries={countries} mode={mapMode} onSelectCountry={openCountry} />
            ) : (
              <UsStatesMap states={usStates} mode={mapMode} onSelectState={openStateView} />
            )}
            <ChartsPanel stats={stats} />
          </TabsContent>

          {/* Browse */}
          <TabsContent value="browse" className="space-y-5">
            <FiltersBar
              meta={meta}
              filters={filters}
              setFilters={setFilters}
              onReset={() => setFilters(DEFAULT_FILTERS)}
              onExport={handleExport}
              onShare={handleShare}
            />
            <div className="flex items-center justify-between">
              <p className="text-sm text-muted-foreground">
                {lawsLoading ? 'Searching…' : `${total} ${total === 1 ? 'result' : 'results'} · showing ${laws.length}`}
              </p>
            </div>
            <BrowseGrid
              laws={laws}
              loading={lawsLoading}
              loadingMore={loadingMore}
              hasMore={laws.length < total}
              onOpen={openLaw}
              onReset={() => setFilters(DEFAULT_FILTERS)}
              onLoadMore={loadMore}
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

      <footer className="border-t border-border/50 py-6">
        <div className="mx-auto max-w-[1220px] px-4 text-center text-xs text-muted-foreground sm:px-6 lg:px-8">
          Data curated from official and public trackers for reference only — not legal advice.
          Always verify against the primary sources linked in each entry.
        </div>
      </footer>

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
      <StatePanel
        stateName={usState}
        open={stateOpen}
        onOpenChange={setStateOpen}
        onOpenLaw={openLawFromPanel}
      />
      <AdminPanel
        open={adminOpen}
        onOpenChange={setAdminOpen}
        meta={meta}
        onDataChanged={refreshData}
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
