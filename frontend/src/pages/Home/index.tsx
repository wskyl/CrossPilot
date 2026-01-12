/**
 * Home page component
 */
import React from 'react';
import { Card, Row, Col, Statistic, Button, List, Tag } from 'antd';
import {
  CloudUploadOutlined,
  FileTextOutlined,
  ThunderboltOutlined,
  RiseOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/hooks/useAuth';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  const features = [
    {
      title: '智能内容解析',
      description: '自动提取关键信息、分析情感基调、识别风格特征',
      icon: '🧠',
    },
    {
      title: '多平台适配',
      description: '支持抖音、小红书、B站等8大主流平台',
      icon: '🎯',
    },
    {
      title: '一键转换',
      description: '自动调整格式、改写文案、生成标题和标签',
      icon: '⚡',
    },
    {
      title: '数据追踪',
      description: '跨平台数据分析、效果对比、智能优化建议',
      icon: '📊',
    },
  ];

  const quickActions = [
    {
      title: '上传视频',
      description: '长/短视频自动拆解，生成多平台版本',
      action: () => navigate('/upload'),
    },
    {
      title: '上传图文',
      description: '公众号文章一键转换为多平台内容',
      action: () => navigate('/upload'),
    },
    {
      title: '查看内容',
      description: '管理已上传的内容和适配结果',
      action: () => navigate('/contents'),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome section */}
      <Card>
        <Row gutter={24} align="middle">
          <Col flex="auto">
            <h1 className="text-2xl font-bold m-0">
              欢迎回来，{user?.username || '创作者'}！
            </h1>
            <p className="text-gray-500 mt-2">
              一次创作，全域共鸣。让AI帮你适配每个平台。
            </p>
          </Col>
          <Col>
            <Button
              type="primary"
              size="large"
              icon={<CloudUploadOutlined />}
              onClick={() => navigate('/upload')}
            >
              开始创作
            </Button>
          </Col>
        </Row>
      </Card>

      {/* Stats */}
      <Row gutter={16}>
        <Col span={6}>
          <Card>
            <Statistic
              title="本月转换次数"
              value={user?.monthly_conversions_used || 0}
              suffix={`/ ${user?.monthly_conversions_limit || 5}`}
              prefix={<ThunderboltOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已上传内容"
              value={0}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已生成适配"
              value={0}
              prefix={<RiseOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="当前套餐"
              value={user?.subscription_plan === 'free' ? '免费版' : '专业版'}
              valueStyle={{ fontSize: 20 }}
            />
          </Card>
        </Col>
      </Row>

      {/* Features */}
      <Card title="核心功能">
        <Row gutter={16}>
          {features.map((feature, index) => (
            <Col span={6} key={index}>
              <div className="text-center p-4">
                <div className="text-4xl mb-3">{feature.icon}</div>
                <h3 className="font-medium">{feature.title}</h3>
                <p className="text-gray-500 text-sm">{feature.description}</p>
              </div>
            </Col>
          ))}
        </Row>
      </Card>

      {/* Quick Actions */}
      <Card title="快速开始">
        <List
          grid={{ gutter: 16, column: 3 }}
          dataSource={quickActions}
          renderItem={(item) => (
            <List.Item>
              <Card
                hoverable
                onClick={item.action}
                className="text-center"
              >
                <h3 className="font-medium">{item.title}</h3>
                <p className="text-gray-500 text-sm m-0">{item.description}</p>
              </Card>
            </List.Item>
          )}
        />
      </Card>

      {/* Supported Platforms */}
      <Card title="支持平台">
        <div className="flex flex-wrap gap-4 justify-center">
          {[
            { name: '抖音', icon: '🎵' },
            { name: '快手', icon: '⚡' },
            { name: '小红书', icon: '📕' },
            { name: '微博', icon: '🔥' },
            { name: 'B站', icon: '📺' },
            { name: '视频号', icon: '📱' },
            { name: '公众号', icon: '📝' },
            { name: '知乎', icon: '🔍' },
          ].map((platform) => (
            <Tag key={platform.name} className="text-base py-2 px-4">
              {platform.icon} {platform.name}
            </Tag>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default HomePage;
