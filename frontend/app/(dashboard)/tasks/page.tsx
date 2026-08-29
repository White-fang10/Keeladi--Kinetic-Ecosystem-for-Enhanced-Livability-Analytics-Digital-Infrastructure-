'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { ClipboardList, ArrowRight, Clock, CheckCircle } from 'lucide-react';
import { apiGet } from '@/lib/api';
import { PaginatedResponse, Task } from '@/types';
import { useAuthStore, ROLES } from '@/stores/authStore';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import { CardSkeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

export default function TasksPage() {
  const user = useAuthStore((s) => s.user);
  
  const { data, isLoading, error } = useQuery<PaginatedResponse<Task>>({
    queryKey: ['tasks'],
    queryFn: () => apiGet('/tasks'),
    retry: false, // Don't retry if endpoint doesn't exist
  });

  const isWorker = user?.role === ROLES.SANITATION_WORKER;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>{isWorker ? "Today's Tasks" : 'Task Force Management'}</h1>
        <p className={styles.subtitle}>
          {isWorker ? 'Manage and verify your assigned field operations.' : 'Overview of all active sanitation tasks.'}
        </p>
      </div>

      <div className={styles.grid}>
        {isLoading ? (
          <>
            <CardSkeleton />
            <CardSkeleton />
          </>
        ) : error ? (
          <div className={styles.emptyState}>
            <ClipboardList size={48} className={styles.emptyIcon} />
            <p>No active tasks assigned at the moment.</p>
          </div>
        ) : data?.data.length === 0 ? (
          <div className={styles.emptyState}>
            <ClipboardList size={48} className={styles.emptyIcon} />
            <p>You have no pending tasks today. Great job!</p>
          </div>
        ) : (
          data?.data.map((task) => (
            <Link key={task.id} href={`/tasks/${task.id}`} className={styles.cardLink}>
              <Card hover className={styles.taskCard}>
                <div className={styles.cardHeader}>
                  <Badge label={task.status} dot />
                  <span className={styles.date}>{new Date(task.created_at).toLocaleDateString()}</span>
                </div>
                
                <h3 className={styles.taskTitle}>
                  {task.priority === 'HIGH' && <span className={styles.highPriority}>[HIGH] </span>}
                  Field Operation
                </h3>
                
                {task.notes && <p className={styles.notes}>{task.notes}</p>}

                <div className={styles.metaInfo}>
                  <div className={styles.metaItem}>
                    <Clock size={14} />
                    <span>{task.deadline ? new Date(task.deadline).toLocaleString() : 'No Deadline'}</span>
                  </div>
                  {task.status === 'COMPLETED' && (
                    <div className={styles.metaItemSuccess}>
                      <CheckCircle size={14} />
                      <span>Verified</span>
                    </div>
                  )}
                </div>

                <div className={styles.cardFooter}>
                  <span className={styles.actionText}>
                    {task.status === 'ASSIGNED' || task.status === 'STARTED' ? 'Execute Task' : 'View Details'} 
                    <ArrowRight size={14} />
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
