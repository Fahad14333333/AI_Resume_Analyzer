export default function ScoreMeter({ score, label }) {
  const meterValue = Math.min(100, Math.max(0, score))
  return (
    <div className="rounded-[2rem] border border-white/10 bg-slate-950/75 p-6 shadow-glass">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">{label}</p>
          <p className="mt-2 text-4xl font-semibold text-white">{meterValue}%</p>
        </div>
        <div className="h-32 w-32 rounded-full bg-slate-900/60 p-3">
          <div className="relative flex h-full w-full items-center justify-center rounded-full bg-gradient-to-br from-slate-800 to-slate-950">
            <span className="absolute text-xl font-semibold text-white">{meterValue}</span>
          </div>
        </div>
      </div>
      <div className="mt-4 h-3 overflow-hidden rounded-full bg-slate-800">
        <div className="h-full rounded-full bg-gradient-to-r from-accent to-violet-500" style={{ width: `${meterValue}%` }} />
      </div>
    </div>
  )
}
