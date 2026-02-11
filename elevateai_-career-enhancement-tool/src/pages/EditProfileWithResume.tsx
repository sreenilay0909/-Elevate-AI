import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Github, Code2, Award, Trophy, Briefcase, FileText, ExternalLink, Save, Loader2, Upload, File, X, CheckCircle } from 'lucide-react';
import profileService, { ProfileData, ProfileUpdateData } from '../services/profileService';

const EditProfile: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [uploadingResume, setUploadingResume] = useState(false);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [profile, setProfile] = useState<ProfileData | null>(null);
  
  const [formData, setFormData] = useState<ProfileUpdateData>({
    githubUsername: '',
    leetcodeUsername: '',
    geeksforgeeksUsername: '',
    codechefUsername: '',
    hackerrankUsername: '',
    devpostUsername: '',
    devtoUsername: '',
    linkedinUrl: '',
    portfolioUrl: '',
  });

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await profileService.getMyProfile();
      setProfile(data);
      setFormData({
        githubUsername: data.githubUsername || '',
        leetcodeUsername: data.leetcodeUsername || '',
        geeksforgeeksUsername: data.geeksforgeeksUsername || '',
        codechefUsername: data.codechefUsername || '',
        hackerrankUsername: data.hackerrankUsername || '',
        devpostUsername: data.devpostUsername || '',
        devtoUsername: data.devtoUsername || '',
        linkedinUrl: data.linkedinUrl || '',
        portfolioUrl: data.portfolioUrl || '',
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setSaving(true);

    try {
      await profileService.updateMyProfile(formData);
      setSuccess('Profile updated successfully!');
      setTimeout(() => {
        navigate('/dashboard');
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field: keyof ProfileUpdateData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  // Resume upload handlers
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (file: File) => {
    if (file.type !== 'application/pdf') {
      setError('Only PDF files are allowed');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }
    setResumeFile(file);
    setError('');
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleUploadResume = async () => {
    if (!resumeFile) return;

    setUploadingResume(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', resumeFile);

      const response = await fetch('http://127.0.0.1:8000/api/v1/profiles/upload-resume', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      setSuccess('Resume uploaded successfully!');
      setResumeFile(null);
      await loadProfile();
    } catch (err: any) {
      setError(err.message || 'Failed to upload resume');
    } finally {
      setUploadingResume(false);
    }
  };

  const handleDeleteResume = async () => {
    if (!confirm('Are you sure you want to delete your resume?')) return;

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/profiles/delete-resume', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Delete failed');
      }

      setSuccess('Resume deleted successfully!');
      await loadProfile();
    } catch (err: any) {
      setError(err.message || 'Failed to delete resume');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-slate-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-slate-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-slate-800 mb-2">Edit Profile</h1>
            <p className="text-slate-600">Update your platform usernames and portfolio information</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700">
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* GitHub */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <Github className="w-4 h-4 inline mr-2" />
                GitHub Username
              </label>
              <input
                type="text"
                value={formData.githubUsername}
                onChange={(e) => handleChange('githubUsername', e.target.value)}
                placeholder="octocat"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* LeetCode */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <Code2 className="w-4 h-4 inline mr-2" />
                LeetCode Username
              </label>
              <input
                type="text"
                value={formData.leetcodeUsername}
                onChange={(e) => handleChange('leetcodeUsername', e.target.value)}
                placeholder="username"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* GeeksforGeeks */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <Award className="w-4 h-4 inline mr-2" />
                GeeksforGeeks Username
              </label>
              <input
                type="text"
                value={formData.geeksforgeeksUsername}
                onChange={(e) => handleChange('geeksforgeeksUsername', e.target.value)}
                placeholder="username"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* CodeChef */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <Trophy className="w-4 h-4 inline mr-2" />
                CodeChef Username
              </label>
              <input
                type="text"
                value={formData.codechefUsername}
                onChange={(e) => handleChange('codechefUsername', e.target.value)}
                placeholder="username"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* HackerRank */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <Code2 className="w-4 h-4 inline mr-2" />
                HackerRank Username
              </label>
              <input
                type="text"
                value={formData.hackerrankUsername}
                onChange={(e) => handleChange('hackerrankUsername', e.target.value)}
                placeholder="username"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* DevPost */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <Briefcase className="w-4 h-4 inline mr-2" />
                DevPost Username
              </label>
              <input
                type="text"
                value={formData.devpostUsername}
                onChange={(e) => handleChange('devpostUsername', e.target.value)}
                placeholder="username"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Dev.to */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <FileText className="w-4 h-4 inline mr-2" />
                Dev.to Username
              </label>
              <input
                type="text"
                value={formData.devtoUsername}
                onChange={(e) => handleChange('devtoUsername', e.target.value)}
                placeholder="username"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* LinkedIn */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <ExternalLink className="w-4 h-4 inline mr-2" />
                LinkedIn Profile URL
              </label>
              <input
                type="url"
                value={formData.linkedinUrl}
                onChange={(e) => handleChange('linkedinUrl', e.target.value)}
                placeholder="https://www.linkedin.com/in/username"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Portfolio URL */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                <ExternalLink className="w-4 h-4 inline mr-2" />
                Portfolio URL
              </label>
              <input
                type="url"
                value={formData.portfolioUrl}
                onChange={(e) => handleChange('portfolioUrl', e.target.value)}
                placeholder="https://yourportfolio.com"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Resume Upload Section */}
            <div className="border-t border-slate-200 pt-6 mt-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Resume
              </h3>
              
              {/* Current Resume */}
              {profile?.resumeUrl && (
                <div className="mb-4 p-4 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl animate-fadeIn">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-green-100 rounded-lg">
                        <CheckCircle className="w-6 h-6 text-green-600" />
                      </div>
                      <div>
                        <p className="font-semibold text-green-900">Resume Uploaded</p>
                        <p className="text-sm text-green-700">Your resume is available for viewing</p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <a
                        href={`http://127.0.0.1:8000${profile.resumeUrl}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all hover:scale-105 font-medium shadow-sm"
                      >
                        View Resume
                      </a>
                      <button
                        type="button"
                        onClick={handleDeleteResume}
                        className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all hover:scale-105 font-medium shadow-sm"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Upload New Resume */}
              <div
                className={`relative border-2 border-dashed rounded-xl p-8 transition-all duration-300 ${
                  dragActive
                    ? 'border-blue-500 bg-blue-50 scale-105 shadow-lg'
                    : 'border-slate-300 bg-gradient-to-br from-slate-50 to-slate-100 hover:border-blue-400'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf"
                  onChange={handleFileInputChange}
                  className="hidden"
                />

                {!resumeFile ? (
                  <div className="text-center">
                    <div className="inline-block p-4 bg-blue-100 rounded-full mb-4 animate-bounce">
                      <Upload className="w-8 h-8 text-blue-600" />
                    </div>
                    <p className="text-lg font-semibold text-slate-700 mb-2">
                      Drop your resume here or click to browse
                    </p>
                    <p className="text-sm text-slate-500 mb-4">
                      PDF only, max 5MB
                    </p>
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all hover:scale-105 font-medium shadow-md"
                    >
                      Choose File
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4 animate-fadeIn">
                    <div className="flex items-center justify-between p-4 bg-white rounded-lg border-2 border-blue-200 shadow-sm">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <File className="w-8 h-8 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-semibold text-slate-900">{resumeFile.name}</p>
                          <p className="text-sm text-slate-500">
                            {(resumeFile.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </div>
                      <button
                        type="button"
                        onClick={() => setResumeFile(null)}
                        className="p-2 hover:bg-red-50 rounded-lg transition-colors group"
                      >
                        <X className="w-5 h-5 text-slate-600 group-hover:text-red-600" />
                      </button>
                    </div>
                    <button
                      type="button"
                      onClick={handleUploadResume}
                      disabled={uploadingResume}
                      className="w-full py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg font-semibold hover:from-green-700 hover:to-emerald-700 transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2 shadow-md"
                    >
                      {uploadingResume ? (
                        <>
                          <Loader2 className="w-5 h-5 animate-spin" />
                          Uploading...
                        </>
                      ) : (
                        <>
                          <Upload className="w-5 h-5" />
                          Upload Resume
                        </>
                      )}
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Buttons */}
            <div className="flex gap-4 pt-4">
              <button
                type="submit"
                disabled={saving}
                className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2 shadow-md"
              >
                {saving ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Saving...
                  </>
                ) : (
                  <>
                    <Save className="w-5 h-5" />
                    Save Changes
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={() => navigate('/dashboard')}
                className="px-8 py-3 border-2 border-slate-300 text-slate-700 rounded-lg font-semibold hover:bg-slate-50 transition-all hover:scale-105 shadow-sm"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default EditProfile;
