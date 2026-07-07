import React, { useState, useMemo } from 'react';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import { Card } from '@/components/ui/card';
import { useTheme } from '@/lib/ThemeContext';
import { maturityFill, statusFill, MATURITY_BINS } from '@/lib/lawUtils';
import { TRACKER } from '@/constants/testIds';

const US_GEO = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';

export const UsStatesMap = ({ states, mode, onSelectState }) => {
  const { isDark } = useTheme();
  const [tooltip, setTooltip] = useState(null);
  const borderColor = isDark ? '#0B1220' : '#FFFFFF';
  const hoverOutline = isDark ? '#67E8F9' : '#0E7490';

  const fillFor = useMemo(
    () => (name) => {
      const s = states?.[name];
      if (mode === 'status') return statusFill(s?.counts, isDark);
      return maturityFill(s ? s.maturity : 0, isDark);
    },
    [states, mode, isDark]
  );

  return (
    <Card className="glass relative overflow-hidden rounded-2xl p-0" data-testid={TRACKER.usMap}>
      <div className="pointer-events-none absolute left-4 top-4 z-10">
        <h2 className="font-display text-sm font-semibold tracking-tight text-foreground">
          United States — by state
        </h2>
        <p className="text-xs text-muted-foreground">Click a state to view its AI laws</p>
      </div>

      <div className="h-[380px] w-full sm:h-[460px] lg:h-[520px]">
        <ComposableMap projection="geoAlbersUsa" width={980} height={520}
          style={{ width: '100%', height: '100%' }}>
          <Geographies geography={US_GEO}>
            {({ geographies }) =>
              geographies.map((geo) => {
                const name = geo.properties.name;
                const hasData = !!states?.[name];
                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    tabIndex={hasData ? 0 : -1}
                    aria-label={name}
                    onMouseEnter={(e) => setTooltip({ x: e.clientX, y: e.clientY, name, data: states?.[name] })}
                    onMouseMove={(e) => setTooltip({ x: e.clientX, y: e.clientY, name, data: states?.[name] })}
                    onMouseLeave={() => setTooltip(null)}
                    onClick={() => hasData && onSelectState(name)}
                    style={{
                      default: { fill: fillFor(name), stroke: borderColor, strokeWidth: 0.5, outline: 'none', cursor: hasData ? 'pointer' : 'default', transition: 'fill 200ms ease' },
                      hover: { fill: fillFor(name), stroke: hasData ? hoverOutline : borderColor, strokeWidth: hasData ? 1.4 : 0.5, outline: 'none', cursor: hasData ? 'pointer' : 'default' },
                      pressed: { fill: fillFor(name), outline: 'none' },
                    }}
                  />
                );
              })
            }
          </Geographies>
        </ComposableMap>
      </div>

      <div data-testid={TRACKER.mapLegend}
        className="flex flex-wrap items-center gap-x-4 gap-y-1 border-t border-border/60 bg-card px-4 py-3 text-xs text-muted-foreground">
        {MATURITY_BINS.map((b) => (
          <span key={b.key} className="inline-flex items-center gap-1.5">
            <span className="h-3 w-3 rounded-sm" style={{ background: isDark ? b.dark : b.light }} />
            {b.label}
          </span>
        ))}
      </div>

      {tooltip && (
        <div className="pointer-events-none fixed z-50 rounded-lg border border-border bg-popover px-3 py-2 text-xs shadow-lg"
          style={{ left: tooltip.x + 14, top: tooltip.y + 14 }}>
          <div className="font-display font-semibold text-foreground">{tooltip.name}</div>
          {tooltip.data ? (
            <div className="mt-1 font-mono text-muted-foreground">
              {tooltip.data.total} {tooltip.data.total === 1 ? 'law' : 'laws'} · {tooltip.data.counts.Enacted} enacted
            </div>
          ) : (
            <div className="mt-1 text-muted-foreground">No tracked AI law</div>
          )}
        </div>
      )}
    </Card>
  );
};
