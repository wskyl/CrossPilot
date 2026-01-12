/**
 * Content list page component
 */
import React, { useEffect, useState } from 'react';
import { Card, List, Tag, Button, Empty, Spin, Space, Modal, message } from 'antd';
import {
  PlayCircleOutlined,
  FileTextOutlined,
  AudioOutlined,
  PictureOutlined,
  ThunderboltOutlined,
  EyeOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import type { Content, ContentType, ContentStatus } from '@/types';
import { contentService } from '@/services/content';
import { useContentStore } from '@/hooks/useContent';

const contentTypeIcons: Record<ContentType, React.ReactNode> = {
  video: <PlayCircleOutlined />,
  article: <FileTextOutlined />,
  audio: <AudioOutlined />,
  image: <PictureOutlined />,
  live_recording: <PlayCircleOutlined />,
  notes: <FileTextOutlined />,
};

const contentTypeLabels: Record<ContentType, string> = {
  video: '视频',
  article: '图文',
  audio: '音频',
  image: '图片',
  live_recording: '直播录屏',
  notes: '笔记',
};

const statusColors: Record<ContentStatus, string> = {
  pending: 'default',
  analyzing: 'processing',
  ready: 'success',
  error: 'error',
};

const statusLabels: Record<ContentStatus, string> = {
  pending: '待处理',
  analyzing: '分析中',
  ready: '已就绪',
  error: '失败',
};

const ContentsPage: React.FC = () => {
  const navigate = useNavigate();
  const { contents, setContents, setCurrentContent, isLoading, setLoading } = useContentStore();
  const [selectedContent, setSelectedContent] = useState<Content | null>(null);

  useEffect(() => {
    loadContents();
  }, []);

  const loadContents = async () => {
    setLoading(true);
    try {
      const data = await contentService.listContents();
      setContents(data);
    } catch (error) {
      message.error('加载内容列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdapt = (content: Content) => {
    setCurrentContent(content);
    navigate(`/adapt/${content.id}`);
  };

  const handleView = (content: Content) => {
    setSelectedContent(content);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold m-0">内容管理</h1>
        <Button type="primary" onClick={() => navigate('/upload')}>
          上传新内容
        </Button>
      </div>

      {contents.length === 0 ? (
        <Empty
          description="还没有上传任何内容"
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        >
          <Button type="primary" onClick={() => navigate('/upload')}>
            立即上传
          </Button>
        </Empty>
      ) : (
        <List
          grid={{ gutter: 16, column: 3 }}
          dataSource={contents}
          renderItem={(content) => (
            <List.Item>
              <Card
                hoverable
                actions={[
                  <Button
                    key="view"
                    type="text"
                    icon={<EyeOutlined />}
                    onClick={() => handleView(content)}
                  >
                    查看
                  </Button>,
                  <Button
                    key="adapt"
                    type="text"
                    icon={<ThunderboltOutlined />}
                    onClick={() => handleAdapt(content)}
                    disabled={content.status !== 'ready'}
                  >
                    适配
                  </Button>,
                ]}
              >
                <Card.Meta
                  avatar={
                    <span className="text-2xl">
                      {contentTypeIcons[content.content_type]}
                    </span>
                  }
                  title={content.title}
                  description={
                    <Space direction="vertical" size="small">
                      <Tag>{contentTypeLabels[content.content_type]}</Tag>
                      <Tag color={statusColors[content.status]}>
                        {statusLabels[content.status]}
                      </Tag>
                      <span className="text-gray-400 text-xs">
                        {new Date(content.created_at).toLocaleDateString()}
                      </span>
                    </Space>
                  }
                />
              </Card>
            </List.Item>
          )}
        />
      )}

      {/* Content Detail Modal */}
      <Modal
        title={selectedContent?.title}
        open={!!selectedContent}
        onCancel={() => setSelectedContent(null)}
        footer={[
          <Button key="close" onClick={() => setSelectedContent(null)}>
            关闭
          </Button>,
          <Button
            key="adapt"
            type="primary"
            onClick={() => {
              if (selectedContent) {
                handleAdapt(selectedContent);
              }
            }}
            disabled={selectedContent?.status !== 'ready'}
          >
            开始适配
          </Button>,
        ]}
        width={600}
      >
        {selectedContent && (
          <div className="space-y-4">
            <div>
              <span className="text-gray-500">类型：</span>
              <Tag>{contentTypeLabels[selectedContent.content_type]}</Tag>
            </div>
            <div>
              <span className="text-gray-500">状态：</span>
              <Tag color={statusColors[selectedContent.status]}>
                {statusLabels[selectedContent.status]}
              </Tag>
            </div>
            {selectedContent.description && (
              <div>
                <span className="text-gray-500">描述：</span>
                <p>{selectedContent.description}</p>
              </div>
            )}
            {selectedContent.analysis_result && (
              <div>
                <span className="text-gray-500">分析结果：</span>
                <div className="mt-2 p-3 bg-gray-50 rounded">
                  <div className="mb-2">
                    <strong>核心观点：</strong>
                    <ul className="mt-1">
                      {selectedContent.analysis_result.key_points?.map((point, i) => (
                        <li key={i}>{point}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="mb-2">
                    <strong>情感基调：</strong>{' '}
                    {selectedContent.analysis_result.emotional_tone}
                  </div>
                  <div>
                    <strong>主要话题：</strong>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {selectedContent.analysis_result.main_topics?.map((topic, i) => (
                        <Tag key={i} color="blue">
                          {topic}
                        </Tag>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
};

export default ContentsPage;
