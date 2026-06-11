# 🎬 AtlasRAG — LinkedIn Screen Recording Guide

A step-by-step guide to create a professional demo video of AtlasRAG for LinkedIn.

---

## 📋 Pre-Recording Checklist

Before you hit record, set up your environment:

- [ ] **Close all notifications** — Turn on Do Not Disturb (Windows: Focus Assist)
- [ ] **Clean browser** — Close unnecessary tabs, clear bookmarks bar if visible
- [ ] **Prepare demo PDF** — Have a good PDF ready (e.g., `BEE module 1 notes.pdf` or `Gen_AI.pdf`)
- [ ] **Clear chat history** — Click "🗑️ Clear Conversation" in sidebar
- [ ] **Reset knowledge base** — Fresh start looks better on camera
- [ ] **Set browser zoom** — 90-100% zoom, fullscreen (F11)
- [ ] **Dark mode browser** — Use a dark browser theme to match the app's dark UI
- [ ] **Prepare questions** — Write 1-2 impressive questions in a notepad for copy-paste
- [ ] **Close VS Code / terminal** — Only the Streamlit app should be visible
- [ ] **Resolution** — Set display to 1920×1080 if possible

---

## 🛠️ Recommended Recording Tools

### Option 1: OBS Studio (FREE — Best Quality)
- **Download:** https://obsproject.com/
- **Settings:**
  - Output: MP4, H.264 encoder
  - Resolution: 1920×1080
  - FPS: 30
  - Audio: Optional (you can add voiceover later)
- **How:** Sources → Display Capture → Start Recording

### Option 2: Loom (FREE tier — Easiest)
- **Download:** https://www.loom.com/
- **Best for:** Quick recordings with webcam overlay
- **Note:** Free tier = 5 min limit per video (more than enough)

### Option 3: ScreenPal (FREE tier)
- **Download:** https://screenpal.com/
- **Best for:** Quick screen recording with basic editing built-in

### Option 4: Windows Built-in (Snipping Tool)
- **How:** `Win + Shift + S` → then use `Win + Alt + R` for Xbox Game Bar recording
- **Limitation:** Can't record desktop, only apps

> 💡 **Recommendation:** Use **OBS Studio** for best quality, or **Loom** for quickest setup.

---

## 🎬 Shot-by-Shot Script (2 minutes)

Follow this exact flow for maximum impact:

### 🔥 Scene 1: The Hook (0:00 – 0:05)
**What to show:** Start with the FINAL result — a completed AI response with glowing Faithfulness and Relevance metric cards showing 95%+ scores.

> **Why:** LinkedIn autoplay shows the first 3 seconds. Start with the impressive payoff to hook viewers.

**Action:** Have a pre-loaded conversation ready. Scroll to show the beautiful response + metrics.

---

### 🏷️ Scene 2: Quick Intro (0:05 – 0:15)
**What to show:** Scroll to the top. Show the full premium dark UI — the hero header with "AtlasRAG" gradient title and the tagline.

**Optional text overlay (add in post):**
> *"I built an AI system that corrects its own hallucinations"*

---

### 📂 Scene 3: Upload Demo (0:15 – 0:40)
**What to show:**
1. Click the sidebar
2. Adjust the **Chunk Size slider** — slide it from 1000 to 1500 and back (shows configurability)
3. Click "Drop your PDFs here" and select your demo PDF
4. Show the file count badge ("📎 1 file selected")
5. Click **"🚀 Update Knowledge Base"**
6. Show the progress bar filling up with status messages:
   - "📂 Preparing files..."
   - "📄 Parsing documents..."
   - "✂️ Chunking (1000 tokens)..."
   - "🧠 Building vector index..."
   - "✅ Knowledge Base Ready!"
7. Show the status pill change to **green "Knowledge Base Active"**

> **Tip:** This is the most impressive part visually. Let it play out fully.

---

### 💬 Scene 4: The Magic — Ask a Question (0:40 – 1:15)
**What to show:**
1. Click on the chat input
2. Type (or paste) an impressive question:
   - If using BEE notes: *"Explain Kirchhoff's Current Law with a practical example"*
   - If using Gen_AI.pdf: *"What are the key differences between supervised and unsupervised learning?"*
3. Hit Enter
4. Show "Searching knowledge base..." state
5. Watch the AI response appear
6. **Key moment:** Show the **3 metric cards** appearing:
   - 🛡️ Faithfulness: XX%
   - 🎯 Relevance: XX%
   - 📚 Sources Used: X
