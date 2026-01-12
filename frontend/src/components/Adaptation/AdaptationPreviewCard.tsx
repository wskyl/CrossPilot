/**
 * Adaptation preview component
 */
import React from 'react';
import { Card, Tag, Input, Button, Space, Divider } from 'antd';
import { EditOutlined, CopyOutlined, CheckOutlined } from '@ant-design/icons';
import type { AdaptationPreview } from '@/types';

const { TextArea } = Input;

interface AdaptationPreviewCardProps {
  preview: AdaptationPreview;
  onTitleChange: (title: string) => void;
  onCaptionChange: (caption: string) => void;
  onHashtagsChange: (hashtags: string[]) => void;
}

const platformIcons: Record<string, string> = {
  douyin: '🎵',
  kuaishou: '⚡',
  xiaohongshu: '📕',
  weibo: '🔥',
  bilibili: '📺',
  wechat_video: '📱',
  wechat_article: '📝',
  zhihu: '🔍',
};

const AdaptationPreviewCard: React.FC<AdaptationPreviewCardProps> = ({
  preview,
  onTitleChange,
  onCaptionChange,
  onHashtagsChange,
}) => {
  const [isEditing, setIsEditing] = React.useState(false);
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    const text = `${preview.suggested_title}\n\n${preview.suggested_caption}\n\n${preview.suggested_hashtags.join(' ')}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card
      title={
        <div className="flex items-center gap-2">
          <span className="text-2xl">{platformIcons[preview.platform]}</span>
          <span>{preview.platform_config.display_name}</span>
          <Tag color="blue">{preview.platform_config.aspect_ratio}</Tag>
        </div>
      }
      extra={
        <Space>
          <Button
            icon={isEditing ? <CheckOutlined /> : <EditOutlined />}
            onClick={() => setIsEditing(!isEditing)}
          >
            {isEditing ? '完成' : '编辑'}
          </Button>
          <Button icon={copied ? <CheckOutlined /> : <CopyOutlined />} onClick={handleCopy}>
            {copied ? '已复制' : '复制'}
          </Button>
        </Space>
      }
    >
      <div className="space-y-4">
        {/* Title */}
        <div>
          <label className="text-sm text-gray-500 block mb-1">
            标题 (最多 {preview.platform_config.max_title_length} 字)
          </label>
          {isEditing ? (
            <Input
              value={preview.suggested_title}
              onChange={(e) => onTitleChange(e.target.value)}
              maxLength={preview.platform_config.max_title_length}
              showCount
            />
          ) : (
            <div className="text-lg font-medium">{preview.suggested_title}</div>
          )}
        </div>

        <Divider />

        {/* Caption */}
        <div>
          <label className="text-sm text-gray-500 block mb-1">
            文案{' '}
            {preview.platform_config.max_caption_length &&
              `(最多 ${preview.platform_config.max_caption_length} 字)`}
          </label>
          {isEditing ? (
            <TextArea
              value={preview.suggested_caption}
              onChange={(e) => onCaptionChange(e.target.value)}
              maxLength={preview.platform_config.max_caption_length || undefined}
              showCount
              rows={4}
            />
          ) : (
            <div className="text-gray-700 whitespace-pre-wrap">
              {preview.suggested_caption}
            </div>
          )}
        </div>

        <Divider />

        {/* Hashtags */}
        <div>
          <label className="text-sm text-gray-500 block mb-2">话题标签</label>
          <div className="flex flex-wrap gap-2">
            {preview.suggested_hashtags.map((tag, index) => (
              <Tag
                key={index}
                color="blue"
                closable={isEditing}
                onClose={() => {
                  const newTags = [...preview.suggested_hashtags];
                  newTags.splice(index, 1);
                  onHashtagsChange(newTags);
                }}
              >
                {tag}
              </Tag>
            ))}
          </div>
        </div>

        {/* Platform tips */}
        <div className="mt-4 p-3 bg-gray-50 rounded">
          <div className="text-sm text-gray-500">平台风格建议：</div>
          <div className="flex flex-wrap gap-1 mt-2">
            {preview.platform_config.style_keywords.map((keyword) => (
              <Tag key={keyword}>{keyword}</Tag>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
};

export default AdaptationPreviewCard;
