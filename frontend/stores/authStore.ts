/**
 * KEELADI Auth Store (Zustand)
 *
 * Persists: JWT token + user profile in sessionStorage
 * Provides: login, logout, hydrate actions
 */

import { create } from 'zustand';

export interface AuthUser {
  id: string;
  full_name: string;
  email: string;
  role: string;
  status: string;
  phone?: string;
  ward_id?: string;
  department_id?: string;
}

interface AuthState {
  token: string | null;
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (token: string, user: AuthUser) => void;
  logout: () => void;
  hydrate: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  isAuthenticated: false,

  login: (token, user) => {
    sessionStorage.setItem('keeladi_token', token);
    sessionStorage.setItem('keeladi_user', JSON.stringify(user));
    // Set cookie so Next.js middleware can read it
    document.cookie = `keeladi_token=${token}; path=/; max-age=86400; SameSite=Lax`;
    set({ token, user, isAuthenticated: true });
  },

  logout: () => {
    sessionStorage.removeItem('keeladi_token');
    sessionStorage.removeItem('keeladi_user');
    // Clear cookie
    document.cookie = 'keeladi_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    set({ token: null, user: null, isAuthenticated: false });
  },

  hydrate: () => {
    if (typeof window === 'undefined') return;
    const token = sessionStorage.getItem('keeladi_token');
    const userRaw = sessionStorage.getItem('keeladi_user');
    if (token && userRaw) {
      try {
        const user: AuthUser = JSON.parse(userRaw);
        set({ token, user, isAuthenticated: true });
      } catch {
        sessionStorage.clear();
      }
    }
  },
}));

/* Role helpers */
export const ROLES = {
  CITIZEN: 'CITIZEN',
  SANITATION_WORKER: 'SANITATION_WORKER',
  SUPERVISOR: 'SUPERVISOR',
  JUNIOR_ENGINEER: 'JUNIOR_ENGINEER',
  EXECUTIVE_ENGINEER: 'EXECUTIVE_ENGINEER',
  CHIEF_ENGINEER: 'CHIEF_ENGINEER',
  DRIVER: 'DRIVER',
  ADMIN: 'ADMIN',
} as const;

export type Role = keyof typeof ROLES;

export const hasRole = (user: AuthUser | null, roles: Role[]): boolean => {
  if (!user) return false;
  return roles.includes(user.role as Role);
};
