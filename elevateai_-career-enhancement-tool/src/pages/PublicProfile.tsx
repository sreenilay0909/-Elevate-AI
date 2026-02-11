import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { User, Github, Code2, Award, Trophy, Briefcase, FileText, ExternalLink, Loader2, Calendar, AlertCircle, CheckCircle, ArrowLeft, Mail } from 'lucide-react';
import profileService, { PublicProfileData } from '../services/profileService';
import platformDataService, { PlatformData } from '../services/platformDataService';
import { formatDistanceToNow } from 'date-fns';
import { useAuth } from '../contexts/AuthContext';
import ModernLoader from '../components/ModernLoader';

const PublicProfile: React.FC = () => {
  const { username } = useParams<{ username: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [profile, setProfile] = useState<PublicProfileData | null>(null);
  const [platformDataMap, setPlatformDataMap] = useState<Record<string, PlatformData>>({});
  const [isResumeBlurred, setIsResumeBlurred] = useState(true);

  useEffect(() => {
    if (username) {
      loadProfile(username);
    }
  }, [username]);

  const loadProfile = async (username: string) => {
    try {
      setLoading(true);
      setError('');
      const data = await profileService.getPublicProfile(username);
      setProfile(data);
      
      // Try to load platform data (may fail if not logged in, that's okay)
      try {
        const allData = await platformDataService.getAllPlatformData();
        const dataMap: Record<string, PlatformData> = {};
        allData.forEach(pd => {
          dataMap[pd.platform] = pd;
        });
        setPlatformDataMap(dataMap);
      } catch (err) {
        // Platform data not available (user not logged in or no data)
        console.log('Platform data not available for public view');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'User not found');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-slate-100 flex items-center justify-center">
        <ModernLoader 
          variant="gradient" 
          size="lg"
          rotatingMessages={[
            "Loading profile...",
            "Gathering data...",
            "Almost ready...",
            "Finalizing..."
          ]}
        />
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <div className="bg-white rounded-2xl shadow-xl p-12 max-w-md">
            <User className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-slate-800 mb-2">User Not Found</h2>
            <p className="text-slate-600 mb-6">{error}</p>
            <Link
              to="/"
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Go Home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const platforms = [
    {
      name: 'GitHub',
      key: 'github',
      username: profile.githubUsername,
      icon: Github,
      url: profile.githubUsername ? `https://github.com/${profile.githubUsername}` : null,
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
      username: profile.leetcodeUsername,
      icon: Code2,
      url: profile.leetcodeUsername ? `https://leetcode.com/${profile.leetcodeUsername}` : null,
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
      username: profile.geeksforgeeksUsername,
      icon: Award,
      url: profile.geeksforgeeksUsername ? `https://www.geeksforgeeks.org/profile/${profile.geeksforgeeksUsername}` : null,
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
      username: profile.codechefUsername,
      icon: Trophy,
      url: profile.codechefUsername ? `https://www.codechef.com/users/${profile.codechefUsername}` : null,
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
      username: profile.hackerrankUsername,
      icon: Code2,
      url: profile.hackerrankUsername ? `https://www.hackerrank.com/${profile.hackerrankUsername}` : null,
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
      username: profile.devpostUsername,
      icon: Briefcase,
      url: profile.devpostUsername ? `https://devpost.com/${profile.devpostUsername}` : null,
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
      username: profile.devtoUsername,
      icon: FileText,
      url: profile.devtoUsername ? `https://dev.to/${profile.devtoUsername}` : null,
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
      username: profile.linkedinUrl,
      icon: Briefcase,
      url: profile.linkedinUrl,
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

  const activePlatforms = platforms.filter(p => p.username);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-slate-900">ElevateAI</h1>
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                Public Profile
              </span>
            </div>
            <div className="flex items-center gap-3">
              {profile.portfolioUrl && (
                <a
                  href={profile.portfolioUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-xl font-medium transition-colors"
                >
                  <ExternalLink size={18} />
                  Portfolio
                </a>
              )}
              {user ? (
                <Link
                  to="/dashboard"
                  className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-medium transition-colors"
                >
                  <ArrowLeft size={18} />
                  Back to Dashboard
                </Link>
              ) : (
                <Link
                  to="/login"
                  className="flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-medium transition-colors"
                >
                  <User size={18} />
                  Login
                </Link>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-white mb-8">
          <div className="flex items-center gap-6">
            {/* Profile Picture */}
            {profile.profilePictureUrl ? (
              <img
                src={`http://127.0.0.1:8000${profile.profilePictureUrl}`}
                alt={profile.name}
                className="w-24 h-24 rounded-full object-cover border-4 border-white/30 shadow-lg"
              />
            ) : (
              <div className="w-24 h-24 bg-white/20 rounded-full flex items-center justify-center border-4 border-white/30">
                <User className="w-12 h-12 text-white" />
              </div>
            )}
            
            <div className="flex-1">
              <h2 className="text-3xl font-bold mb-2">{profile.name}'s Profile 👋</h2>
              <p className="text-blue-100">
                @{profile.username}
              </p>
            </div>
          </div>
        </div>

        {/* User Info Card */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
          <h3 className="text-xl font-bold text-slate-900 mb-6">Profile Information</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Full Name */}
            {profile.fullName && (
              <div className="flex items-start gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <User className="text-blue-600" size={20} />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Full Name</p>
                  <p className="text-slate-900 font-semibold">{profile.fullName}</p>
                </div>
              </div>
            )}

            {/* Username */}
            <div className="flex items-start gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <User className="text-purple-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-slate-500 font-medium">Username</p>
                <p className="text-slate-900 font-semibold">@{profile.username}</p>
              </div>
            </div>

            {/* Email */}
            <div className="flex items-start gap-3">
              <div className="p-2 bg-indigo-100 rounded-lg">
                <Mail className="text-indigo-600" size={20} />
              </div>
              <div>
                <p className="text-sm text-slate-500 font-medium">Email</p>
                <p className="text-slate-900 font-semibold">{profile.email}</p>
              </div>
            </div>

            {/* Gender */}
            {profile.gender && (
              <div className="flex items-start gap-3">
                <div className="p-2 bg-pink-100 rounded-lg">
                  <User className="text-pink-600" size={20} />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Gender</p>
                  <p className="text-slate-900 font-semibold">{profile.gender}</p>
                </div>
              </div>
            )}

            {/* Contact Number */}
            {profile.contactNumber && (
              <div className="flex items-start gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <FileText className="text-green-600" size={20} />
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Contact</p>
                  <p className="text-slate-900 font-semibold">{profile.contactNumber}</p>
                </div>
              </div>
            )}
          </div>

          {/* Bio */}
          {profile.bio && (
            <div className="mt-6 pt-6 border-t border-slate-200">
              <h4 className="text-sm font-medium text-slate-500 mb-2">About</h4>
              <p className="text-slate-900 leading-relaxed">{profile.bio}</p>
            </div>
          )}
        </div>

        {/* Education Card */}
        {(profile.collegeName || profile.degree || profile.fieldOfStudy) && (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
            <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
              <Award className="w-5 h-5 text-blue-600" />
              Education
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {profile.collegeName && (
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-indigo-100 rounded-lg">
                    <Award className="text-indigo-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-slate-500 font-medium">College / University</p>
                    <p className="text-slate-900 font-semibold">{profile.collegeName}</p>
                  </div>
                </div>
              )}

              {profile.degree && (
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Award className="text-blue-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-slate-500 font-medium">Degree</p>
                    <p className="text-slate-900 font-semibold">{profile.degree}</p>
                  </div>
                </div>
              )}

              {profile.fieldOfStudy && (
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Code2 className="text-purple-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-slate-500 font-medium">Field of Study</p>
                    <p className="text-slate-900 font-semibold">{profile.fieldOfStudy}</p>
                  </div>
                </div>
              )}

              {profile.currentYear && (
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <Calendar className="text-green-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-slate-500 font-medium">Current Year</p>
                    <p className="text-slate-900 font-semibold">{profile.currentYear}</p>
                  </div>
                </div>
              )}

              {profile.graduationYear && (
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-amber-100 rounded-lg">
                    <Calendar className="text-amber-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-slate-500 font-medium">Graduation Year</p>
                    <p className="text-slate-900 font-semibold">{profile.graduationYear}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Skills Card */}
        {profile.skills && (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
            <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
              <Code2 className="w-5 h-5 text-blue-600" />
              Skills & Technologies
            </h3>
            
            <div className="flex flex-wrap gap-3">
              {profile.skills.split(',').map((skill, index) => (
                <span
                  key={index}
                  className="px-4 py-2 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 text-blue-700 rounded-full text-sm font-medium hover:shadow-md transition-shadow"
                >
                  {skill.trim()}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Connected Platforms */}
        {activePlatforms.length > 0 ? (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-slate-900">Connected Platforms</h3>
            </div>

            {/* Two Column Layout: Platforms (61%) + Resume (39%) */}
            <div className="flex flex-col lg:flex-row gap-6">
              {/* Left Side: Platform Cards Grid (61%) */}
              <div className="flex-1 lg:w-[61%]">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {activePlatforms.map((platform) => {
                    const platformData = platformDataMap[platform.key];
                    const stats = platformData?.data ? platform.getStats(platformData.data) : null;
                    
                    return (
                      <div
                        key={platform.name}
                        className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-center gap-4 mb-4">
                          <div className={`w-12 h-12 ${platform.color} rounded-lg flex items-center justify-center`}>
                            <platform.icon className="w-6 h-6 text-white" />
                          </div>
                          <div className="flex-1">
                            <h4 className="font-semibold text-slate-800">{platform.name}</h4>
                            <p className="text-sm text-slate-600">@{platform.username}</p>
                          </div>
                        </div>

                        {stats ? (
                          <div className="space-y-2 mb-4">
                            {stats.map((stat, idx) => (
                              <div key={idx} className="flex justify-between items-center">
                                <span className="text-sm text-slate-600">{stat.label}</span>
                                <span className="text-sm font-semibold text-slate-900">{stat.value}</span>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                            <div className="flex items-center gap-2 text-amber-700">
                              <AlertCircle size={16} />
                              <span className="text-sm">Statistics not available</span>
                            </div>
                          </div>
                        )}

                        <div className="flex items-center justify-between pt-3 border-t border-slate-200">
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
                {profile.resumeUrl ? (
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
                    <div 
                      className="relative bg-slate-50 border-b border-slate-200 cursor-pointer group" 
                      style={{ height: '500px' }}
                      onClick={() => setIsResumeBlurred(false)}
                      title={isResumeBlurred ? "Click to view resume clearly" : "Resume visible"}
                    >
                      <iframe
                        src={`http://127.0.0.1:8000${profile.resumeUrl}#toolbar=0&navpanes=0&scrollbar=0`}
                        className="w-full h-full"
                        title="Resume Preview"
                        style={{ 
                          pointerEvents: 'none',
                          filter: isResumeBlurred ? 'blur(8px)' : 'none',
                          transition: 'filter 0.3s ease'
                        }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-white/80 via-transparent to-transparent pointer-events-none" />
                      
                      {/* Click to View Overlay */}
                      {isResumeBlurred && (
                        <div className="absolute inset-0 flex items-center justify-center bg-black/10 group-hover:bg-black/20 transition-colors">
                          <div className="bg-white/95 backdrop-blur-sm px-6 py-3 rounded-full shadow-lg border-2 border-purple-300 group-hover:border-purple-400 transition-all">
                            <p className="text-slate-800 font-semibold flex items-center gap-2">
                              <ExternalLink size={18} className="text-purple-600" />
                              Click to view resume
                            </p>
                          </div>
                        </div>
                      )}
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
                    </div>
                  </div>
                ) : (
                  <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl shadow-sm border-2 border-dashed border-slate-300 p-6 sticky top-4">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 bg-slate-200 rounded-lg flex items-center justify-center">
                        <FileText className="w-6 h-6 text-slate-400" />
                      </div>
                      <div className="flex-1">
                        <h4 className="font-semibold text-slate-800">Resume</h4>
                        <p className="text-sm text-slate-600">Not uploaded yet</p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <div className="flex items-center gap-2 text-amber-700 bg-amber-50 px-3 py-2 rounded-lg">
                        <AlertCircle size={16} />
                        <span className="text-sm font-medium">No resume available</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-12 text-center mb-8">
            <Code2 className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-slate-800 mb-2">No Platforms Connected</h3>
            <p className="text-slate-600">
              This user hasn't connected any coding platforms yet.
            </p>
          </div>
        )}
      </main>
    </div>
  );
};

export default PublicProfile;
