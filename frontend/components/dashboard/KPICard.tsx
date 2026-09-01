'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';
import Card from '@/components/ui/Card';
import { Skeleton } from '@/components/ui/Skeleton';
import styles from './KPICard.module.css';

interface KPICardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  isLoading?: boolean;
}

export default function KPICard({ title, value, icon: Icon, trend, isLoading }: KPICardProps) {
  return (
    <Card padding="lg" className={styles.kpiCard}>
      <div className={styles.header}>
        <span className={styles.title}>{title}</span>
        <div className={styles.iconWrapper}>
          <Icon size={18} />
        </div>
      </div>
      
      <div className={styles.body}>
        {isLoading ? (
          <Skeleton width={80} height={36} />
        ) : (
          <span className={styles.value}>{value}</span>
        )}
      </div>

      {trend && !isLoading && (
        <div className={styles.footer}>
          <span className={[styles.trend, trend.isPositive ? styles.positive : styles.negative].join(' ')}>
            {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
          </span>
          <span className={styles.trendLabel}>vs last week</span>
        </div>
      )}
    </Card>
  );
}
