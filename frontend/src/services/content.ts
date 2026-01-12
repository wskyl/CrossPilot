/**
 * Content API services
 */
import apiClient from './api';
import type { Content, Adaptation, AdaptationPreview, Platform, PlatformConfig, ContentType } from '@/types';

export const contentService = {
  async uploadContent(
    file: File,
    title: string,
    contentType: ContentType,
    description?: string
  ): Promise<Content> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('content_type', contentType);
    if (description) {
      formData.append('description', description);
    }

    const response = await apiClient.post<Content>('/contents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async listContents(skip = 0, limit = 20): Promise<Content[]> {
    const response = await apiClient.get<Content[]>('/contents/', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getContent(contentId: number): Promise<Content> {
    const response = await apiClient.get<Content>(`/contents/${contentId}`);
    return response.data;
  },

  async analyzeContent(contentId: number): Promise<Content> {
    const response = await apiClient.post<Content>(`/contents/${contentId}/analyze`);
    return response.data;
  },

  async previewAdaptations(
    contentId: number,
    targetPlatforms: Platform[]
  ): Promise<AdaptationPreview[]> {
    const response = await apiClient.post<AdaptationPreview[]>(
      `/contents/${contentId}/adapt/preview`,
      targetPlatforms
    );
    return response.data;
  },

  async createAdaptations(
    contentId: number,
    previews: AdaptationPreview[]
  ): Promise<Adaptation[]> {
    const response = await apiClient.post<Adaptation[]>(
      `/contents/${contentId}/adapt`,
      previews
    );
    return response.data;
  },

  async listContentAdaptations(contentId: number): Promise<Adaptation[]> {
    const response = await apiClient.get<Adaptation[]>(
      `/contents/${contentId}/adaptations`
    );
    return response.data;
  },

  async getPlatformConfigs(): Promise<PlatformConfig[]> {
    const response = await apiClient.get<PlatformConfig[]>('/contents/platforms/config');
    return response.data;
  },
};
