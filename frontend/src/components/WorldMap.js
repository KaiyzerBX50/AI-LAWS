import React, { useState, useMemo } from 'react';
import { ComposableMap, Geographies, Geography, ZoomableGroup } from 'react-simple-maps';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/lib/ThemeContext';
import { maturityFill, statusFill, pendingFill, MATURITY_BINS, PENDING_BINS } from '@/lib/lawUtils';
import { Plus, Minus, Locate } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

const GEO_URL = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json';

export const WorldMap = ({ countries, mode, onSelectCountry }) => {
  const { isDark } = useTheme();
  const [tooltip, setTooltip] = useState(null);
  const [pos, setPos] = useState({ coordinates: [0, 20], zoom: 1 });

  const borderColor = isDark ? '#0B1220' : '#FFFFFF';
  const hoverOutline = isDark ? '#67E8F9' : '#0E7490';

  const fillFor = useMemo(
    () => (name) => {
      const c = countries?.[name];
      if (mode === 'status') return statusFill(c?.counts, isDark);
      if (mode === 'pending') return pendingFill(c?.counts, isDark);
      return maturityFill(c ? c.maturity : 0, isDark);
    },
    [countries, mode, isDark]
  );

  const handleMove = (e, geo) => {
    const name = geo.properties.name;
    const c = countries?.[name];
    setTooltip({
      x: e.clientX,
      y: e.clientY,
      name,
      data: c,
    });
  };

  const clamp = (z) => Math.max(1, Math.min(6, z));

  return (
    <Card className="glass relative overflow-hidden rounded-2xl p-0" data-testid={TRACKER.worldMap}>
      <div className="pointer-events-none absolute left-4 top-4 z-10">
        <h2 className="font-display text-sm font-semibold tracking-tight text-foreground">
          Explore by country
        </h2>
        <p className="text-xs text-muted-foreground">Click a country to view its AI laws</p>
      </div>

      {/* zoom controls */}
      <div className="absolute right-4 top-4 z-10 flex flex-col gap-1.5">
        <Button variant="secondary" size="icon" className="h-8 w-8" aria-label="Zoom in"
          onClick={() => setPos((p) => ({ ...p, zoom: clamp(p.zoom * 1.5) }))}>
          <Plus className="h-4 w-4" />
        </Button>
        <Button variant="secondary" size="icon" className="h-8 w-8" aria-label="Zoom out"
          onClick={() => setPos((p) => ({ ...p, zoom: clamp(p.zoom / 1.5) }))}>
          <Minus className="h-4 w-4" />
        </Button>
        <Button variant="secondary" size="icon" className="h-8 w-8" aria-label="Reset view"
          onClick={() => setPos({ coordinates: [0, 20], zoom: 1 })}>
          <Locate className="h-4 w-4" />
        </Button>
      </div>

      <div className="h-[380px] w-full sm:h-[460px] lg:h-[520px]">
        <ComposableMap projectionConfig={{ scale: 150 }} width={980} height={520}
          style={{ width: '100%', height: '100%' }}>
          <ZoomableGroup
            zoom={pos.zoom}
            center={pos.coordinates}
            onMoveEnd={(p) => setPos(p)}
            maxZoom={6}
          >
            <Geographies geography={GEO_URL}>
              {({ geographies }) =>
                geographies.map((geo) => {
                  const name = geo.properties.name;
                  const hasData = !!countries?.[name];
                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      tabIndex={hasData ? 0 : -1}
                      aria-label={name}
                      onMouseEnter={(e) => handleMove(e, geo)}
                      onMouseMove={(e) => handleMove(e, geo)}
                      onMouseLeave={() => setTooltip(null)}
                      onClick={() => hasData && onSelectCountry(name)}
                      style={{
                        default: {
                          fill: fillFor(name),
                          stroke: borderColor,
                          strokeWidth: 0.4,
                          outline: 'none',
                          cursor: hasData ? 'pointer' : 'default',
                          transition: 'fill 200ms ease',
                        },
                        hover: {
                          fill: fillFor(name),
                          stroke: hasData ? hoverOutline : borderColor,
                          strokeWidth: hasData ? 1.2 : 0.4,
                          outline: 'none',
                          cursor: hasData ? 'pointer' : 'default',
                        },
                        pressed: { fill: fillFor(name), outline: 'none' },
                      }}
                    />
                  );
                })
              }
            </Geographies>
          </ZoomableGroup>
        </ComposableMap>
      </div>

      {/* legend */}
      <div
        data-testid={TRACKER.mapLegend}
        className="relative z-10 flex flex-wrap items-center gap-x-4 gap-y-1 border-t border-border/50 bg-background/30 backdrop-blur-md px-4 py-3 text-xs text-muted-foreground"
      >
        {mode === 'maturity' ? (
          MATURITY_BINS.map((b) => (
            <span key={b.key} className="inline-flex items-center gap-1.5">
              <span className="h-3 w-3 rounded-sm" style={{ background: isDark ? b.dark : b.light }} />
              {b.label}
            </span>
          ))
        ) : mode === 'pending' ? (
          PENDING_BINS.map((b) => (
            <span key={b.label} className="inline-flex items-center gap-1.5">
              <span className="h-3 w-3 rounded-sm" style={{ background: isDark ? b.dark : b.light }} />
              {b.label}
            </span>
          ))
        ) : (
          <>
            <LegendSwatch color={isDark ? '#2A7F8E' : '#1F7A8C'} label="Has enacted law" />
            <LegendSwatch color={isDark ? '#7c5a1e' : '#F0B454'} label="Proposed only" />
            <LegendSwatch color={isDark ? '#334155' : '#94A3B8'} label="Draft only" />
            <LegendSwatch color={isDark ? '#1B2633' : '#E7EDF3'} label="No tracked law" />
          </>
        )}
      </div>

      {tooltip && (
        <div
          className="pointer-events-none fixed z-50 rounded-lg border border-border bg-popover px-3 py-2 text-xs shadow-lg"
          style={{ left: tooltip.x + 14, top: tooltip.y + 14 }}
        >
          <div className="font-display font-semibold text-foreground">{tooltip.name}</div>
          {tooltip.data ? (
            <div className="mt-1 space-y-0.5 text-muted-foreground">
              <div>{tooltip.data.maturity_label}</div>
              <div className="font-mono">
                {tooltip.data.counts.Enacted} enacted · {tooltip.data.counts.Proposed} proposed
              </div>
            </div>
          ) : (
            <div className="mt-1 text-muted-foreground">No tracked AI law</div>
          )}
        </div>
      )}
    </Card>
  );
};

const LegendSwatch = ({ color, label }) => (
  <span className="inline-flex items-center gap-1.5">
    <span className="h-3 w-3 rounded-sm" style={{ background: color }} />
    {label}
  </span>
);
