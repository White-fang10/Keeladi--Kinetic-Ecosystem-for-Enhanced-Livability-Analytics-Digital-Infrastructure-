'use client';

import React, { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { ArrowLeft, MapPin, Clock, Camera, Navigation, CheckCircle } from 'lucide-react';
import { apiGet, apiPost } from '@/lib/api';
import { StandardResponse, Task, Complaint } from '@/types';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import { Skeleton, CardSkeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

export default function TaskDetailPage() {
  const params = useParams();
  const router = useRouter();
  const taskId = params.id as string;

  const [isLocating, setIsLocating] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  // Note: Backend might not have /tasks/{id}, but we assume it does based on standard REST.
  // We'll fall back to loading if it fails.
  const { data: taskData, isLoading } = useQuery<StandardResponse<Task>>({
    queryKey: ['tasks', taskId],
    queryFn: () => apiGet(`/tasks/${taskId}`),
    retry: false,
  });

  const task = taskData?.data;

  // We also might want the associated complaint details
  const { data: complaintData } = useQuery<StandardResponse<Complaint>>({
    queryKey: ['complaints', task?.complaint_id],
    queryFn: () => apiGet(`/complaints/${task?.complaint_id}`),
    enabled: !!task?.complaint_id,
  });

  const handleVerificationUpload = async (type: 'before' | 'after') => {
    if (!navigator.geolocation) {
      toast.error('Geolocation is not supported by your browser');
      return;
    }

    // 1. Get Location
    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        setIsLocating(false);
        const { latitude, longitude } = position.coords;
        
        // 2. Mock Image Upload (We would use a hidden <input type="file" /> in a real app, 
        // but since we need to upload quickly and this is a hackathon MVP, we'll simulate picking an image
        // or just use a placeholder URL for the payload).
        const dummyImageUrl = `https://example.com/mock-${type}-image.jpg`;

        try {
          setIsUploading(true);
          const payload = {
            task_id: taskId,
            [`${type}_image_url`]: dummyImageUrl,
            [`${type}_lat`]: latitude,
            [`${type}_lng`]: longitude,
          };
          
          await apiPost(`/verification/${type}`, payload);
          toast.success(`${type.toUpperCase()} Verification Uploaded Successfully!`);
          
          // In a real app we'd invalidate queries here
          // queryClient.invalidateQueries(['tasks', taskId])
        } catch (error: any) {
          toast.error(error.response?.data?.detail || 'Verification failed');
        } finally {
          setIsUploading(false);
        }
      },
      (error) => {
        setIsLocating(false);
        toast.error('Could not get location. GPS access is required for verification.');
      }
    );
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <Skeleton width={120} height={36} />
        <CardSkeleton />
      </div>
    );
  }

  // Graceful degradation if backend endpoint is missing during hackathon
  if (!task) {
    return (
      <div className={styles.container}>
        <h2>Task Details</h2>
        <p className={styles.mutedText}>Task data unavailable. The endpoint might not be active.</p>
        <Button onClick={() => router.back()}>Go Back</Button>
      </div>
    );
  }

  const complaint = complaintData?.data;

  return (
    <div className={styles.container}>
      <Button 
        variant="ghost" 
        size="sm" 
        leftIcon={<ArrowLeft size={16} />} 
        onClick={() => router.back()}
        className={styles.backBtn}
      >
        Back to Tasks
      </Button>

      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Task Execution</h1>
          <p className={styles.subtitle}>Upload geo-verified photos to complete your assignment.</p>
        </div>
        <Badge label={task.status} className={styles.statusBadge} />
      </div>

      <div className={styles.grid}>
        {/* Left Column: Verification Action */}
        <div className={styles.mainContent}>
          <Card className={styles.actionCard}>
            <h3 className={styles.sectionTitle}>Geo Verification</h3>
            <p className={styles.instructions}>
              You must be at the physical location of the issue to verify. GPS coordinates will be recorded.
            </p>
            
            <div className={styles.uploadGrid}>
              {/* Before Verification */}
              <div className={[styles.uploadBox, task.status !== 'ASSIGNED' ? styles.disabled : ''].join(' ')}>
                <div className={styles.uploadHeader}>
                  <h4>1. Before Work</h4>
                  {task.status !== 'ASSIGNED' && <CheckCircle size={16} color="#6ddc6d" />}
                </div>
                <p>Take a photo of the issue before cleaning.</p>
                <Button 
                  onClick={() => handleVerificationUpload('before')}
                  isLoading={isLocating || isUploading}
                  disabled={task.status !== 'ASSIGNED'}
                  leftIcon={<Camera size={16} />}
                  fullWidth
                >
                  Upload Before Photo
                </Button>
              </div>

              {/* After Verification */}
              <div className={[styles.uploadBox, task.status !== 'STARTED' ? styles.disabled : ''].join(' ')}>
                <div className={styles.uploadHeader}>
                  <h4>2. After Work</h4>
                  {task.status === 'VERIFICATION' || task.status === 'COMPLETED' ? <CheckCircle size={16} color="#6ddc6d" /> : null}
                </div>
                <p>Take a photo of the area after cleaning.</p>
                <Button 
                  onClick={() => handleVerificationUpload('after')}
                  isLoading={isLocating || isUploading}
                  disabled={task.status !== 'STARTED'}
                  leftIcon={<Camera size={16} />}
                  fullWidth
                >
                  Upload After Photo
                </Button>
              </div>
            </div>
            
            <div className={styles.gpsNote}>
              <Navigation size={14} />
              <span>GPS Tracking Active</span>
            </div>
          </Card>
        </div>

        {/* Right Column: Task Info */}
        <div className={styles.sideContent}>
          <Card className={styles.infoCard}>
            <h3 className={styles.sectionTitle}>Instructions</h3>
            <p className={styles.notes}>{task.notes || 'No specific instructions provided.'}</p>
            
            <div className={styles.metaList}>
              <div className={styles.metaItem}>
                <Clock size={16} />
                <div>
                  <span className={styles.metaLabel}>Deadline</span>
                  <span className={styles.metaValue}>{task.deadline ? new Date(task.deadline).toLocaleString() : 'N/A'}</span>
                </div>
              </div>
              <div className={styles.metaItem}>
                <MapPin size={16} />
                <div>
                  <span className={styles.metaLabel}>Location</span>
                  <span className={styles.metaValue}>{complaint?.address || 'Loading...'}</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
