'use client';

import React from 'react';
import { useAuthStore } from '@/stores/authStore';
import { LogOut, Menu, User, Bell } from 'lucide-react';
import styles from './TopNav.module.css';

export default function TopNav({ onMenuClick }: { onMenuClick: () => void }) {
  const { user, logout } = useAuthStore();

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <button className={styles.menuBtn} onClick={onMenuClick} aria-label="Toggle menu">
          <Menu size={24} />
        </button>
        {/* We can put a breadcrumb or page title here eventually */}
      </div>

      <div className={styles.right}>
        <button className={styles.iconBtn} aria-label="Notifications">
          <Bell size={20} />
          <span className={styles.badge}></span>
        </button>

        <div className={styles.userProfile}>
          <div className={styles.avatar}>
            <User size={18} />
          </div>
          <div className={styles.userInfo}>
            <span className={styles.userName}>{user?.full_name}</span>
            <span className={styles.userRole}>{user?.role.replace('_', ' ')}</span>
          </div>
        </div>

        <button className={styles.logoutBtn} onClick={logout} title="Logout">
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
}
