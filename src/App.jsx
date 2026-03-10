import { useState, useEffect, useRef } from 'react'

const getSessionId = () => {
  let sessionId = window.location.hash.slice(1)
  if (!sessionId) {
    sessionId = 'sess_' + Math.random().toString(36).slice(2, 15)
    window.location.hash = sessionId
  }
  return sessionId
}

const loadMessages = (sessionId) => {
  try {
    const saved = localStorage.getItem(`chat_${sessionId}`)
    return saved ? JSON.parse(saved) : null
  } catch {
    return null
  }
}

const saveMessages = (sessionId, messages) => {
  try {
    localStorage.setItem(`chat_${sessionId}`, JSON.stringify(messages))
  } catch {}
}

// ============ API CONFIG ============
const API_KEY = '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'
const API_URL = 'https://openrouter.ai/api/v1/chat/completions'

// ALL FREE MODELS from OpenRouter
const FREE_MODELS = [
  // Qwen
  { id: 'qwen/qwen3-next-80b-a3b-instruct:free', name: 'Qwen 3 80B', desc: '⚡ Ultra Fast' },
  { id: 'qwen/qwen3-coder:free', name: 'Qwen Coder', desc: '💻 Best for Code' },
  { id: 'qwen/qwen3-4b:free', name: 'Qwen 3 4B', desc: '🪶 Lightweight' },
  { id: 'qwen/qwen3-vl-30b-a3b-thinking:free', name: 'Qwen VL 30B', desc: '🖼️ Vision + Think' },
  { id: 'qwen/qwen3-vl-235b-a22b-thinking:free', name: 'Qwen VL 235B', desc: '🔥 Most Powerful' },
  
  // StepFun
  { id: 'stepfun/step-3.5-flash:free', name: 'Step 3.5 Flash', desc: '⚡ Fast' },
  
  // NVIDIA
  { id: 'nvidia/nemotron-3-nano-30b-a3b:free', name: 'Nemotron 3 30B', desc: '💪 Strong' },
  { id: 'nvidia/nemotron-nano-12b-v2-vl:free', name: 'Nemotron Nano 12B VL', desc: '🖼️ Vision' },
  { id: 'nvidia/nemotron-nano-9b-v2:free', name: 'Nemotron Nano 9B', desc: '📱 Efficient' },
  
  // Google
  { id: 'google/gemma-3-27b-it:free', name: 'Gemma 3 27B', desc: '🔥 Top Performance' },
  { id: 'google/gemma-3-4b-it:free', name: 'Gemma 3 4B', desc: '⚡ Fast & Smart' },
  { id: 'google/gemma-3-12b-it:free', name: 'Gemma 3 12B', desc: '💪 More Power' },
  { id: 'google/gemma-3n-e2b-it:free', name: 'Gemma 3n E2B', desc: '🪶 Lightweight' },
  { id: 'google/gemma-3n-e4b-it:free', name: 'Gemma 3n E4B', desc: '📱 Mobile' },
  
  // Meta
  { id: 'meta-llama/llama-3.3-70b-instruct:free', name: 'Llama 3.3 70B', desc: '🔥 Very Strong' },
  { id: 'meta-llama/llama-3.2-3b-instruct:free', name: 'Llama 3.2 3B', desc: '🪶 Lightweight' },
  
  // Mistral
  { id: 'mistralai/mistral-small-3.1-24b-instruct:free', name: 'Mistral 3.1 24B', desc: '💪 Balanced' },
  
  // Nous
  { id: 'nousresearch/hermes-3-llama-3.1-405b:free', name: 'Hermes 3 405B', desc: '🔥 Top Tier' },
  
  // Arcee
  { id: 'arcee-ai/trinity-mini:free', name: 'Trinity Mini', desc: '🪶 Tiny' },
  { id: 'arcee-ai/trinity-large-preview:free', name: 'Trinity Large', desc: '💪 Strong' },
  
  // OpenRouter
  { id: 'openrouter/free', name: 'OpenRouter Auto', desc: '🤖 Best Free Model' },
  
  // OpenAI
  { id: 'openai/gpt-oss-120b:free', name: 'GPT OSS 120B', desc: '💪 Large' },
  { id: 'openai/gpt-oss-20b:free', name: 'GPT OSS 20B', desc: '🪶 Compact' },
  
  // Z-ai
  { id: 'z-ai/glm-4.5-air:free', name: 'GLM 4.5 Air', desc: '⚡ Fast' },
  
  // Liquid
  { id: 'liquid/lfm-2.5-1.2b-thinking:free', name: 'LFM 2.5 1.2B Think', desc: '🧠 Reasoning' },
  { id: 'liquid/lfm-2.5-1.2b-instruct:free', name: 'LFM 2.5 1.2B', desc: '🪶 Tiny' },
  
  // Cognitive Computations
  { id: 'cognitivecomputations/dolphin-mistral-24b-venice-edition:free', name: 'Dolphin 24B', desc: '🐬 Great Chat' },
]

