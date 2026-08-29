'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { AlertTriangle, CheckCircle, Truck, Users } from 'lucide-react';
import { apiGet } from '@/lib/api';
import { useAuthStore, ROLES } from '@/stores/authStore';
import { Complaint, PaginatedResponse, Vehicle, Task } from '@/types';
import KPICard from '@/components/dashboard/KPICard';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import { TableRowSkeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';
import Link from 'next/link';

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const isOfficer = user && [ROLES.ADMIN, ROLES.CHIEF_ENGINEER, ROLES.EXECUTIVE_ENGINEER, ROLES.JUNIOR_ENGINEER, ROLES.SUPERVISOR].includes(user.role as any);

  // Fetch aggregate data
  const { data: complaintsData, isLoading: complaintsLoading } = useQuery<PaginatedResponse<Complaint>>({
    queryKey: ['complaints', 'recent'],
    queryFn: () => apiGet('/complaints?per_page=5'),
  });

  const { data: vehiclesData, isLoading: vehiclesLoading } = useQuery<PaginatedResponse<Vehicle>>({
    queryKey: ['vehicles'],
    queryFn: () => apiGet('/vehicles'),
    enabled: !!isOfficer,
  });

  const { data: tasksData, isLoading: tasksLoading } = useQuery<PaginatedResponse<Task>>({
    queryKey: ['tasks'],
    queryFn: () => apiGet('/tasks'),
    enabled: !!isOfficer,
  });

  // Calculate mock KPI data based on actual responses for now
  const totalComplaints = complaintsData?.total || 0;
  const activeVehicles = vehiclesData?.data.filter(v => (v.status as string) !== 'MAINTENANCE' && (v.status as string) !== 'IDLE').length || 0;
  const activeTasks = tasksData?.data.filter(t => (t.status as string) === 'STARTED' || (t.status as string) === 'ASSIGNED').length || 0;
  const resolvedComplaints = complaintsData?.data.filter(c => (c.status as string) === 'RESOLVED').length || 0;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Command Center</h1>
        <p className={styles.subtitle}>Real-time overview of municipal operations.</p>
      </div>

      {isOfficer && (
        <div className={styles.kpiGrid}>
          <KPICard 
            title="Total Complaints" 
            value={totalComplaints} 
            icon={AlertTriangle} 
            isLoading={complaintsLoading}
            trend={{ value: 12, isPositive: false }}
          />
          <KPICard 
            title="Resolved Issues" 
            value={resolvedComplaints} 
            icon={CheckCircle} 
            isLoading={complaintsLoading}
            trend={{ value: 8, isPositive: true }}
          />
          <KPICard 
            title="Active Vehicles" 
            value={activeVehicles} 
            icon={Truck} 
            isLoading={vehiclesLoading}
          />
          <KPICard 
            title="Workers On Field" 
            value={activeTasks} 
            icon={Users} 
            isLoading={tasksLoading}
          />
        </div>
      )}

      <div className={styles.mainGrid}>
        {/* Recent Complaints Table */}
        <Card className={styles.tableCard}>
          <div className={styles.cardHeader}>
            <h3>Recent Complaints</h3>
            <Link href="/complaints" className={styles.viewAll}>View All</Link>
          </div>
          
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Reference</th>
                  <th>Category</th>
                  <th>Location</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {complaintsLoading ? (
                  <>
                    <TableRowSkeleton cols={5} />
                    <TableRowSkeleton cols={5} />
                    <TableRowSkeleton cols={5} />
                  </>
                ) : complaintsData?.data.length === 0 ? (
                  <tr>
                    <td colSpan={5} className={styles.emptyCell}>No recent complaints.</td>
                  </tr>
                ) : (
                  complaintsData?.data.map(complaint => (
                    <tr key={complaint.id}>
                      <td className={styles.monoCell}>{complaint.reference_number}</td>
                      <td>{complaint.category.replace('_', ' ')}</td>
                      <td className={styles.truncateCell}>{complaint.address || 'GPS Coordinate'}</td>
                      <td><Badge label={complaint.status} /></td>
                      <td className={styles.dateCell}>{new Date(complaint.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Prediction Panel Placeholder (For Phase 8) */}
        {isOfficer && (
          <Card glass className={styles.predictionCard}>
            <div className={styles.cardHeader}>
              <div className={styles.aiHeader}>
                <span className={styles.aiGlow} />
                <h3>Gemini Insights</h3>
              </div>
            </div>
            <div className={styles.placeholderContent}>
              <p>Predictive analytics module will be activated in Phase 8.</p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
