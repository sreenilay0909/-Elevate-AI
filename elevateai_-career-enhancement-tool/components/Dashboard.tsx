
import React from 'react';
import { 
  Radar, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';
import { AnalysisResult } from '../types';
// Fixed icon imports: added Briefcase and kept existing icons
import { Award, Target, TrendingUp, Zap, Briefcase } from 'lucide-react';

interface DashboardProps {
  data: AnalysisResult;
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  const radarData = data.platformScores.map(p => ({
    subject: p.name,
    A: p.score,
    fullMark: p.total,
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-500 text-sm font-medium">Composite Score</p>
              <h3 className="text-3xl font-bold mt-1">{data.compositeScore}%</h3>
            </div>
            <div className="p-3 bg-blue-50 rounded-xl text-blue-600">
              <Award size={24} />
            </div>
          </div>
          <div className="mt-4 flex items-center text-xs text-green-600 font-medium">
            <TrendingUp size={14} className="mr-1" />
            Top 15% in your field
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-500 text-sm font-medium">Market Fit</p>
              <h3 className="text-3xl font-bold mt-1">{data.marketAnalysis.demandScore}/100</h3>
            </div>
            <div className="p-3 bg-emerald-50 rounded-xl text-emerald-600">
              <Target size={24} />
            </div>
          </div>
          <div className="mt-4 w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
            <div 
              className="bg-emerald-500 h-full rounded-full transition-all duration-1000" 
              style={{ width: `${data.marketAnalysis.demandScore}%` }}
            />
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-500 text-sm font-medium">Job Match</p>
              <h3 className="text-3xl font-bold mt-1">{data.jobMatch.fitPercent}%</h3>
            </div>
            <div className="p-3 bg-amber-50 rounded-xl text-amber-600">
              <Briefcase size={24} />
            </div>
          </div>
          <p className="mt-4 text-xs text-slate-500">Matching {data.jobMatch.role}</p>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-500 text-sm font-medium">Avg Salary Est.</p>
              <h3 className="text-3xl font-bold mt-1">{data.marketAnalysis.salaryEstimate}</h3>
            </div>
            <div className="p-3 bg-purple-50 rounded-xl text-purple-600">
              <Zap size={24} />
            </div>
          </div>
          <p className="mt-4 text-xs text-slate-500">Based on active skill sets</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <h3 className="text-lg font-bold mb-6">Skill Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12 }} />
                <Radar
                  name="Score"
                  dataKey="A"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.6}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <h3 className="text-lg font-bold mb-6">Platform Benchmarks</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.platformScores}>
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
                <YAxis hide />
                <Tooltip 
                  cursor={{ fill: 'transparent' }}
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Bar dataKey="score" radius={[8, 8, 0, 0]} barSize={40}>
                  {data.platformScores.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
        <h3 className="text-lg font-bold mb-6">Quick Recommendations</h3>
        <div className="space-y-4">
          {data.recommendations.slice(0, 3).map((rec, i) => (
            <div key={i} className="flex gap-4 p-4 rounded-xl bg-slate-50 border border-slate-100 hover:border-blue-200 transition-colors">
              <div className={`mt-1 h-2 w-2 rounded-full flex-shrink-0 ${
                rec.priority === 'High' ? 'bg-red-500' : 'bg-amber-500'
              }`} />
              <div>
                <h4 className="font-semibold text-slate-800">{rec.title}</h4>
                <p className="text-sm text-slate-600 mt-1">{rec.description}</p>
                <span className="inline-block mt-3 px-2 py-1 bg-white border border-slate-200 rounded text-[10px] font-bold uppercase tracking-wider text-slate-500">
                  {rec.category}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