// ==================================

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedModel, setSelectedModel] = useState('google/gemma-3-4b-it:free')
  const [showSettings, setShowSettings] = useState(false)
  const [sessionId] = useState(getSessionId)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    const saved = loadMessages(sessionId)
    if (saved && saved.length > 0) {
      setMessages(saved)
    } else {
      setMessages([{
        role: 'assistant',
        content: `👋 Welcome to ChatNoLogin!\n\n✨ **100% Free AI Chat**\n\n🎯 Select a model in settings (⚙️):\n${FREE_MODELS.map(m => `• ${m.name}: ${m.desc}`).join('\n')}\n\n🔒 Privacy First:\n• No login required\n• No tracking\n• No ads\n• Open source\n\n💬 Start chatting!`
      }])
    }
  }, [sessionId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const callAPI = async (msgs, model) => {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'HTTP-Referer': 'https://dasfletchi.github.io',
        'X-Title': 'ChatNoLogin'
      },
      body: JSON.stringify({
        model: model,
        messages: msgs.map(m => ({ role: m.role === 'assistant' ? 'assistant' : 'user', content: m.content })),
        max_tokens: 1024
      })
    })
    
    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.error?.message || `API Error: ${response.status}`)
    }
    
    const data = await response.json()
    return data.choices?.[0]?.message?.content || 'No response'
  }

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    
    const userMessage = { role: 'user', content: input.trim(), timestamp: Date.now() }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setInput('')
    setLoading(true)
    
    let reply
    
    // Use API - we have a working key!
    try {
      reply = await callAPI(newMessages, selectedModel)
    } catch (err) {
      reply = `❌ Error: ${err.message}\n\nTry selecting a different model in settings!`
    }
    
    const assistantMessage = { role: 'assistant', content: reply, timestamp: Date.now() }
    setMessages([...newMessages, assistantMessage])
    saveMessages(sessionId, [...newMessages, assistantMessage])
    
    setLoading(false)
    inputRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const clearChat = () => {
    if (confirm('Clear chat?')) {
      setMessages([{ role: 'assistant', content: '✨ Chat cleared!' }])
      saveMessages(sessionId, [])
    }
  }

  const newChat = () => {
    window.location.hash = 'sess_' + Math.random().toString(36).slice(2, 15)
    window.location.reload()
  }

  const currentModel = FREE_MODELS.find(m => m.id === selectedModel)

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🤖</span>
          <span>ChatNoLogin</span>
        </div>
        <div className="header-actions">
          <button onClick={() => setShowSettings(!showSettings)} className="btn-settings" title="Settings">
            ⚙️
          </button>
          <button onClick={newChat} className="btn-secondary">➕</button>
          <button onClick={clearChat} className="btn-secondary">🗑️</button>
        </div>
      </header>

      {/* Settings Panel */}
      {showSettings && (
        <div className="settings-panel">
          <h3>⚙️ Select Free Model</h3>
          <div className="model-list">
            {FREE_MODELS.map(m => (
              <button
                key={m.id}
                className={`model-btn ${selectedModel === m.id ? 'active' : ''}`}
                onClick={() => setSelectedModel(m.id)}
              >
                <span className="model-name">{m.name}</span>
                <span className="model-desc">{m.desc}</span>
              </button>
            ))}
          </div>
          <p className="model-info">Current: {currentModel?.name}</p>
        </div>
      )}
      
      <main className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="avatar">{msg.role === 'user' ? '👤' : '🤖'}</div>
            <div className="content">
              {msg.content.split('\n').map((line, j) => (
                <p key={j}>{line}</p>
              ))}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="avatar">🤖</div>
            <div className="content typing">
              <span>●</span><span>●</span><span>●</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>
      
      <footer className="input-area">
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type message... (Enter to send)"
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          {loading ? '⏳' : '➤'}
        </button>
      </footer>
      
      <div className="badge">
        🔒 Privacy First • 💯 Free • {currentModel?.name}
      </div>
    </div>
  )
}

export default App
