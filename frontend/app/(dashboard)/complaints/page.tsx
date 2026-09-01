'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { Plus, MapPin, Calendar, ArrowRight } from 'lucide-react';
import { apiGet } from '@/lib/api';
import { Complaint, StandardResponse } from '@/types';
import { useAuthStore } from '@/stores/authStore';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import { Skeleton, CardSkeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

export default function ComplaintsPage() {
  const user = useAuthStore((s) => s.user);

  const { data, isLoading } = useQuery<StandardResponse<Complaint[]>>({
    queryKey: ['complaints'],
    queryFn: () => apiGet('/complaints'),
  });

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Complaints</h1>
          <p className={styles.subtitle}>Track and manage civic issues.</p>
        </div>
        
        {user?.role === 'CITIZEN' && (
          <Link href="/complaints/new">
            <Button leftIcon={<Plus size={18} />}>Report Issue</Button>
          </Link>
        )}
      </div>

      <div className={styles.grid}>
        {isLoading ? (
          <>
            <CardSkeleton />
            <CardSkeleton />
            <CardSkeleton />
          </>
        ) : data?.data.length === 0 ? (
          <div className={styles.emptyState}>
            <p>No complaints found.</p>
          </div>
        ) : (
          data?.data.map((complaint) => (
            <Link key={complaint.id} href={`/complaints/${complaint.id}`} className={styles.cardLink}>
              <Card hover className={styles.complaintCard}>
                <div className={styles.cardHeader}>
                  <span className={styles.refNumber}>{complaint.reference_number}</span>
                  <Badge label={complaint.status} dot />
                </div>
                
                <h3 className={styles.complaintTitle}>{complaint.title}</h3>
                <p className={styles.category}>{complaint.category.replace('_', ' ')}</p>

                <div className={styles.metaInfo}>
                  <div className={styles.metaItem}>
                    <MapPin size={14} />
                    <span>{complaint.address || 'Location provided'}</span>
                  </div>
                  <div className={styles.metaItem}>
                    <Calendar size={14} />
                    <span>{new Date(complaint.created_at).toLocaleDateString()}</span>
                  </div>
                </div>

                <div className={styles.cardFooter}>
                  <span className={styles.viewDetails}>
                    View Details <ArrowRight size={14} />
                  </span>
                </div>
              </Card>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}
