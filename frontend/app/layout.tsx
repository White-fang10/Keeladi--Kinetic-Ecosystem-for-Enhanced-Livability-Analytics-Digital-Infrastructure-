/**
 * KEELADI — Root App Layout
 * Sets dark theme, Providers, font variables, and global toast
 */
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Providers from './providers';
import OfflineDetector from '@/components/layout/OfflineDetector';
import './globals.css';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

export const metadata: Metadata = {
  title: 'KEELADI | Kinetic Ecosystem for Enhanced Livability',
  description: 'Smart Civic Operations Platform',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.variable}>
        <Providers>
          {children}
          <OfflineDetector />
        </Providers>
      </body>
    </html>
  );
}
