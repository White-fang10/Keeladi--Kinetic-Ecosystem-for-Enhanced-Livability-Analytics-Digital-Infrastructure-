'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuthStore, ROLES } from '@/stores/authStore';
import Logo from '@/components/ui/Logo';
import {
  LayoutDashboard,
  Map as MapIcon,
  AlertTriangle,
  ClipboardList,
  Truck,
  CheckCircle,
  BarChart2,
  Sparkles,
  Bell,
  Settings,
} from 'lucide-react';
import styles from './Sidebar.module.css';

const NAV_ITEMS = [
  { label: 'Command Center', href: '/dashboard', icon: LayoutDashboard, roles: [ROLES.ADMIN, ROLES.CHIEF_ENGINEER, ROLES.EXECUTIVE_ENGINEER, ROLES.JUNIOR_ENGINEER, ROLES.SUPERVISOR] },
  { label: 'Live GIS Map', href: '/map', icon: MapIcon, roles: [ROLES.ADMIN, ROLES.CHIEF_ENGINEER, ROLES.EXECUTIVE_ENGINEER, ROLES.JUNIOR_ENGINEER, ROLES.SUPERVISOR] },
  { label: 'Analytics', href: '/analytics', icon: BarChart2, roles: [ROLES.ADMIN, ROLES.CHIEF_ENGINEER, ROLES.EXECUTIVE_ENGINEER, ROLES.JUNIOR_ENGINEER] },
  { label: 'AI Prediction', href: '/prediction', icon: Sparkles, roles: [ROLES.ADMIN, ROLES.CHIEF_ENGINEER, ROLES.EXECUTIVE_ENGINEER] },
  { label: 'My Complaints', href: '/complaints', icon: AlertTriangle, roles: [ROLES.CITIZEN] },
  { label: 'All Complaints', href: '/complaints', icon: AlertTriangle, roles: [ROLES.ADMIN, ROLES.CHIEF_ENGINEER, ROLES.EXECUTIVE_ENGINEER, ROLES.JUNIOR_ENGINEER, ROLES.SUPERVISOR] },
  { label: 'Task Force', href: '/tasks', icon: ClipboardList, roles: [ROLES.ADMIN, ROLES.CHIEF_ENGINEER, ROLES.EXECUTIVE_ENGINEER, ROLES.JUNIOR_ENGINEER, ROLES.SUPERVISOR, ROLES.SANITATION_WORKER] },
  { label: 'Fleet Tracker', href: '/fleet', icon: Truck, roles: [ROLES.ADMIN, ROLES.CHIEF_ENGINEER, ROLES.EXECUTIVE_ENGINEER, ROLES.DRIVER] },
  { label: 'Verification', href: '/verification', icon: CheckCircle, roles: [ROLES.ADMIN, ROLES.SUPERVISOR] },
];

export default function Sidebar() {
  const pathname = usePathname();
  const user = useAuthStore((s) => s.user);

  if (!user) return null;

  const allowedNavItems = NAV_ITEMS.filter((item) => (item.roles as string[]).includes(user.role));

  return (
    <aside className={styles.sidebar}>
      <div className={styles.logoContainer}>
        <Logo size={32} />
      </div>

      <nav className={styles.nav}>
        {allowedNavItems.map((item) => {
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.label}
              href={item.href}
              className={[styles.navItem, isActive ? styles.active : ''].join(' ')}
            >
              <item.icon size={20} className={styles.icon} />
              <span>{item.label}</span>
              {isActive && <div className={styles.activeGlow} />}
            </Link>
          );
        })}
      </nav>

      <div className={styles.bottomNav}>
        <Link href="/notifications" className={[styles.navItem, pathname.startsWith('/notifications') ? styles.active : ''].join(' ')}>
          <Bell size={20} className={styles.icon} />
          <span>Notifications</span>
        </Link>
        <Link href="/settings" className={[styles.navItem, pathname.startsWith('/settings') ? styles.active : ''].join(' ')}>
          <Settings size={20} className={styles.icon} />
          <span>Settings</span>
        </Link>
      </div>
    </aside>
  );
}
