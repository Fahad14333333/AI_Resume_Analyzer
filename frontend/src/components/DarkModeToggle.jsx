import { useState } from 'react'

export default function DarkModeToggle() {
  const [enabled, setEnabled] = useState(true)

  const handleToggle = () => {
    setEnabled(!enabled)
    document.documentElement.classList.toggle('dark', !enabled)
  }

  return (
    <button onClick={handleToggle} className="rounded-full border border-white/10 bg-slate-950/80 px-5 py-3 text-sm font-medium text-white transition hover:border-accent">
      {enabled ? 'Dark mode enabled' : 'Light mode enabled'}
    </button>
  )
}
