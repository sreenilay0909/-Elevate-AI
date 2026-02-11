import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { getAnalysis, chatWithPlatform, AnalysisResponse, ChatMessage } from '../services/aiAnalysisService';
import platformDataService from '../services/platformDataService';
import ModernLoader from '../components/ModernLoader';

const PlatformDetailEnhanced: React.FC = () => {
  const { platform } = useParams<{ platform: string }>();
  const navigate = useNavigate();
  const chatEndRef = useRef<HTMLDivElement>(null);
  
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [platformData, setPlatformData] = useState<any>(null);
  const [error, setError] = useState<string>('');
  
  // Chat state
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  
  // Animation state
  const [showCharts, setShowCharts] = useState(false);
  
  useEffect(() => {
    loadData();
  }, [platform]);
  
  useEffect(() => {
    if (analysis) {
      setTimeout(() => setShowCharts(true), 300);
    }
  }, [analysis]);
  
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const loadData = async () => {
    if (!platform) return;
    
    try {
      setLoading(true);
      setError('');
      
      const [data, analysisData] = await Promise.all([
        platformDataService.getPlatformData(platform),
        getAnalysis(platform)
      ]);
      
      setPlatformData(data);
      setAnalysis(analysisData);
    } catch (err: any) {
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };
  
  const handleSendMessage = async () => {
    if (!chatInput.trim() || !platform) return;
    
    const userMessage: ChatMessage = {
      role: 'user',
      content: chatInput
    };
    
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setChatLoading(true);
    
    try {
      const response = await chatWithPlatform(platform, chatInput, chatMessages);
      
      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: response.answer
      };
      
      setChatMessages(prev => [...prev, aiMessage]);
    } catch (err: any) {
      setError(err.message || 'Failed to send message');
    } finally {
      setChatLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'good': return 'text-green-600 bg-green-50';
      case 'average': return 'text-yellow-600 bg-yellow-50';
      case 'needs_improvement': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };
  
  const getPlatformName = () => {
    const names: { [key: string]: string } = {
      github: 'GitHub',
      leetcode: 'LeetCode',
      geeksforgeeks: 'GeeksforGeeks',
      codechef: 'CodeChef',
      hackerrank: 'HackerRank',
      devpost: 'DevPost',
      devto: 'Dev.to',
      linkedin: 'LinkedIn'
    };
    return names[platform || ''] || platform;
  };
  
  const getPlatformColor = () => {
    const colors: { [key: string]: string } = {
      github: '#181717',
      leetcode: '#FFA116',
      geeksforgeeks: '#2F8D46',
      codechef: '#5B4638',
      hackerrank: '#00EA64',
      devpost: '#003E54',
      devto: '#0A0A0A',
      linkedin: '#0A66C2'
    };
    return colors[platform || ''] || '#3B82F6';
  };

  // Prepare chart data
  const getStrengthWeaknessData = () => {
    if (!analysis) return [];
    
    const strengths = analysis.strengths.reduce((sum, s) => sum + s.score, 0) / analysis.strengths.length;
    const weaknesses = analysis.weaknesses.reduce((sum, w) => sum + w.score, 0) / analysis.weaknesses.length;
    
    return [
      { name: 'Strengths', value: strengths, color: '#10B981' },
      { name: 'Weaknesses', value: weaknesses, color: '#F59E0B' },
      { name: 'Potential', value: 100 - ((strengths + weaknesses) / 2), color: '#E5E7EB' }
    ];
  };
  
  const getMetricsRadarData = () => {
    if (!analysis) return [];
    
    return analysis.keyMetrics.slice(0, 6).map(metric => ({
      metric: metric.name,
      score: metric.status === 'good' ? 90 : metric.status === 'average' ? 60 : 30,
      fullMark: 100
    }));
  };
  
  const getProgressData = () => {
    if (!analysis) return [];
    
    return Object.entries(analysis.weeklyPlan).map(([day, task], index) => ({
      day: `Day ${index + 1}`,
      progress: (index + 1) * 14.3,
      target: 100
    }));
  };

  if (loading) {
    const loadingMessages = [
      "Your profile is OK.....",
      "Convert Heart into Rock...",
      "Your results are coming....",
      "200 established...."
    ];
    
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <ModernLoader 
          variant="orbit"
          size="lg"
          rotatingMessages={loadingMessages}
        />
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white p-8 rounded-2xl shadow-xl max-w-md w-full"
        >
          <div className="text-red-600 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">Oops!</h2>
          <p className="text-gray-600 text-center mb-6">{error}</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-4 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 font-medium"
          >
            Back to Dashboard
          </button>
        </motion.div>
      </div>
    );
  }
  
  if (!analysis) return null;

  const platformColor = getPlatformColor();
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      {/* Header */}
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white shadow-lg border-b border-gray-100"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <motion.button
                whileHover={{ scale: 1.1, x: -5 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/dashboard')}
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
              </motion.button>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  {getPlatformName()} Analysis
                </h1>
                <p className="text-sm text-gray-500 mt-1">@{analysis.username}</p>
              </div>
            </div>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: 'spring' }}
              className="flex items-center space-x-3"
            >
              <div className="text-right">
                <div className="text-3xl font-bold" style={{ color: platformColor }}>
                  {analysis.overallScore}
                </div>
                <div className="text-xs text-gray-500 font-medium">Overall Score</div>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Data & Analysis */}
          <div className="lg:col-span-2 space-y-6">
            {/* Overall Performance Card with Pie Chart */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
            >
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Overall Performance</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Percentile Rank */}
                <div>
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm font-semibold text-gray-700">Percentile Rank</span>
                      <motion.span
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.3, type: 'spring' }}
                        className="text-3xl font-bold text-blue-600"
                      >
                        {analysis.percentileRank}%
                      </motion.span>
                    </div>
                    <div className="relative w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${analysis.percentileRank}%` }}
                        transition={{ delay: 0.4, duration: 1, ease: 'easeOut' }}
                        className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full"
                      />
                    </div>
                    <p className="text-sm text-gray-600 mt-3">{analysis.globalRanking}</p>
                  </div>
                </div>
                
                {/* Pie Chart */}
                {showCharts && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.5 }}
                  >
                    <ResponsiveContainer width="100%" height={200}>
                      <PieChart>
                        <Pie
                          data={getStrengthWeaknessData()}
                          cx="50%"
                          cy="50%"
                          innerRadius={50}
                          outerRadius={80}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {getStrengthWeaknessData().map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                    <div className="flex justify-center space-x-4 mt-2">
                      {getStrengthWeaknessData().map((item, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                          <span className="text-xs text-gray-600">{item.name}</span>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </div>
            </motion.div>

            {/* Metrics Radar Chart */}
            {showCharts && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
              >
                <h2 className="text-xl font-bold text-gray-900 mb-4">Performance Radar</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={getMetricsRadarData()}>
                    <PolarGrid stroke="#E5E7EB" />
                    <PolarAngleAxis dataKey="metric" tick={{ fill: '#6B7280', fontSize: 12 }} />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#9CA3AF' }} />
                    <Radar name="Your Score" dataKey="score" stroke={platformColor} fill={platformColor} fillOpacity={0.6} />
                    <Tooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </motion.div>
            )}
            
            {/* Weekly Progress Line Chart */}
            {showCharts && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 }}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
              >
                <h2 className="text-xl font-bold text-gray-900 mb-4">7-Day Progress Projection</h2>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={getProgressData()}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis dataKey="day" tick={{ fill: '#6B7280' }} />
                    <YAxis tick={{ fill: '#6B7280' }} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="progress" stroke="#3B82F6" strokeWidth={3} dot={{ fill: '#3B82F6', r: 5 }} activeDot={{ r: 8 }} />
                    <Line type="monotone" dataKey="target" stroke="#10B981" strokeWidth={2} strokeDasharray="5 5" />
                  </LineChart>
                </ResponsiveContainer>
              </motion.div>
            )}

            {/* Key Metrics Table */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
            >
              <h2 className="text-xl font-bold text-gray-900 mb-4">Key Metrics</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Metric</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Your Value</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Benchmark</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {analysis.keyMetrics.map((metric, index) => (
                      <motion.tr
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 + index * 0.05 }}
                        className="hover:bg-gray-50 transition-colors"
                      >
                        <td className="px-4 py-3 text-sm font-medium text-gray-900">{metric.name}</td>
                        <td className="px-4 py-3 text-sm text-gray-700 font-semibold">{metric.value}</td>
                        <td className="px-4 py-3 text-sm text-gray-500">{metric.benchmark}</td>
                        <td className="px-4 py-3">
                          <span className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(metric.status)}`}>
                            {metric.status.replace('_', ' ')}
                          </span>
                        </td>
                      </motion.tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </motion.div>

            {/* Strengths */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
            >
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <svg className="w-6 h-6 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Strengths
              </h2>
              <div className="space-y-4">
                {analysis.strengths.map((strength, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 + index * 0.1 }}
                    className="border-l-4 border-green-500 pl-4 py-2 bg-green-50 rounded-r-lg hover:bg-green-100 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <h3 className="font-semibold text-gray-900">{strength.topic}</h3>
                      <span className="text-sm font-bold text-green-600">{strength.score}/100</span>
                    </div>
                    <p className="text-sm text-gray-600">{strength.description}</p>
                  </motion.div>
                ))}
              </div>
            </motion.div>
            
            {/* Weaknesses */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
            >
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <svg className="w-6 h-6 text-orange-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                Areas for Improvement
              </h2>
              <div className="space-y-4">
                {analysis.weaknesses.map((weakness, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    className="border-l-4 border-orange-500 pl-4 py-2 bg-orange-50 rounded-r-lg hover:bg-orange-100 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <h3 className="font-semibold text-gray-900">{weakness.topic}</h3>
                      <span className="text-sm font-bold text-orange-600">{weakness.score}/100</span>
                    </div>
                    <p className="text-sm text-gray-600">{weakness.description}</p>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Recommendations */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
            >
              <h2 className="text-xl font-bold text-gray-900 mb-4">Recommendations</h2>
              <ul className="space-y-3">
                {analysis.recommendations.map((rec, index) => (
                  <motion.li
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + index * 0.05 }}
                    className="flex items-start group"
                  >
                    <svg className="w-5 h-5 text-blue-600 mr-3 mt-0.5 flex-shrink-0 group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700 group-hover:text-gray-900 transition-colors">{rec}</span>
                  </motion.li>
                ))}
              </ul>
            </motion.div>
            
            {/* Weekly Plan */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl shadow-lg p-6 border border-blue-100"
            >
              <h2 className="text-xl font-bold text-gray-900 mb-4">7-Day Improvement Plan</h2>
              <div className="space-y-3">
                {Object.entries(analysis.weeklyPlan).map(([day, task], index) => (
                  <motion.div
                    key={day}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.7 + index * 0.05 }}
                    className="flex items-start bg-white rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex-shrink-0 w-16">
                      <span className="inline-flex items-center justify-center w-14 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-sm font-bold">
                        Day {index + 1}
                      </span>
                    </div>
                    <div className="flex-1 ml-4">
                      <p className="text-gray-700">{task}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Right Column - Enhanced Chatbot */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white rounded-2xl shadow-xl sticky top-4 overflow-hidden border border-gray-100"
            >
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-5 text-white">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                  </div>
                  <div>
                    <h2 className="text-lg font-bold">AI Assistant</h2>
                    <p className="text-sm text-blue-100">
                      Ask about your {getPlatformName()} performance
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="h-96 overflow-y-auto p-4 space-y-4 bg-gray-50">
                <AnimatePresence>
                  {chatMessages.length === 0 ? (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                      className="text-center text-gray-500 mt-12"
                    >
                      <motion.div
                        animate={{ y: [0, -10, 0] }}
                        transition={{ repeat: Infinity, duration: 2 }}
                      >
                        <svg className="w-16 h-16 mx-auto mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                        </svg>
                      </motion.div>
                      <p className="text-sm font-medium">Start a conversation!</p>
                      <p className="text-xs mt-2 text-gray-400">Ask me anything about your {getPlatformName()} performance</p>
                    </motion.div>
                  ) : (
                    chatMessages.map((msg, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20, scale: 0.8 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-xs px-4 py-3 rounded-2xl shadow-md ${
                            msg.role === 'user'
                              ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-br-none'
                              : 'bg-white text-gray-900 rounded-bl-none border border-gray-200'
                          }`}
                        >
                          <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                        </div>
                      </motion.div>
                    ))
                  )}
                </AnimatePresence>
                {chatLoading && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="bg-white px-4 py-3 rounded-2xl rounded-bl-none shadow-md border border-gray-200">
                      <div className="flex space-x-2">
                        <motion.div
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{ repeat: Infinity, duration: 1, delay: 0 }}
                          className="w-2 h-2 bg-gray-400 rounded-full"
                        />
                        <motion.div
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{ repeat: Infinity, duration: 1, delay: 0.2 }}
                          className="w-2 h-2 bg-gray-400 rounded-full"
                        />
                        <motion.div
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{ repeat: Infinity, duration: 1, delay: 0.4 }}
                          className="w-2 h-2 bg-gray-400 rounded-full"
                        />
                      </div>
                    </div>
                  </motion.div>
                )}
                <div ref={chatEndRef} />
              </div>
              
              <div className="p-4 bg-white border-t border-gray-200">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                    placeholder="Ask a question..."
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    disabled={chatLoading}
                  />
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleSendMessage}
                    disabled={chatLoading || !chatInput.trim()}
                    className="px-4 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-md"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </motion.button>
                </div>
                <p className="text-xs text-gray-500 mt-2 text-center">
                  Press Enter to send • Shift+Enter for new line
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlatformDetailEnhanced;
