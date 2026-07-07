{
  "meta": {
    "product": "Global AI Law Tracker",
    "design_personality": [
      "policy-grade / authoritative",
      "calmly futuristic (data-viz forward, not sci-fi)",
      "high-clarity dense information",
      "interactive + responsive",
      "day/night parity (same hierarchy, different surfaces)"
    ],
    "north_star": "Make global AI regulation feel explorable: map → filter → compare → cite sources, with confident status semantics and delightful micro-interactions."
  },

  "brand_attributes": {
    "trustworthy": "Neutral surfaces, restrained accents, strong typographic hierarchy, visible sources.",
    "analytical": "Bento grid, consistent scales, legends, and data-dense cards.",
    "interactive": "Hover previews, animated state changes, keyboard-first navigation, smooth transitions (no transition: all)."
  },

  "inspiration_refs": {
    "what_to_borrow": [
      {
        "source": "Dribbble map tracking / world map UI tags",
        "url": "https://dribbble.com/tags/map-tracking",
        "takeaways": [
          "Map as hero with side panel details",
          "Soft choropleth + crisp borders",
          "Legend as compact pill group"
        ]
      },
      {
        "source": "Dashboard design principles (hierarchy + modular KPI layout)",
        "url": "https://improvado.io/blog/dashboard-design-guide",
        "takeaways": [
          "Top-left primary KPI, modular cards",
          "Avoid over-filtering; progressive disclosure",
          "Timestamp freshness visible"
        ]
      },
      {
        "source": "Data-viz palette guidance (sequential palettes for maps)",
        "url": "https://carto.com/carto-colors/",
        "takeaways": [
          "Use sequential palettes with lightness steps",
          "Colorblind-safe ramps",
          "Different ramps for light vs dark surfaces"
        ]
      }
    ]
  },

  "typography": {
    "font_pairing": {
      "display": {
        "name": "Space Grotesk",
        "fallback": "ui-sans-serif, system-ui",
        "usage": "H1/H2, KPI numbers, map headline"
      },
      "body": {
        "name": "IBM Plex Sans",
        "fallback": "ui-sans-serif, system-ui",
        "usage": "Body, tables, filters, long summaries"
      },
      "mono": {
        "name": "IBM Plex Mono",
        "fallback": "ui-monospace, SFMono-Regular",
        "usage": "Law IDs, citations, dates, code-like metadata"
      }
    },
    "google_fonts_import": {
      "instructions": "In /app/frontend/src/index.css (or in index.html), import via Google Fonts. Keep weights minimal for performance.",
      "css": "@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');"
    },
    "type_scale_tailwind": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight",
      "h2": "text-base md:text-lg font-medium text-muted-foreground",
      "section_title": "text-lg font-semibold tracking-tight",
      "kpi_number": "text-3xl sm:text-4xl font-semibold tabular-nums",
      "body": "text-sm sm:text-base leading-relaxed",
      "small": "text-xs sm:text-sm text-muted-foreground"
    },
    "line_length": {
      "target": "60–80 characters",
      "implementation": "Use max-w-prose for long summaries; keep tables full-width."
    }
  },

  "layout_and_grid": {
    "page_shell": {
      "pattern": "Left rail (desktop) + top bar; mobile uses bottom sheet filters",
      "max_width": "max-w-[1200px]",
      "gutters": "px-4 sm:px-6 lg:px-8",
      "vertical_rhythm": "space-y-6 sm:space-y-8",
      "avoid": "Do not center-align all text; keep left-aligned reading flow."
    },
    "bento_dashboard": {
      "grid": "grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6",
      "recommended_spans": {
        "map": "lg:col-span-8",
        "side_panel": "lg:col-span-4",
        "kpi_row": "lg:col-span-12",
        "charts": "lg:col-span-6",
        "table": "lg:col-span-12"
      }
    },
    "density_modes": {
      "default": "Comfortable spacing (policy reading)",
      "compact_optional": "Add a density toggle later; not required for MVP"
    }
  },

  "color_system": {
    "notes": [
      "No purple for AI assistant/chat.",
      "No dark/saturated gradients; gradients only as subtle section accents (<20% viewport).",
      "Use semantic tokens; do not hardcode colors in components except charts/maps where needed."
    ],

    "palette_light": {
      "bg": "hsl(210 20% 98%)",
      "surface": "hsl(0 0% 100%)",
      "surface_2": "hsl(210 16% 96%)",
      "text": "hsl(222 47% 11%)",
      "muted_text": "hsl(215 16% 35%)",
      "border": "hsl(214 18% 88%)",
      "primary": "hsl(203 72% 28%)",
      "primary_fg": "hsl(0 0% 98%)",
      "accent": "hsl(168 55% 34%)",
      "accent_fg": "hsl(0 0% 98%)",
      "focus_ring": "hsl(203 72% 38%)",
      "shadow_rgba": "rgba(15, 23, 42, 0.08)"
    },

    "palette_dark": {
      "bg": "hsl(222 47% 7%)",
      "surface": "hsl(222 35% 10%)",
      "surface_2": "hsl(222 28% 14%)",
      "text": "hsl(210 40% 96%)",
      "muted_text": "hsl(215 20% 70%)",
      "border": "hsl(222 18% 22%)",
      "primary": "hsl(203 78% 62%)",
      "primary_fg": "hsl(222 47% 10%)",
      "accent": "hsl(168 60% 45%)",
      "accent_fg": "hsl(222 47% 10%)",
      "focus_ring": "hsl(203 78% 70%)",
      "shadow_rgba": "rgba(0, 0, 0, 0.35)"
    },

    "semantic_status_colors": {
      "enacted": {
        "label": "Enacted",
        "light": {
          "bg": "hsl(152 55% 92%)",
          "fg": "hsl(160 84% 18%)",
          "border": "hsl(152 40% 78%)"
        },
        "dark": {
          "bg": "hsl(160 45% 16%)",
          "fg": "hsl(152 60% 86%)",
          "border": "hsl(160 35% 26%)"
        }
      },
      "proposed": {
        "label": "Proposed",
        "light": {
          "bg": "hsl(38 90% 92%)",
          "fg": "hsl(24 90% 22%)",
          "border": "hsl(32 70% 78%)"
        },
        "dark": {
          "bg": "hsl(28 55% 18%)",
          "fg": "hsl(38 90% 86%)",
          "border": "hsl(28 40% 28%)"
        }
      },
      "draft": {
        "label": "Draft",
        "light": {
          "bg": "hsl(210 22% 92%)",
          "fg": "hsl(222 47% 18%)",
          "border": "hsl(214 18% 80%)"
        },
        "dark": {
          "bg": "hsl(222 28% 18%)",
          "fg": "hsl(210 30% 88%)",
          "border": "hsl(222 18% 28%)"
        }
      },
      "repealed_or_superseded": {
        "label": "Superseded",
        "light": {
          "bg": "hsl(0 0% 92%)",
          "fg": "hsl(0 0% 28%)",
          "border": "hsl(0 0% 82%)"
        },
        "dark": {
          "bg": "hsl(0 0% 18%)",
          "fg": "hsl(0 0% 82%)",
          "border": "hsl(0 0% 28%)"
        }
      }
    },

    "map_maturity_scale": {
      "meaning": "AI regulation maturity / coverage score (0–4). Use sequential ramp; do NOT use gradients in UI chrome—only in the map fill colors.",
      "bins": [
        {
          "key": "0-none",
          "label": "No tracked AI law",
          "light_fill": "#E7EDF3",
          "dark_fill": "#1B2633"
        },
        {
          "key": "1-emerging",
          "label": "Emerging signals",
          "light_fill": "#CFE6F2",
          "dark_fill": "#1E3A4A"
        },
        {
          "key": "2-developing",
          "label": "Developing framework",
          "light_fill": "#9FD3E6",
          "dark_fill": "#1F5566"
        },
        {
          "key": "3-established",
          "label": "Established regulation",
          "light_fill": "#4FB6C8",
          "dark_fill": "#2A7F8E"
        },
        {
          "key": "4-comprehensive",
          "label": "Comprehensive / multi-act",
          "light_fill": "#1F7A8C",
          "dark_fill": "#6FD6D1"
        }
      ],
      "borders": {
        "light": "#FFFFFF",
        "dark": "#0B1220"
      },
      "hover": {
        "light_outline": "#0E7490",
        "dark_outline": "#67E8F9"
      }
    },

    "allowed_background_accent_gradient": {
      "usage": "Hero header only (max 15–20% viewport height).",
      "light": "radial-gradient(1200px circle at 20% 10%, rgba(79,182,200,0.18), transparent 55%), radial-gradient(900px circle at 80% 0%, rgba(16,185,129,0.12), transparent 50%)",
      "dark": "radial-gradient(1200px circle at 20% 10%, rgba(103,232,249,0.10), transparent 55%), radial-gradient(900px circle at 80% 0%, rgba(52,211,153,0.08), transparent 50%)"
    }
  },

  "design_tokens_css": {
    "instructions": "Replace the default shadcn tokens in /app/frontend/src/index.css with these (keep the same variable names). Add extra custom tokens under :root and .dark. Avoid transition: all.",
    "css": ":root {\n  --background: 210 20% 98%;\n  --foreground: 222 47% 11%;\n  --card: 0 0% 100%;\n  --card-foreground: 222 47% 11%;\n  --popover: 0 0% 100%;\n  --popover-foreground: 222 47% 11%;\n\n  --primary: 203 72% 28%;\n  --primary-foreground: 0 0% 98%;\n  --secondary: 210 16% 96%;\n  --secondary-foreground: 222 47% 11%;\n  --muted: 210 16% 96%;\n  --muted-foreground: 215 16% 35%;\n  --accent: 168 55% 34%;\n  --accent-foreground: 0 0% 98%;\n  --destructive: 0 72% 52%;\n  --destructive-foreground: 0 0% 98%;\n\n  --border: 214 18% 88%;\n  --input: 214 18% 88%;\n  --ring: 203 72% 38%;\n\n  --radius: 0.75rem;\n\n  /* Custom */\n  --surface-2: 210 16% 96%;\n  --shadow-color: 222 47% 11%;\n  --shadow-alpha: 0.08;\n  --law-enacted: 160 84% 18%;\n  --law-proposed: 24 90% 22%;\n  --law-draft: 222 47% 18%;\n}\n\n.dark {\n  --background: 222 47% 7%;\n  --foreground: 210 40% 96%;\n  --card: 222 35% 10%;\n  --card-foreground: 210 40% 96%;\n  --popover: 222 35% 10%;\n  --popover-foreground: 210 40% 96%;\n\n  --primary: 203 78% 62%;\n  --primary-foreground: 222 47% 10%;\n  --secondary: 222 28% 14%;\n  --secondary-foreground: 210 40% 96%;\n  --muted: 222 28% 14%;\n  --muted-foreground: 215 20% 70%;\n  --accent: 168 60% 45%;\n  --accent-foreground: 222 47% 10%;\n  --destructive: 0 62% 40%;\n  --destructive-foreground: 210 40% 96%;\n\n  --border: 222 18% 22%;\n  --input: 222 18% 22%;\n  --ring: 203 78% 70%;\n\n  /* Custom */\n  --surface-2: 222 28% 14%;\n  --shadow-color: 0 0% 0%;\n  --shadow-alpha: 0.35;\n  --law-enacted: 152 60% 86%;\n  --law-proposed: 38 90% 86%;\n  --law-draft: 210 30% 88%;\n}\n\nhtml {\n  font-family: 'IBM Plex Sans', ui-sans-serif, system-ui;\n}\n\nh1,h2,h3,.font-display {\n  font-family: 'Space Grotesk', ui-sans-serif, system-ui;\n}\n\ncode, .font-mono {\n  font-family: 'IBM Plex Mono', ui-monospace, SFMono-Regular;\n}\n\n::selection {\n  background: rgba(79, 182, 200, 0.25);\n}\n"
  },

  "components": {
    "component_path": {
      "shadcn_ui": "/app/frontend/src/components/ui/",
      "use_these": [
        "button.jsx",
        "badge.jsx",
        "card.jsx",
        "tabs.jsx",
        "table.jsx",
        "dialog.jsx",
        "drawer.jsx",
        "sheet.jsx",
        "command.jsx",
        "input.jsx",
        "select.jsx",
        "checkbox.jsx",
        "switch.jsx",
        "tooltip.jsx",
        "scroll-area.jsx",
        "separator.jsx",
        "pagination.jsx",
        "calendar.jsx",
        "sonner.jsx"
      ]
    },

    "top_nav": {
      "layout": "Sticky top bar with search + theme toggle + quick filters",
      "tailwind": "sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80",
      "elements": [
        {
          "name": "Global search (Command)",
          "component": "command.jsx",
          "data_testid": "global-command-search"
        },
        {
          "name": "Theme toggle (Switch or Button)",
          "component": "switch.jsx",
          "data_testid": "theme-toggle"
        },
        {
          "name": "Last updated timestamp",
          "component": "badge.jsx",
          "data_testid": "data-freshness-badge"
        }
      ]
    },

    "map_card": {
      "container": "Card with map + legend + hover preview",
      "use": ["card.jsx", "tooltip.jsx", "hover-card.jsx"],
      "card_class": "rounded-xl border bg-card shadow-[0_10px_30px_rgba(0,0,0,var(--shadow-alpha))]",
      "header": {
        "title": "Explore by country",
        "subtitle": "Click a country to view laws, timeline, and sources.",
        "right_controls": ["Tabs: Maturity / Status", "Zoom controls"]
      },
      "legend": {
        "style": "Compact horizontal legend with 5 swatches + labels",
        "tailwind": "flex flex-wrap items-center gap-2 text-xs text-muted-foreground",
        "data_testid": "map-legend"
      },
      "hover_behavior": {
        "country_hover": "On hover: outline + tooltip with country name + counts (enacted/proposed/draft).",
        "tooltip_component": "tooltip.jsx",
        "data_testid": "map-country-tooltip"
      }
    },

    "law_card": {
      "use": ["card.jsx", "badge.jsx", "button.jsx"],
      "layout": "Title + metadata row + summary (2–3 lines) + tags + CTA",
      "card_class": "group rounded-xl border bg-card p-4 sm:p-5 shadow-sm hover:shadow-md",
      "hover": "On hover: elevate shadow + subtle border tint; reveal quick actions row.",
      "quick_actions": [
        {
          "label": "Open details",
          "variant": "secondary",
          "data_testid": "law-card-open-details"
        },
        {
          "label": "Copy citation",
          "variant": "ghost",
          "data_testid": "law-card-copy-citation"
        }
      ],
      "badges": {
        "status_badge": {
          "component": "badge.jsx",
          "data_testid": "law-status-badge",
          "style": "Use semantic status colors; include icon via lucide-react (check, clock, file-text)."
        },
        "category_tags": {
          "style": "Muted outline badges",
          "data_testid": "law-category-tag"
        }
      }
    },

    "filters_panel": {
      "desktop": "Left rail or right side panel (Sheet) with sticky apply/reset",
      "mobile": "Bottom Drawer with sections (Accordion)",
      "use": ["sheet.jsx", "drawer.jsx", "accordion.jsx", "select.jsx", "checkbox.jsx", "calendar.jsx"],
      "controls": [
        {
          "name": "Region",
          "component": "select.jsx",
          "data_testid": "filter-region"
        },
        {
          "name": "Status",
          "component": "toggle-group.jsx",
          "data_testid": "filter-status"
        },
        {
          "name": "Year range",
          "component": "slider.jsx",
          "data_testid": "filter-year-range"
        },
        {
          "name": "Date picker (optional for enacted date)",
          "component": "calendar.jsx",
          "data_testid": "filter-date-calendar"
        },
        {
          "name": "Reset",
          "component": "button.jsx",
          "data_testid": "filters-reset-button"
        },
        {
          "name": "Apply",
          "component": "button.jsx",
          "data_testid": "filters-apply-button"
        }
      ]
    },

    "law_detail": {
      "pattern": "Desktop: Dialog; Mobile: Drawer",
      "use": ["dialog.jsx", "drawer.jsx", "tabs.jsx", "scroll-area.jsx", "separator.jsx"],
      "sections": [
        "Overview (summary + status + dates)",
        "Key provisions (bulleted)",
        "Scope & definitions",
        "Source links (always visible)",
        "Related laws"
      ],
      "source_links": {
        "style": "Use external-link icon; show domain + last accessed",
        "data_testid": "law-source-links"
      }
    },

    "timeline_view": {
      "use": ["tabs.jsx", "card.jsx", "separator.jsx"],
      "layout": "Year rail (left) + events list (right). Mobile: stacked with sticky year chips.",
      "micro_interaction": "Scroll-linked highlight of current year; smooth anchor jumps.",
      "data_testid": "timeline-view"
    },

    "compare_view": {
      "use": ["select.jsx", "table.jsx", "tabs.jsx", "badge.jsx"],
      "layout": "Pick 2–3 countries → comparison table + mini charts",
      "table": {
        "style": "Sticky first column; zebra rows via muted surfaces",
        "data_testid": "country-compare-table"
      }
    },

    "stats_and_charts": {
      "charts_library": "recharts",
      "chart_cards": "Use Card with header + small legend; keep axes subtle.",
      "recommended_charts": [
        "Stacked bar: enacted/proposed/draft by region",
        "Line: laws over time",
        "Donut: category distribution"
      ],
      "chart_colors": {
        "enacted": "#1F7A8C",
        "proposed": "#F59E0B (use toned down in dark mode)",
        "draft": "#64748B",
        "neutral_grid": "use border token"
      },
      "data_testid": "stats-dashboard"
    },

    "ai_assistant_panel": {
      "no_purple_rule": "Assistant accents must use ocean/teal + slate neutrals.",
      "use": ["card.jsx", "textarea.jsx", "button.jsx", "scroll-area.jsx", "sonner.jsx"],
      "layout": "Right-side resizable panel on desktop; full page on mobile.",
      "message_bubbles": {
        "user": "bg-primary text-primary-foreground",
        "assistant": "bg-secondary text-foreground border",
        "citations": "Use mono + small chips linking to sources"
      },
      "streaming": "Show typing indicator skeleton lines; keep scroll pinned to bottom unless user scrolls up.",
      "data_testid": {
        "panel": "ai-assistant-panel",
        "input": "ai-assistant-input",
        "send": "ai-assistant-send-button",
        "message": "ai-assistant-message"
      }
    }
  },

  "motion_and_microinteractions": {
    "libraries": {
      "framer_motion": {
        "why": "Map hover previews, panel transitions, list reordering, subtle entrance animations.",
        "install": "npm i framer-motion",
        "usage_notes": [
          "Prefer opacity + translateY (4–8px) for entrances",
          "Use layout animations for card grid changes",
          "Respect prefers-reduced-motion"
        ]
      }
    },
    "principles": {
      "durations": {
        "fast": "120–160ms",
        "base": "180–220ms",
        "slow": "260–320ms"
      },
      "easing": {
        "standard": "cubic-bezier(0.2, 0.8, 0.2, 1)",
        "emphasis": "cubic-bezier(0.16, 1, 0.3, 1)"
      },
      "hover": [
        "Buttons: bg/border change + shadow change (no transform unless intentional)",
        "Cards: shadow-sm → shadow-md, border tint",
        "Map: outline + tooltip fade-in"
      ],
      "scroll": [
        "Sticky legend + subtle blur on top nav",
        "Timeline year highlight transitions"
      ]
    },
    "tailwind_snippets": {
      "button_hover": "transition-colors duration-200",
      "card_hover": "transition-shadow duration-200 hover:shadow-md",
      "tooltip": "data-[state=delayed-open]:animate-in data-[state=closed]:animate-out"
    }
  },

  "accessibility": {
    "contrast": "WCAG AA for text; ensure badges have sufficient contrast in both themes.",
    "keyboard": [
      "Map countries must be focusable (tabIndex=0) with visible focus outline",
      "Command search opens with Ctrl/Cmd+K",
      "Dialog/Drawer traps focus (shadcn handles)"
    ],
    "reduced_motion": "Wrap motion with prefers-reduced-motion checks; disable parallax.",
    "colorblind": "Never rely on color alone for status—pair with icon + label."
  },

  "data_density_rules": {
    "law_cards": {
      "max_summary_lines": 3,
      "always_show": ["country", "status", "year", "category", "source count"],
      "progressive_disclosure": "Full provisions only in detail drawer/dialog"
    },
    "tables": {
      "sticky_header": true,
      "row_height": "py-3",
      "empty_state": "Use Skeleton + helpful copy + reset filters button"
    }
  },

  "image_urls": {
    "note": "Image selector tool failed in this environment. Use CSS-based visuals instead: subtle noise overlay + map-driven visuals. If you later enable providers, fetch: abstract map textures, government architecture, document flatlays.",
    "css_noise_overlay": {
      "category": "background texture",
      "description": "Add a subtle grain/noise overlay via CSS to avoid flat surfaces.",
      "snippet": ".noise::before{content:'';position:absolute;inset:0;background-image:url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"120\" height=\"120\"><filter id=\"n\"><feTurbulence type=\"fractalNoise\" baseFrequency=\"0.9\" numOctaves=\"2\" stitchTiles=\"stitch\"/></filter><rect width=\"120\" height=\"120\" filter=\"url(%23n)\" opacity=\"0.08\"/></svg>');mix-blend-mode:overlay;pointer-events:none;}"
    }
  },

  "instructions_to_main_agent": {
    "theme_toggle_persistence": [
      "Use class-based dark mode (already in index.css tokens).",
      "Persist user choice in localStorage key: theme=light|dark|system.",
      "Toggle must have data-testid=theme-toggle.",
      "Animate theme change by transitioning background-color and color only on body/surfaces (no transition: all)."
    ],
    "react_simple_maps": [
      "Use the maturity scale bins for fill colors.",
      "On hover/focus: apply outline stroke + tooltip.",
      "On click: open country side panel (Sheet) with laws list.",
      "All countries should be keyboard focusable and have aria-label with country name."
    ],
    "status_badges": [
      "Implement a status→className mapping (enacted/proposed/draft/superseded).",
      "Badge must include icon + text label.",
      "Badge must include data-testid=law-status-badge."
    ],
    "testing_attributes": [
      "Add data-testid to: map, legend, filters, search, law cards, compare selectors, timeline, chat input/send, dialogs/drawers.",
      "Use kebab-case describing role (not appearance)."
    ],
    "remove_default_cra_styles": [
      "App.css currently contains CRA demo styles; remove/ignore .App-header centering patterns.",
      "Do not add .App { text-align:center }."
    ]
  },

  "general_ui_ux_design_guidelines": [
    "- You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms",
    "- You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text",
    "- NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json",
    "\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead.\n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals."
  ]
}
