/**
 * Type definitions for API responses and requests
 */

// User types
export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  avatar_url: string | null;
  subscription_plan: SubscriptionPlan;
  monthly_conversions_used: number;
  monthly_conversions_limit: number;
  is_verified: boolean;
  created_at: string;
}

export type SubscriptionPlan = 'free' | 'professional' | 'team' | 'enterprise';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  full_name?: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// Content types
export type ContentType = 'video' | 'article' | 'audio' | 'image' | 'live_recording' | 'notes';
export type ContentStatus = 'pending' | 'analyzing' | 'ready' | 'error';
export type Platform = 'douyin' | 'kuaishou' | 'xiaohongshu' | 'weibo' | 'bilibili' | 'wechat_video' | 'wechat_article' | 'zhihu';
export type AdaptationStatus = 'pending' | 'processing' | 'completed' | 'published' | 'error';

export interface Content {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  content_type: ContentType;
  original_file_url: string;
  file_size: number | null;
  duration_seconds: number | null;
  status: ContentStatus;
  analysis_result: AnalysisResult | null;
  created_at: string;
  updated_at: string;
}

export interface AnalysisResult {
  key_points: string[];
  emotional_tone: string;
  main_topics: string[];
  visual_elements: string[];
  style_fingerprint: {
    language_style: string;
    visual_style: string;
    pace: string;
  };
  transcript?: string;
}

export interface PlatformConfig {
  platform: Platform;
  name: string;
  display_name: string;
  max_duration_seconds: number | null;
  aspect_ratio: string;
  max_title_length: number;
  max_caption_length: number | null;
  supported_formats: string[];
  style_keywords: string[];
}

export interface AdaptationPreview {
  platform: Platform;
  platform_config: PlatformConfig;
  suggested_title: string;
  suggested_caption: string;
  suggested_hashtags: string[];
  thumbnail_preview_url: string | null;
  estimated_duration_seconds: number | null;
}

export interface Adaptation {
  id: number;
  content_id: number;
  user_id: number;
  platform: Platform;
  title: string;
  caption: string | null;
  hashtags: string[] | null;
  adapted_file_url: string | null;
  thumbnail_url: string | null;
  status: AdaptationStatus;
  published_at: string | null;
  platform_post_url: string | null;
  analytics_data: AnalyticsData | null;
  created_at: string;
  updated_at: string;
}

export interface AnalyticsData {
  views: number;
  likes: number;
  comments: number;
  shares: number;
  saves: number;
  completion_rate?: number;
}
