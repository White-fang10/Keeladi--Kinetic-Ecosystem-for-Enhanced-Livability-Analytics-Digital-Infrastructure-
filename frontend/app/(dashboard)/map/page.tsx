'use client';

import React from 'react';
import dynamic from 'next/dynamic';
import { useAuthStore, ROLES } from '@/stores/authStore';
import { Skeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

// Leaflet relies on window, so we MUST load it dynamically with ssr: false
const LiveMap = dynamic(() => import('@/components/gis/LiveMap'), {
  ssr: false,
  loading: () => <Skeleton height="calc(100vh - 180px)" width="100%" borderRadius="var(--radius-xl)" />,
});

export default function GISMapPage() {
  const user = useAuthStore((s) => s.user);

  // Extra guard in case a citizen navigates here manually
  if (user?.role === ROLES.CITIZEN) {
    return <div>Access Denied. Command Center clearance required.</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Live GIS Map</h1>
          <p className={styles.subtitle}>
            Real-time geospatial tracking of civic assets, fleet, and field operations.
          </p>
        </div>
      </div>

      <div className={styles.mapWrapper}>
        <LiveMap />
      </div>
    </div>
  );
}
