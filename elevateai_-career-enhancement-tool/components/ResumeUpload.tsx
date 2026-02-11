import React, { useState } from 'react';
import { Upload, FileText, X, CheckCircle2, AlertCircle, File } from 'lucide-react';

interface ResumeUploadProps {
  onUpload: (file: File) => void;
  onRemove: () => void;
  uploadedFile: File | null;
  error?: string;
}

const ResumeUpload: React.FC<ResumeUploadProps> = ({ 
  onUpload, 
  onRemove, 
  uploadedFile,
  error 
}) => {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateFile = (file: File): string | null => {
    // Check file type
    const validTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      return 'Please upload PDF or image files only (PDF, JPG, PNG, WEBP)';
    }

    // Check file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      return 'File size must be less than 10MB';
    }

    return null;
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      const error = validateFile(file);
      if (!error) {
        onUpload(file);
      } else {
        alert(error);
      }
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const error = validateFile(file);
      if (!error) {
        onUpload(file);
      } else {
        alert(error);
      }
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  return (
    <div>
      {!uploadedFile ? (
        <div
          className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all ${
            dragActive 
              ? 'border-blue-500 bg-blue-50' 
              : error
              ? 'border-red-300 bg-red-50'
              : 'border-slate-200 bg-slate-50 hover:border-blue-300'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept=".pdf,.jpg,.jpeg,.png,.webp"
            onChange={handleChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          <Upload className={`mx-auto mb-4 ${error ? 'text-red-400' : 'text-slate-400'}`} size={40} />
          <p className="text-sm font-semibold text-slate-700 mb-1">
            Drop your resume here or click to browse
          </p>
          <p className="text-xs text-slate-500 mb-2">
            Supports PDF and Images (JPG, PNG, WEBP)
          </p>
          <p className="text-xs text-slate-400">
            Max file size: 10MB
          </p>
          {error && (
            <div className="mt-3 flex items-center justify-center gap-2 text-red-600 text-xs">
              <AlertCircle size={14} />
              <span>{error}</span>
            </div>
          )}
        </div>
      ) : (
        <div className="flex items-center justify-between p-4 bg-emerald-50 border border-emerald-200 rounded-xl">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-emerald-100 rounded-lg">
              {uploadedFile.type === 'application/pdf' ? (
                <FileText className="text-emerald-600" size={20} />
              ) : (
                <File className="text-emerald-600" size={20} />
              )}
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-900">{uploadedFile.name}</p>
              <p className="text-xs text-slate-500">
                {formatFileSize(uploadedFile.size)} • {uploadedFile.type.split('/')[1].toUpperCase()}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="text-emerald-600" size={20} />
            <button
              onClick={onRemove}
              className="p-1 hover:bg-emerald-100 rounded-lg transition-colors"
              title="Remove file"
            >
              <X className="text-slate-500" size={18} />
            </button>
          </div>
        </div>
      )}
      
      <div className="mt-3 text-xs text-slate-500">
        <p className="font-semibold mb-1">✨ What we'll analyze:</p>
        <ul className="space-y-1 ml-4">
          <li>• Content quality and structure</li>
          <li>• ATS (Applicant Tracking System) compatibility</li>
          <li>• Skills and experience extraction</li>
          <li>• Keyword optimization score</li>
        </ul>
      </div>
    </div>
  );
};

export default ResumeUpload;
