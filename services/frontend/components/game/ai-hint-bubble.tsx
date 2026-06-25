interface AIHintBubbleProps {
  message: string
  avatarSrc?: string
}

export function AIHintBubble({ 
  message, 
  avatarSrc = "https://lh3.googleusercontent.com/aida-public/AB6AXuCXVslkxL5mUe52UQ6fE-uLTHmKs9g60rjRNH_XLwtZyBrPsecIXA7GvMBkfNYDb1FkfQlg9hxwc8tasFjYKxmnfPTu2NaIHLU7e3QwcsKxZy-ttUyb_NgO01ZmTDTP7FpAV76OTFy-runmKK6DbCdu3pPYKbEemwsT51u3nxFXU1eiKvYR6DgkaXDgKqu1h7s07Foof1uE7XS3rbPxYpp7SNjkg6Wmw_EXlADYixqZt5DqADeoVl6EomPE37D7NKGOa6jInc05gjPY" 
}: AIHintBubbleProps) {
  return (
    <div className="flex items-start gap-3">
      <div className="w-16 h-16 rounded-full flex-shrink-0 relative overflow-hidden border-2 border-white shadow-[4px_4px_0px_0px_var(--color-secondary)]">
        <img
          src={avatarSrc}
          alt="Paula AI Assistant"
          className="object-cover w-full h-full"
          crossOrigin="anonymous"
        />
      </div>
      <div className="flex-grow bg-secondary p-4 rounded-2xl rounded-tl-none border-2 border-destructive shadow-[4px_4px_0px_0px_rgba(227,6,19,0.3)] relative">
        <p className="font-sans text-white italic">{message}</p>
        <div className="absolute -left-[10px] top-0 w-0 h-0 border-t-[15px] border-t-secondary border-l-[15px] border-l-transparent" />
      </div>
    </div>
  )
}
