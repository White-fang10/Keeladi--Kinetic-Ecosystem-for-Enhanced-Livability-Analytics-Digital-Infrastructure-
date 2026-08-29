'use client';

import React from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, MapPin, Calendar, CheckCircle2, Clock } from 'lucide-react';
import { apiGet } from '@/lib/api';
import { Complaint, ComplaintHistory, StandardResponse } from '@/types';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import { Skeleton, CardSkeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

export default function ComplaintDetailPage() {
  const params = useParams();
  const router = useRouter();
  const complaintId = params.id as string;

  const { data: complaintData, isLoading } = useQuery<StandardResponse<Complaint>>({
    queryKey: ['complaints', complaintId],
    queryFn: () => apiGet(`/complaints/${complaintId}`),
  });

  const { data: historyData } = useQuery<StandardResponse<ComplaintHistory[]>>({
    queryKey: ['complaints', complaintId, 'history'],
    queryFn: () => apiGet(`/complaints/${complaintId}/history`),
    enabled: !!complaintData,
  });

  if (isLoading) {
    return (
      <div className={styles.container}>
        <Skeleton width={120} height={36} />
        <CardSkeleton />
        <CardSkeleton />
      </div>
    );
  }

  const complaint = complaintData?.data;

  if (!complaint) {
    return (
      <div className={styles.container}>
        <h2>Complaint Not Found</h2>
        <Button onClick={() => router.back()}>Go Back</Button>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Button 
        variant="ghost" 
        size="sm" 
        leftIcon={<ArrowLeft size={16} />} 
        onClick={() => router.back()}
        className={styles.backBtn}
      >
        Back to Complaints
      </Button>

      <div className={styles.header}>
        <div>
          <div className={styles.refBadge}>{complaint.reference_number}</div>
          <h1 className={styles.title}>{complaint.title}</h1>
        </div>
        <Badge label={complaint.status} dot className={styles.statusBadge} />
      </div>

      <div className={styles.grid}>
        {/* Left Column - Details */}
        <div className={styles.mainContent}>
          <Card className={styles.detailCard}>
            <div className={styles.section}>
              <h3>Description</h3>
              <p className={styles.text}>{complaint.description || 'No description provided.'}</p>
            </div>

            <div className={styles.divider} />

            <div className={styles.metaGrid}>
              <div className={styles.metaBox}>
                <span className={styles.metaLabel}>Category</span>
                <span className={styles.metaValue}>{complaint.category.replace('_', ' ')}</span>
              </div>
              <div className={styles.metaBox}>
                <span className={styles.metaLabel}>Date Submitted</span>
                <span className={styles.metaValue}>
                  {new Date(complaint.created_at).toLocaleString()}
                </span>
              </div>
              <div className={styles.metaBox}>
                <span className={styles.metaLabel}>Location</span>
                <span className={styles.metaValue}>{complaint.address || 'GPS Coordinates Provided'}</span>
              </div>
            </div>
          </Card>

          {/* AI Insights Card (Phase 5/8 overlap) */}
          {complaint.ai_waste_type && (
            <Card className={styles.aiCard} glass>
              <div className={styles.aiHeader}>
                <span className={styles.aiGlow} />
                <h3>Gemini AI Analysis</h3>
              </div>
              <div className={styles.metaGrid}>
                <div className={styles.metaBox}>
                  <span className={styles.metaLabel}>Identified Waste</span>
                  <span className={styles.metaValue}>{complaint.ai_waste_type}</span>
                </div>
                <div className={styles.metaBox}>
                  <span className={styles.metaLabel}>Severity Score</span>
                  <Badge 
                    label={`Level ${complaint.ai_severity}`} 
                    variant={complaint.ai_severity! > 7 ? 'danger' : 'warning'} 
                  />
                </div>
              </div>
            </Card>
          )}
        </div>

        {/* Right Column - Timeline */}
        <div className={styles.sideContent}>
          <Card className={styles.timelineCard}>
            <h3 className={styles.timelineTitle}>Status History</h3>
            
            <div className={styles.timeline}>
              {historyData?.data.map((item, index) => (
                <div key={item.id} className={styles.timelineItem}>
                  <div className={styles.timelineIcon}>
                    {index === 0 ? <CheckCircle2 size={16} /> : <Clock size={16} />}
                  </div>
                  <div className={styles.timelineContent}>
                    <div className={styles.timelineHeader}>
                      <Badge label={item.to_status} />
                      <span className={styles.timelineDate}>
                        {new Date(item.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <p className={styles.timelineAction}>{item.action}</p>
                    {item.remarks && <p className={styles.timelineRemarks}>"{item.remarks}"</p>}
                  </div>
                </div>
              ))}
              {!historyData?.data && <Skeleton count={3} height={40} />}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
