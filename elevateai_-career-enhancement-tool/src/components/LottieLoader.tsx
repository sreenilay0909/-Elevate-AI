import React from 'react';
import { Player } from '@lottiefiles/react-lottie-player';
import { motion } from 'framer-motion';

interface LottieLoaderProps {
  message?: string;
  size?: number;
  className?: string;
}

const LottieLoader: React.FC<LottieLoaderProps> = ({ 
  message = 'Loading...', 
  size = 200,
  className = ''
}) => {
  return (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Player
          autoplay
          loop
          src="/src/assets/paperplane-loader.lottie"
          style={{ height: `${size}px`, width: `${size}px` }}
        />
      </motion.div>
      {message && (
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-4 text-gray-600 font-medium text-center"
        >
          {message}
        </motion.p>
      )}
    </div>
  );
};

export default LottieLoader;
