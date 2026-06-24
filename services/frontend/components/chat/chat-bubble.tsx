import { cn } from "@/lib/utils"

interface Message {
  id: string
  role: "assistant" | "user"
  content: string
  timestamp: string
}

interface ChatBubbleProps {
  message: Message
  avatarSrc?: string
}

export function ChatBubble({ 
  message, 
  avatarSrc = "https://lh3.googleusercontent.com/aida-public/AB6AXuCXVslkxL5mUe52UQ6fE-uLTHmKs9g60rjRNH_XLwtZyBrPsecIXA7GvMBkfNYDb1FkfQlg9hxwc8tasFjYKxmnfPTu2NaIHLU7e3QwcsKxZy-ttUyb_NgO01ZmTDTP7FpAV76OTFy-runmKK6DbCdu3pPYKbEemwsT51u3nxFXU1eiKvYR6DgkaXDgKqu1h7s07Foof1uE7XS3rbPxYpp7SNjkg6Wmw_EXlADYixqZt5DqADeoVl6EomPE37D7NKGOa6jInc05gjPY"
}: ChatBubbleProps) {
  const isUser = message.role === "user"

  return (
    <div className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}>
      <div className="max-w-[85%] md:max-w-[70%]">
        <div
          className={cn(
            "p-4",
            isUser
              ? "bg-accent text-white border-2 border-primary rounded-tl-2xl rounded-br-2xl rounded-bl-2xl shadow-[4px_4px_0px_0px_rgba(0,0,0,0.3)] transition-transform hover:-translate-y-0.5"
              : "bg-card border-[1.5px] border-border rounded-tr-2xl rounded-br-2xl rounded-bl-2xl shadow-lg"
          )}
        >
          <p className={cn("font-sans", isUser && "font-medium")}>
            {message.content}
          </p>
        </div>
        <span
          className={cn(
            "font-mono text-xs text-muted-foreground mt-2 block",
            isUser ? "mr-3 text-right" : "ml-3"
          )}
        >
          {message.timestamp}
        </span>
      </div>
    </div>
  )
}

interface RecipeBubbleProps {
  title: string
  description: string
  tag: string
  ingredients: { icon: string; iconColor: string; text: string }[]
  timestamp: string
}

export function RecipeBubble({ title, description, tag, ingredients, timestamp }: RecipeBubbleProps) {
  return (
    <div className="flex w-full justify-start">
      <div className="max-w-[85%] md:max-w-[70%]">
        <div className="bg-card border-[1.5px] border-border p-4 rounded-tr-2xl rounded-br-2xl rounded-bl-2xl shadow-lg flex flex-col gap-3">
          <p className="font-sans text-foreground font-bold">{title}</p>
          <p className="font-sans text-foreground">
            {description.split(tag)[0]}
            <span className="bg-destructive text-white px-2 py-0.5 rounded-md uppercase font-bold text-xs shadow-sm">
              {tag}
            </span>
            {description.split(tag)[1]}
          </p>
          <div className="bg-background border border-accent/30 p-3 mt-1 rounded-xl">
            <ul className="space-y-1 font-mono text-xs text-muted-foreground">
              {ingredients.map((item, index) => (
                <li key={index} className="flex items-center gap-3">
                  <span className={cn("material-symbols-outlined text-lg", item.iconColor)}>
                    {item.icon}
                  </span>
                  {item.text}
                </li>
              ))}
            </ul>
          </div>
        </div>
        <span className="font-mono text-xs text-muted-foreground mt-2 ml-3 block">
          {timestamp}
        </span>
      </div>
    </div>
  )
}

interface ChatInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  placeholder?: string
}

export function ChatInput({ value, onChange, onSubmit, placeholder = "Type your command..." }: ChatInputProps) {
  return (
    <footer className="bg-secondary border-t-[3px] border-destructive p-4 pb-20 z-20 relative shadow-[0_-8px_24px_rgba(0,0,0,0.6)]">
      <div className="max-w-4xl mx-auto relative flex items-center w-full">
        <div className="absolute -top-[10px] left-4 px-2 bg-secondary text-primary font-mono text-[10px] z-30 font-bold tracking-widest uppercase">
          Transmit Signal
        </div>
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && onSubmit()}
          className="w-full bg-white/10 border-[1.5px] border-destructive/50 text-white p-3 pl-4 pr-16 h-[52px] rounded-xl font-sans focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50 placeholder:text-white/40 transition-all"
          placeholder={placeholder}
        />
        <button
          onClick={onSubmit}
          className="absolute right-[6px] top-[6px] bottom-[6px] w-[40px] bg-destructive text-white rounded-lg hover:brightness-110 transition-all z-30 flex items-center justify-center active:scale-95 shadow-md"
          aria-label="Send message"
        >
          <span
            className="material-symbols-outlined text-xl font-bold"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            send
          </span>
        </button>
      </div>
    </footer>
  )
}
