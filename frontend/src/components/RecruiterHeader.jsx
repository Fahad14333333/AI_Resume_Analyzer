export default function RecruiterHeader() {
  const openProject = () => {
    window.open(window.location.origin, '_blank')
  }

  return (
    <header className="mx-auto mb-6 max-w-7xl rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-glass backdrop-blur-xl">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.4em] text-slate-400">AI Resume Analyzer</p>
          <h1 className="mt-2 text-4xl font-semibold text-white">Resume matching, ranking, and recruiter intelligence</h1>
        </div>
        <div className="space-y-4 text-right text-slate-300">
          <div>
            <p>Modern NLP, embeddings and ATS scoring</p>
            <p>PDF / DOCX support • OCR • multilingual resume insights</p>
          </div>
          <button
            type="button"
            onClick={openProject}
            className="rounded-full bg-accent px-5 py-2 text-sm font-semibold text-white transition hover:bg-violet-500"
          >
            Open Project in New Tab
          </button>
        </div>
      </div>
    </header>
  )
}
