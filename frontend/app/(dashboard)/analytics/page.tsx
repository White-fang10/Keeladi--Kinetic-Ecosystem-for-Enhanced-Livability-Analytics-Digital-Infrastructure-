'use client';

import React from 'react';
import dynamic from 'next/dynamic';
import { useQuery } from '@tanstack/react-query';
import { apiGet } from '@/lib/api';
import { useAuthStore, ROLES } from '@/stores/authStore';
import Card from '@/components/ui/Card';
import { Skeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

// Phase 11: Performance Optimization - Dynamic Imports for heavy charting libraries
const ResponsiveContainer = dynamic(() => import('recharts').then(mod => mod.ResponsiveContainer), { ssr: false });
const AreaChart = dynamic(() => import('recharts').then(mod => mod.AreaChart), { ssr: false });
const Area = dynamic(() => import('recharts').then(mod => mod.Area), { ssr: false });
const XAxis = dynamic(() => import('recharts').then(mod => mod.XAxis), { ssr: false });
const YAxis = dynamic(() => import('recharts').then(mod => mod.YAxis), { ssr: false });
const CartesianGrid = dynamic(() => import('recharts').then(mod => mod.CartesianGrid), { ssr: false });
const Tooltip = dynamic(() => import('recharts').then(mod => mod.Tooltip), { ssr: false });
const BarChart = dynamic(() => import('recharts').then(mod => mod.BarChart), { ssr: false });
const Bar = dynamic(() => import('recharts').then(mod => mod.Bar), { ssr: false });
const Legend = dynamic(() => import('recharts').then(mod => mod.Legend), { ssr: false });
const PieChart = dynamic(() => import('recharts').then(mod => mod.PieChart), { ssr: false });
const Pie = dynamic(() => import('recharts').then(mod => mod.Pie), { ssr: false });
const Cell = dynamic(() => import('recharts').then(mod => mod.Cell), { ssr: false });

// Mock data to gracefully handle missing backend endpoints while demonstrating Recharts capability
const DAILY_TREND_MOCK = [
  { day: 'Mon', new: 12, resolved: 10 },
  { day: 'Tue', new: 19, resolved: 14 },
  { day: 'Wed', new: 15, resolved: 18 },
  { day: 'Thu', new: 22, resolved: 20 },
  { day: 'Fri', new: 28, resolved: 25 },
  { day: 'Sat', new: 14, resolved: 22 },
  { day: 'Sun', new: 8, resolved: 15 },
];

const WARD_PERFORMANCE_MOCK = [
  { name: 'Ward 12', pending: 45, resolved: 120 },
  { name: 'Ward 14', pending: 30, resolved: 95 },
  { name: 'Ward 18', pending: 60, resolved: 150 },
  { name: 'Ward 22', pending: 25, resolved: 80 },
];

const WASTE_CATEGORIES = [
  { name: 'Waste Accumulation', value: 400, color: '#ff7b7b' },
  { name: 'Bin Overflow', value: 300, color: '#E6FF2B' },
  { name: 'Illegal Dumping', value: 200, color: '#50b4dc' },
  { name: 'Dead Animal', value: 50, color: '#6ddc6d' },
];

export default function AnalyticsPage() {
  const user = useAuthStore((s) => s.user);

  // Attempting to fetch live analytics data as per API Contract
  interface AnalyticsResponse {
    data?: {
      daily_trend?: { day: string; new: number; resolved: number }[];
      ward_performance?: { name: string; pending: number; resolved: number }[];
      category_distribution?: { name: string; value: number }[];
    };
  }
  const { data: analyticsData, isLoading } = useQuery<AnalyticsResponse>({
    queryKey: ['analytics', 'complaints'],
    queryFn: () => apiGet('/analytics/complaints'),
    retry: false, // Fallback to mock data gracefully since it's not implemented on backend
  });

  if (user?.role === ROLES.CITIZEN || user?.role === ROLES.SANITATION_WORKER) {
    return <div>Access Denied. Officer clearance required.</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Analytics & Reports</h1>
        <p className={styles.subtitle}>
          Data-driven insights into civic operations, complaint resolution, and resource allocation.
        </p>
      </div>

      <div className={styles.grid}>
        
        {/* Daily Reports Chart - Area Chart */}
        <Card className={styles.chartCard}>
          <div className={styles.cardHeader}>
            <h3>Daily Complaint Resolution (Last 7 Days)</h3>
          </div>
          <div className={styles.chartWrapper}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={analyticsData?.data?.daily_trend || DAILY_TREND_MOCK}>
                <defs>
                  <linearGradient id="colorNew" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ff7b7b" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ff7b7b" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorResolved" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#E6FF2B" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#E6FF2B" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                <XAxis dataKey="day" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--glass-bg)', borderColor: 'var(--glass-border)', borderRadius: '8px', color: 'var(--text-primary)' }}
                  itemStyle={{ color: 'var(--text-primary)' }}
                />
                <Legend />
                <Area type="monotone" dataKey="new" name="New Complaints" stroke="#ff7b7b" fillOpacity={1} fill="url(#colorNew)" />
                <Area type="monotone" dataKey="resolved" name="Resolved" stroke="#E6FF2B" fillOpacity={1} fill="url(#colorResolved)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Monthly Performance - Bar Chart */}
        <Card className={styles.chartCard}>
          <div className={styles.cardHeader}>
            <h3>Ward Performance (Current Month)</h3>
          </div>
          <div className={styles.chartWrapper}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={WARD_PERFORMANCE_MOCK}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                  contentStyle={{ backgroundColor: 'var(--glass-bg)', borderColor: 'var(--glass-border)', borderRadius: '8px' }}
                />
                <Legend />
                <Bar dataKey="resolved" name="Resolved" fill="#50b4dc" radius={[4, 4, 0, 0]} />
                <Bar dataKey="pending" name="Pending" fill="#ff7b7b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Predictive Trends / Categorization - Pie Chart */}
        <Card className={styles.pieCard}>
          <div className={styles.cardHeader}>
            <h3>Issues by Category</h3>
          </div>
          <div className={styles.pieWrapper}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={WASTE_CATEGORIES}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {WASTE_CATEGORIES.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--glass-bg)', borderColor: 'var(--glass-border)', borderRadius: '8px' }}
                  itemStyle={{ color: 'var(--text-primary)' }}
                />
                <Legend verticalAlign="bottom" height={36} iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Card>

      </div>
    </div>
  );
}
