/**
 * Upload page component
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import ContentUpload from '@/components/Content/ContentUpload';

const UploadPage: React.FC = () => {
  const navigate = useNavigate();

  const handleUploadSuccess = () => {
    // Navigate to contents page after successful upload
    navigate('/contents');
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">上传内容</h1>
      <ContentUpload onSuccess={handleUploadSuccess} />
    </div>
  );
};

export default UploadPage;
