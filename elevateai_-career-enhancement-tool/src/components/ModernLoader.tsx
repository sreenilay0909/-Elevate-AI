import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface ModernLoaderProps {
  message?: string;
  variant?: 'dots' | 'pulse' | 'orbit' | 'wave' | 'gradient';
  size?: 'sm' | 'md' | 'lg';
  rotatingMessages?: string[];
}

const ModernLoader: React.FC<ModernLoaderProps> = ({ 
  message = 'Loading...', 
  variant = 'orbit',
  size = 'md',
  rotatingMessages
}) => {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [displayMessage, setDisplayMessage] = useState(message);

  useEffect(() => {
    if (rotatingMessages && rotatingMessages.length > 0) {
      setDisplayMessage(rotatingMessages[0]);
      
      const interval = setInterval(() => {
        setCurrentMessageIndex((prev) => (prev + 1) % rotatingMessages.length);
      }, 2000);

      return () => clearInterval(interval);
    }
  }, [rotatingMessages]);

  useEffect(() => {
    if (rotatingMessages && rotatingMessages.length > 0) {
      setDisplayMessage(rotatingMessages[currentMessageIndex]);
    }
  }, [currentMessageIndex, rotatingMessages]);
  const sizeClasses = {
    sm: 'w-12 h-12',
    md: 'w-20 h-20',
    lg: 'w-32 h-32'
  };

  const renderLoader = () => {
    switch (variant) {
      case 'dots':
        return (
          <div className="flex space-x-2">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-4 h-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"
                animate={{
                  y: [0, -20, 0],
                  scale: [1, 1.2, 1],
                }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  delay: i * 0.15,
                }}
              />
            ))}
          </div>
        );

      case 'pulse':
        return (
          <div className="relative">
            <motion.div
              className={`${sizeClasses[size]} rounded-full bg-gradient-to-r from-blue-500 to-purple-600`}
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.7, 1, 0.7],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
            <motion.div
              className={`absolute inset-0 ${sizeClasses[size]} rounded-full border-4 border-blue-500`}
              animate={{
                scale: [1, 1.5, 1],
                opacity: [1, 0, 1],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
          </div>
        );

      case 'orbit':
        return (
          <div className={`relative ${sizeClasses[size]}`}>
            <motion.div
              className="absolute inset-0"
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <div className="w-3 h-3 bg-blue-500 rounded-full absolute top-0 left-1/2 transform -translate-x-1/2" />
            </motion.div>
            <motion.div
              className="absolute inset-0"
              animate={{ rotate: -360 }}
              transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
            >
              <div className="w-3 h-3 bg-purple-500 rounded-full absolute bottom-0 left-1/2 transform -translate-x-1/2" />
            </motion.div>
            <motion.div
              className="absolute inset-0"
              animate={{ rotate: 360 }}
              transition={{ duration: 2.5, repeat: Infinity, ease: "linear" }}
            >
              <div className="w-3 h-3 bg-pink-500 rounded-full absolute left-0 top-1/2 transform -translate-y-1/2" />
            </motion.div>
            <div className="absolute inset-0 flex items-center justify-center">
              <motion.div
                className="w-4 h-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"
                animate={{
                  scale: [1, 1.3, 1],
                }}
                transition={{
                  duration: 1,
                  repeat: Infinity,
                }}
              />
            </div>
          </div>
        );

      case 'wave':
        return (
          <div className="flex space-x-1">
            {[0, 1, 2, 3, 4].map((i) => (
              <motion.div
                key={i}
                className="w-2 bg-gradient-to-t from-blue-500 to-purple-600 rounded-full"
                animate={{
                  height: [20, 40, 20],
                }}
                transition={{
                  duration: 0.8,
                  repeat: Infinity,
                  delay: i * 0.1,
                }}
              />
            ))}
          </div>
        );

      case 'gradient':
        return (
          <div className="relative">
            <motion.div
              className={`${sizeClasses[size]} rounded-full`}
              style={{
                background: 'conic-gradient(from 0deg, #3B82F6, #8B5CF6, #EC4899, #3B82F6)',
              }}
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            />
            <div className={`absolute inset-2 bg-white rounded-full`} />
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col items-center justify-center space-y-6"
    >
      {renderLoader()}
      {(displayMessage || message) && (
        <div className="h-8 flex items-center justify-center">
          <AnimatePresence mode="wait">
            <motion.p
              key={displayMessage}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="text-gray-600 font-medium text-center text-lg"
            >
              {displayMessage}
            </motion.p>
          </AnimatePresence>
        </div>
      )}
    </motion.div>
  );
};

export default ModernLoader;
