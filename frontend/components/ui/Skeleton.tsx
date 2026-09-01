'use client';

import styles from './Skeleton.module.css';

interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  borderRadius?: string;
  className?: string;
  count?: number;
}

export function Skeleton({ width = '100%', height = 16, borderRadius, className = '' }: SkeletonProps) {
  return (
    <div
      className={[styles.skeleton, className].join(' ')}
      style={{
        width,
        height,
        borderRadius: borderRadius ?? 'var(--radius-md)',
      }}
      aria-hidden="true"
    />
  );
}

export function CardSkeleton() {
  return (
    <div className={[styles.card, 'neo-card'].join(' ')}>
      <Skeleton width="60%" height={14} />
      <Skeleton width="100%" height={36} />
      <Skeleton width="40%" height={12} />
    </div>
  );
}

export function TableRowSkeleton({ cols = 5 }: { cols?: number }) {
  return (
    <tr className={styles.tableRow}>
      {Array.from({ length: cols }).map((_, i) => (
        <td key={i} style={{ padding: '14px 16px' }}>
          <Skeleton height={14} width={i === 0 ? '80%' : '60%'} />
        </td>
      ))}
    </tr>
  );
}
