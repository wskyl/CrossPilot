/**
 * Authentication API services
 */
import apiClient from './api';
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '@/types';

export const authService = {
  async login(data: LoginRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/auth/login', data);
    return response.data;
  },

  async register(data: RegisterRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/auth/register', data);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },

  logout(): void {
    localStorage.removeItem('access_token');
  },

  setToken(token: string): void {
    localStorage.setItem('access_token', token);
  },

  getToken(): string | null {
    return localStorage.getItem('access_token');
  },

  isAuthenticated(): boolean {
    return !!this.getToken();
  },
};
