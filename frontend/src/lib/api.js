import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API });

export const getMeta = () => api.get('/meta').then((r) => r.data);
export const getStats = () => api.get('/stats').then((r) => r.data);
export const getCountries = () => api.get('/countries').then((r) => r.data);
export const getCountryDetail = (name) =>
  api.get(`/countries/${encodeURIComponent(name)}`).then((r) => r.data);
export const getLawById = (id) => api.get(`/laws/${id}`).then((r) => r.data);

const cleanParams = (params = {}) => {
  const clean = {};
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '' && v !== 'all') clean[k] = v;
  });
  return clean;
};

export const getLaws = (params = {}) =>
  api.get('/laws', { params: cleanParams(params) }).then((r) => r.data);

export const getUsStates = () => api.get('/us-states').then((r) => r.data);
export const getUsStateDetail = (name) =>
  api.get(`/us-states/${encodeURIComponent(name)}`).then((r) => r.data);

// ---- Admin (token-protected) ----
const adminHeaders = (token) => ({ headers: { 'X-Admin-Token': token } });
export const verifyAdmin = (token) =>
  api.get('/admin/verify', adminHeaders(token)).then((r) => r.data);
export const createLaw = (token, body) =>
  api.post('/admin/laws', body, adminHeaders(token)).then((r) => r.data);
export const updateLaw = (token, id, body) =>
  api.put(`/admin/laws/${id}`, body, adminHeaders(token)).then((r) => r.data);
export const deleteLaw = (token, id) =>
  api.delete(`/admin/laws/${id}`, adminHeaders(token)).then((r) => r.data);

export const buildExportUrl = (params = {}) => {
  const qs = new URLSearchParams(cleanParams(params)).toString();
  return `${API}/laws/export${qs ? `?${qs}` : ''}`;
};

// Stream chat via fetch (SSE-style). onDelta(text), onRefs(refs), onDone(), onError(msg)
export async function streamChat({ sessionId, message, onRefs, onDelta, onDone, onError }) {
  try {
    const res = await fetch(`${API}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message }),
    });
    if (!res.ok || !res.body) {
      onError && onError('Failed to reach the assistant.');
      return;
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split('\n\n');
      buffer = parts.pop();
      for (const part of parts) {
        const line = part.trim();
        if (!line.startsWith('data:')) continue;
        const payload = line.slice(5).trim();
        if (!payload) continue;
        let evt;
        try { evt = JSON.parse(payload); } catch { continue; }
        if (evt.type === 'refs') onRefs && onRefs(evt.refs || []);
        else if (evt.type === 'delta') onDelta && onDelta(evt.content || '');
        else if (evt.type === 'error') onError && onError(evt.message || 'Error');
        else if (evt.type === 'done') onDone && onDone();
      }
    }
    onDone && onDone();
  } catch (e) {
    onError && onError(e.message || 'Network error');
  }
}
