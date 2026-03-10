// Cloudflare Worker - OpenRouter Proxy
// Deploy at: https://workers.cloudflare.com (free)

export default {
  async fetch(request) {
    const OPENROUTER_KEY = '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'
    
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
          'Access-Control-Allow-Headers': 'content-type, authorization',
        }
      })
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 })
    }

    try {
      const body = await request.json()
      
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${OPENROUTER_KEY}`,
          'HTTP-Referer': 'https://dasfletchi.github.io',
          'X-Title': 'ChatNoLogin'
        },
        body: JSON.stringify(body)
      })

      const data = await response.json()
      
      return new Response(JSON.stringify(data), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        }
      })
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      })
    }
  }
}
