import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth APIs
export const authAPI = {
  register: (data: { email: string; username: string; password: string }) =>
    api.post('/auth/register', data),

  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),

  googleAuth: (credential: string) =>
    api.post('/auth/google', { credential }),

  verifyEmail: (token: string) =>
    api.post('/auth/verify-email', { token }),

  resendVerification: (email: string) =>
    api.post('/auth/resend-verification', null, { params: { email } }),

  getCurrentUser: () =>
    api.get('/auth/me'),

  updateProfile: (data: {
    username?: string;
    full_name?: string;
    phone?: string;
    current_password?: string;
    new_password?: string;
  }) => api.put('/auth/me', data),

  // Password Reset APIs
  forgotPassword: (email: string) =>
    api.post('/auth/forgot-password', { email }),

  resetPassword: (token: string, new_password: string) =>
    api.post('/auth/reset-password', { token, new_password }),
};

// Portfolio APIs
export const portfolioAPI = {
  getOverview: () => api.get('/portfolio/overview'),
  getPerformanceHistory: (days: number = 30) => api.get(`/portfolio/performance-history?days=${days}`),
  getCategoryPerformanceHistory: (category: string, days: number = 30) => api.get(`/portfolio/performance-history/${category}?days=${days}`),
  getGainsSummary: () => api.get('/portfolio/gains-summary'),
  searchStocks: (query: string, limit: number = 10) => api.get(`/portfolio/search-stocks?q=${encodeURIComponent(query)}&limit=${limit}`),
  getByCategory: () => api.get('/portfolio/by-category'),
};

// Assets APIs
export const assetsAPI = {
  getAll: () => api.get('/assets/'),

  create: (data: {
    symbol: string;
    name: string;
    quantity: number;
    average_buy_price: number;
    asset_type: string;
    asset_category?: string;
    currency?: string;
    purchase_date?: string;
    remarks?: string;
  }) => api.post('/assets/', data),

  update: (id: number, data: any) => api.put(`/assets/${id}`, data),

  delete: (id: number) => api.delete(`/assets/${id}`),

  getAutoFillData: (symbol: string) => api.get(`/assets/auto-fill/${symbol}`),
};

// Transactions APIs
export const transactionsAPI = {
  getAll: (skip = 0, limit = 100) =>
    api.get(`/transactions/?skip=${skip}&limit=${limit}`),

  getById: (id: number) => api.get(`/transactions/${id}`),

  create: (data: {
    asset_id: number;
    transaction_type: 'buy' | 'sell';
    quantity: number;
    price_per_unit: number;
    notes?: string;
    transaction_date?: string;
  }) => api.post('/transactions/', data),
};

export default api;
