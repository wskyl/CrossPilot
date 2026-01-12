/**
 * Adaptation page component
 */
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Steps, Button, Row, Col, message, Spin, Result } from 'antd';
import { ArrowLeftOutlined, CheckOutlined } from '@ant-design/icons';
import type { Content, Platform, AdaptationPreview } from '@/types';
import { contentService } from '@/services/content';
import { useContentStore } from '@/hooks/useContent';
import PlatformCard from '@/components/Platform/PlatformCard';
import AdaptationPreviewCard from '@/components/Adaptation/AdaptationPreviewCard';

const AdaptPage: React.FC = () => {
  const { contentId } = useParams<{ contentId: string }>();
  const navigate = useNavigate();

  const {
    currentContent,
    setCurrentContent,
    platformConfigs,
    setPlatformConfigs,
    selectedPlatforms,
    setSelectedPlatforms,
    togglePlatform,
  } = useContentStore();

  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [previews, setPreviews] = useState<AdaptationPreview[]>([]);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    loadData();
  }, [contentId]);

  const loadData = async () => {
    setLoading(true);
    try {
      // Load platform configs
      const configs = await contentService.getPlatformConfigs();
      setPlatformConfigs(configs);

      // Load content if not already loaded
      if (!currentContent || currentContent.id !== Number(contentId)) {
        const content = await contentService.getContent(Number(contentId));
        setCurrentContent(content);
      }
    } catch (error) {
      message.error('加载数据失败');
      navigate('/contents');
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePreview = async () => {
    if (selectedPlatforms.length === 0) {
      message.warning('请至少选择一个平台');
      return;
    }

    setLoading(true);
    try {
      const result = await contentService.previewAdaptations(
        Number(contentId),
        selectedPlatforms
      );
      setPreviews(result);
      setCurrentStep(1);
    } catch (error) {
      message.error('生成预览失败');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAdaptations = async () => {
    setLoading(true);
    try {
      await contentService.createAdaptations(Number(contentId), previews);
      setCompleted(true);
      setCurrentStep(2);
      message.success('适配内容创建成功！');
    } catch (error) {
      message.error('创建适配失败');
    } finally {
      setLoading(false);
    }
  };

  const updatePreview = (
    index: number,
    field: 'suggested_title' | 'suggested_caption' | 'suggested_hashtags',
    value: string | string[]
  ) => {
    const newPreviews = [...previews];
    newPreviews[index] = { ...newPreviews[index], [field]: value };
    setPreviews(newPreviews);
  };

  if (loading && !currentContent) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spin size="large" />
      </div>
    );
  }

  if (completed) {
    return (
      <Result
        status="success"
        title="适配内容创建成功！"
        subTitle={`已为 ${previews.length} 个平台生成适配内容`}
        extra={[
          <Button key="back" onClick={() => navigate('/contents')}>
            返回内容列表
          </Button>,
          <Button
            key="new"
            type="primary"
            onClick={() => {
              setCompleted(false);
              setCurrentStep(0);
              setSelectedPlatforms([]);
              setPreviews([]);
            }}
          >
            继续适配其他平台
          </Button>,
        ]}
      />
    );
  }

  return (
    <div>
      <Button
        icon={<ArrowLeftOutlined />}
        onClick={() => navigate('/contents')}
        className="mb-4"
      >
        返回
      </Button>

      <Card className="mb-6">
        <h1 className="text-xl font-bold m-0">{currentContent?.title}</h1>
        <p className="text-gray-500 mt-2">{currentContent?.description}</p>
      </Card>

      <Steps
        current={currentStep}
        items={[
          { title: '选择平台' },
          { title: '预览调整' },
          { title: '完成' },
        ]}
        className="mb-8"
      />

      {currentStep === 0 && (
        <div>
          <h2 className="text-lg font-medium mb-4">
            选择目标平台 ({selectedPlatforms.length} 已选)
          </h2>
          <Row gutter={[16, 16]}>
            {platformConfigs.map((config) => (
              <Col span={6} key={config.platform}>
                <PlatformCard
                  config={config}
                  selected={selectedPlatforms.includes(config.platform)}
                  onSelect={togglePlatform}
                />
              </Col>
            ))}
          </Row>
          <div className="mt-6 text-right">
            <Button
              type="primary"
              size="large"
              onClick={handleGeneratePreview}
              loading={loading}
              disabled={selectedPlatforms.length === 0}
            >
              生成适配预览
            </Button>
          </div>
        </div>
      )}

      {currentStep === 1 && (
        <div>
          <h2 className="text-lg font-medium mb-4">预览并调整</h2>
          <Row gutter={[16, 16]}>
            {previews.map((preview, index) => (
              <Col span={12} key={preview.platform}>
                <AdaptationPreviewCard
                  preview={preview}
                  onTitleChange={(title) =>
                    updatePreview(index, 'suggested_title', title)
                  }
                  onCaptionChange={(caption) =>
                    updatePreview(index, 'suggested_caption', caption)
                  }
                  onHashtagsChange={(hashtags) =>
                    updatePreview(index, 'suggested_hashtags', hashtags)
                  }
                />
              </Col>
            ))}
          </Row>
          <div className="mt-6 flex justify-between">
            <Button onClick={() => setCurrentStep(0)}>上一步</Button>
            <Button
              type="primary"
              size="large"
              icon={<CheckOutlined />}
              onClick={handleCreateAdaptations}
              loading={loading}
            >
              确认创建适配
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdaptPage;
