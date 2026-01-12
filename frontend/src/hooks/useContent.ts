/**
 * Content management store using Zustand
 */
import { create } from 'zustand';
import type { Content, Adaptation, Platform, PlatformConfig } from '@/types';

interface ContentState {
  contents: Content[];
  currentContent: Content | null;
  adaptations: Adaptation[];
  platformConfigs: PlatformConfig[];
  selectedPlatforms: Platform[];
  isLoading: boolean;

  setContents: (contents: Content[]) => void;
  addContent: (content: Content) => void;
  setCurrentContent: (content: Content | null) => void;
  setAdaptations: (adaptations: Adaptation[]) => void;
  setPlatformConfigs: (configs: PlatformConfig[]) => void;
  setSelectedPlatforms: (platforms: Platform[]) => void;
  togglePlatform: (platform: Platform) => void;
  setLoading: (loading: boolean) => void;
}

export const useContentStore = create<ContentState>((set) => ({
  contents: [],
  currentContent: null,
  adaptations: [],
  platformConfigs: [],
  selectedPlatforms: [],
  isLoading: false,

  setContents: (contents) => set({ contents }),

  addContent: (content) =>
    set((state) => ({ contents: [content, ...state.contents] })),

  setCurrentContent: (content) => set({ currentContent: content }),

  setAdaptations: (adaptations) => set({ adaptations }),

  setPlatformConfigs: (configs) => set({ platformConfigs: configs }),

  setSelectedPlatforms: (platforms) => set({ selectedPlatforms: platforms }),

  togglePlatform: (platform) =>
    set((state) => ({
      selectedPlatforms: state.selectedPlatforms.includes(platform)
        ? state.selectedPlatforms.filter((p) => p !== platform)
        : [...state.selectedPlatforms, platform],
    })),

  setLoading: (loading) => set({ isLoading: loading }),
}));
