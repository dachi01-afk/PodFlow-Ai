# PodFlow AI Frontend Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a responsive dashboard UI for PodFlow AI using Jinja2 + HTMX + Tailwind CSS with dark theme, episode management, and real-time updates.

**Architecture:** Server-side rendered HTML templates with HTMX for dynamic updates. Tailwind CSS via CDN for styling. FastAPI serves templates and static files.

**Tech Stack:** Jinja2, HTMX 1.9.10, Tailwind CSS (CDN), FastAPI

## Global Constraints

- Python 3.9+ (Vercel runtime)
- FastAPI backend (existing)
- No additional JavaScript frameworks
- Dark theme (gray-900 background, purple accent)
- All API calls via HTMX (no custom JS)

---

## File Structure

```
templates/
├── base.html          # Base template with nav, Tailwind, HTMX
├── dashboard.html     # Episodes list + stats cards
├── episode.html       # Episode detail + pipeline progress + player
└── create.html        # Create episode form

static/
└── css/
    └── styles.css     # Custom styles (progress bar, badges, animations)
```

---

### Task 1: Create Base Template

**Files:**
- Create: `templates/base.html`

**Interfaces:**
- Produces: Base layout for all pages (nav, scripts, content block)

- [ ] **Step 1: Create templates/base.html**

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PodFlow AI - {% block title %}Dashboard{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <nav class="bg-gray-800 p-4">
        <div class="container mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-purple-400">🎙️ PodFlow AI</a>
            <div class="space-x-4">
                <a href="/" class="hover:text-purple-400">Dashboard</a>
                <a href="/create" class="bg-purple-600 px-4 py-2 rounded hover:bg-purple-700">+ New Episode</a>
            </div>
        </div>
    </nav>
    
    <main class="container mx-auto p-6">
        {% block content %}{% endblock %}
    </main>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            setInterval(function() {
                htmx.trigger('#episodes-list', 'refresh');
            }, 5000);
        });
    </script>
</body>
</html>
```

- [ ] **Step 2: Verify template loads**

Run: `curl http://localhost:8000/`
Expected: HTML response with nav bar

- [ ] **Step 3: Commit**

```bash
git add templates/base.html
git commit -m "feat: add base template with nav and HTMX"
```

---

### Task 2: Create Dashboard Page

**Files:**
- Create: `templates/dashboard.html`

**Interfaces:**
- Consumes: Base template (Task 1)
- Produces: Episodes list with stats cards

- [ ] **Step 1: Create templates/dashboard.html**

```html
{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="mb-6">
    <h1 class="text-3xl font-bold mb-2">Podcast Dashboard</h1>
    <p class="text-gray-400">Kelola episode podcast Anda secara otonom</p>
</div>

<!-- Stats -->
<div class="grid grid-cols-4 gap-4 mb-6">
    <div class="bg-gray-800 p-4 rounded-lg">
        <div class="text-2xl font-bold text-purple-400">--</div>
        <div class="text-gray-400">Total Episodes</div>
    </div>
    <div class="bg-gray-800 p-4 rounded-lg">
        <div class="text-2xl font-bold text-green-400">--</div>
        <div class="text-gray-400">Completed</div>
    </div>
    <div class="bg-gray-800 p-4 rounded-lg">
        <div class="text-2xl font-bold text-yellow-400">--</div>
        <div class="text-gray-400">Processing</div>
    </div>
    <div class="bg-gray-800 p-4 rounded-lg">
        <div class="text-2xl font-bold text-red-400">--</div>
        <div class="text-gray-400">Failed</div>
    </div>
</div>

<!-- Episodes List -->
<div id="episodes-list" 
     hx-get="/api/episodes" 
     hx-trigger="refresh from:body" 
     hx-swap="innerHTML"
     class="bg-gray-800 rounded-lg p-4">
    <div class="text-center text-gray-400 py-8">Loading episodes...</div>
</div>

{% endblock %}
```

- [ ] **Step 2: Verify dashboard loads**

Run: `curl http://localhost:8000/`
Expected: Dashboard with stats cards and loading indicator

- [ ] **Step 3: Commit**

```bash
git add templates/dashboard.html
git commit -m "feat: add dashboard page with stats and episode list"
```

---

### Task 3: Create Episode Detail Page

**Files:**
- Create: `templates/episode.html`

**Interfaces:**
- Consumes: Base template (Task 1)
- Produces: Episode detail with pipeline progress and audio player

- [ ] **Step 1: Create templates/episode.html**

