'use client';

import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Bell, Check, Trash2, CheckCircle2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { apiGet, apiPatch, apiDelete } from '@/lib/api';
import { Notification, StandardResponse, PaginatedResponse } from '@/types';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import { Skeleton } from '@/components/ui/Skeleton';
import styles from './page.module.css';

export default function NotificationsPage() {
  const queryClient = useQueryClient();

  // Poll for notifications every 10 seconds
  const { data, isLoading } = useQuery<PaginatedResponse<Notification>>({
    queryKey: ['notifications'],
    queryFn: () => apiGet('/notifications?per_page=50'),
    refetchInterval: 10000,
  });

  const markReadMutation = useMutation({
    mutationFn: (id: string) => apiPatch(`/notifications/${id}/read`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
    onError: () => toast.error('Failed to mark notification as read'),
  });

  const markAllReadMutation = useMutation({
    mutationFn: () => apiPatch('/notifications/read-all'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      toast.success('All notifications marked as read');
    },
    onError: () => toast.error('Failed to mark all as read'),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => apiDelete(`/notifications/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
    onError: () => toast.error('Failed to delete notification'),
  });

  const notifications = data?.data || [];
  const unreadCount = notifications.filter(n => !n.is_read).length;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.titleWrapper}>
          <h1 className={styles.title}>Notifications</h1>
          {unreadCount > 0 && <Badge label={`${unreadCount} Unread`} variant="danger" />}
        </div>
        
        {unreadCount > 0 && (
          <Button 
            variant="secondary" 
            size="sm" 
            leftIcon={<CheckCircle2 size={16} />} 
            onClick={() => markAllReadMutation.mutate()}
            isLoading={markAllReadMutation.isPending}
          >
            Mark All Read
          </Button>
        )}
      </div>

      <div className={styles.list}>
        {isLoading ? (
          <>
            <Skeleton height={80} />
            <Skeleton height={80} />
            <Skeleton height={80} />
          </>
        ) : notifications.length === 0 ? (
          <div className={styles.emptyState}>
            <Bell size={48} className={styles.emptyIcon} />
            <h3>All Caught Up!</h3>
            <p>You have no new notifications.</p>
          </div>
        ) : (
          notifications.map((notif) => (
            <Card key={notif.id} className={[styles.notifCard, !notif.is_read ? styles.unread : ''].join(' ')} padding="md">
              <div className={styles.notifContent}>
                <div className={styles.notifHeader}>
                  <h4>{notif.title}</h4>
                  <span className={styles.date}>{new Date(notif.created_at).toLocaleString()}</span>
                </div>
                <p className={styles.message}>{notif.message}</p>
              </div>

              <div className={styles.actions}>
                {!notif.is_read && (
                  <button 
                    className={styles.iconBtn} 
                    onClick={() => markReadMutation.mutate(notif.id)}
                    title="Mark as Read"
                  >
                    <Check size={18} />
                  </button>
                )}
                <button 
                  className={[styles.iconBtn, styles.deleteBtn].join(' ')} 
                  onClick={() => deleteMutation.mutate(notif.id)}
                  title="Delete"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
