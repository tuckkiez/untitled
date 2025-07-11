import React, { useState, useEffect } from 'react';
import {
  Modal,
  Form,
  Select,
  Button,
  Card,
  Typography,
  Space,
  Divider,
  Alert,
  Spin,
  Tag,
  Row,
  Col,
  Statistic
} from 'antd';
import {
  SettingOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  BarChartOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { adminAPI } from '../../services/api';

const { Title, Text } = Typography;
const { Option } = Select;

const AdminPanel = ({ visible, onClose }) => {
  const [form] = Form.useForm();
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [showStats, setShowStats] = useState(false);
  const queryClient = useQueryClient();

  // Fetch matches for dropdown
  const { data: matchesData, isLoading: matchesLoading } = useQuery({
    queryKey: ['admin-matches'],
    queryFn: () => adminAPI.getAllMatches(),
    enabled: visible
  });

  // Fetch categories for dropdown
  const { data: categoriesData } = useQuery({
    queryKey: ['admin-categories'],
    queryFn: () => adminAPI.getCategories(),
    enabled: visible
  });

  // Fetch match details when match is selected
  const { data: matchDetails, isLoading: detailsLoading } = useQuery({
    queryKey: ['match-details', selectedMatch],
    queryFn: () => adminAPI.getMatchDetails(selectedMatch),
    enabled: !!selectedMatch
  });

  // Fetch accuracy stats
  const { data: statsData, isLoading: statsLoading } = useQuery({
    queryKey: ['accuracy-stats'],
    queryFn: () => adminAPI.getAccuracyStats(),
    enabled: showStats
  });

  // Update result mutation
  const updateResultMutation = useMutation({
    mutationFn: adminAPI.updatePredictionResult,
    onSuccess: () => {
      toast.success('Result updated successfully!');
      queryClient.invalidateQueries(['admin-matches']);
      queryClient.invalidateQueries(['match-details']);
      queryClient.invalidateQueries(['accuracy-stats']);
      form.resetFields();
      setSelectedMatch(null);
    },
    onError: (error) => {
      toast.error(error.response?.data?.error || 'Failed to update result');
    }
  });

  const handleMatchSelect = (matchId) => {
    setSelectedMatch(matchId);
    form.setFieldsValue({ matchId });
  };

  const handleSubmit = async (values) => {
    try {
      await updateResultMutation.mutateAsync({
        matchId: values.matchId,
        category: values.category,
        isCorrect: values.result === 'correct',
        actualOutcome: values.actualOutcome || '',
        updatedBy: 'admin'
      });
    } catch (error) {
      // Error handled in mutation
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 75) return '#4caf50';
    if (confidence >= 65) return '#64b5f6';
    if (confidence >= 50) return '#ff9800';
    return '#f44336';
  };

  const getResultIcon = (result) => {
    if (result?.isCorrect === true) {
      return <CheckCircleOutlined style={{ color: '#4caf50', fontSize: '18px' }} />;
    }
    if (result?.isCorrect === false) {
      return <CloseCircleOutlined style={{ color: '#f44336', fontSize: '18px' }} />;
    }
    return null;
  };

  return (
    <Modal
      title={
        <Space>
          <SettingOutlined />
          <span>Admin Panel</span>
        </Space>
      }
      open={visible}
      onCancel={onClose}
      width={800}
      footer={null}
      destroyOnClose
    >
      <div style={{ maxHeight: '70vh', overflowY: 'auto' }}>
        {/* Quick Stats */}
        {statsData && (
          <Card size="small" style={{ marginBottom: 16 }}>
            <Row gutter={16}>
              <Col span={6}>
                <Statistic
                  title="Overall Accuracy"
                  value={statsData.data.overall.accuracy}
                  suffix="%"
                  valueStyle={{ color: getConfidenceColor(statsData.data.overall.accuracy) }}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="Total Predictions"
                  value={statsData.data.overall.total}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="Correct"
                  value={statsData.data.overall.correct}
                  valueStyle={{ color: '#4caf50' }}
                />
              </Col>
              <Col span={6}>
                <Button
                  icon={<BarChartOutlined />}
                  onClick={() => setShowStats(!showStats)}
                  type={showStats ? 'primary' : 'default'}
                >
                  {showStats ? 'Hide' : 'Show'} Stats
                </Button>
              </Col>
            </Row>
          </Card>
        )}

        {/* Update Form */}
        <Card title="Update Prediction Result" size="small">
          <Form
            form={form}
            layout="vertical"
            onFinish={handleSubmit}
            disabled={updateResultMutation.isPending}
          >
            <Form.Item
              name="matchId"
              label="Select Match"
              rules={[{ required: true, message: 'Please select a match' }]}
            >
              <Select
                placeholder="Search and select a match..."
                showSearch
                loading={matchesLoading}
                filterOption={(input, option) =>
                  option?.children?.toLowerCase().includes(input.toLowerCase())
                }
                onChange={handleMatchSelect}
                size="large"
              >
                {matchesData?.data?.map(match => (
                  <Option key={match.id} value={match.id}>
                    <Space>
                      <Text strong>#{match.id}</Text>
                      <Text>{match.homeTeam} vs {match.awayTeam}</Text>
                      <Tag color="blue">{match.league}</Tag>
                      <Tag color={match.status === 'FINISHED' ? 'green' : 'orange'}>
                        {match.status}
                      </Tag>
                    </Space>
                  </Option>
                ))}
              </Select>
            </Form.Item>

            {/* Match Details */}
            {matchDetails && (
              <Card size="small" style={{ marginBottom: 16, backgroundColor: 'rgba(100, 181, 246, 0.1)' }}>
                <Title level={5}>
                  {matchDetails.data.homeTeam} vs {matchDetails.data.awayTeam}
                </Title>
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Text>
                    <strong>League:</strong> {matchDetails.data.league.name}
                  </Text>
                  <Text>
                    <strong>Date:</strong> {new Date(matchDetails.data.matchDate).toLocaleDateString()} {matchDetails.data.matchTime}
                  </Text>
                  {matchDetails.data.homeScore !== null && (
                    <Text>
                      <strong>Score:</strong> {matchDetails.data.homeScore} - {matchDetails.data.awayScore}
                    </Text>
                  )}
                  
                  <Divider />
                  
                  <Title level={5}>Current Predictions:</Title>
                  {matchDetails.data.predictions.map(prediction => (
                    <div key={prediction.category} style={{ 
                      padding: '8px 12px', 
                      border: '1px solid rgba(255,255,255,0.1)', 
                      borderRadius: '8px',
                      marginBottom: '8px',
                      backgroundColor: 'rgba(255,255,255,0.05)'
                    }}>
                      <Space style={{ width: '100%', justifyContent: 'space-between' }}>
                        <Space>
                          <Text strong>{prediction.category.replace('_', ' ')}</Text>
                          <Text>{prediction.prediction}</Text>
                          <Tag color={getConfidenceColor(prediction.confidence)}>
                            {prediction.confidence}%
                          </Tag>
                        </Space>
                        <Space>
                          {getResultIcon(prediction.result)}
                          {prediction.result && (
                            <Text type={prediction.result.isCorrect ? 'success' : 'danger'}>
                              {prediction.result.isCorrect ? 'Correct' : 'Incorrect'}
                            </Text>
                          )}
                        </Space>
                      </Space>
                    </div>
                  ))}
                </Space>
              </Card>
            )}

            <Row gutter={16}>
              <Col span={12}>
                <Form.Item
                  name="category"
                  label="Category"
                  rules={[{ required: true, message: 'Please select a category' }]}
                >
                  <Select placeholder="Select category" size="large">
                    {categoriesData?.data?.map(category => (
                      <Option key={category.value} value={category.value}>
                        {category.label}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  name="result"
                  label="Result"
                  rules={[{ required: true, message: 'Please select result' }]}
                >
                  <Select placeholder="Select result" size="large">
                    <Option value="correct">
                      <Space>
                        <CheckCircleOutlined style={{ color: '#4caf50' }} />
                        Correct
                      </Space>
                    </Option>
                    <Option value="incorrect">
                      <Space>
                        <CloseCircleOutlined style={{ color: '#f44336' }} />
                        Incorrect
                      </Space>
                    </Option>
                  </Select>
                </Form.Item>
              </Col>
            </Row>

            <Form.Item
              name="actualOutcome"
              label="Actual Outcome (Optional)"
            >
              <Select placeholder="What actually happened?" allowClear size="large">
                <Option value="Home Win">Home Win</Option>
                <Option value="Draw">Draw</Option>
                <Option value="Away Win">Away Win</Option>
                <Option value="Over 2.5">Over 2.5</Option>
                <Option value="Under 2.5">Under 2.5</Option>
                <Option value="Over 9.5 Corners">Over 9.5 Corners</Option>
                <Option value="Under 9.5 Corners">Under 9.5 Corners</Option>
              </Select>
            </Form.Item>

            <Form.Item>
              <Space>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={updateResultMutation.isPending}
                  size="large"
                >
                  Update Result
                </Button>
                <Button
                  onClick={() => {
                    form.resetFields();
                    setSelectedMatch(null);
                  }}
                  size="large"
                >
                  Clear
                </Button>
                <Button
                  icon={<ReloadOutlined />}
                  onClick={() => {
                    queryClient.invalidateQueries(['admin-matches']);
                    queryClient.invalidateQueries(['accuracy-stats']);
                  }}
                  size="large"
                >
                  Refresh
                </Button>
              </Space>
            </Form.Item>
          </Form>
        </Card>

        {/* Detailed Stats */}
        {showStats && statsData && (
          <Card title="Detailed Statistics" size="small">
            <Row gutter={16}>
              <Col span={12}>
                <Title level={5}>By Category</Title>
                {Object.entries(statsData.data.byCategory).map(([category, stats]) => (
                  <div key={category} style={{ marginBottom: 8 }}>
                    <Space style={{ width: '100%', justifyContent: 'space-between' }}>
                      <Text>{category.replace('_', ' ')}</Text>
                      <Space>
                        <Text>{stats.correct}/{stats.total}</Text>
                        <Tag color={getConfidenceColor(stats.accuracy)}>
                          {stats.accuracy}%
                        </Tag>
                      </Space>
                    </Space>
                  </div>
                ))}
              </Col>
              <Col span={12}>
                <Title level={5}>By League</Title>
                {Object.entries(statsData.data.byLeague).map(([league, stats]) => (
                  <div key={league} style={{ marginBottom: 8 }}>
                    <Space style={{ width: '100%', justifyContent: 'space-between' }}>
                      <Text>{league}</Text>
                      <Space>
                        <Text>{stats.correct}/{stats.total}</Text>
                        <Tag color={getConfidenceColor(stats.accuracy)}>
                          {stats.accuracy}%
                        </Tag>
                      </Space>
                    </Space>
                  </div>
                ))}
              </Col>
            </Row>
          </Card>
        )}

        {/* Help */}
        <Alert
          message="How to use Admin Panel"
          description={
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              <li>Select a match from the dropdown (shows Match ID, teams, league, and status)</li>
              <li>View current predictions and their confidence levels</li>
              <li>Choose the prediction category you want to update</li>
              <li>Mark as Correct ✓ or Incorrect ✗</li>
              <li>Optionally specify what actually happened</li>
              <li>Click "Update Result" to save</li>
            </ul>
          }
          type="info"
          showIcon
          style={{ marginTop: 16 }}
        />
      </div>
    </Modal>
  );
};

export default AdminPanel;
