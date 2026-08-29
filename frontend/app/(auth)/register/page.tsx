'use client';

import React, { useState } from 'react';
import { useForm as useReactHookForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useRouter } from 'next/navigation';
import { Mail, Lock, User, Phone, ArrowRight } from 'lucide-react';
import toast from 'react-hot-toast';

import { apiPost } from '@/lib/api';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import styles from './page.module.css';
import Link from 'next/link';

const registerSchema = z.object({
  full_name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  phone: z.string().optional(),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

type RegisterFormValues = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useReactHookForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormValues) => {
    try {
      setIsLoading(true);
      await apiPost('/auth/register', data);
      toast.success('Registration successful. Please login.');
      router.push('/login');
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      const errMsg = Array.isArray(detail) 
        ? detail.map(err => err.msg).join(', ') 
        : (detail || 'Registration failed');
      toast.error(errMsg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <Card padding="lg" className={styles.card}>
        <div className={styles.header}>
          <h2>Create Account</h2>
          <p>Join the KEELADI Citizen Network</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
          <Input
            label="Full Name"
            placeholder="John Doe"
            leftIcon={<User size={18} />}
            error={errors.full_name?.message}
            {...register('full_name')}
          />

          <Input
            label="Email Address"
            type="email"
            placeholder="john@example.com"
            leftIcon={<Mail size={18} />}
            error={errors.email?.message}
            {...register('email')}
          />

          <Input
            label="Phone Number (Optional)"
            placeholder="+91 9876543210"
            leftIcon={<Phone size={18} />}
            error={errors.phone?.message}
            {...register('phone')}
          />

          <Input
            label="Password"
            type="password"
            placeholder="••••••••"
            leftIcon={<Lock size={18} />}
            error={errors.password?.message}
            autoComplete="new-password"
            {...register('password')}
          />

          <Button
            type="submit"
            variant="primary"
            fullWidth
            isLoading={isLoading}
            rightIcon={<ArrowRight size={18} />}
            className={styles.submitBtn}
          >
            Register
          </Button>
        </form>

        <div className={styles.footer}>
          <span>Already have an account?</span>
          <Link href="/login" className={styles.link}>
            Sign In
          </Link>
        </div>
      </Card>
    </div>
  );
}
