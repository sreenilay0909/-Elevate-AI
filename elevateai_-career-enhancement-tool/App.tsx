
import React, { useState, useCallback } from 'react';
import { 
  Plus, 
  Github, 
  Linkedin, 
  Code, 
  FileText, 
  ArrowRight,
  ChevronRight,
  ExternalLink,
  BookOpen,
  Trophy,
  CheckCircle2,
  Zap,
  Briefcase,
  MapPin,
  Building2,
  Search
} from 'lucide-react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import ResumeUpload from './components/ResumeUpload';
import { analyzeProfile } from './services/geminiService';
import { ProfileData, AnalysisResult } from './types';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [profileData, setProfileData] = useState<ProfileData>({
    github: '',
    leetcode: '',
    linkedin: '',
    resumeText: '',
    targetRole: ''
  });
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setProfileData(prev => ({ ...prev, [name]: value }));
  };

  const handleResumeUpload = (file: File) => {
    setResumeFile(file);
    setError(null);
  };

  const handleResumeRemove = () => {
    setResumeFile(null);
  };

  const startAnalysis = async () => {
    setIsAnalyzing(true);
    setError(null);
    try {
      const result = await analyzeProfile(profileData, resumeFile);
      setAnalysisResult(result);
    } catch (err: any) {
      setError(err.message || 'An error occurred during analysis.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderContent = () => {
    if (!analysisResult) {
      return (
        <div className="max-w-4xl mx-auto py-12 px-6">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-extrabold text-slate-900 tracking-tight">Elevate Your Career Path</h2>
            <p className="mt-4 text-xl text-slate-600">Connect your professional footprints and let AI map your growth journey.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                <Plus size={20} className="text-blue-500" />
                Input Your Profiles
              </h3>
              
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Target Career Role</label>
                  <input 
                    type="text" 
                    name="targetRole"
                    value={profileData.targetRole}
                    onChange={handleInputChange}
                    placeholder="e.g. Senior Backend Engineer" 
                    className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                      <Github size={16} className="text-slate-500" /> GitHub
                    </label>
                    <input 
                      type="text" 
                      name="github"
                      value={profileData.github}
                      onChange={handleInputChange}
                      placeholder="Username" 
                      className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                      <Code size={16} className="text-orange-500" /> LeetCode
                    </label>
                    <input 
                      type="text" 
                      name="leetcode"
                      value={profileData.leetcode}
                      onChange={handleInputChange}
                      placeholder="Username" 
                      className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                    <Linkedin size={16} className="text-blue-600" /> LinkedIn
                  </label>
                  <input 
                    type="text" 
                    name="linkedin"
                    value={profileData.linkedin}
                    onChange={handleInputChange}
                    placeholder="Profile URL" 
                    className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                    <FileText size={16} className="text-emerald-600" /> Resume Upload (PDF or Image)
                  </label>
                  <ResumeUpload
                    onUpload={handleResumeUpload}
                    onRemove={handleResumeRemove}
                    uploadedFile={resumeFile}
                    error={error || undefined}
                  />
                </div>

                <button 
                  onClick={startAnalysis}
                  disabled={isAnalyzing}
                  className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-blue-500/20 disabled:opacity-70"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Analyzing Resume & Profiles...
                    </>
                  ) : (
                    <>
                      Generate Report
                      <ArrowRight size={20} />
                    </>
                  )}
                </button>
                {error && <p className="text-red-500 text-sm mt-2 text-center">{error}</p>}
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-gradient-to-br from-slate-900 to-slate-800 p-8 rounded-3xl text-white shadow-xl">
                <h3 className="text-xl font-bold mb-4">How it works?</h3>
                <ul className="space-y-4">
                  {[
                    "Aggregate code quality and impact from GitHub",
                    "Analyze algorithmic strength via LeetCode stats",
                    "Map LinkedIn network and professional influence",
                    "Evaluate skill gaps against current market trends",
                    "Generate a personalized learning roadmap",
                    "Find live job openings with real-time match scores"
                  ].map((item, i) => (
                    <li key={i} className="flex gap-3 text-slate-400">
                      <div className="mt-1.5 h-1.5 w-1.5 rounded-full bg-blue-500 flex-shrink-0" />
                      <span className="text-sm leading-relaxed">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-blue-50 p-8 rounded-3xl border border-blue-100">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
                    <Trophy size={20} />
                  </div>
                  <h4 className="font-bold text-slate-900">Premium Insights</h4>
                </div>
                <p className="text-sm text-slate-600 leading-relaxed">
                  Join 10k+ developers using ElevateAI to benchmark themselves against industry peers and secure top-tier roles.
                </p>
              </div>
            </div>
          </div>
        </div>
      );
    }

    switch (activeTab) {
      case 'overview':
        return <Dashboard data={analysisResult} />;
      
      case 'profiles':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold">Platform Analysis</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {analysisResult.platformScores.map((p, idx) => (
                <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-lg font-bold flex items-center gap-2">
                      {p.name === 'GitHub' && <Github className="text-slate-800" />}
                      {p.name === 'LeetCode' && <Code className="text-orange-500" />}
                      {p.name === 'LinkedIn' && <Linkedin className="text-blue-600" />}
                      {p.name}
                    </h3>
                    <div className="text-right">
                      <span className="text-2xl font-bold text-slate-900">{p.score}</span>
                      <span className="text-slate-400">/{p.total}</span>
                    </div>
                  </div>
                  
                  <div className="space-y-4 mb-6">
                    {p.metrics.map((m, mIdx) => (
                      <div key={mIdx}>
                        <div className="flex justify-between text-xs font-medium mb-1">
                          <span className="text-slate-500 uppercase tracking-wider">{m.name}</span>
                          <span className="text-slate-900">{m.value}%</span>
                        </div>
                        <div className="w-full bg-slate-100 h-1.5 rounded-full">
                          <div className="bg-blue-500 h-full rounded-full" style={{ width: `${m.value}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="border-t border-slate-50 pt-4">
                    <p className="text-xs font-bold text-slate-400 mb-3 uppercase tracking-wider">Key Highlights</p>
                    <ul className="space-y-2">
                      {p.highlights.map((h, hIdx) => (
                        <li key={hIdx} className="flex gap-2 text-sm text-slate-600">
                          <CheckCircle2 size={16} className="text-emerald-500 flex-shrink-0" />
                          {h}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'market':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold">Market Analysis: {analysisResult.jobMatch.role}</h2>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
                <h3 className="text-lg font-bold mb-6">In-Demand Skills</h3>
                <div className="flex flex-wrap gap-3">
                  {analysisResult.marketAnalysis.trendingSkills.map((skill, i) => (
                    <div key={i} className="px-4 py-2 bg-blue-50 text-blue-700 rounded-full font-medium flex items-center gap-2">
                      <Zap size={14} />
                      {skill}
                    </div>
                  ))}
                </div>
                
                <h3 className="text-lg font-bold mt-12 mb-6">Target Companies</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {analysisResult.marketAnalysis.topCompanies.map((company, i) => (
                    <div key={i} className="p-4 bg-slate-50 border border-slate-100 rounded-xl text-center font-bold text-slate-700">
                      {company}
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-slate-900 text-white p-8 rounded-2xl shadow-xl">
                <h3 className="text-lg font-bold mb-6">Salary Landscape</h3>
                <div className="text-center py-10 bg-white/5 rounded-3xl border border-white/10">
                  <p className="text-slate-400 text-sm mb-2 uppercase tracking-widest font-bold">Estimated Average</p>
                  <h4 className="text-4xl font-extrabold text-blue-400">{analysisResult.marketAnalysis.salaryEstimate}</h4>
                </div>
                <div className="mt-8 space-y-4">
                  <p className="text-sm text-slate-400 italic">"Based on skills in {analysisResult.marketAnalysis.trendingSkills.slice(0, 3).join(', ')}"</p>
                  <button className="w-full py-3 bg-white/10 hover:bg-white/20 transition-colors rounded-xl text-sm font-bold flex items-center justify-center gap-2">
                    Detailed Salary Insights <ExternalLink size={14} />
                  </button>
                </div>
              </div>
            </div>
          </div>
        );

      case 'roadmap':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold">Your Growth Roadmap</h2>
            <div className="space-y-8 relative before:absolute before:left-[19px] before:top-4 before:bottom-4 before:w-0.5 before:bg-slate-200">
              {analysisResult.roadmap.map((step, idx) => (
                <div key={idx} className="relative pl-12">
                  <div className="absolute left-0 top-0 w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold shadow-lg shadow-blue-500/30 z-10">
                    {idx + 1}
                  </div>
                  <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                    <h3 className="text-lg font-bold text-slate-900 mb-4">{step.phase}</h3>
                    <ul className="space-y-3 mb-6">
                      {step.tasks.map((task, tIdx) => (
                        <li key={tIdx} className="flex gap-3 text-slate-600 text-sm">
                          <div className="mt-1 h-1 w-1 rounded-full bg-slate-300 flex-shrink-0" />
                          {task}
                        </li>
                      ))}
                    </ul>
                    <div className="flex gap-4">
                      {step.resources.map((res, rIdx) => (
                        <a 
                          key={rIdx} 
                          href="#" 
                          className="flex items-center gap-2 text-xs font-bold text-blue-600 hover:text-blue-700 transition-colors bg-blue-50 px-3 py-2 rounded-lg"
                        >
                          <BookOpen size={14} />
                          {res.name}
                        </a>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      case 'jobs':
        return (
          <div className="space-y-12">
            <div>
              <h2 className="text-2xl font-bold mb-6">Job Matching Insights</h2>
              <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 flex flex-col md:flex-row items-center gap-12">
                <div className="relative w-48 h-48 flex-shrink-0">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle
                      cx="96" cy="96" r="80"
                      fill="transparent"
                      stroke="#f1f5f9"
                      strokeWidth="16"
                    />
                    <circle
                      cx="96" cy="96" r="80"
                      fill="transparent"
                      stroke="#3b82f6"
                      strokeWidth="16"
                      strokeDasharray={2 * Math.PI * 80}
                      strokeDashoffset={2 * Math.PI * 80 * (1 - analysisResult.jobMatch.fitPercent / 100)}
                      strokeLinecap="round"
                      className="transition-all duration-1000"
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-4xl font-extrabold text-slate-900">{analysisResult.jobMatch.fitPercent}%</span>
                    <span className="text-slate-400 text-xs font-bold uppercase tracking-widest">Match</span>
                  </div>
                </div>

                <div>
                  <h3 className="text-2xl font-bold text-slate-900 mb-2">Target Role: {analysisResult.jobMatch.role}</h3>
                  <p className="text-slate-600 leading-relaxed max-w-lg mb-6">
                    Your current profile has strong foundations, but there are a few critical gaps to bridge for the next level.
                  </p>
                  <div className="space-y-3">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Missing Skills / Experience</h4>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.jobMatch.gaps.map((gap, i) => (
                        <span key={i} className="px-3 py-1 bg-red-50 text-red-600 rounded-lg text-xs font-semibold flex items-center gap-2">
                          <Plus className="rotate-45" size={12} />
                          {gap}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h2 className="text-2xl font-bold text-slate-900">Live Opportunities</h2>
                  <p className="text-slate-500 text-sm mt-1">Real-time openings matched to your profile via AI Search</p>
                </div>
                <div className="flex items-center gap-2 text-xs font-bold text-blue-600 bg-blue-50 px-3 py-2 rounded-lg border border-blue-100">
                  <Search size={14} />
                  Grounded with Google Search
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {analysisResult.jobListings?.map((job, idx) => (
                  <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col hover:shadow-md hover:-translate-y-1 transition-all duration-300">
                    <div className="flex justify-between items-start mb-4">
                      <div className="p-2 bg-slate-50 rounded-xl border border-slate-100">
                        <Building2 size={24} className="text-slate-400" />
                      </div>
                      <div className={`px-2 py-1 rounded-lg text-[10px] font-extrabold uppercase tracking-widest ${
                        job.matchScore > 85 ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700'
                      }`}>
                        {job.matchScore}% Match
                      </div>
                    </div>
                    
                    <h3 className="text-lg font-bold text-slate-900 line-clamp-1">{job.title}</h3>
                    <p className="text-slate-500 text-sm font-medium mt-1">{job.company}</p>
                    
                    <div className="mt-4 space-y-2">
                      <div className="flex items-center gap-2 text-xs text-slate-500">
                        <MapPin size={14} className="text-slate-400" />
                        {job.location}
                      </div>
                      <div className="flex items-center gap-2 text-xs text-slate-400">
                        <Briefcase size={14} className="text-slate-300" />
                        Source: {job.source}
                      </div>
                    </div>
                    
                    <div className="mt-auto pt-6">
                      <a 
                        href={job.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="w-full flex items-center justify-center gap-2 py-2.5 bg-slate-900 hover:bg-blue-600 text-white text-sm font-bold rounded-xl transition-all"
                      >
                        Apply Now
                        <ExternalLink size={14} />
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
              <div className="bg-emerald-50 p-6 rounded-2xl border border-emerald-100">
                <h3 className="font-bold text-emerald-900 mb-4">Why you match</h3>
                <ul className="space-y-2">
                  <li className="flex gap-2 text-sm text-emerald-700">
                    <CheckCircle2 size={16} className="mt-0.5" /> Strong algorithm consistency on LeetCode.
                  </li>
                  <li className="flex gap-2 text-sm text-emerald-700">
                    <CheckCircle2 size={16} className="mt-0.5" /> High project impact on GitHub.
                  </li>
                </ul>
              </div>
              <div className="bg-amber-50 p-6 rounded-2xl border border-amber-100">
                <h3 className="font-bold text-amber-900 mb-4">Action Plan</h3>
                <ul className="space-y-2">
                  <li className="flex gap-2 text-sm text-amber-700">
                    <ArrowRight size={16} className="mt-0.5" /> Complete 1 System Design project.
                  </li>
                  <li className="flex gap-2 text-sm text-amber-700">
                    <ArrowRight size={16} className="mt-0.5" /> Obtain an AWS certification.
                  </li>
                </ul>
              </div>
            </div>
          </div>
        );

      default:
        return <div>Select a tab to view analysis.</div>;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-slate-500 text-sm font-medium tracking-wide">Welcome back, Developer</h2>
            <h1 className="text-3xl font-extrabold text-slate-900">
              {analysisResult ? 'Career Dashboard' : 'Profile Analyzer'}
            </h1>
          </div>
          
          <div className="flex items-center gap-4">
            <button 
              onClick={() => {
                setAnalysisResult(null);
                setProfileData({ github: '', leetcode: '', linkedin: '', resumeText: '', targetRole: '' });
                setActiveTab('overview');
              }}
              className="px-4 py-2 bg-white border border-slate-200 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-50 transition-colors"
            >
              Start New Analysis
            </button>
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold border-2 border-white shadow-sm">
              JD
            </div>
          </div>
        </header>

        <div className="transition-all duration-500">
          {renderContent()}
        </div>
      </main>
    </div>
  );
};

export default App;
