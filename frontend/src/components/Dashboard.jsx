import ScoreMeter from './ScoreMeter'
import SkillChart from './SkillChart'

export default function Dashboard({ analysis }) {
  const parsed = analysis.parsed_resume
  const skills = parsed.skills.map((skill) => ({ name: skill, confidence: 82 }))
  return (
    <section className="space-y-6 rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-glass backdrop-blur-xl">
      <div className="grid gap-4 lg:grid-cols-3">
        <ScoreMeter score={analysis.analysis.ats_score} label="ATS Compatibility" />
        <ScoreMeter score={analysis.analysis.semantic_similarity} label="Semantic Similarity" />
        <ScoreMeter score={analysis.analysis.grammar_score} label="Grammar & Quality" />
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
        <div className="rounded-[2rem] border border-white/10 bg-slate-950/75 p-6">
          <h3 className="text-xl font-semibold text-white">Resume insights</h3>
          <div className="mt-5 space-y-4 text-slate-300">
            <p><strong>Name:</strong> {parsed.name || 'Unknown'}</p>
            <p><strong>Email:</strong> {parsed.email || 'Not detected'}</p>
            <p><strong>Phone:</strong> {parsed.phone || 'Not detected'}</p>
            <p><strong>Skills:</strong> {parsed.skills.length ? parsed.skills.join(', ') : 'No skills detected'}</p>
            <p><strong>Missing skills:</strong> {analysis.analysis.missing_skills.length ? analysis.analysis.missing_skills.join(', ') : 'None'}</p>
            <p><strong>Keyword stuffing:</strong> {analysis.analysis.keyword_stuffing ? 'Detected' : 'None detected'}</p>
          </div>
        </div>
        <div className="space-y-6">
          <div className="rounded-[2rem] border border-white/10 bg-slate-950/75 p-6">
            <h3 className="text-xl font-semibold">Recruiter summary</h3>
            <p className="mt-4 text-slate-300">Use the ATS score, skill match, and quick resume review to shortlist high-potential candidates.</p>
          </div>
          <div className="rounded-[2rem] border border-white/10 bg-slate-950/75 p-6">
            <h3 className="text-xl font-semibold">Explainable results</h3>
            <p className="mt-4 text-slate-300">Matched skills: {analysis.analysis.explainable.matched_skills.join(', ') || 'None'}</p>
            <p className="mt-2 text-slate-300">Detected JD skills: {analysis.analysis.explainable.detected_job_skills.join(', ') || 'None'}</p>
          </div>
        </div>
      </div>

      <SkillChart skills={skills} />
    </section>
  )
}
