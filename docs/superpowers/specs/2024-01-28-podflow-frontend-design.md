# PodFlow AI - Frontend Dashboard Design

## Overview

Dashboard UI untuk PodFlow AI menggunakan Jinja2 + HTMX + Tailwind CSS dengan dark theme. Menampilkan episodes list, pipeline progress, audio player, dan create episode form.

## Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Template Engine | Jinja2 |
| Real-time Updates | HTMX 1.9.10 |
| CSS Framework | Tailwind CSS (CDN) |
| Server | FastAPI (existing) |

## Pages

### 1. Dashboard (Home)

**Route:** `GET /`

**Components:**
- **Navbar**: Logo "🎙️ PodFlow AI", links ke Dashboard dan "+ New Episode"
- **Stat Cards**: 4 cards (Total Episodes, Completed, Processing, Failed) dengan warna berbeda
- **Episodes List**: Table/card list semua episodes dengan status, progress, aksi

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ 🎙️ PodFlow AI          [Dashboard]  [+ New Episode]    │
├─────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│ │ Total    │ │Completed │ │Processing│ │ Failed   │   │
│ │    12    │ │    8     │ │    3     │ │    1     │   │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                         │
│ [Episodes List with HTMX auto-refresh]                 │
└─────────────────────────────────────────────────────────┘
```

### 2. Episode Detail

**Route:** `GET /episode/{id}`

**Components:**
- **Pipeline Progress**: Visual 4 tahap (Research → Script → Audio → Publish)
- **Episode Info**: Topic, status, duration, created date
- **Audio Player**: HTML5 audio element untuk preview
- **Actions**: Download MP4, View RSS, Delete

**Pipeline Visual:**
```
[✅ Research] → [✅ Script] → [🎙️ Audio] → [⏳ Publish]
     100%          100%         75%           0%
```

### 3. Create Episode

**Route:** `GET /create`

**Components:**
- **Form**: Channel select + Topic input
- **Submit**: "🚀 Create & Start Production" button

## Components

### Episode Card

```
┌─────────────────────────────────────────────────────────┐
│ 🎯 Topic: Strategi Keuangan Mikro untuk UMKM            │
│ Status: ● Completed                                     │
│ Duration: 5:32 | Created: 2024-01-28                    │
│                                                         │
│ [▶ Play Audio] [📥 Download MP4] [📋 View RSS] [🗑️]   │
└─────────────────────────────────────────────────────────┘
```

### Status Badges

| Status | Color | Icon |
|--------|-------|------|
| pending | gray | ⏳ |
| researching | blue | 🔍 |
| writing | yellow | ✍️ |
| producing | orange | 🎙️ |
| publishing | purple | 📤 |
| completed | green | ✅ |
| failed | red | ❌ |

### Progress Bar

- Width berdasarkan persentase status
- Animasi transition 0.5s
- Warna mengikuti status

## HTMX Integration

### Auto-refresh
```html
<div id="episodes-list" 
     hx-get="/api/episodes" 
     hx-trigger="refresh from:body" 
     hx-swap="innerHTML">
```

### Polling
- Setiap 5 detik trigger refresh
- Real-time updates tanpa page reload

## Files to Create

| File | Purpose |
|------|---------|
| `templates/base.html` | Base template with nav, Tailwind, HTMX |
| `templates/dashboard.html` | Episodes list + stats |
| `templates/episode.html` | Episode detail + player |
| `templates/create.html` | Create episode form |
| `static/css/styles.css` | Custom styles (progress bar, badges) |

## API Integration

Dashboard consume existing API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/episodes` | GET | List all episodes |
| `/api/episodes` | POST | Create new episode |
| `/api/episodes/{id}` | GET | Get episode detail |
| `/api/episodes/{id}` | DELETE | Delete episode |
| `/api/pipeline/start/{id}` | POST | Start production |
| `/audio/{filename}` | GET | Stream audio |
| `/video/{filename}` | GET | Stream video |
| `/rss/{channel_id}.xml` | GET | RSS feed |

## Styling

### Colors
- Background: `bg-gray-900`
- Cards: `bg-gray-800`
- Primary: `purple-400/600`
- Success: `green-400`
- Warning: `yellow-400`
- Error: `red-400`

### Typography
- Headings: `font-bold text-2xl/3xl`
- Body: `text-white`
- Muted: `text-gray-400`

## Implementation Order

1. Create `templates/base.html`
2. Create `templates/dashboard.html`
3. Create `templates/episode.html`
4. Create `templates/create.html`
5. Create `static/css/styles.css`
6. Update `main.py` to serve templates
7. Test locally
