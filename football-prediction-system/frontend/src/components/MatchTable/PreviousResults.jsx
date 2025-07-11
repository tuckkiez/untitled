import React from 'react';
import { Table, Tag, Space, Typography, Avatar } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';

const { Text } = Typography;

const PreviousResults = ({ matches, loading }) => {
  const getConfidenceColor = (confidence) => {
    if (confidence >= 75) return 'success';
    if (confidence >= 65) return 'success';
    if (confidence >= 50) return 'success';
    return 'error';
  };

  const getConfidenceStyle = (confidence) => {
    if (confidence >= 75) return { backgroundColor: '#095f00', borderColor: '#b7eb8f' };
    if (confidence >= 65) return { backgroundColor: '#095f00', borderColor: '#91d5ff' };
    if (confidence >= 50) return { backgroundColor: '#095f00', borderColor: '#ffd591' };
    return { backgroundColor: '#a11219', borderColor: '#ffccc7' };
  };

  const renderResultCell = (prediction, result) => {
    if (!prediction) return '-';

    const isCorrect = result?.isCorrect;
    
    return (
      <div style={{ 
        padding: '8px 12px', 
        borderRadius: '6px',
        ...getConfidenceStyle(prediction.confidence),
        position: 'relative',
        minHeight: '60px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        {/* Large Result Icon */}
        <div style={{ marginBottom: '4px' }}>
          {isCorrect === true ? (
            <Avatar 
              size={32}
              style={{ 
                backgroundColor: '#52c41a',
                boxShadow: '0 2px 8px rgba(82, 196, 26, 0.3)'
              }}
              icon={<CheckCircleOutlined />}
            />
          ) : isCorrect === false ? (
            <Avatar 
              size={32}
              style={{ 
                backgroundColor: '#ff4d4f',
                boxShadow: '0 2px 8px rgba(255, 77, 79, 0.3)'
              }}
              icon={<CloseCircleOutlined />}
            />
          ) : (
            <Avatar 
              size={32}
              style={{ 
                backgroundColor: '#faad14',
                boxShadow: '0 2px 8px rgba(250, 173, 20, 0.3)'
              }}
            >
              ?
            </Avatar>
          )}
        </div>
        
        {/* Prediction Text */}
        <div style={{ 
          fontSize: '11px', 
          fontWeight: '500', 
          marginBottom: '2px',
          textAlign: 'center',
          lineHeight: '1.2'
        }}>
          {prediction.prediction}
        </div>
        
        {/* Confidence Badge */}
        <Tag 
          color={getConfidenceColor(prediction.confidence)} 
          size="small"
          style={{ fontSize: '10px', margin: 0 }}
        >
          {prediction.confidence}%
        </Tag>
        
        {/* Actual Outcome */}
        {result?.actualOutcome && (
          <div style={{ 
            fontSize: '9px', 
            color: '#666', 
            marginTop: '2px',
            textAlign: 'center'
          }}>
            Actual: {result.actualOutcome}
          </div>
        )}
      </div>
    );
  };

  const columns = [
    {
      title: 'Match',
      dataIndex: 'match',
      key: 'match',
      width: 250,
      render: (_, record) => (
        <div>
          <div style={{ fontWeight: '600', marginBottom: '4px' }}>
            <Space>
              <Text>{record.homeTeam} vs {record.awayTeam}</Text>
              <Tag size="small" color="blue">#{record.id}</Tag>
            </Space>
          </div>
          <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>
            {dayjs(record.matchDate).format('MMM DD')} {record.matchTime}
          </div>
          {record.homeScore !== null && record.awayScore !== null && (
            <div style={{ 
              fontSize: '14px', 
              color: '#1890ff', 
              fontWeight: '700',
              padding: '2px 8px',
              backgroundColor: '#e6f7ff',
              borderRadius: '4px',
              display: 'inline-block'
            }}>
              {record.homeScore} - {record.awayScore}
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Match Result',
      dataIndex: 'matchResult',
      key: 'matchResult',
      width: 120,
      render: (_, record) => {
        const prediction = record.predictions?.find(p => p.category === 'MATCH_RESULT');
        const result = record.results?.find(r => r.category === 'MATCH_RESULT');
        return renderResultCell(prediction, result);
      },
    },
    {
      title: 'Handicap',
      dataIndex: 'handicap',
      key: 'handicap',
      width: 120,
      render: (_, record) => {
        const prediction = record.predictions?.find(p => p.category === 'HANDICAP');
        const result = record.results?.find(r => r.category === 'HANDICAP');
        return renderResultCell(prediction, result);
      },
    },
    {
      title: 'Over/Under',
      dataIndex: 'overUnder',
      key: 'overUnder',
      width: 120,
      render: (_, record) => {
        const prediction = record.predictions?.find(p => p.category === 'OVER_UNDER');
        const result = record.results?.find(r => r.category === 'OVER_UNDER');
        return renderResultCell(prediction, result);
      },
    },
    {
      title: 'Corners',
      dataIndex: 'corners',
      key: 'corners',
      width: 120,
      render: (_, record) => {
        const prediction = record.predictions?.find(p => p.category === 'CORNERS');
        const result = record.results?.find(r => r.category === 'CORNERS');
        return renderResultCell(prediction, result);
      },
    },
  ];

  return (
    <div>
      <Table
        columns={columns}
        dataSource={matches}
        loading={loading}
        rowKey="id"
        pagination={false}
        size="middle"
        scroll={{ x: 800 }}
        locale={{
          emptyText: 'No previous results available'
        }}
      />
      
      {matches && matches.length > 0 && (
        <div style={{ 
          marginTop: '16px', 
          padding: '12px', 
          backgroundColor: 'rgba(24, 144, 255, 0.1)', 
          borderRadius: '6px',
          fontSize: '12px',
          color: '#666'
        }}>
          <Space>
            <CheckCircleOutlined style={{ color: '#52c41a' }} />
            <span>Correct Prediction</span>
            <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
            <span>Incorrect Prediction</span>
            <span>•</span>
            <span>Showing results from last 2 weeks</span>
          </Space>
        </div>
      )}
    </div>
  );
};

export default PreviousResults;
