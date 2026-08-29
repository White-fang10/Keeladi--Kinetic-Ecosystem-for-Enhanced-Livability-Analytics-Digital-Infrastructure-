'use client';

import styles from './Badge.module.css';

type BadgeVariant = 'default' | 'accent' | 'success' | 'warning' | 'danger' | 'info' | 'muted';

const STATUS_MAP: Record<string, BadgeVariant> = {
  NEW: 'info',
  ASSIGNED: 'accent',
  IN_PROGRESS: 'warning',
  VERIFICATION: 'warning',
  RESOLVED: 'success',
  REJECTED: 'danger',
  ESCALATED: 'danger',
  AVAILABLE: 'success',
  COLLECTING: 'warning',
  FULL: 'danger',
  MAINTENANCE: 'muted',
  IDLE: 'muted',
  COMPLETED: 'success',
  STARTED: 'warning',
  REASSIGNED: 'info',
  ACTIVE: 'success',
  INACTIVE: 'muted',
  SUSPENDED: 'danger',
};

interface BadgeProps {
  label: string;
  variant?: BadgeVariant;
  dot?: boolean;
  className?: string;
}

export default function Badge({ label, variant, dot = false, className = '' }: BadgeProps) {
  const resolvedVariant = variant ?? STATUS_MAP[label.toUpperCase()] ?? 'default';

  return (
    <span className={[styles.badge, styles[resolvedVariant], className].join(' ')}>
      {dot && <span className={styles.dot} aria-hidden />}
      {label}
    </span>
  );
}
