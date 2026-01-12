/**
 * Platform selection card component
 */
import React from 'react';
import { Card, Tag } from 'antd';
import { CheckCircleFilled } from '@ant-design/icons';
import type { PlatformConfig, Platform } from '@/types';

interface PlatformCardProps {
  config: PlatformConfig;
  selected: boolean;
  onSelect: (platform: Platform) => void;
}

const platformIcons: Record<Platform, string> = {
  douyin: '🎵',
  kuaishou: '⚡',
  xiaohongshu: '📕',
  weibo: '🔥',
  bilibili: '📺',
  wechat_video: '📱',
  wechat_article: '📝',
  zhihu: '🔍',
};

const PlatformCard: React.FC<PlatformCardProps> = ({ config, selected, onSelect }) => {
  return (
    <Card
      className={`platform-card ${selected ? 'selected' : ''}`}
      onClick={() => onSelect(config.platform)}
      hoverable
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{platformIcons[config.platform]}</span>
          <div>
            <h3 className="text-lg font-medium m-0">{config.display_name}</h3>
            <p className="text-gray-500 text-sm m-0 mt-1">
              {config.aspect_ratio} · {config.max_duration_seconds ? `${config.max_duration_seconds}秒` : '不限时长'}
            </p>
          </div>
        </div>
        {selected && <CheckCircleFilled className="text-primary text-xl" />}
      </div>
      <div className="mt-3 flex flex-wrap gap-1">
        {config.style_keywords.slice(0, 3).map((keyword) => (
          <Tag key={keyword} color="blue">
            {keyword}
          </Tag>
        ))}
      </div>
    </Card>
  );
};

export default PlatformCard;
