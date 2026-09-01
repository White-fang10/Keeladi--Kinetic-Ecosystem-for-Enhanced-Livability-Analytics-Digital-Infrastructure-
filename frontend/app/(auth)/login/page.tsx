'use client';

import React, { Suspense, useState } from 'react';
import { useForm as useReactHookForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useRouter, useSearchParams } from 'next/navigation';
import { Mail, Lock, ArrowRight } from 'lucide-react';
import toast from 'react-hot-toast';

import { apiLoginForm } from '@/lib/api';
import { useAuthStore } from '@/stores/authStore';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import styles from './page.module.css';
import Link from 'next/link';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

type LoginFormValues = z.infer<typeof loginSchema>;

// Inner component that uses useSearchParams — must be wrapped in Suspense
function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const login = useAuthStore((s) => s.login);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useReactHookForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormValues) => {
    try {
      setIsLoading(true);
      const res = await apiLoginForm(data.email, data.password);
      
      const token = res.access_token;
      sessionStorage.setItem('keeladi_token', token);
      
      const userRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const userData = await userRes.json();
      
      login(token, userData.data);
      toast.success('Welcome to KEELADI');
      
      const redirectTo = searchParams.get('redirect') || '/dashboard';
      router.push(redirectTo);
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      const errMsg = Array.isArray(detail)
        ? detail.map(err => err.msg).join(', ')
        : (detail || 'Invalid credentials');
      toast.error(errMsg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <Card padding="lg" className={styles.card}>
        <div className={styles.header}>
          <h2>Welcome Back</h2>
          <p>Sign in to access your dashboard</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
          <Input
            label="Email Address"
            type="email"
            placeholder="admin@keeladi.gov"
            leftIcon={<Mail size={18} />}
            error={errors.email?.message}
            autoComplete="email"
            {...register('email')}
          />

          <Input
            label="Password"
            type="password"
            placeholder="••••••••"
            leftIcon={<Lock size={18} />}
            error={errors.password?.message}
            autoComplete="current-password"
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
            Sign In
          </Button>
        </form>

        <div className={styles.footer}>
          <span>Don&apos;t have an account?</span>
          <Link href="/register" className={styles.link}>
            Register as Citizen
          </Link>
        </div>
      </Card>
    </div>
  );
}

// Page export wraps LoginForm in Suspense to satisfy Next.js static generation
export default function LoginPage() {
  return (
    <Suspense fallback={<div className="animate-pulse" />}>
      <LoginForm />
    </Suspense>
  );
}
