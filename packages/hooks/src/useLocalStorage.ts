import { useState } from "react";
export function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    try { const item = window.localStorage.getItem(key); return item ? JSON.parse(item) : initial; } catch { return initial; }
  });
  const set = (v: T) => { setValue(v); try { window.localStorage.setItem(key, JSON.stringify(v)); } catch {} };
  return [value, set] as const;
}
