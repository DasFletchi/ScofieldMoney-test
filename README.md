# 🤖 ChatNoLogin

**Free AI Chat - No Login Required**

A minimalist AI chatbot that works without signup. Just open and chat!

---

## 🚀 Live Demo

**https://dasfletchi.github.io/NoLoginChat/**

---

## ✨ Features

- **No Login Required** - Just open and start chatting
- **Session-Based** - Your chat is saved in your URL (shareable)
- **Privacy First** - No tracking, no accounts, no data collection
- **Mobile Ready** - Works great on phone and desktop
- **Dark Theme** - Easy on the eyes
- **Code Highlighting** - Copy code blocks with one click

---

## 🔧 Setup AI (Optional)

The app works in **Demo Mode** by default. To enable real AI:

1. Edit `src/App.jsx`
2. Add your API key:

```javascript
const API_KEY = 'your-key-here'
const MODEL = 'meta-llama/llama-3.1-8b-instruct'
const API_URL = 'https://openrouter.ai/api/v1/chat/completions'
```

3. Redeploy!

### Free APIs to Use:
- **OpenRouter** (recommended) - openrouter.ai
- **OpenAI** - platform.openai.com  
- **Anthropic** - anthropic.com
- **Groq** - groq.com

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | React + Vite |
| Styling | Custom CSS |
| Hosting | GitHub Pages |
| Storage | localStorage (browser) |

---

## 📱 Usage

1. Open the URL
2. Start typing
3. Share the URL to save/share your chat

---

## 📄 Files

```
├── src/
│   ├── App.jsx       # Main chat component
│   ├── index.css      # Styling
│   └── main.jsx      # Entry point
├── index.html        # HTML template
├── package.json      # Dependencies
└── vite.config.js   # Build config
```

---

## 🚀 Deploy

```bash
# Install deps
npm install

# Build
npm run build

# Deploy to GitHub Pages
# Just push to main branch!
```

---

## 📊 Marketing

- **SEO Keywords**: `seo_keywords.csv`
- **Social Posts**: `social_posts/drafts.md`
- **Ad Copy**: `ads/copy.md`

---

Built with ❤️ by Scofield 🤖
