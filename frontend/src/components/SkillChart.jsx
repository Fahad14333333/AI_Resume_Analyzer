import { Bar } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

export default function SkillChart({ skills }) {
  const labels = skills.map((skill) => skill.name)
  const data = {
    labels,
    datasets: [
      {
        label: 'Skill Match Confidence',
        backgroundColor: 'rgba(79, 70, 229, 0.75)',
        borderRadius: 12,
        data: skills.map((skill) => skill.confidence || 70),
      },
    ],
  }

  return (
    <div className="rounded-[2rem] border border-white/10 bg-slate-950/75 p-6 shadow-glass">
      <h3 className="text-lg font-semibold">Skill matching overview</h3>
      <div className="mt-5">
        <Bar data={data} options={{ responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100 }, x: { ticks: { color: '#cbd5e1' } } } }} />
      </div>
    </div>
  )
}
