import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, User, Mail, Calendar, CheckCircle, XCircle, Settings, ExternalLink, Github, Code2, Award, Trophy, Briefcase, FileText, Loader2, RefreshCw, AlertCircle, Search } from 'lucide-react';
import profileService, { ProfileData } from '../services/profileService';
import platformDataService, { PlatformData } from '../services/platformDataService';
import { formatDistanceToNow } from 'date-fns';
import ModernLoader from '../components/ModernLoader';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [platformDataMap, setPlatformDataMap] = useState<Record<string, PlatformData>>({});
  const [refreshingAll, setRefreshingAll] = useState(false);
  const [refreshingPlatform, setRefreshingPlatform] = useState<string | null>(null);
  
  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Array<{
    username: string;
    name: string;
    fullName?: string;
    bio?: string;
    collegeName?: string;
  }>>([]);
  const [searching, setSearching] = useState(false);
  const [showSearchResults, setShowSearchResults] = useState(false);

  useEffect(() => {
    loadProfile();
    loadPlatformData();
    
    // Close search results when clicking outside
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (!target.closest('.search-container')) {
        setShowSearchResults(false);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await profileService.getMyProfile();
      console.log('Profile loaded:', data);
      setProfile(data);
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadPlatformData = async () => {
    try {
      console.log('Loading platform data...');
      const allData = await platformDataService.getAllPlatformData();
      console.log('Raw platform data from API:', allData);
      const dataMap: Record<string, PlatformData> = {};
      allData.forEach(pd => {
        console.log(`Processing platform: ${pd.platform}`, pd);
        dataMap[pd.platform] = pd;
      });
      console.log('Final platform data map:', dataMap);
      setPlatformDataMap(dataMap);
    } catch (error) {
      console.error('Failed to load platform data:', error);
    }
  };

  const handleRefreshPlatform = async (platform: string) => {
    try {
      console.log(`Refreshing platform: ${platform}`);
      setRefreshingPlatform(platform);
      const result = await platformDataService.fetchPlatformData(platform);
      console.log(`Refresh result for ${platform}:`, result);
      
      if (result.status === 'success' && result.data) {
        setPlatformDataMap(prev => ({
          ...prev,
          [platform]: {
            platform,
            data: result.data!,
            lastUpdated: result.lastUpdated,
            fetchStatus: 'success'
          }
        }));
      } else {
        console.error(`Failed to refresh ${platform}:`, result.error);
        alert(`Failed to refresh ${platform}: ${result.error}`);
      }
    } catch (error) {
      console.error(`Error refreshing ${platform}:`, error);
      alert(`Error refreshing ${platform}: ${error}`);
    } finally {
      setRefreshingPlatform(null);
    }
  };

  const handleRefreshAll = async () => {
    try {
      setRefreshingAll(true);
      const result = await platformDataService.fetchAllPlatforms();
      
      const newDataMap: Record<string, PlatformData> = { ...platformDataMap };
      result.results.forEach(r => {
        if (r.status === 'success' && r.data) {
          newDataMap[r.platform] = {
            platform: r.platform,
            data: r.data,
            lastUpdated: r.lastUpdated,
            fetchStatus: 'success'
          };
        }
      });
      setPlatformDataMap(newDataMap);
      
      if (result.failed > 0) {
        console.warn(`${result.failed} platform(s) failed to refresh`);
      }
    } catch (error) {
      console.error('Error refreshing all platforms:', error);
    } finally {
      setRefreshingAll(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/dashboard');
  };

  // Search functionality
  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    
    if (query.length < 2) {
      setSearchResults([]);
      setShowSearchResults(false);
      return;
    }
    
    setSearching(true);
    try {
      const results = await profileService.searchUsers(query);
      setSearchResults(results);
      setShowSearchResults(true);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
    } finally {
      setSearching(false);
    }
  };

  const handleSearchResultClick = (username: string) => {
    setShowSearchResults(false);
    setSearchQuery('');
    navigate(`/profile/${username}`);
  };

  if (!user) return null;

  const platforms = [
    {
      name: 'GitHub',
      key: 'github',
      username: profile?.githubUsername,
      icon: Github,
      url: profile?.githubUsername ? `https://github.com/${profile.githubUsername}` : null,
      color: 'bg-gray-800',
      getStats: (data: any) => [
        { label: 'Repositories', value: data?.repositories || 0 },
        { label: 'Total Stars', value: data?.totalStars || 0 },
        { label: 'Commits (Year)', value: data?.commitsLastYear || 0 },
        { label: 'Streak', value: data?.contributionStreak ? `${data.contributionStreak} days` : 'N/A' },
      ]
    },
    {
      name: 'LeetCode',
      key: 'leetcode',
      username: profile?.leetcodeUsername,
      icon: Code2,
      url: profile?.leetcodeUsername ? `https://leetcode.com/${profile.leetcodeUsername}` : null,
      color: 'bg-orange-500',
      getStats: (data: any) => [
        { label: 'Problems Solved', value: data?.totalSolved || 0 },
        { label: 'Easy', value: data?.easySolved || 0 },
        { label: 'Medium', value: data?.mediumSolved || 0 },
        { label: 'Hard', value: data?.hardSolved || 0 },
      ]
    },
    {
      name: 'GeeksforGeeks',
      key: 'geeksforgeeks',
      username: profile?.geeksforgeeksUsername,
      icon: Award,
      url: profile?.geeksforgeeksUsername ? `https://www.geeksforgeeks.org/profile/${profile.geeksforgeeksUsername}` : null,
      color: 'bg-green-600',
      getStats: (data: any) => [
        { label: 'Coding Score', value: data?.codingScore || 0 },
        { label: 'Problems Solved', value: data?.problemsSolved || 0 },
        { label: 'Institute Rank', value: data?.instituteRank || 'N/A' },
        { label: 'Articles Published', value: data?.articlesPublished || 0 },
        { label: 'Longest Streak', value: data?.longestStreak ? `${data.longestStreak} days` : 'N/A' },
        { label: 'POTDs Solved', value: data?.potdsSolved || 0 },
      ]
    },
    {
      name: 'CodeChef',
      key: 'codechef',
      username: profile?.codechefUsername,
      icon: Trophy,
      url: profile?.codechefUsername ? `https://www.codechef.com/users/${profile.codechefUsername}` : null,
      color: 'bg-brown-600',
      getStats: (data: any) => [
        { label: 'Rating', value: data?.currentRating || 0 },
        { label: 'Stars', value: data?.stars ? `${data.stars}★` : 'N/A' },
        { label: 'Problems Solved', value: data?.problemsSolved || 0 },
        { label: 'Contests', value: data?.contestsParticipated || 0 },
        { label: 'Global Rank', value: data?.globalRank || 'N/A' },
        { label: 'Country Rank', value: data?.countryRank || 'N/A' },
      ]
    },
    {
      name: 'HackerRank',
      key: 'hackerrank',
      username: profile?.hackerrankUsername,
      icon: Code2,
      url: profile?.hackerrankUsername ? `https://www.hackerrank.com/${profile.hackerrankUsername}` : null,
      color: 'bg-green-500',
      getStats: (data: any) => [
        { label: 'Total Stars', value: data?.totalStars || 0 },
        { label: 'Badges', value: data?.badges || 0 },
        { label: 'Skills Verified', value: data?.skillsVerified || 0 },
        { label: 'Certificates', value: data?.certificates || 0 },
      ]
    },
    {
      name: 'DevPost',
      key: 'devpost',
      username: profile?.devpostUsername,
      icon: Briefcase,
      url: profile?.devpostUsername ? `https://devpost.com/${profile.devpostUsername}` : null,
      color: 'bg-blue-700',
      getStats: (data: any) => [
        { label: 'Projects', value: data?.projectsSubmitted || 0 },
        { label: 'Hackathons', value: data?.hackathonsParticipated || 0 },
        { label: 'Prizes Won', value: data?.prizesWon || 0 },
        { label: 'Followers', value: data?.followers || 0 },
      ]
    },
    {
      name: 'Dev.to',
      key: 'devto',
      username: profile?.devtoUsername,
      icon: FileText,
      url: profile?.devtoUsername ? `https://dev.to/${profile.devtoUsername}` : null,
      color: 'bg-black',
      getStats: (data: any) => [
        { label: 'Articles', value: data?.articlesPublished || 0 },
        { label: 'Reactions', value: data?.totalReactions || 0 },
        { label: 'Comments', value: data?.totalComments || 0 },
        { label: 'Followers', value: data?.followers || 0 },
      ]
    },
    {
      name: 'LinkedIn',
      key: 'linkedin',
      username: profile?.linkedinUrl,
      icon: Briefcase,
      url: profile?.linkedinUrl,
      color: 'bg-blue-700',
      getStats: (data: any) => [
        { label: 'Connections', value: data?.connections || 0 },
        { label: 'Headline', value: data?.headline || 'N/A' },
        { label: 'Location', value: data?.location || 'N/A' },
        { label: 'Experience', value: data?.experienceCount || 0 },
        { label: 'Education', value: data?.educationCount || 0 },
        { label: 'Skills', value: data?.skillsCount || 0 },
      ]
    },
  ];

  const connectedPlatforms = platforms.filter(p => p.username);
  
  console.log('Profile:', profile);
  console.log('Connected platforms:', connectedPlatforms);
  console.log('Platform data map:', platformDataMap);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-slate-900">ElevateAI</h1>
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                Dashboard
              </span>
            </div>
            
            {/* Search Bar */}
            <div className="flex-1 max-w-md relative search-container">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  onFocus={() => searchQuery.length >= 2 && setShowSearchResults(true)}
                  placeholder="Search users by name or username..."
                  className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {searching && (
                  <Loader2 className="absolute right-3 top-1/2 transform -translate-y-1/2 text-blue-600 animate-spin" size={20} />
                )}
              </div>
              
              {/* Search Results Dropdown */}
              {showSearchResults && searchResults.length > 0 && (
                <div className="absolute top-full mt-2 w-full bg-white border border-slate-200 rounded-lg shadow-xl z-50 max-h-96 overflow-y-auto">
                  {searchResults.map((result) => (
                    <button
                      key={result.username}
                      onClick={() => handleSearchResultClick(result.username)}
                      className="w-full px-4 py-3 hover:bg-slate-50 transition-colors text-left border-b border-slate-100 last:border-b-0"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                          <User className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="font-semibold text-slate-900 truncate">
                            {result.fullName || result.name}
                          </p>
                          <p className="text-sm text-slate-600 truncate">@{result.username}</p>
                          {result.collegeName && (
                            <p className="text-xs text-slate-500 truncate">{result.collegeName}</p>
                          )}
                        </div>
                        <ExternalLink className="w-4 h-4 text-slate-400 flex-shrink-0" />
                      </div>
                    </button>
                  ))}
                </div>
              )}
              
              {/* No Results */}
              {showSearchResults && searchQuery.length >= 2 && searchResults.length === 0 && !searching && (
                <div className="absolute top-full mt-2 w-full bg-white border border-slate-200 rounded-lg shadow-xl z-50 p-4 text-center">
                  <p className="text-slate-600">No users found</p>
                </div>
              )}
            </div>
            
            <div className="flex items-center gap-3">
              <Link
                to={`/profile/${user.username}`}
                className="flex items-center gap-2 px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-xl font-medium transition-colors"
              >
                <ExternalLink size={18} />
                View Public Profile
              </Link>
              <Link
                to="/edit-profile"
                className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-medium transition-colors"
              >
                <Settings size={18} />
                Edit Profile
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-medium transition-colors"
              >
                <LogOut size={18} />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-white mb-8">
          <h2 className="text-3xl font-bold mb-2">Welcome back, {user.name}! 👋</h2>
          <p className="text-blue-100">
            You're logged in and ready to elevate your developer profile.
          </p>
        </div>

        {/* User Info Card */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
          <h3 className="text-xl font-bold text-slate-900 mb-6">Your Account</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <User className="text-blue-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-slate-500 font-medium">Username</p>
                <p className="text-slate-900 font-semibold">@{user.username}</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Mail className="text-purple-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-slate-500 font-medium">Email</p>
                <p className="text-slate-900 font-semibold">{user.email}</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Calendar className="text-green-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-slate-500 font-medium">Member Since</p>
                <p className="text-slate-900 font-semibold">
                  {new Date(user.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className={`p-2 rounded-lg ${user.email_verified ? 'bg-green-100' : 'bg-amber-100'}`}>
                {user.email_verified ? (
                  <CheckCircle className="text-green-600" size={20} />
                ) : (
                  <XCircle className="text-amber-600" size={20} />
                )}
              </div>
              <div>
                <p className="text-sm text-slate-500 font-medium">Email Status</p>
                <p className={`font-semibold ${user.email_verified ? 'text-green-600' : 'text-amber-600'}`}>
                  {user.email_verified ? 'Verified' : 'Not Verified'}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Connected Platforms */}
        {loading ? (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-12 text-center">
            <ModernLoader 
              variant="wave" 
              size="md"
              rotatingMessages={[
                "Fetching your platforms...",
                "Almost there...",
                "Loading data...",
                "Just a moment..."
              ]}
            />
          </div>
        ) : connectedPlatforms.length > 0 ? (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-slate-900">Connected Platforms</h3>
              <div className="flex items-center gap-3">
                <button
                  onClick={handleRefreshAll}
                  disabled={refreshingAll}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-medium transition-colors"
                >
                  <RefreshCw size={18} className={refreshingAll ? 'animate-spin' : ''} />
                  {refreshingAll ? 'Refreshing...' : 'Refresh All'}
                </button>
                <Link
                  to="/edit-profile"
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  Manage Platforms →
                </Link>
              </div>
            </div>

            {/* Two Column Layout: Platforms (61%) + Resume (39%) */}
            <div className="flex flex-col lg:flex-row gap-6">
              {/* Left Side: Platform Cards Grid (61%) */}
              <div className="flex-1 lg:w-[61%]">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {connectedPlatforms.map((platform) => {
                    const platformData = platformDataMap[platform.key];
                    const stats = platformData?.data ? platform.getStats(platformData.data) : null;
                    const isRefreshing = refreshingPlatform === platform.key;
                    
                    return (
                      <div
                        key={platform.name}
                        className="bg-white rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow overflow-hidden"
                      >
                        {/* Clickable area for AI analysis */}
                        <div
                          onClick={() => stats && navigate(`/platform/${platform.key}`)}
                          className={`p-6 ${stats ? 'cursor-pointer hover:bg-slate-50' : ''} transition-colors`}
                        >
                          <div className="flex items-center gap-4 mb-4">
                            <div className={`w-12 h-12 ${platform.color} rounded-lg flex items-center justify-center`}>
                              <platform.icon className="w-6 h-6 text-white" />
                            </div>
                            <div className="flex-1">
                              <h4 className="font-semibold text-slate-800">{platform.name}</h4>
                              <p className="text-sm text-slate-600">@{platform.username}</p>
                            </div>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleRefreshPlatform(platform.key);
                              }}
                              disabled={isRefreshing}
                              className="p-2 hover:bg-slate-100 rounded-lg transition-colors disabled:opacity-50"
                              title="Refresh data"
                            >
                              <RefreshCw size={18} className={`text-slate-600 ${isRefreshing ? 'animate-spin' : ''}`} />
                            </button>
                          </div>

                          {stats ? (
                            <>
                              <div className="space-y-2 mb-4">
                                {stats.map((stat, idx) => (
                                  <div key={idx} className="flex justify-between items-center">
                                    <span className="text-sm text-slate-600">{stat.label}</span>
                                    <span className="text-sm font-semibold text-slate-900">{stat.value}</span>
                                  </div>
                                ))}
                              </div>
                              
                              {/* AI Analysis Button */}
                              <div className="mt-4 p-3 bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg">
                                <div className="flex items-center justify-between">
                                  <div className="flex items-center gap-2">
                                    <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                    </svg>
                                    <span className="text-sm font-medium text-purple-700">AI Analysis Available</span>
                                  </div>
                                  <svg className="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                  </svg>
                                </div>
                                <p className="text-xs text-purple-600 mt-1">Click to view detailed analysis & insights</p>
                              </div>
                            </>
                          ) : (
                            <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                              <div className="flex items-center gap-2 text-amber-700">
                                <AlertCircle size={16} />
                                <span className="text-sm">No data yet. Click refresh to fetch.</span>
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Footer with timestamp and external link */}
                        <div className="flex items-center justify-between px-6 py-3 bg-slate-50 border-t border-slate-200">
                          {platformData?.lastUpdated ? (
                            <span className="text-xs text-slate-500">
                              Updated {formatDistanceToNow(new Date(platformData.lastUpdated), { addSuffix: true })}
                            </span>
                          ) : (
                            <span className="text-xs text-slate-500">Never updated</span>
                          )}
                          {platform.url && (
                            <a
                              href={platform.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              onClick={(e) => e.stopPropagation()}
                              className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1"
                            >
                              View Profile
                              <ExternalLink size={14} />
                            </a>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Right Side: Resume Card (39%) */}
              <div className="lg:w-[39%] lg:min-w-[320px] w-full">
                {profile?.resumeUrl ? (
                  <div className="bg-white rounded-xl shadow-sm border-2 border-purple-200 overflow-hidden hover:shadow-lg transition-all sticky top-4">
                    <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                          <FileText className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1">
                          <h4 className="font-semibold text-white">Resume</h4>
                          <p className="text-xs text-purple-100">PDF Document</p>
                        </div>
                        <div className="flex items-center gap-1 bg-green-500 px-2 py-1 rounded-full">
                          <CheckCircle size={12} className="text-white" />
                          <span className="text-xs font-medium text-white">Active</span>
                        </div>
                      </div>
                    </div>

                    {/* PDF Preview */}
                    <div className="relative bg-slate-50 border-b border-slate-200" style={{ height: '500px' }}>
                      <iframe
                        src={`http://127.0.0.1:8000${profile.resumeUrl}#toolbar=0&navpanes=0&scrollbar=0`}
                        className="w-full h-full"
                        title="Resume Preview"
                        style={{ pointerEvents: 'none' }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-white/80 via-transparent to-transparent pointer-events-none" />
                    </div>

                    <div className="p-4 space-y-2">
                      <a
                        href={`http://127.0.0.1:8000${profile.resumeUrl}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="w-full py-2.5 px-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all font-medium text-center flex items-center justify-center gap-2 shadow-md hover:shadow-lg"
                      >
                        <ExternalLink size={16} />
                        View Full Resume
                      </a>
                      <Link
                        to="/edit-profile"
                        className="w-full py-2 px-4 bg-slate-100 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors font-medium text-center flex items-center justify-center gap-2"
                      >
                        <FileText size={16} />
                        Update Resume
                      </Link>
                    </div>
                  </div>
                ) : (
                  <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl shadow-sm border-2 border-dashed border-slate-300 p-6 hover:border-purple-400 hover:shadow-md transition-all sticky top-4">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 bg-slate-200 rounded-lg flex items-center justify-center">
                        <FileText className="w-6 h-6 text-slate-400" />
                      </div>
                      <div className="flex-1">
                        <h4 className="font-semibold text-slate-800">Resume</h4>
                        <p className="text-sm text-slate-600">Not uploaded yet</p>
                      </div>
                    </div>

                    <div className="space-y-3 mb-4">
                      <div className="flex items-center gap-2 text-amber-700 bg-amber-50 px-3 py-2 rounded-lg">
                        <AlertCircle size={16} />
                        <span className="text-sm font-medium">No resume uploaded</span>
                      </div>
                      <p className="text-sm text-slate-600">
                        Upload your resume to make it available for recruiters and showcase your experience.
                      </p>
                    </div>

                    <Link
                      to="/edit-profile"
                      className="w-full py-2 px-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all font-medium text-center flex items-center justify-center gap-2"
                    >
                      <FileText size={16} />
                      Upload Resume
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-12 text-center mb-8">
            <Code2 className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-slate-800 mb-2">No Platforms Connected</h3>
            <p className="text-slate-600 mb-6">
              Connect your coding platforms to track your progress and showcase your skills
            </p>
            <Link
              to="/edit-profile"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              <Settings size={18} />
              Connect Platforms
            </Link>
          </div>
        )}

        {/* Coming Soon Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 text-center">
          <div className="max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              🚀 More Features Coming Soon!
            </h3>
            <p className="text-slate-600 mb-6">
              We're working on exciting features including:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
              <div className="p-4 bg-slate-50 rounded-xl">
                <p className="font-semibold text-slate-900 mb-1">📊 Real-time Statistics</p>
                <p className="text-sm text-slate-600">
                  View your GitHub repos, LeetCode problems, and more
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl">
                <p className="font-semibold text-slate-900 mb-1">🎯 Skill Analysis</p>
                <p className="text-sm text-slate-600">
                  Get insights on your strengths and areas to improve
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl">
                <p className="font-semibold text-slate-900 mb-1">📈 Progress Tracking</p>
                <p className="text-sm text-slate-600">
                  Track your coding journey over time
                </p>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl">
                <p className="font-semibold text-slate-900 mb-1">🏆 Industry Benchmarks</p>
                <p className="text-sm text-slate-600">
                  Compare your skills with industry standards
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;
