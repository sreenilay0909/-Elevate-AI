import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Github, Code2, Award, Trophy, Briefcase, FileText, ExternalLink, Save, Loader2, Upload, File, X, CheckCircle, Camera, Image as ImageIcon } from 'lucide-react';
import profileService, { ProfileData, ProfileUpdateData } from '../services/profileService';
import { SORTED_SKILLS } from '../data/skills';

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
  
  // Profile picture state
  const [uploadingProfilePic, setUploadingProfilePic] = useState(false);
  const [profilePicFile, setProfilePicFile] = useState<File | null>(null);
  const profilePicInputRef = useRef<HTMLInputElement>(null);
  
  // Skills state
  const [skillInput, setSkillInput] = useState('');
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [filteredSkills, setFilteredSkills] = useState<string[]>([]);
  const [showSkillsDropdown, setShowSkillsDropdown] = useState(false);
  const skillsInputRef = useRef<HTMLInputElement>(null);
  
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
    // Personal Information
    fullName: '',
    gender: '',
    contactNumber: '',
    bio: '',
    // Education
    collegeName: '',
    degree: '',
    fieldOfStudy: '',
    currentYear: '',
    graduationYear: undefined,
    // Skills
    skills: '',
  });

  useEffect(() => {
    loadProfile();
    
    // Close skills dropdown when clicking outside
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (skillsInputRef.current && !skillsInputRef.current.contains(target)) {
        setShowSkillsDropdown(false);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
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
        // Personal Information
        fullName: data.fullName || '',
        gender: data.gender || '',
        contactNumber: data.contactNumber || '',
        bio: data.bio || '',
        // Education
        collegeName: data.collegeName || '',
        degree: data.degree || '',
        fieldOfStudy: data.fieldOfStudy || '',
        currentYear: data.currentYear || '',
        graduationYear: data.graduationYear || undefined,
        // Skills - will be managed separately
        skills: '',
      });
      
      // Parse skills into array
      if (data.skills) {
        setSelectedSkills(data.skills.split(',').map(s => s.trim()).filter(s => s));
      }
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
      // Combine form data with skills
      const dataToSubmit = {
        ...formData,
        skills: selectedSkills.join(', ')
      };
      
      await profileService.updateMyProfile(dataToSubmit);
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

  // Skills handlers
  const handleSkillInputChange = (value: string) => {
    setSkillInput(value);
    
    if (value.trim()) {
      const filtered = SORTED_SKILLS.filter(skill =>
        skill.toLowerCase().includes(value.toLowerCase()) &&
        !selectedSkills.includes(skill)
      ).slice(0, 10); // Show top 10 matches
      setFilteredSkills(filtered);
      setShowSkillsDropdown(true);
    } else {
      setFilteredSkills([]);
      setShowSkillsDropdown(false);
    }
  };

  const handleSkillSelect = (skill: string) => {
    if (!selectedSkills.includes(skill)) {
      setSelectedSkills([...selectedSkills, skill]);
    }
    setSkillInput('');
    setFilteredSkills([]);
    setShowSkillsDropdown(false);
    skillsInputRef.current?.focus();
  };

  const handleSkillRemove = (skillToRemove: string) => {
    setSelectedSkills(selectedSkills.filter(skill => skill !== skillToRemove));
  };

  const handleSkillKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const trimmedInput = skillInput.trim();
      
      if (trimmedInput && !selectedSkills.includes(trimmedInput)) {
        setSelectedSkills([...selectedSkills, trimmedInput]);
        setSkillInput('');
        setFilteredSkills([]);
        setShowSkillsDropdown(false);
      }
    } else if (e.key === 'Backspace' && !skillInput && selectedSkills.length > 0) {
      // Remove last skill if backspace is pressed with empty input
      setSelectedSkills(selectedSkills.slice(0, -1));
    }
  };

  // Profile picture handlers
  const handleProfilePicSelect = (file: File) => {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      setError('Only image files (JPG, PNG, GIF, WEBP) are allowed');
      return;
    }
    if (file.size > 2 * 1024 * 1024) {
      setError('Image size must be less than 2MB');
      return;
    }
    setProfilePicFile(file);
    setError('');
  };

  const handleProfilePicInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleProfilePicSelect(e.target.files[0]);
    }
  };

  const handleUploadProfilePic = async () => {
    if (!profilePicFile) return;

    setUploadingProfilePic(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', profilePicFile);

      const response = await fetch('http://127.0.0.1:8000/api/v1/profiles/upload-profile-picture', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      setSuccess('Profile picture uploaded successfully!');
      setProfilePicFile(null);
      await loadProfile();
    } catch (err: any) {
      setError(err.message || 'Failed to upload profile picture');
    } finally {
      setUploadingProfilePic(false);
    }
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
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
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
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
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
            {/* Personal Information Section */}
            <div className="border-b border-slate-200 pb-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <User className="w-5 h-5" />
                Personal Information
              </h3>
              
              <div className="space-y-4">
                {/* Full Name */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    value={formData.fullName}
                    onChange={(e) => handleChange('fullName', e.target.value)}
                    placeholder="Enter your full name"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Gender */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Gender
                  </label>
                  <select
                    value={formData.gender}
                    onChange={(e) => handleChange('gender', e.target.value)}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                  </select>
                </div>

                {/* Contact Number */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Contact Number
                  </label>
                  <input
                    type="tel"
                    value={formData.contactNumber}
                    onChange={(e) => handleChange('contactNumber', e.target.value)}
                    placeholder="+1 (555) 123-4567"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Bio */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Bio / Self Introduction
                  </label>
                  <textarea
                    value={formData.bio}
                    onChange={(e) => handleChange('bio', e.target.value)}
                    placeholder="Tell us about yourself..."
                    rows={4}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  />
                  <p className="text-xs text-slate-500 mt-1">
                    {formData.bio?.length || 0} / 1000 characters
                  </p>
                </div>
              </div>
            </div>

            {/* Education Section */}
            <div className="border-b border-slate-200 pb-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <Award className="w-5 h-5" />
                Education
              </h3>
              
              <div className="space-y-4">
                {/* College Name */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    College / University Name
                  </label>
                  <input
                    type="text"
                    value={formData.collegeName}
                    onChange={(e) => handleChange('collegeName', e.target.value)}
                    placeholder="e.g., Massachusetts Institute of Technology"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Degree */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Degree
                  </label>
                  <select
                    value={formData.degree}
                    onChange={(e) => handleChange('degree', e.target.value)}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select degree</option>
                    <option value="Bachelor's">Bachelor's</option>
                    <option value="Master's">Master's</option>
                    <option value="PhD">PhD</option>
                    <option value="Associate">Associate</option>
                    <option value="Diploma">Diploma</option>
                  </select>
                </div>

                {/* Field of Study */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Field of Study / Major
                  </label>
                  <input
                    type="text"
                    value={formData.fieldOfStudy}
                    onChange={(e) => handleChange('fieldOfStudy', e.target.value)}
                    placeholder="e.g., Computer Science, Software Engineering"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Current Year */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Current Year
                    </label>
                    <select
                      value={formData.currentYear}
                      onChange={(e) => handleChange('currentYear', e.target.value)}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Select year</option>
                      <option value="1st Year">1st Year</option>
                      <option value="2nd Year">2nd Year</option>
                      <option value="3rd Year">3rd Year</option>
                      <option value="4th Year">4th Year</option>
                      <option value="Final Year">Final Year</option>
                      <option value="Graduated">Graduated</option>
                    </select>
                  </div>

                  {/* Graduation Year */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Graduation Year
                    </label>
                    <input
                      type="number"
                      value={formData.graduationYear || ''}
                      onChange={(e) => handleChange('graduationYear', e.target.value)}
                      placeholder="2025"
                      min="1950"
                      max="2050"
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Skills Section */}
            <div className="border-b border-slate-200 pb-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <Code2 className="w-5 h-5" />
                Skills & Technologies
              </h3>
              
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Add Skills (Press Enter or select from dropdown)
                </label>
                
                {/* Selected Skills Tags */}
                <div className="flex flex-wrap gap-2 mb-3 min-h-[40px] p-2 border border-slate-300 rounded-lg bg-slate-50">
                  {selectedSkills.map((skill, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
                    >
                      {skill}
                      <button
                        type="button"
                        onClick={() => handleSkillRemove(skill)}
                        className="hover:bg-blue-200 rounded-full p-0.5 transition-colors"
                      >
                        <X size={14} />
                      </button>
                    </span>
                  ))}
                  {selectedSkills.length === 0 && (
                    <span className="text-slate-400 text-sm">No skills added yet</span>
                  )}
                </div>
                
                {/* Skills Input with Autocomplete */}
                <div className="relative">
                  <input
                    ref={skillsInputRef}
                    type="text"
                    value={skillInput}
                    onChange={(e) => handleSkillInputChange(e.target.value)}
                    onKeyDown={handleSkillKeyDown}
                    onFocus={() => skillInput && setShowSkillsDropdown(true)}
                    placeholder="Type to search skills (e.g., JavaScript, Python, React)..."
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  
                  {/* Autocomplete Dropdown */}
                  {showSkillsDropdown && filteredSkills.length > 0 && (
                    <div className="absolute z-10 w-full mt-1 bg-white border border-slate-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                      {filteredSkills.map((skill, index) => (
                        <button
                          key={index}
                          type="button"
                          onClick={() => handleSkillSelect(skill)}
                          className="w-full px-4 py-2 text-left hover:bg-blue-50 transition-colors border-b border-slate-100 last:border-b-0"
                        >
                          <span className="text-slate-900">{skill}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                
                <p className="text-xs text-slate-500 mt-2">
                  Type and press Enter to add custom skills, or select from suggestions. {selectedSkills.length} skill(s) added.
                </p>
              </div>
            </div>

            {/* Profile Picture Section */}
            <div className="border-b border-slate-200 pb-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <Camera className="w-5 h-5" />
                Profile Picture
              </h3>
              
              {/* Current Profile Picture */}
              {profile?.profilePictureUrl && (
                <div className="mb-4 flex items-center gap-4">
                  <img
                    src={`http://127.0.0.1:8000${profile.profilePictureUrl}`}
                    alt="Profile"
                    className="w-24 h-24 rounded-full object-cover border-4 border-blue-200"
                  />
                  <div>
                    <p className="text-sm font-medium text-slate-700">Current profile picture</p>
                    <p className="text-xs text-slate-500">Upload a new one to replace it</p>
                  </div>
                </div>
              )}

              {/* Upload New Profile Picture */}
              <div className="space-y-3">
                <input
                  ref={profilePicInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleProfilePicInputChange}
                  className="hidden"
                />

                {!profilePicFile ? (
                  <button
                    type="button"
                    onClick={() => profilePicInputRef.current?.click()}
                    className="w-full px-4 py-3 border-2 border-dashed border-slate-300 rounded-lg hover:border-blue-400 transition-colors flex items-center justify-center gap-2 text-slate-600 hover:text-blue-600"
                  >
                    <ImageIcon className="w-5 h-5" />
                    Choose Profile Picture
                  </button>
                ) : (
                  <div className="space-y-3">
                    <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                      <ImageIcon className="w-8 h-8 text-blue-600" />
                      <div className="flex-1">
                        <p className="font-medium text-slate-900">{profilePicFile.name}</p>
                        <p className="text-sm text-slate-500">
                          {(profilePicFile.size / 1024).toFixed(2)} KB
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() => setProfilePicFile(null)}
                        className="p-1 hover:bg-blue-100 rounded transition-colors"
                      >
                        <X className="w-5 h-5 text-slate-600" />
                      </button>
                    </div>
                    <button
                      type="button"
                      onClick={handleUploadProfilePic}
                      disabled={uploadingProfilePic}
                      className="w-full py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      {uploadingProfilePic ? (
                        <>
                          <Loader2 className="w-5 h-5 animate-spin" />
                          Uploading...
                        </>
                      ) : (
                        <>
                          <Upload className="w-5 h-5" />
                          Upload Profile Picture
                        </>
                      )}
                    </button>
                  </div>
                )}
                
                <p className="text-xs text-slate-500">
                  Supported: JPG, PNG, GIF, WEBP (max 2MB)
                </p>
              </div>
            </div>

            {/* Platform Usernames Section */}
            <div className="border-b border-slate-200 pb-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <Github className="w-5 h-5" />
                Platform Usernames
              </h3>
              
              <div className="space-y-4">
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
              </div>
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
