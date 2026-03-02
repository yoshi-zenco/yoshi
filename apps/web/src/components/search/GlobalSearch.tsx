"use client";
import { useState } from "react";
import { Search, X } from "lucide-react";

export function GlobalSearch() {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  return (
    <>
      <button onClick={() => setOpen(true)} className="flex items-center gap-2 px-3 py-1.5 bg-zinc-800 rounded-lg text-zinc-400 text-sm hover:bg-zinc-700 transition-colors">
        <Search className="w-4 h-4" />
        <span>Search...</span>
        <kbd className="ml-2 px-1.5 py-0.5 bg-zinc-700 rounded text-xs">⌘K</kbd>
      </button>
      {open && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4 bg-black/60" onClick={() => setOpen(false)}>
          <div className="w-full max-w-xl bg-zinc-900 border border-zinc-700 rounded-2xl shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex items-center gap-3 px-4 py-3 border-b border-zinc-800">
              <Search className="w-5 h-5 text-zinc-400" />
              <input autoFocus value={query} onChange={e => setQuery(e.target.value)} placeholder="Search conversations, images, stories..." className="flex-1 bg-transparent text-white placeholder-zinc-500 focus:outline-none" />
              <button onClick={() => setOpen(false)}><X className="w-4 h-4 text-zinc-400" /></button>
            </div>
            <div className="p-4 text-sm text-zinc-500">{query ? `Searching for "${query}"...` : "Start typing to search"}</div>
          </div>
        </div>
      )}
    </>
  );
}
