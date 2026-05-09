import { useState } from 'react'

export default function UploadCard({ onUpload, jobDescription, setJobDescription, loading }) {
  const [file, setFile] = useState(null)

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!file) {
      return alert('Please select a resume file.')
    }
    onUpload(file, jobDescription)
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-glass backdrop-blur-xl">
      <h2 className="text-3xl font-semibold">Upload resume</h2>
      <p className="mt-3 text-slate-300">Drop a PDF or DOCX resume and add the job description to power the ATS and semantic analysis.</p>

      <label className="mt-6 flex min-h-[180px] cursor-pointer flex-col items-center justify-center rounded-3xl border-2 border-dashed border-slate-600 bg-slate-950/40 p-6 text-center text-slate-300 transition hover:border-accent/80 hover:text-white">
        <span className="text-lg font-medium">Drag & drop here or click to browse</span>
        <span className="mt-2 text-sm text-slate-500">Supported files: PDF, DOCX</span>
        <input className="sr-only" type="file" accept=".pdf,.docx" onChange={(event) => setFile(event.target.files[0])} />
      </label>

      <div className="mt-6">
        <label className="block text-sm font-medium text-slate-200">Job Description</label>
        <textarea
          value={jobDescription}
          onChange={(event) => setJobDescription(event.target.value)}
          rows="8"
          placeholder="Paste the job description here to compare resumes effectively."
          className="mt-2 w-full resize-none rounded-3xl border border-white/10 bg-slate-950/80 p-4 text-sm text-white outline-none transition focus:border-accent"
        />
      </div>

      <button type="submit" disabled={loading} className="mt-6 inline-flex items-center justify-center rounded-full bg-accent px-6 py-3 text-sm font-semibold text-white transition hover:bg-violet-500 disabled:cursor-not-allowed disabled:opacity-60">
        {loading ? 'Analyzing...' : 'Analyze Resume'}
      </button>
    </form>
  )
}