7. Click **"📖 View Source Context"** expander to show the actual source chunks

> **Tip:** Type slowly and deliberately — it looks more professional on video.

---

### 🔍 Scene 5: Architecture Highlight (1:15 – 1:35)
**What to show:**
1. Ask a second, different question to show consistency
2. While it processes, you could add a text overlay explaining:
   - "Hybrid Search: Vector + BM25"
   - "LLM-as-a-Judge evaluation"
3. Show the second response with its own metric scores

---

### 🎬 Scene 6: Closing (1:35 – 2:00)
**What to show:**
1. Click **"📥 Export Chat History"** to show the download feature
2. Scroll up to show the full beautiful conversation
3. Show the sidebar Model Info section (Gemini 2.5 Flash, MiniLM-L6-v2)

**End card (add in post-production):**
```
🌍 AtlasRAG
github.com/R-Roy03/AtlasRAG
⭐ Star if useful!
```

---

## ✂️ Post-Production Tips

### Adding Captions / Text Overlays
- **CapCut Desktop** (FREE) — Best for quick edits + auto-captions
  - Download: https://www.capcut.com/
  - Use "Auto Captions" feature for voiceover
- **Canva Video Editor** (FREE) — Good for text overlays and end cards
- **DaVinci Resolve** (FREE) — Professional grade, more complex

### Background Music
- Use royalty-free music at LOW volume (10-15%):
  - https://pixabay.com/music/ (Free, no attribution needed)
  - Search: "tech", "inspiring", "corporate" — pick something subtle
- **Duration:** Match to your video length, fade out at end

### Export Settings for LinkedIn
| Setting | Value |
|---------|-------|
| Format | MP4 (H.264) |
| Resolution | 1920×1080 or 1280×720 |
| FPS | 30 |
| Duration | 1:30 – 2:00 (sweet spot) |
| Max file size | 5 GB (LinkedIn limit) |
| Aspect ratio | 16:9 (landscape) |

> 💡 **Pro tip:** LinkedIn's algorithm favors videos under 2 minutes. Keep it tight.

---

## 📝 LinkedIn Post Template

Copy-paste and customize:

```
🚀 I built an AI system that corrects its own hallucinations.

Meet AtlasRAG — an Enterprise RAG platform with a built-in "AI Judge" 
that scores every response before showing it to you.

Here's what makes it different:

🧠 Hybrid Search — Combines Vector (semantic) + BM25 (keyword) retrieval
⚖️ LLM-as-a-Judge — Real-time Faithfulness & Relevance scoring
📄 Live PDF Ingestion — Upload → Chunk → Index → Query in seconds
🔒 Privacy-First — Local ChromaDB, no data leaves your machine
⚡ Cost Optimized — Powered by Google Gemini 2.5 Flash

Tech Stack: Python · Streamlit · LangChain · ChromaDB · Gemini AI

The evaluation engine catches hallucinations BEFORE they reach the user.
That's the gap between a demo project and an enterprise solution.

🔗 Try it yourself: [YOUR_STREAMLIT_URL]
⭐ Star on GitHub: github.com/R-Roy03/AtlasRAG

What feature would you add next? Drop a comment 👇

#GenAI #RAG #LLM #AI #MachineLearning #Python #Streamlit 
#GoogleGemini #LangChain #OpenSource #BuildInPublic #AIEngineering
```

### LinkedIn Posting Tips
1. **Post timing:** Tuesday–Thursday, 8-10 AM IST (peak engagement in India)
2. **First line is everything** — LinkedIn shows only the first 2 lines before "...see more"
3. **Upload as native video** — Don't paste a YouTube link; upload the MP4 directly
4. **Engage in comments** — Reply to every comment within the first 2 hours
5. **Tag relevant people** — Tag mentors, professors, or collaborators
6. **Add a carousel too** — Consider posting an architecture diagram as a follow-up post

---

## 🎯 Quick Recording Checklist

```
□ Notifications off
□ Browser fullscreen + dark mode
□ Demo PDF ready
□ Chat cleared
□ Questions prepared in notepad
□ OBS/Loom open and tested
□ Record a 10-sec test first
□ Do 2-3 takes, pick the best
□ Export as MP4 1080p
□ Add captions in CapCut
□ Upload to LinkedIn as native video
□ Paste the post template
□ Engage with comments for 2 hours
```

---

*Good luck with the recording, Rakesh! 🎬🚀*
