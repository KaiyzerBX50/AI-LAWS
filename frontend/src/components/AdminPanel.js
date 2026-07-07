import React, { useState, useEffect, useCallback } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { verifyAdmin, createLaw, updateLaw, deleteLaw, getLaws } from '@/lib/api';
import { StatusBadge } from '@/components/StatusBadge';
import { toast } from 'sonner';
import { Lock, Plus, Pencil, Trash2, Save, X, ShieldCheck } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

const EMPTY = {
  id: null, title: '', country: '', jurisdiction: '', region: 'Europe',
  status: 'Enacted', category: 'AI governance', year: new Date().getFullYear(),
  summary: '', source_url: '', group: 'International',
};

const STATUSES = ['Enacted', 'Proposed', 'Draft', 'Superseded'];
const GROUPS = ['International', 'United States', 'Multilateral'];

export const AdminPanel = ({ open, onOpenChange, meta, onDataChanged }) => {
  const [token, setToken] = useState(() => localStorage.getItem('adminToken') || '');
  const [authed, setAuthed] = useState(false);
  const [checking, setChecking] = useState(false);
  const [form, setForm] = useState(EMPTY);
  const [saving, setSaving] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const tryVerify = useCallback(async (t) => {
    if (!t) return;
    setChecking(true);
    try {
      await verifyAdmin(t);
      setAuthed(true);
      localStorage.setItem('adminToken', t);
    } catch {
      setAuthed(false);
      toast.error('Invalid admin token');
    } finally {
      setChecking(false);
    }
  }, []);

  useEffect(() => {
    if (open && token) tryVerify(token);
  }, [open]); // eslint-disable-line

  const search = useCallback(async (q) => {
    const d = await getLaws({ search: q, limit: 15, sort: 'newest' });
    setResults(d.laws);
  }, []);

  useEffect(() => {
    if (authed) search(query);
  }, [authed, query, search]);

  const submit = async () => {
    if (!form.title || !form.country) {
      toast.error('Title and country are required');
      return;
    }
    setSaving(true);
    const body = {
      country: form.country, jurisdiction: form.jurisdiction || form.country,
      region: form.region, title: form.title, status: form.status,
      category: form.category, year: Number(form.year) || 2025,
      summary: form.summary, source_url: form.source_url, group: form.group,
    };
    try {
      if (form.id) {
        await updateLaw(token, form.id, body);
        toast.success('Law updated');
      } else {
        await createLaw(token, body);
        toast.success('Law added');
      }
      setForm(EMPTY);
      await search(query);
      onDataChanged && onDataChanged();
    } catch {
      toast.error('Save failed');
    } finally {
      setSaving(false);
    }
  };

  const remove = async (id) => {
    try {
      await deleteLaw(token, id);
      toast.success('Law deleted');
      await search(query);
      onDataChanged && onDataChanged();
    } catch {
      toast.error('Delete failed');
    }
  };

  const editLaw = (l) => setForm({
    id: l.id, title: l.title, country: l.country, jurisdiction: l.jurisdiction || '',
    region: l.region, status: l.status, category: l.category, year: l.year,
    summary: l.summary, source_url: (l.sources && l.sources[0]?.url) || '', group: l.group || 'International',
  });

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] max-w-3xl overflow-hidden p-0">
        <ScrollArea className="max-h-[90vh]">
          <div className="p-6">
            <DialogHeader className="text-left">
              <DialogTitle className="flex items-center gap-2 font-display text-xl">
                <ShieldCheck className="h-5 w-5 text-accent" /> Admin — manage laws
              </DialogTitle>
              <DialogDescription>
                Add, edit, or remove AI laws. Changes persist and update the whole tracker.
              </DialogDescription>
            </DialogHeader>

            {!authed ? (
              <div className="mt-6 flex flex-col items-center gap-3 rounded-xl border border-border bg-secondary/40 p-8 text-center">
                <Lock className="h-8 w-8 text-muted-foreground" />
                <p className="text-sm text-muted-foreground">Enter the admin token to continue.</p>
                <div className="flex w-full max-w-sm gap-2">
                  <Input
                    data-testid={TRACKER.adminTokenInput}
                    type="password"
                    value={token}
                    onChange={(e) => setToken(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && tryVerify(token)}
                    placeholder="Admin token"
                  />
                  <Button data-testid={TRACKER.adminLoginButton} onClick={() => tryVerify(token)} disabled={checking}>
                    {checking ? 'Checking…' : 'Unlock'}
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground/70">Default (testing): ailaw-admin-2025</p>
              </div>
            ) : (
              <div className="mt-5 space-y-6">
                {/* form */}
                <div className="rounded-xl border border-border bg-secondary/30 p-4">
                  <div className="mb-3 flex items-center justify-between">
                    <h4 className="font-display text-sm font-semibold text-foreground">
                      {form.id ? 'Edit law' : 'Add new law'}
                    </h4>
                    {form.id && (
                      <Button variant="ghost" size="sm" className="h-7 gap-1 text-xs" onClick={() => setForm(EMPTY)}>
                        <X className="h-3 w-3" /> New instead
                      </Button>
                    )}
                  </div>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <Input placeholder="Title *" value={form.title} onChange={(e) => set('title', e.target.value)} className="sm:col-span-2" />
                    <Input placeholder="Country / body *" value={form.country} onChange={(e) => set('country', e.target.value)} />
                    <Input placeholder="Jurisdiction label" value={form.jurisdiction} onChange={(e) => set('jurisdiction', e.target.value)} />
                    <Input placeholder="Region" value={form.region} onChange={(e) => set('region', e.target.value)} />
                    <Input placeholder="Category" value={form.category} onChange={(e) => set('category', e.target.value)} />
                    <Input type="number" placeholder="Year" value={form.year} onChange={(e) => set('year', e.target.value)} />
                    <div className="grid grid-cols-2 gap-3">
                      <Select value={form.status} onValueChange={(v) => set('status', v)}>
                        <SelectTrigger><SelectValue placeholder="Status" /></SelectTrigger>
                        <SelectContent>{STATUSES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
                      </Select>
                      <Select value={form.group} onValueChange={(v) => set('group', v)}>
                        <SelectTrigger><SelectValue placeholder="Scope" /></SelectTrigger>
                        <SelectContent>{GROUPS.map((g) => <SelectItem key={g} value={g}>{g}</SelectItem>)}</SelectContent>
                      </Select>
                    </div>
                    <Input placeholder="Source URL" value={form.source_url} onChange={(e) => set('source_url', e.target.value)} className="sm:col-span-2" />
                    <Textarea placeholder="Summary" value={form.summary} onChange={(e) => set('summary', e.target.value)} className="sm:col-span-2" rows={2} />
                  </div>
                  <div className="mt-3 flex justify-end">
                    <Button data-testid={form.id ? TRACKER.adminSaveButton : TRACKER.adminAddButton} onClick={submit} disabled={saving} className="gap-1.5">
                      {form.id ? <Save className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
                      {saving ? 'Saving…' : form.id ? 'Save changes' : 'Add law'}
                    </Button>
                  </div>
                </div>

                {/* search + list */}
                <div>
                  <Input
                    data-testid={TRACKER.adminSearchInput}
                    placeholder="Search existing laws to edit or delete…"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="mb-3"
                  />
                  <div className="space-y-2">
                    {results.map((l) => (
                      <div key={l.id} className="flex items-center gap-2 rounded-lg border border-border bg-card p-2.5">
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center gap-2">
                            <StatusBadge status={l.status} />
                            <span className="truncate text-xs text-muted-foreground">{l.jurisdiction || l.country} · {l.year}</span>
                          </div>
                          <p className="mt-1 truncate text-sm font-medium text-foreground">{l.title}</p>
                        </div>
                        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => editLaw(l)} aria-label="Edit">
                          <Pencil className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive" data-testid={TRACKER.adminDeleteButton} onClick={() => remove(l.id)} aria-label="Delete">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    ))}
                    {results.length === 0 && <p className="py-4 text-center text-sm text-muted-foreground">No matching laws.</p>}
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
};
