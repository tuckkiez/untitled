import React from 'react';
import { Layout, Typography, Card, Button, Space } from 'antd';
import { ArrowLeftOutlined, SettingOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import AdminPanel from '../components/AdminPanel/AdminPanel';

const { Header, Content } = Layout;
const { Title, Text } = Typography;

const Admin = () => {
  const navigate = useNavigate();

  return (
    <Layout style={{ minHeight: '100vh', background: 'transparent' }}>
      {/* Header */}
      <Header style={{
        background: 'rgba(20, 20, 30, 0.95)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        padding: '0 24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <Space>
          <Button 
            icon={<ArrowLeftOutlined />} 
            onClick={() => navigate('/')}
            type="text"
            style={{ color: '#e0e0e0' }}
          >
            Back to Dashboard
          </Button>
          <Title level={2} style={{ margin: 0, color: '#e0e0e0' }}>
            <SettingOutlined style={{ marginRight: 8, color: '#64b5f6' }} />
            Admin Panel
          </Title>
        </Space>
      </Header>

      {/* Content */}
      <Content style={{ padding: '24px' }}>
        <Card 
          style={{ 
            background: 'rgba(20, 20, 30, 0.8)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: '16px'
          }}
        >
          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <Title level={3} style={{ color: '#64b5f6' }}>
              Football Prediction Admin
            </Title>
            <Text style={{ color: '#b0b0b0' }}>
              Manage prediction results and view system statistics
            </Text>
          </div>
          
          {/* Admin Panel Component */}
          <AdminPanel visible={true} onClose={() => navigate('/')} />
        </Card>
      </Content>
    </Layout>
  );
};

export default Admin;
