'use client';

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Truck, MapPin, Gauge, User, RefreshCw, Filter } from 'lucide-react';
import toast from 'react-hot-toast';

import { apiGet, apiPatch } from '@/lib/api';
import { Vehicle, StandardResponse } from '@/types';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import { CardSkeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

const STATUS_COLORS: Record<string, string> = {
  AVAILABLE:   'success',
  COLLECTING:  'warning',
  FULL:        'error',
  MAINTENANCE: 'default',
  DISPOSAL:    'info',
};

const STATUS_OPTIONS = ['ALL', 'AVAILABLE', 'COLLECTING', 'FULL', 'MAINTENANCE', 'DISPOSAL'];

const VEHICLE_TYPE_ICONS: Record<string, string> = {
  COMPACTOR:   '🚛',
  TIPPER:      '🚚',
  AUTO_TIPPER: '🛺',
  MINI_TRUCK:  '🚐',
};

export default function FleetPage() {
  const queryClient = useQueryClient();
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [updatingId, setUpdatingId] = useState<string | null>(null);

  const { data, isLoading, refetch } = useQuery<StandardResponse<Vehicle[]>>({
    queryKey: ['vehicles'],
    queryFn: () => apiGet('/vehicles'),
    refetchInterval: 30000,
  });

  const statusMutation = useMutation({
    mutationFn: ({ vehicleId, status }: { vehicleId: string; status: string }) =>
      apiPatch(`/vehicles/${vehicleId}/status`, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vehicles'] });
      toast.success('Vehicle status updated');
      setUpdatingId(null);
    },
    onError: () => {
      toast.error('Failed to update status');
      setUpdatingId(null);
    },
  });

  const vehicles = data?.data ?? [];
  const filtered = filterStatus === 'ALL' ? vehicles : vehicles.filter(v => v.status === filterStatus);

  const counts = STATUS_OPTIONS.slice(1).reduce((acc, s) => ({
    ...acc,
    [s]: vehicles.filter(v => v.status === s).length
  }), {} as Record<string, number>);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Fleet Tracker</h1>
          <p className={styles.subtitle}>Real-time status of all sanitation vehicles.</p>
        </div>
        <Button variant="secondary" leftIcon={<RefreshCw size={16} />} onClick={() => refetch()}>
          Refresh
        </Button>
      </div>

      {/* KPI Strip */}
      <div className={styles.kpiRow}>
        {[
          { label: 'Total Fleet',   value: vehicles.length, color: 'var(--color-primary)' },
          { label: 'Available',     value: counts.AVAILABLE   ?? 0, color: 'var(--color-success)' },
          { label: 'On Route',      value: counts.COLLECTING  ?? 0, color: 'var(--color-warning)' },
          { label: 'Full / Return', value: counts.FULL        ?? 0, color: 'var(--color-error)' },
          { label: 'Maintenance',   value: counts.MAINTENANCE ?? 0, color: 'var(--color-text-secondary)' },
        ].map(k => (
          <Card key={k.label} className={styles.kpiCard}>
            <span className={styles.kpiValue} style={{ color: k.color }}>{k.value}</span>
            <span className={styles.kpiLabel}>{k.label}</span>
          </Card>
        ))}
      </div>

      {/* Filter Tabs */}
      <div className={styles.filterRow}>
        <Filter size={16} className={styles.filterIcon} />
        {STATUS_OPTIONS.map(s => (
          <button
            key={s}
            className={[styles.filterTab, filterStatus === s ? styles.filterTabActive : ''].join(' ')}
            onClick={() => setFilterStatus(s)}
          >
            {s === 'ALL' ? `All (${vehicles.length})` : `${s} (${counts[s] ?? 0})`}
          </button>
        ))}
      </div>

      {/* Vehicle Grid */}
      <div className={styles.grid}>
        {isLoading ? (
          Array.from({ length: 6 }).map((_, i) => <CardSkeleton key={i} />)
        ) : filtered.length === 0 ? (
          <div className={styles.emptyState}>
            <Truck size={48} className={styles.emptyIcon} />
            <p>No vehicles match this filter.</p>
          </div>
        ) : (
          filtered.map(vehicle => (
            <Card key={vehicle.id} className={styles.vehicleCard} hover>
              <div className={styles.cardTop}>
                <span className={styles.vehicleEmoji}>{VEHICLE_TYPE_ICONS[vehicle.vehicle_type] ?? '🚛'}</span>
                <Badge label={vehicle.status} variant={STATUS_COLORS[vehicle.status] as any} dot />
              </div>

              <h3 className={styles.regNumber}>{vehicle.registration_number}</h3>
              <p className={styles.vehicleType}>{vehicle.vehicle_type.replace('_', ' ')}</p>

              <div className={styles.metaList}>
                <div className={styles.metaItem}>
                  <Gauge size={14} />
                  <span>Capacity: {vehicle.capacity_kg.toLocaleString()} kg</span>
                </div>
                {vehicle.make_model && (
                  <div className={styles.metaItem}>
                    <Truck size={14} />
                    <span>{vehicle.make_model}</span>
                  </div>
                )}
                <div className={styles.metaItem}>
                  <MapPin size={14} />
                  <span>Ward {vehicle.ward_id?.replace('ward-', '')}</span>
                </div>
                <div className={styles.metaItem}>
                  <User size={14} />
                  <span>{vehicle.driver_id ? 'Driver assigned' : 'No driver'}</span>
                </div>
              </div>

              {/* Status Update */}
              <div className={styles.statusUpdate}>
                <label className={styles.statusLabel}>Update Status</label>
                <select
                  className={styles.statusSelect}
                  value={vehicle.status}
                  disabled={updatingId === vehicle.id}
                  onChange={e => {
                    setUpdatingId(vehicle.id);
                    statusMutation.mutate({ vehicleId: vehicle.id, status: e.target.value });
                  }}
                >
                  {STATUS_OPTIONS.slice(1).map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
