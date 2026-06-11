# 🎬 AtlasRAG — Demo GIF Creation Guide

> A step-by-step guide to recording a polished demo GIF of the AtlasRAG premium dark UI and adding it to the project README.

---

## Table of Contents

1. [Recommended Tools](#-1-recommended-tools)
2. [Optimal Recording Settings](#-2-optimal-recording-settings)
3. [What to Capture (Demo Flow)](#-3-what-to-capture-demo-flow)
4. [How to Optimize File Size](#-4-how-to-optimize-file-size)
5. [How to Add the GIF to README.md](#-5-how-to-add-the-gif-to-readmemd)
6. [Quick-Reference Cheatsheet](#-quick-reference-cheatsheet)

---

## 🛠️ 1. Recommended Tools

### Option A — ScreenToGif ⭐ Best Pick

| | |
| :--- | :--- |
| **Platform** | Windows (FREE & open-source) |
| **Download** | [https://www.screentogif.com](https://www.screentogif.com) |
| **Why** | Built-in editor, frame-by-frame control, direct GIF export |

**How to use:**

1. Download and install from the link above (portable version also available — no install needed).
2. Launch **ScreenToGif** → click **Recorder**.
3. Resize the transparent capture frame to cover the AtlasRAG Streamlit window.
4. Click the red **⏺ Record** button, perform the demo flow (see [Section 3](#-3-what-to-capture-demo-flow)), then click **⏹ Stop**.
5. The built-in **Editor** opens automatically:
   - Delete any unnecessary frames at the start/end.
   - Go to **Image → Resize** and set width to **800** or **960** px.
   - Go to **File → Save As → GIF** and tweak quality (see [Section 2](#-2-optimal-recording-settings)).
6. Save the file as `demo.gif`.

> [!TIP]
> Use the **"Fixed Frame Rate"** option under Playback in the editor to lock your GIF to a consistent 12–15 FPS before exporting.

---

### Option B — LICEcap (Lightweight Alternative)

| | |
| :--- | :--- |
| **Platform** | Windows / macOS (FREE) |
| **Download** | [https://www.cockos.com/licecap](https://www.cockos.com/licecap) |
| **Why** | Tiny footprint (~200 KB), records directly to `.gif` |

**How to use:**

1. Download and run **LICEcap** (no install required).
2. Position the semi-transparent window over the AtlasRAG UI.
3. Set the **Max FPS** to `12` in the bottom bar.
4. Click **Record…**, choose a save location, and perform the demo flow.
5. Click **Stop** when done. Your GIF is ready instantly.

> [!NOTE]
> LICEcap produces the GIF immediately but has no built-in editor. If you need to trim frames or adjust colors, pair it with [gifsicle](https://www.lcdf.org/gifsicle/) or [ezgif.com](https://ezgif.com).

---

### Option C — ffmpeg (Convert MP4 → GIF from Command Line)

Best if you already have a screen recording as an `.mp4` file (e.g., from OBS Studio, Xbox Game Bar `Win + G`, or ShareX).

**Install ffmpeg on Windows:**

```powershell
# Using winget (built into Windows 10/11):
winget install Gyan.FFmpeg

# Or using Chocolatey:
choco install ffmpeg
```

**Convert an MP4 to a high-quality GIF:**

```bash
# Two-pass method for best color quality:

# Step 1 — Generate an optimized color palette
ffmpeg -i input.mp4 -vf "fps=12,scale=800:-1:flags=lanczos,palettegen" palette.png

# Step 2 — Create the GIF using that palette
ffmpeg -i input.mp4 -i palette.png -lavfi "fps=12,scale=800:-1:flags=lanczos [x]; [x][1:v] paletteuse" output.gif
```

> [!IMPORTANT]
> The two-pass palette method produces **significantly** better colors than a single-pass conversion — especially important for the AtlasRAG dark UI where banding artifacts are very visible.

---

## ⚙️ 2. Optimal Recording Settings

Use these settings for a GIF that looks crisp on GitHub while staying lightweight:

| Setting | Recommended Value | Why |
| :--- | :--- | :--- |
| **Dimensions** | `800×450` or `960×540` | 16:9 aspect ratio; fills GitHub README width nicely |
| **Frame Rate** | `12–15 FPS` | Smooth enough to read; keeps file size small |
| **Duration** | `15–25 seconds` max | Holds attention; GitHub renders inline GIFs best at this length |
| **Color Depth** | `128–256 colors` | GIF max is 256; dropping to 128 cuts size ~30% |
| **File Size Target** | `< 10 MB` | GitHub displays inline up to 10 MB; smaller = faster loading |
| **Looping** | `Infinite loop` | The GIF should restart seamlessly |

> [!WARNING]
> GIFs over **10 MB** will still render on GitHub but load very slowly for visitors on mobile. Always aim for the smallest file size that looks acceptable.

---

## 🎥 3. What to Capture (Demo Flow)

Follow this exact sequence for a professional, compelling demo. Practice it once before recording!

### Pre-Recording Checklist

- [ ] AtlasRAG is running (`streamlit run app.py`)
- [ ] Browser is in **full-screen** or sized to **800×450** / **960×540**
- [ ] Dark theme is active (it should be by default)
- [ ] Chat history is **cleared** (fresh state)
- [ ] A sample PDF is ready on the Desktop for quick drag-and-drop

### The Demo Script (6 Beats)

```
Beat 1 → The Hero Shot              (~3 sec)
Beat 2 → Upload a PDF               (~4 sec)
Beat 3 → Update Knowledge Base      (~4 sec)
Beat 4 → Type a Question            (~4 sec)
Beat 5 → AI Response + Scores       (~5 sec)
Beat 6 → Final Beauty Shot          (~3 sec)
```

#### Beat 1 — The Hero Shot (3 seconds)
Pause on the **empty premium UI**. Let the viewer absorb:
- The dark theme background
- The hero header / branding
- The clean, empty chat area
- The sidebar with controls

#### Beat 2 — Upload a PDF (4 seconds)
- Open the sidebar (if collapsed).
- **Drag and drop** a PDF file onto the upload area.
- Let the filename appear in the uploader widget.

#### Beat 3 — Update Knowledge Base (4 seconds)
- Click the **"Update Knowledge Base"** button.
- Let the **progress bar / spinner** animate fully.
- Wait for the success message to appear.

#### Beat 4 — Type a Question (4 seconds)
- Click the chat input box.
- **Type slowly and deliberately** (viewers need to read along):
  - Example: *"Explain Kirchhoff's Current Law with an example."*
- Press Enter.

> [!TIP]
> Type at about **half your normal speed**. Fast typing in GIFs looks like a blur and viewers can't follow along.

#### Beat 5 — AI Response + Evaluation Scores (5 seconds)
- Let the response stream in.
- Pause so the viewer can see:
  - The AI-generated answer text
  - The **Faithfulness** score bar
  - The **Relevance** score bar
- Hold for a beat so the numbers register.

#### Beat 6 — Final Beauty Shot (3 seconds)
- Keep the cursor still.
- Let the final state sit on screen — the complete conversation with scores visible.
- This is the frame that lingers when the GIF loops back.

---

## 📉 4. How to Optimize File Size

GIFs can balloon in size quickly. Here's how to keep `demo.gif` lean and fast-loading.

### Strategy 1 — Reduce Color Depth

GIFs support up to 256 colors. Dropping to **128 colors** saves ~30% with minimal visible difference on a dark UI.

**In ScreenToGif:**
- Editor → **File → Save As** → set **Maximum Colors** to `128`.

### Strategy 2 — Crop to the Essential Area

Don't record the entire desktop. Crop tightly to just the Streamlit app window — no browser chrome, no taskbar, no bookmark bar.

**In ScreenToGif:**
- Editor → **Image → Crop** → drag to select the essential area.

### Strategy 3 — ffmpeg Conversion with Optimization

If you recorded as MP4 first:

```bash
# Single command — good quality, small file
ffmpeg -i input.mp4 -vf "fps=12,scale=800:-1:flags=lanczos" -c:v gif output.gif
```

For best results, use the **two-pass palette method** from [Section 1C](#option-c--ffmpeg-convert-mp4--gif-from-command-line).

### Strategy 4 — gifsicle Compression (Final Polish)

[gifsicle](https://www.lcdf.org/gifsicle/) squeezes out extra bytes from any GIF.

```powershell
# Install via Chocolatey
choco install gifsicle

# Optimize the GIF (O3 = maximum compression)
gifsicle -O3 --colors 128 --lossy=80 demo.gif -o demo_optimized.gif
```

### Strategy 5 — Use ezgif.com (No Install)

If you prefer a web-based tool:

1. Go to [ezgif.com/optimize](https://ezgif.com/optimize)
2. Upload your GIF
3. Choose **"Lossy GIF"** compression at level **80–100**
4. Download the optimized version

### File Size Troubleshooting

| File Size | Action |
| :--- | :--- |
| **< 5 MB** | ✅ Perfect — ship it! |
| **5–10 MB** | ⚠️ Acceptable — try reducing colors or trimming 2–3 seconds |
| **10–15 MB** | 🔶 Too large — crop area, lower FPS to 10, reduce to 128 colors |
| **> 15 MB** | 🔴 Way too large — re-record at smaller dimensions or shorter duration |

---

## 📝 5. How to Add the GIF to README.md

### Step 1 — Save the GIF

Place the final optimized GIF in the project's existing `assets/` folder:

```
AtlasRAG/
├── assets/
│   ├── atlasrag_architecture.png   ← already here
│   └── demo.gif                    ← add your GIF here
├── README.md
└── ...
```

### Step 2 — Add to README.md

Insert the following markdown in your `README.md`, ideally right below the badges and tagline (before the **Key Features** section):

```markdown
## 🎬 Live Demo

<p align="center">
  <img src="assets/demo.gif" alt="AtlasRAG Demo" width="800">
</p>
```

Or for a simpler inline approach:

```markdown
## 🎬 Live Demo

![AtlasRAG Demo](assets/demo.gif)
```

> [!NOTE]
> The `<p align="center">` version centers the GIF and gives you explicit width control, which looks more polished on GitHub. The simple `![...]()` syntax is quicker but left-aligns the GIF.

### Step 3 — Commit and Push

```bash
# Stage the GIF file
git add assets/demo.gif

# Commit with a descriptive message
git commit -m "docs: add demo GIF showcasing RAG pipeline"

# Push to your remote
git push origin main
```

> [!CAUTION]
> Git tracks binary files (like GIFs) forever in history. If you re-record the demo later, the old version stays in the repo. To keep the repo lean, **get the GIF right before committing** — or use [Git LFS](https://git-lfs.github.com/) for large assets.

---

## 📋 Quick-Reference Cheatsheet

```
┌──────────────────────────────────────────────────────┐
│               ATLASRAG DEMO GIF RECIPE               │
├──────────────────────────────────────────────────────┤
│                                                      │
│  TOOL:      ScreenToGif (screentogif.com)            │
│  SIZE:      800×450  or  960×540                     │
│  FPS:       12–15                                    │
│  DURATION:  15–25 seconds                            │
│  COLORS:    128                                      │
│  TARGET:    < 10 MB  (ideally < 5 MB)                │
│                                                      │
│  FLOW:                                               │
│  1. Hero shot (empty UI)          3 sec              │
│  2. Upload PDF                    4 sec              │
│  3. Update Knowledge Base         4 sec              │
│  4. Type a question               4 sec              │
│  5. AI response + scores          5 sec              │
│  6. Final beauty shot             3 sec              │
│                                        ───────       │
│                                  TOTAL: ~23 sec      │
│                                                      │
│  OPTIMIZE:                                           │
│  gifsicle -O3 --colors 128 --lossy=80 in.gif -o out │
│                                                      │
│  ADD TO README:                                      │
│  ![AtlasRAG Demo](assets/demo.gif)                  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

*Happy recording! 🎥 A great demo GIF is the fastest way to make AtlasRAG shine on GitHub.*
