'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/stores/authStore';

function AuthHydrator({ children }: { children: React.ReactNode }) {
  const hydrate = useAuthStore((s) => s.hydrate);

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return <>{children}</>;
}

export default function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      <AuthHydrator>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: 'var(--glass-bg)',
              backdropFilter: 'blur(16px)',
              border: '1px solid var(--glass-border)',
              color: 'var(--text-primary)',
              borderRadius: 'var(--radius-lg)',
              boxShadow: 'var(--neo-shadow)',
              fontFamily: 'var(--font-sans)',
              fontSize: '0.9rem',
            },
            success: {
              iconTheme: { primary: '#E6FF2B', secondary: '#0B4550' },
            },
            error: {
              iconTheme: { primary: '#ff7b7b', secondary: '#0B4550' },
            },
          }}
        />
      </AuthHydrator>
    </QueryClientProvider>
  );
}
