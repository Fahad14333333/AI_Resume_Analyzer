import { useState } from 'react'
import { uploadResume, analyzeResume } from './api/apiClient'
import UploadCard from './components/UploadCard'
import Dashboard from './components/Dashboard'
import RecruiterHeader from './components/RecruiterHeader'
import DarkModeToggle from './components/DarkModeToggle'

function App() {
  const [analysis, setAnalysis] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)

  const handleUpload = async (file, jd) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('job_description', jd)
    setLoading(true)
    try {
      const response = await uploadResume(formData)
      setAnalysis(response.data)
    } catch (error) {
      console.error(error)
      alert(error?.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(99,102,241,0.24),_transparent_35%),linear-gradient(180deg,#050816_0%,#0a0f1d_100%)] text-white px-4 py-6">
      <RecruiterHeader />
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[1.2fr_1fr]">
        <UploadCard
          onUpload={handleUpload}
          jobDescription={jobDescription}
          setJobDescription={setJobDescription}
          loading={loading}
        />
        <div className="space-y-6">
          <DarkModeToggle />
          {analysis ? <Dashboard analysis={analysis} /> : <div className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-glass backdrop-blur-xl">
            <h2 className="text-2xl font-semibold">Resume intelligence in one dashboard</h2>
            <p className="mt-4 text-sm text-slate-300">Upload a resume and job description to get ATS scoring, missing skills, interview questions, and a recruiter-ready analytics view.</p>
          </div>}
        </div>
      </div>
    </div>
  )
}

export default App
