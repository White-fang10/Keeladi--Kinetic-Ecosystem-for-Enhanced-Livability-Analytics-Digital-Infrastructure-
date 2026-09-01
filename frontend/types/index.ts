/**
 * KEELADI Shared TypeScript Types
 * Mirrors the FastAPI Pydantic schemas exactly.
 */

/* ── Core ── */
export interface StandardResponse<T> {
  success: boolean;
  message?: string;
  data: T;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  total: number;
  page: number;
  per_page: number;
}

/* ── Auth ── */
export interface Token {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  full_name: string;
  email: string;
  phone?: string;
  role: string;
  status: string;
  ward_id?: string;
  department_id?: string;
  created_at: string;
  updated_at: string;
}

/* ── Complaint ── */
export type ComplaintStatus =
  | 'NEW' | 'ASSIGNED' | 'IN_PROGRESS' | 'VERIFICATION' | 'RESOLVED' | 'REJECTED' | 'ESCALATED';

export interface Complaint {
  id: string;
  reference_number: string;
  title: string;
  description?: string;
  category: string;
  priority?: string;
  status: ComplaintStatus;
  latitude: number;
  longitude: number;
  address?: string;
  ward_id?: string;
  user_id: string;
  ai_waste_type?: string;
  ai_severity?: number;
  ai_suggested_category?: string;
  ai_description?: string;
  ai_classified_at?: string;
  resolved_at?: string;
  created_at: string;
  updated_at: string;
}

export interface ComplaintHistory {
  id: string;
  complaint_id: string;
  from_status?: string;
  to_status: string;
  action: string;
  remarks?: string;
  changed_by: string;
  created_at: string;
}

export interface ComplaintCreate {
  title: string;
  description?: string;
  category: string;
  priority?: string;
  latitude: number;
  longitude: number;
  address?: string;
  ward_id?: string;
}

export interface ComplaintStatusUpdate {
  status: ComplaintStatus;
  remarks?: string;
}

/* ── Task ── */
export type TaskStatus = 'ASSIGNED' | 'STARTED' | 'VERIFICATION' | 'COMPLETED' | 'REASSIGNED';

export interface Task {
  id: string;
  complaint_id: string;
  worker_id: string;
  assigned_by: string;
  status: TaskStatus;
  priority?: string;
  deadline?: string;
  notes?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

/* ── Vehicle ── */
export type VehicleStatus = 'AVAILABLE' | 'COLLECTING' | 'FULL' | 'MAINTENANCE' | 'IDLE';

export interface Vehicle {
  id: string;
  registration_number: string;
  vehicle_type: string;
  capacity_kg: number;
  status: VehicleStatus;
  ward_id?: string;
  driver_id?: string;
  current_lat?: number;
  current_lng?: number;
  created_at: string;
  updated_at: string;
}

/* ── Verification ── */
export interface Verification {
  id: string;
  task_id: string;
  before_image_url?: string;
  before_lat?: number;
  before_lng?: number;
  before_captured_at?: string;
  after_image_url?: string;
  after_lat?: number;
  after_lng?: number;
  after_captured_at?: string;
  distance_from_complaint?: number;
  location_verified?: boolean;
  approval_status?: string;
  approved_by?: string;
  approval_remarks?: string;
  approved_at?: string;
  created_at: string;
}

/* ── Notification ── */
export interface Notification {
  id: string;
  user_id: string;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  read_at?: string;
  created_at: string;
}

/* ── Prediction ── */
export interface PredictionResult {
  id: string;
  ward_id: string;
  prediction_period: string;
  estimated_waste_kg: number;
  recommended_trucks: number;
  risk_level: string;
  confidence_score: number;
  recommendations: string;
  created_at: string;
}
