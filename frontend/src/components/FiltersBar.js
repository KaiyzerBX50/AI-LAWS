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
import { Search, RotateCcw } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

export const FiltersBar = ({ meta, filters, setFilters, onReset }) => {
  const update = (key, value) => setFilters((f) => ({ ...f, [key]: value }));

  return (
    <div className="flex flex-col gap-3 rounded-xl border border-border bg-card p-3 shadow-sm lg:flex-row lg:items-center">
      <div className="relative flex-1">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          data-testid={TRACKER.searchInput}
          value={filters.search}
          onChange={(e) => update('search', e.target.value)}
          placeholder="Search laws, countries, categories…"
          className="pl-9"
        />
      </div>

      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4 lg:flex">
        <Select value={filters.region} onValueChange={(v) => update('region', v)}>
          <SelectTrigger data-testid={TRACKER.filterRegion} className="w-full lg:w-[150px]">
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
          <SelectTrigger data-testid={TRACKER.filterStatus} className="w-full lg:w-[140px]">
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
          <SelectTrigger data-testid={TRACKER.filterCategory} className="w-full lg:w-[160px]">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All categories</SelectItem>
            {meta?.categories?.map((c) => (
              <SelectItem key={c} value={c}>{c}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={filters.sort} onValueChange={(v) => update('sort', v)}>
          <SelectTrigger data-testid={TRACKER.filterSort} className="w-full lg:w-[140px]">
            <SelectValue placeholder="Sort" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="newest">Newest first</SelectItem>
            <SelectItem value="oldest">Oldest first</SelectItem>
            <SelectItem value="country">By country</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Button
        variant="outline"
        size="icon"
        onClick={onReset}
        data-testid={TRACKER.filtersReset}
        aria-label="Reset filters"
        className="shrink-0"
      >
        <RotateCcw className="h-4 w-4" />
      </Button>
    </div>
  );
};
