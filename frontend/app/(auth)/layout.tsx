import React from 'react';
import styles from './layout.module.css';
import Logo from '@/components/ui/Logo';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className={styles.container}>
      {/* Left Panel — Branding (Hidden on mobile) */}
      <div className={styles.brandPanel}>
        <div className={styles.brandContent}>
          <Logo size={48} />
          <h1 className={styles.title}>
            Kinetic Ecosystem for Enhanced Livability, Analytics & Digital Infrastructure
          </h1>
          <p className={styles.subtitle}>
            A premium, AI-powered platform designed to optimize municipal waste management and civic operations through real-time GIS tracking and predictive analytics.
          </p>
          
          <div className={styles.decorativeElements}>
            <div className={styles.glowOrb} />
            <div className={styles.glassCard}>
              <div className={styles.statLabel}>Operations Handled</div>
              <div className={styles.statValue}>Real-Time</div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Panel — Form Area */}
      <div className={styles.formPanel}>
        <div className={styles.formContainer}>
          <div className={styles.mobileLogo}>
            <Logo size={40} />
          </div>
          {children}
        </div>
      </div>
    </div>
  );
}
