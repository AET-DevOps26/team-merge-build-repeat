import { useState, useRef, useEffect } from "react"
import { ChatBubble } from "./chat-bubble"

interface Message {
  id: string
  role: "assistant" | "user"
  content: string
  timestamp: string
}

interface GameChatProps {
  gameId: string
  board: number[][]
  candidates: number[][][]
}

// Placeholder token until real auth is wired up. The genai service only checks
// that a non-blank Bearer token is present.
const AUTH_TOKEN = "dev-token"

function now(): string {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}

async function fetchAnswer(
  gameId: string,
  board: number[][],
  candidates: number[][][],
  message: string,
): Promise<string> {
  const res = await fetch("/genai/v1/chat/answer", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${AUTH_TOKEN}`,
    },
    body: JSON.stringify({ gameId, board, candidates, message }),
  })
  if (!res.ok) throw new Error(`Assistant request failed: ${res.status}`)
  const data = await res.json()
  return data.assistantResponse
}

export function GameChat({ gameId, board, candidates }: GameChatProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight })
  }, [messages, loading])

  const handleSend = async () => {
    const trimmed = input.trim()
    if (!trimmed || loading) return

    const userMessage: Message = {
      id: `${Date.now()}-user`,
      role: "user",
      content: trimmed,
      timestamp: now(),
    }
    setMessages(prev => [...prev, userMessage])
    setInput("")
    setError(null)
    setLoading(true)

    try {
      const answer = await fetchAnswer(gameId, board, candidates, trimmed)
      setMessages(prev => [...prev, {
        id: `${Date.now()}-assistant`,
        role: "assistant",
        content: answer,
        timestamp: now(),
      }])
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to reach the assistant")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex-1 bg-card border-2 border-secondary rounded p-4 flex flex-col gap-4 min-h-0">
      <h2 className="text-lg font-bold text-foreground flex-shrink-0">AI Assistant</h2>

      <div ref={scrollRef} className="flex-1 overflow-y-auto flex flex-col gap-4 min-h-0">
        {messages.length === 0 && !loading && (
          <div className="flex-1 flex items-center justify-center text-muted">
            <p>Ask the assistant for a hint…</p>
          </div>
        )}
        {messages.map(message => (
          <ChatBubble key={message.id} message={message} />
        ))}
        {loading && (
          <div className="flex w-full justify-start">
            <div className="bg-card border-[1.5px] border-border rounded-tr-2xl rounded-br-2xl rounded-bl-2xl shadow-lg p-4">
              <span className="material-symbols-outlined text-accent animate-spin">progress_activity</span>
            </div>
          </div>
        )}
        {error && (
          <p className="text-destructive font-semibold text-sm">{error}</p>
        )}
      </div>

      <div className="flex-shrink-0 flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()}
          disabled={loading}
          placeholder="Type a message…"
          className="flex-1 bg-white/10 border-[1.5px] border-accent/50 text-foreground p-3 h-12 rounded-xl font-sans focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50 placeholder:text-muted disabled:opacity-50 transition-all"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          aria-label="Send message"
          className="bg-accent text-white w-12 h-12 flex-shrink-0 flex items-center justify-center rounded-xl border-2 border-primary shadow-[2px_2px_0px_0px_var(--color-primary)] active:translate-y-1 active:translate-x-1 active:shadow-none transition-all hover:brightness-110 disabled:opacity-40 disabled:pointer-events-none"
        >
          <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>send</span>
        </button>
      </div>
    </div>
  )
}
