'use client';

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { CheckCircle, XCircle, Clock, MapPin, ImageIcon, AlertTriangle } from 'lucide-react';
import toast from 'react-hot-toast';

import { apiGet, apiPatch } from '@/lib/api';
import { Verification, StandardResponse } from '@/types';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import { CardSkeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

const STATUS_TABS = ['ALL', 'PENDING', 'APPROVED', 'REJECTED'];

export default function VerificationPage() {
  const queryClient = useQueryClient();
  const [filter, setFilter] = useState('PENDING');
  const [remarksMap, setRemarksMap] = useState<Record<string, string>>({});

  const { data, isLoading } = useQuery<StandardResponse<Verification[]>>({
    queryKey: ['verifications'],
    queryFn: () => apiGet('/verification'),
  });

  const approveMutation = useMutation({
    mutationFn: ({ verificationId, status, remarks }: { verificationId: string; status: string; remarks: string }) =>
      apiPatch(`/verification/${verificationId}/approve`, { status, remarks }),
    onSuccess: (_, vars) => {
      queryClient.invalidateQueries({ queryKey: ['verifications'] });
      queryClient.invalidateQueries({ queryKey: ['complaints'] });
      toast.success(`Verification ${vars.status.toLowerCase()} successfully`);
    },
    onError: () => toast.error('Failed to update verification'),
  });

  const allVerifications = data?.data ?? [];
  const filtered = filter === 'ALL'
    ? allVerifications
    : allVerifications.filter(v => v.approval_status === filter);

  const counts = {
    PENDING:  allVerifications.filter(v => v.approval_status === 'PENDING').length,
    APPROVED: allVerifications.filter(v => v.approval_status === 'APPROVED').length,
    REJECTED: allVerifications.filter(v => v.approval_status === 'REJECTED').length,
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Verification Centre</h1>
          <p className={styles.subtitle}>Review before/after evidence and approve completed field work.</p>
        </div>
      </div>

      {/* Summary Badges */}
      <div className={styles.summaryRow}>
        <div className={styles.summaryCard}>
          <Clock size={20} className={styles.summaryIconPending} />
          <span className={styles.summaryVal}>{counts.PENDING}</span>
          <span className={styles.summaryLabel}>Pending</span>
        </div>
        <div className={styles.summaryCard}>
          <CheckCircle size={20} className={styles.summaryIconApproved} />
          <span className={styles.summaryVal}>{counts.APPROVED}</span>
          <span className={styles.summaryLabel}>Approved</span>
        </div>
        <div className={styles.summaryCard}>
          <XCircle size={20} className={styles.summaryIconRejected} />
          <span className={styles.summaryVal}>{counts.REJECTED}</span>
          <span className={styles.summaryLabel}>Rejected</span>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className={styles.tabs}>
        {STATUS_TABS.map(tab => (
          <button
            key={tab}
            className={[styles.tab, filter === tab ? styles.tabActive : ''].join(' ')}
            onClick={() => setFilter(tab)}
          >
            {tab === 'ALL' ? `All (${allVerifications.length})` : `${tab} (${counts[tab as keyof typeof counts] ?? 0})`}
          </button>
        ))}
      </div>

      {/* Cards */}
      <div className={styles.list}>
        {isLoading ? (
          Array.from({ length: 3 }).map((_, i) => <CardSkeleton key={i} />)
        ) : filtered.length === 0 ? (
          <div className={styles.emptyState}>
            <CheckCircle size={48} className={styles.emptyIcon} />
            <p>No {filter !== 'ALL' ? filter.toLowerCase() : ''} verifications found.</p>
          </div>
        ) : (
          filtered.map(v => (
            <Card key={v.id} className={styles.verifCard}>
              <div className={styles.cardHeader}>
                <div className={styles.cardIdBlock}>
                  <span className={styles.verifId}>Task: {v.task_id?.slice(0, 8)}…</span>
                  <Badge
                    label={v.approval_status}
                    variant={
                      v.approval_status === 'APPROVED' ? 'success' :
                      v.approval_status === 'REJECTED' ? 'error' : 'warning'
                    }
                    dot
                  />
                </div>
                {v.location_verified !== null && (
                  <div className={styles.locationBadge}>
                    <MapPin size={12} />
                    <span>{v.location_verified ? 'Location Verified' : 'Location Mismatch'}</span>
                    {v.distance_from_complaint !== null && v.distance_from_complaint !== undefined && (
                      <span className={styles.distance}>({v.distance_from_complaint.toFixed(1)}m away)</span>
                    )}
                  </div>
                )}
              </div>

              {/* Before / After Images */}
              <div className={styles.imageGrid}>
                <div className={styles.imageBlock}>
                  <span className={styles.imageLabel}>Before</span>
                  {v.before_image_url ? (
                    <img src={v.before_image_url} alt="Before" className={styles.image} />
                  ) : (
                    <div className={styles.imagePlaceholder}><ImageIcon size={32} /><span>No image</span></div>
                  )}
                  {v.before_captured_at && (
                    <span className={styles.timestamp}>{new Date(v.before_captured_at).toLocaleString()}</span>
                  )}
                </div>
                <div className={styles.imageBlock}>
                  <span className={styles.imageLabel}>After</span>
                  {v.after_image_url ? (
                    <img src={v.after_image_url} alt="After" className={styles.image} />
                  ) : (
                    <div className={styles.imagePlaceholder}><ImageIcon size={32} /><span>Pending upload</span></div>
                  )}
                  {v.after_captured_at && (
                    <span className={styles.timestamp}>{new Date(v.after_captured_at).toLocaleString()}</span>
                  )}
                </div>
              </div>

              {/* Existing remarks */}
              {v.approval_remarks && (
                <div className={styles.existingRemarks}>
                  <AlertTriangle size={14} />
                  <span>{v.approval_remarks}</span>
                </div>
              )}

              {/* Approve/Reject Actions */}
              {v.approval_status === 'PENDING' && v.after_image_url && (
                <div className={styles.actions}>
                  <textarea
                    className={styles.remarksInput}
                    placeholder="Remarks (optional)"
                    rows={2}
                    value={remarksMap[v.id] ?? ''}
                    onChange={e => setRemarksMap(prev => ({ ...prev, [v.id]: e.target.value }))}
                  />
                  <div className={styles.actionButtons}>
                    <Button
                      variant="primary"
                      leftIcon={<CheckCircle size={16} />}
                      isLoading={approveMutation.isPending}
                      onClick={() => approveMutation.mutate({ verificationId: v.id, status: 'APPROVED', remarks: remarksMap[v.id] ?? '' })}
                    >
                      Approve
                    </Button>
                    <Button
                      variant="danger"
                      leftIcon={<XCircle size={16} />}
                      isLoading={approveMutation.isPending}
                      onClick={() => approveMutation.mutate({ verificationId: v.id, status: 'REJECTED', remarks: remarksMap[v.id] ?? 'Rejected - rework required' })}
                    >
                      Reject
                    </Button>
                  </div>
                </div>
              )}
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
