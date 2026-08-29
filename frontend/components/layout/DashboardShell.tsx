'use client';

import React, { useState } from 'react';
import Sidebar from './Sidebar';
import TopNav from './TopNav';
import styles from './DashboardShell.module.css';

export default function DashboardShell({ children }: { children: React.ReactNode }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className={[styles.shell, isSidebarOpen ? 'sidebar-open' : ''].join(' ')}>
      <Sidebar />
      
      {/* Mobile overlay */}
      {isSidebarOpen && (
        <div className={styles.overlay} onClick={() => setIsSidebarOpen(false)} />
      )}

      <main className={styles.main}>
        <TopNav onMenuClick={() => setIsSidebarOpen(true)} />
        <div className={styles.content}>
          <div className="animate-fade-in">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