```html
{% extends "base.html" %}

{% block title %}Episode Detail{% endblock %}

{% block content %}
<div id="episode-detail" 
     hx-get="/api/episodes/{{ episode_id }}" 
     hx-trigger="load, every 5s" 
     hx-swap="innerHTML">
    <div class="text-center text-gray-400 py-8">Loading episode...</div>
</div>
{% endblock %}
```

- [ ] **Step 2: Verify episode page loads**

Run: `curl http://localhost:8000/episode/{episode_id}`
Expected: Episode detail page with loading indicator

- [ ] **Step 3: Commit**

```bash
git add templates/episode.html
git commit -m "feat: add episode detail page"
```

---

### Task 4: Create Episode Form

**Files:**
- Create: `templates/create.html`

**Interfaces:**
- Consumes: Base template (Task 1)
- Produces: Create episode form

- [ ] **Step 1: Create templates/create.html**

```html
{% extends "base.html" %}

{% block title %}Create Episode{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Create New Episode</h1>
    
    <form hx-post="/api/episodes" 
          hx-swap="none"
          hx-on::after-request="if(event.detail.successful) window.location='/'"
          class="bg-gray-800 p-6 rounded-lg space-y-4">
        
        <div>
            <label class="block text-gray-400 mb-2">Channel</label>
            <select name="channel_id" required
                    class="w-full bg-gray-700 rounded px-4 py-2 focus:ring-2 focus:ring-purple-500">
                <option value="">Select Channel</option>
            </select>
        </div>
        
        <div>
            <label class="block text-gray-400 mb-2">Topic</label>
            <input type="text" name="topic" required
                   placeholder="Contoh: Strategi Keuangan Mikro untuk Usaha Kecil"
                   class="w-full bg-gray-700 rounded px-4 py-2 focus:ring-2 focus:ring-purple-500">
        </div>
        
        <button type="submit" 
                class="w-full bg-purple-600 hover:bg-purple-700 py-3 rounded font-bold">
            🚀 Create & Start Production
        </button>
    </form>
</div>
{% endblock %}
```

- [ ] **Step 2: Verify create form loads**

Run: `curl http://localhost:8000/create`
Expected: Create form with channel select and topic input

- [ ] **Step 3: Commit**

```bash
git add templates/create.html
git commit -m "feat: add create episode form"
```

---

### Task 5: Create Custom Styles

**Files:**
- Create: `static/css/styles.css`

**Interfaces:**
- Produces: Custom CSS for progress bars, status badges, animations

- [ ] **Step 1: Create static/css/styles.css**

```css
/* Custom styles for PodFlow AI */

/* Progress bar animation */
.progress-bar {
    transition: width 0.5s ease-in-out;
}

/* Status badges */
.status-pending { @apply bg-gray-500; }
.status-researching { @apply bg-blue-500; }
.status-writing { @apply bg-yellow-500; }
.status-producing { @apply bg-orange-500; }
.status-publishing { @apply bg-purple-500; }
.status-completed { @apply bg-green-500; }
.status-failed { @apply bg-red-500; }

/* Pulse animation for processing */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.animate-pulse {
    animation: pulse 2s infinite;
}
```

- [ ] **Step 2: Verify styles load**

Run: `curl http://localhost:8000/static/css/styles.css`
Expected: CSS file returned

- [ ] **Step 3: Commit**

```bash
git add static/css/styles.css
git commit -m "feat: add custom styles for progress bars and badges"
```

---

### Task 6: Update Main.py for Templates

**Files:**
- Modify: `main.py`

**Interfaces:**
- Consumes: Templates (Tasks 1-4)
- Produces: HTML responses for page routes

- [ ] **Step 1: Update main.py to serve templates**

Add to `main.py`:

```python
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/create", response_class=HTMLResponse)
async def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.get("/episode/{episode_id}", response_class=HTMLResponse)
async def episode_page(request: Request, episode_id: str):
    return templates.TemplateResponse("episode.html", {"request": request, "episode_id": episode_id})
```

- [ ] **Step 2: Verify pages load**

Run: `curl http://localhost:8000/`
Expected: HTML dashboard page

- [ ] **Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add template routes for dashboard pages"
```

---

### Task 7: Test Full Dashboard

**Files:**
- None (testing only)

**Interfaces:**
- None

- [ ] **Step 1: Start server**

Run: `python main.py`

- [ ] **Step 2: Test all pages**

- `http://localhost:8000/` - Dashboard
- `http://localhost:8000/create` - Create form
- `http://localhost:8000/episode/{id}` - Episode detail

- [ ] **Step 3: Test HTMX updates**

- Create new episode via form
- Verify auto-refresh updates list
- Test audio player playback

- [ ] **Step 4: Final commit**

```bash
git add .
git commit -m "feat: complete frontend dashboard implementation"
```
