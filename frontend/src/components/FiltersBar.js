import React from 'react';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Search, RotateCcw, Download, Share2 } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const FiltersBar = ({ meta, filters, setFilters, onReset, onExport, onShare }) => {
  const update = (key, value) => setFilters((f) => ({ ...f, [key]: value }));

  return (
    <div className="glass flex flex-col gap-3 rounded-2xl p-3">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            data-testid={TRACKER.searchInput}
            value={filters.search}
            onChange={(e) => update('search', e.target.value)}
            placeholder="Search 370+ laws, jurisdictions, categories…"
            className="border-border/60 bg-background/50 pl-9"
          />
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={onShare}
            data-testid={TRACKER.shareButton}
            className="gap-1.5 border-border/60 bg-background/40"
          >
            <Share2 className="h-4 w-4" /> Share
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={onExport}
            data-testid={TRACKER.exportButton}
            className="gap-1.5 border-border/60 bg-background/40"
          >
            <Download className="h-4 w-4" /> CSV
          </Button>
          <Button
            variant="outline"
            size="icon"
            onClick={onReset}
            data-testid={TRACKER.filtersReset}
            aria-label="Reset filters"
            className="shrink-0 border-border/60 bg-background/40"
          >
            <RotateCcw className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-5">
        <Select value={filters.group} onValueChange={(v) => update('group', v)}>
          <SelectTrigger data-testid={TRACKER.filterGroup} className="border-border/60 bg-background/50">
            <SelectValue placeholder="Scope" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All scopes</SelectItem>
            {meta?.groups?.map((g) => (
              <SelectItem key={g} value={g}>{g}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={filters.region} onValueChange={(v) => update('region', v)}>
          <SelectTrigger data-testid={TRACKER.filterRegion} className="border-border/60 bg-background/50">
            <SelectValue placeholder="Region" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All regions</SelectItem>
            {meta?.regions?.map((r) => (
              <SelectItem key={r} value={r}>{r}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={filters.status} onValueChange={(v) => update('status', v)}>
          <SelectTrigger data-testid={TRACKER.filterStatus} className="border-border/60 bg-background/50">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All statuses</SelectItem>
            {meta?.statuses?.map((s) => (
              <SelectItem key={s} value={s}>{s}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={filters.category} onValueChange={(v) => update('category', v)}>
          <SelectTrigger data-testid={TRACKER.filterCategory} className="border-border/60 bg-background/50">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent className="max-h-72">
            <SelectItem value="all">All categories</SelectItem>
            {meta?.categories?.map((c) => (
              <SelectItem key={c} value={c}>{c}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={filters.sort} onValueChange={(v) => update('sort', v)}>
          <SelectTrigger data-testid={TRACKER.filterSort} className="border-border/60 bg-background/50">
            <SelectValue placeholder="Sort" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="newest">Newest first</SelectItem>
            <SelectItem value="oldest">Oldest first</SelectItem>
            <SelectItem value="country">By jurisdiction</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
};
