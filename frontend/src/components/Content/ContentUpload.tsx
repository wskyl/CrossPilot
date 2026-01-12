/**
 * Content upload component with drag and drop
 */
import React, { useState, useCallback } from 'react';
import { Upload, Button, Input, Select, message, Progress, Card } from 'antd';
import { InboxOutlined, CloudUploadOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import type { ContentType } from '@/types';
import { contentService } from '@/services/content';
import { useContentStore } from '@/hooks/useContent';

const { Dragger } = Upload;
const { TextArea } = Input;

const contentTypeOptions = [
  { value: 'video', label: '视频' },
  { value: 'article', label: '图文/文章' },
  { value: 'audio', label: '音频' },
  { value: 'image', label: '图片' },
  { value: 'live_recording', label: '直播录屏' },
  { value: 'notes', label: '灵感笔记' },
];

interface ContentUploadProps {
  onSuccess?: () => void;
}

const ContentUpload: React.FC<ContentUploadProps> = ({ onSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [contentType, setContentType] = useState<ContentType>('video');
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const { addContent } = useContentStore();

  const handleUpload = async () => {
    if (!file) {
      message.error('请先选择文件');
      return;
    }
    if (!title.trim()) {
      message.error('请输入内容标题');
      return;
    }

    setUploading(true);
    setProgress(0);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const content = await contentService.uploadContent(
        file,
        title,
        contentType,
        description || undefined
      );

      clearInterval(progressInterval);
      setProgress(100);

      addContent(content);
      message.success('内容上传成功，正在分析中...');

      // Reset form
      setFile(null);
      setTitle('');
      setDescription('');
      setProgress(0);

      onSuccess?.();
    } catch (error) {
      message.error('上传失败，请重试');
    } finally {
      setUploading(false);
    }
  };

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    showUploadList: false,
    beforeUpload: (file) => {
      setFile(file);
      // Auto-detect content type from file
      if (file.type.startsWith('video/')) {
        setContentType('video');
      } else if (file.type.startsWith('audio/')) {
        setContentType('audio');
      } else if (file.type.startsWith('image/')) {
        setContentType('image');
      }
      // Auto-fill title from filename
      if (!title) {
        setTitle(file.name.replace(/\.[^/.]+$/, ''));
      }
      return false; // Prevent auto upload
    },
    onDrop: (e) => {
      console.log('Dropped files', e.dataTransfer.files);
    },
  };

  return (
    <Card title="上传内容" className="max-w-2xl mx-auto">
      <div className="space-y-6">
        <Dragger {...uploadProps} className={file ? 'border-primary' : ''}>
          <p className="text-4xl text-gray-400">
            <InboxOutlined />
          </p>
          <p className="text-lg mt-4">
            {file ? file.name : '点击或拖拽文件到此区域上传'}
          </p>
          <p className="text-gray-500">
            支持视频、图片、音频、文档等多种格式
          </p>
        </Dragger>

        <div>
          <label className="block text-sm font-medium mb-2">内容类型</label>
          <Select
            value={contentType}
            onChange={setContentType}
            options={contentTypeOptions}
            style={{ width: '100%' }}
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">内容标题 *</label>
          <Input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="输入内容标题"
            maxLength={200}
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">内容描述</label>
          <TextArea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="输入内容描述（可选）"
            rows={4}
            maxLength={2000}
          />
        </div>

        {uploading && <Progress percent={progress} status="active" />}

        <Button
          type="primary"
          icon={<CloudUploadOutlined />}
          onClick={handleUpload}
          loading={uploading}
          disabled={!file || !title.trim()}
          size="large"
          block
        >
          {uploading ? '上传中...' : '上传并分析'}
        </Button>
      </div>
    </Card>
  );
};

export default ContentUpload;
