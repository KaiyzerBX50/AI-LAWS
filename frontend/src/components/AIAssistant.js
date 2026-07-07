import React, { useEffect, useRef, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { streamChat } from '@/lib/api';
import { Send, Sparkle, User } from 'lucide-react';
import { TRACKER } from '@/constants/testIds';

const SUGGESTIONS = [
  'What is the EU AI Act and how does it work?',
  'How does China regulate generative AI?',
  'Compare the US and EU approaches to AI regulation.',
  'Which countries have enacted comprehensive AI laws?',
];

const sessionId =
  (typeof crypto !== 'undefined' && crypto.randomUUID)
    ? crypto.randomUUID()
    : `sess-${Date.now()}`;

export const AIAssistant = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const scrollRef = useRef(null);

  const scrollToBottom = () => {
    requestAnimationFrame(() => {
      const el = scrollRef.current;
      if (el) el.scrollTop = el.scrollHeight;
    });
  };

  useEffect(scrollToBottom, [messages]);

  const send = async (text) => {
    const q = (text ?? input).trim();
    if (!q || streaming) return;
    setInput('');
    setMessages((m) => [...m, { role: 'user', content: q }]);
    setMessages((m) => [...m, { role: 'assistant', content: '', refs: [], loading: true }]);
    setStreaming(true);

    await streamChat({
      sessionId,
      message: q,
      onRefs: (refs) =>
        setMessages((m) => {
          const copy = [...m];
          copy[copy.length - 1] = { ...copy[copy.length - 1], refs };
          return copy;
        }),
      onDelta: (chunk) =>
        setMessages((m) => {
          const copy = [...m];
          const last = copy[copy.length - 1];
          copy[copy.length - 1] = { ...last, content: last.content + chunk, loading: false };
          return copy;
        }),
      onError: (msg) =>
        setMessages((m) => {
          const copy = [...m];
          const last = copy[copy.length - 1];
          copy[copy.length - 1] = {
            ...last,
            content: last.content || `⚠️ ${msg}`,
            loading: false,
          };
          return copy;
        }),
      onDone: () => setStreaming(false),
    });
    setStreaming(false);
  };

  return (
    <Card
      data-testid={TRACKER.assistantPanel}
      className="flex h-[calc(100vh-220px)] min-h-[460px] flex-col overflow-hidden rounded-xl border bg-card shadow-sm"
    >
      <div className="flex items-center gap-2 border-b border-border px-4 py-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent/10 text-accent">
          <Sparkle className="h-4 w-4" />
        </div>
        <div>
          <h2 className="font-display text-sm font-semibold text-foreground">AI Policy Assistant</h2>
          <p className="text-xs text-muted-foreground">Grounded in tracked laws · cites sources</p>
        </div>
      </div>

      <ScrollArea className="flex-1">
        <div ref={scrollRef} className="h-full space-y-4 overflow-y-auto p-4 thin-scrollbar">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center gap-4 py-10 text-center">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-accent/10 text-accent">
                <Sparkle className="h-7 w-7" />
              </div>
              <div>
                <p className="font-display text-base font-semibold text-foreground">
                  Ask about global AI regulation
                </p>
                <p className="mt-1 text-sm text-muted-foreground">
                  I answer using the laws tracked in this app and cite my sources.
                </p>
              </div>
              <div className="grid w-full max-w-md grid-cols-1 gap-2 sm:grid-cols-2">
                {SUGGESTIONS.map((s, i) => (
                  <button
                    key={i}
                    data-testid={TRACKER.assistantSuggestion}
                    onClick={() => send(s)}
                    className="rounded-lg border border-border bg-secondary/50 p-3 text-left text-xs text-foreground transition-colors duration-200 hover:border-accent/50 hover:bg-secondary"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div
                key={i}
                data-testid={TRACKER.assistantMessage}
                className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
              >
                <div
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
                    msg.role === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-accent/10 text-accent'
                  }`}
                >
                  {msg.role === 'user' ? <User className="h-4 w-4" /> : <Sparkle className="h-4 w-4" />}
                </div>
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'border border-border bg-secondary text-foreground'
                  }`}
                >
                  {msg.loading && !msg.content ? (
                    <span className="inline-flex gap-1">
                      <span className="typing-dot h-1.5 w-1.5 rounded-full bg-current" />
                      <span className="typing-dot h-1.5 w-1.5 rounded-full bg-current" style={{ animationDelay: '0.2s' }} />
                      <span className="typing-dot h-1.5 w-1.5 rounded-full bg-current" style={{ animationDelay: '0.4s' }} />
                    </span>
                  ) : (
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                  )}
                  {msg.role === 'assistant' && msg.refs?.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1.5 border-t border-border/60 pt-2">
                      {msg.refs.map((r) => (
                        <span
                          key={r.index}
                          title={r.title}
                          className="rounded-md bg-card px-2 py-0.5 font-mono text-[10px] text-muted-foreground"
                        >
                          [{r.index}] {r.country} {r.year}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </ScrollArea>

      <div className="border-t border-border p-3">
        <div className="flex items-end gap-2">
          <Textarea
            data-testid={TRACKER.assistantInput}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            placeholder="Ask about AI laws, acts, or regulations…"
            rows={1}
            className="max-h-32 min-h-[42px] resize-none"
          />
          <Button
            data-testid={TRACKER.assistantSend}
            onClick={() => send()}
            disabled={streaming || !input.trim()}
            size="icon"
            className="h-[42px] w-[42px] shrink-0"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </Card>
  );
};
