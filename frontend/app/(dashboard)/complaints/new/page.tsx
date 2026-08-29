'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm as useReactHookForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import toast from 'react-hot-toast';
import { MapPin, Navigation, Type, AlignLeft } from 'lucide-react';

import { apiPost } from '@/lib/api';
import Card from '@/components/ui/Card';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import styles from './page.module.css';

const complaintSchema = z.object({
  title: z.string().min(5, 'Title is too short'),
  description: z.string().optional(),
  category: z.string().min(1, 'Category is required'),
  address: z.string().min(5, 'Address is required'),
  latitude: z.number(),
  longitude: z.number(),
});

type ComplaintFormValues = z.infer<typeof complaintSchema>;

export default function NewComplaintPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [isLocating, setIsLocating] = useState(false);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useReactHookForm<ComplaintFormValues>({
    resolver: zodResolver(complaintSchema),
    defaultValues: {
      category: 'GARBAGE_OVERFLOW',
    },
  });

  // Auto-fetch location on mount
  useEffect(() => {
    handleGetLocation();
  }, []);

  const handleGetLocation = () => {
    if (!navigator.geolocation) {
      toast.error('Geolocation is not supported by your browser');
      return;
    }

    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setValue('latitude', position.coords.latitude);
        setValue('longitude', position.coords.longitude);
        setValue('address', 'Current Location (GPS Verified)');
        setIsLocating(false);
        toast.success('Location acquired');
      },
      (error) => {
        setIsLocating(false);
        toast.error('Could not get location. Please allow GPS access.');
      }
    );
  };

  const onSubmit = async (data: ComplaintFormValues) => {
    try {
      setIsLoading(true);
      const payload = { ...data, ward_id: 'ward-1' };
      await apiPost('/complaints', payload);
      toast.success('Complaint submitted successfully');
      router.push('/complaints');
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      const errMsg = Array.isArray(detail) 
        ? detail.map(err => err.msg).join(', ') 
        : (detail || 'Failed to submit complaint');
      toast.error(errMsg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Report an Issue</h1>
        <p className={styles.subtitle}>Submit a new civic complaint to the KEELADI network.</p>
      </div>

      <div className={styles.content}>
        <Card className={styles.formCard}>
          <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
            
            <div className={styles.fieldGroup}>
              <Input
                label="Issue Title"
                placeholder="e.g. Overflowing bin on Main St"
                leftIcon={<Type size={18} />}
                error={errors.title?.message}
                {...register('title')}
              />
            </div>

            <div className={styles.fieldGroup}>
              <label className={styles.label}>Category</label>
              <select 
                className={[styles.select, errors.category ? styles.hasError : ''].join(' ')} 
                {...register('category')}
              >
                <option value="GARBAGE_OVERFLOW">Garbage Overflow</option>
                <option value="ILLEGAL_DUMPING">Illegal Dumping</option>
                <option value="BROKEN_BIN">Broken Bin</option>
                <option value="STREET_WASTE">Street Waste</option>
                <option value="DRAIN_BLOCKAGE">Drain Blockage</option>
                <option value="OTHER">Other</option>
              </select>
              {errors.category && <span className={styles.errorText}>{errors.category.message}</span>}
            </div>

            <div className={styles.fieldGroup}>
              <label className={styles.label}>Description (Optional)</label>
              <textarea 
                className={styles.textarea}
                placeholder="Provide additional details..."
                rows={4}
                {...register('description')}
              />
            </div>

            <div className={styles.locationSection}>
              <div className={styles.locationHeader}>
                <h3>Location Details</h3>
                <Button 
                  type="button" 
                  variant="secondary" 
                  size="sm" 
                  leftIcon={<Navigation size={14} />}
                  onClick={handleGetLocation}
                  isLoading={isLocating}
                >
                  Get Current GPS
                </Button>
              </div>
              
              <Input
                label="Address / Landmark"
                placeholder="Enter nearby landmark"
                leftIcon={<MapPin size={18} />}
                error={errors.address?.message}
                {...register('address')}
              />
              
              <div className={styles.coordinates}>
                <Input
                  label="Latitude"
                  type="number"
                  step="any"
                  readOnly
                  {...register('latitude', { valueAsNumber: true })}
                />
                <Input
                  label="Longitude"
                  type="number"
                  step="any"
                  readOnly
                  {...register('longitude', { valueAsNumber: true })}
                />
              </div>
              {(errors.latitude || errors.longitude) && (
                <span className={styles.errorText}>GPS Coordinates are required. Click 'Get Current GPS'.</span>
              )}
            </div>

            <div className={styles.actions}>
              <Button type="button" variant="ghost" onClick={() => router.back()}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={isLoading}>
                Submit Complaint
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
}
