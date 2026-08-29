'use client';

import { useEffect } from 'react';
import toast from 'react-hot-toast';

export default function OfflineDetector() {
  useEffect(() => {
    const handleOnline = () => {
      toast.success('Connection restored. You are back online.', {
        id: 'offline-toast',
      });
    };

    const handleOffline = () => {
      toast.error('Network disconnected. Operating in offline mode.', {
        id: 'offline-toast',
        duration: Infinity, // Keep it visible until online
      });
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Check initial state just in case
    if (!navigator.onLine) {
      handleOffline();
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return null; // Component does not render any DOM directly
}
