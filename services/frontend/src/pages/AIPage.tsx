import { useState } from "react"
import { Header, BottomNav } from "@/components/navigation"
import { ChatBubble, RecipeBubble, ChatInput } from "@/components/chat"

const initialMessages = [
  {
    id: "1",
    role: "assistant" as const,
    content: "YO! Ready to ride the flavor wave? I'm Paula, your digital mixologist. Hit me with what you're craving.",
    timestamp: "10:42 AM",
  },
  {
    id: "2",
    role: "user" as const,
    content: "Need something intense. I've got a massive coding marathon ahead and I'm dragging. Suggest a high-voltage combo.",
    timestamp: "10:44 AM",
  },
]

export default function AIPage() {
  const [messages, setMessages] = useState(initialMessages)
  const [input, setInput] = useState("")

  const handleSubmit = () => {
    if (!input.trim()) return
    
    const newMessage = {
      id: Date.now().toString(),
      role: "user" as const,
      content: input,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    }
    
    setMessages([...messages, newMessage])
    setInput("")
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: (Date.now() + 1).toString(),
        role: "assistant" as const,
        content: "Entering the Grid? Say less. Let me mix something special for you...",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      }
      setMessages((prev) => [...prev, aiResponse])
    }, 1000)
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header showBackButton variant="chat" />
      
      {/* Chat Header Banner */}
      <div className="bg-primary px-6 py-3 flex items-center gap-3 border-b-2 border-secondary">
        <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-white">
          <img
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuCXVslkxL5mUe52UQ6fE-uLTHmKs9g60rjRNH_XLwtZyBrPsecIXA7GvMBkfNYDb1FkfQlg9hxwc8tasFjYKxmnfPTu2NaIHLU7e3QwcsKxZy-ttUyb_NgO01ZmTDTP7FpAV76OTFy-runmKK6DbCdu3pPYKbEemwsT51u3nxFXU1eiKvYR6DgkaXDgKqu1h7s07Foof1uE7XS3rbPxYpp7SNjkg6Wmw_EXlADYixqZt5DqADeoVl6EomPE37D7NKGOa6jInc05gjPY"
            alt="Paula"
            className="w-full h-full object-cover"
            crossOrigin="anonymous"
          />
        </div>
        <div>
          <div className="font-heading font-bold text-secondary">PAULANA ZUDOKYU</div>
          <div className="flex items-center gap-1 text-xs text-secondary/80">
            <span className="w-2 h-2 bg-green-500 rounded-full" />
            FULLY CHARGED
          </div>
        </div>
      </div>
      
      {/* Messages */}
      <main 
        className="flex-1 overflow-y-auto px-4 py-6 space-y-6"
        style={{
          background: 'linear-gradient(180deg, rgba(72,52,212,0.2) 0%, rgba(26,26,26,1) 50%)'
        }}
      >
        {messages.map((message) => (
          <ChatBubble key={message.id} message={message} />
        ))}
        
        {/* Example Recipe Bubble */}
        <RecipeBubble
          title="Entering the Grid? Say less."
          description="You need the NEON SURGE combo:"
          tag="NEON SURGE"
          ingredients={[
            { icon: "bolt", iconColor: "text-primary", text: "Double espresso base" },
            { icon: "local_fire_department", iconColor: "text-destructive", text: "Spezi Energy Shot" },
            { icon: "ac_unit", iconColor: "text-blue-400", text: "Ice cold, no dilution" },
          ]}
          timestamp="10:45 AM"
        />
      </main>

      <ChatInput
        value={input}
        onChange={setInput}
        onSubmit={handleSubmit}
      />
      
      <BottomNav />
    </div>
  )
}
