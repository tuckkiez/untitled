import React from 'react';
import { Table, Tag, Space, Typography, Tooltip } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import './MatchTable.css';

const { Text } = Typography;

const MatchTable = ({ matches, loading, type = 'upcoming' }) => {
  const getConfidenceColor = (confidence) => {
    if (confidence >= 50) return 'success';  // เขียว - ผ่านเกณฑ์
    return 'error';                          // แดง - ไม่ผ่านเกณฑ์
  };

  const getConfidenceStyle = (confidence) => {
    if (confidence >= 80) return { 
      backgroundColor: 'rgba(82, 196, 26, 0.12)', 
      borderColor: 'rgba(82, 196, 26, 0.35)',
      color: '#95de64'
    };
    if (confidence >= 70) return { 
      backgroundColor: 'rgba(82, 196, 26, 0.10)', 
      borderColor: 'rgba(82, 196, 26, 0.30)',
      color: '#73d13d'
    };
    if (confidence >= 60) return { 
      backgroundColor: 'rgba(82, 196, 26, 0.08)', 
      borderColor: 'rgba(82, 196, 26, 0.25)',
      color: '#52c41a'
    };
    if (confidence >= 50) return { 
      backgroundColor: 'rgba(82, 196, 26, 0.06)', 
      borderColor: 'rgba(82, 196, 26, 0.20)',
      color: '#389e0d'
    };
    // ต่ำกว่า 50% = แดง
    return { 
      backgroundColor: 'rgba(255, 77, 79, 0.12)', 
      borderColor: 'rgba(255, 77, 79, 0.35)',
      color: '#ff7875'
    };
  };

  const renderPredictionCell = (prediction, result) => {
    if (!prediction) return '-';

    const hasResult = result && (result.isCorrect === true || result.isCorrect === false);
    const confidence = Math.round(prediction.confidence);
    
    return (
      <div 
        className="prediction-cell"
        style={{ 
          padding: '12px 14px', 
          borderRadius: '10px',
          border: '1px solid',
          ...getConfidenceStyle(confidence),
          position: 'relative',
          minHeight: '65px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}
      >
        {hasResult && (
          <div style={{ position: 'absolute', top: '8px', right: '8px' }}>
            {result.isCorrect ? (
              <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '16px' }} />
            ) : (
              <CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: '16px' }} />
            )}
          </div>
        )}
        
        <div style={{ 
          fontSize: '13px', 
          fontWeight: '600', 
          marginBottom: '8px',
          lineHeight: '1.3',
          paddingRight: hasResult ? '20px' : '0'
        }}>
          {prediction.prediction}
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Tag 
            color={getConfidenceColor(confidence)} 
            className={confidence >= 75 ? 'confidence-high' : confidence >= 60 ? 'confidence-good' : ''}
            style={{ 
              fontSize: '11px', 
              fontWeight: '600',
              margin: 0,
              padding: '3px 8px',
              borderRadius: '6px',
              border: 'none'
            }}
          >
            {confidence}%
          </Tag>
          
          {confidence >= 80 && (
            <span style={{ 
              fontSize: '11px', 
              color: '#95de64', 
              fontWeight: '700',
              textShadow: '0 0 4px rgba(149, 222, 100, 0.5)'
            }}>
              🔥 HOT
            </span>
          )}
          
          {confidence >= 70 && confidence < 80 && (
            <span style={{ 
              fontSize: '11px', 
              color: '#73d13d', 
              fontWeight: '600' 
            }}>
              ⭐ GOOD
            </span>
          )}
          
          {confidence < 50 && (
            <span style={{ 
              fontSize: '11px', 
              color: '#ff7875', 
              fontWeight: '600' 
            }}>
              ⚠️ LOW
            </span>
          )}
        </div>
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
        <div className="match-info">
          <div className="match-teams" style={{ marginBottom: '6px' }}>
            <Space>
              <Text style={{ color: '#ffffff', fontWeight: '600' }}>
                {record.homeTeam} vs {record.awayTeam}
              </Text>
              <Tag size="small" color="blue" style={{ borderRadius: '4px' }}>
                #{record.id}
              </Tag>
            </Space>
          </div>
          <div className="match-date" style={{ marginBottom: '4px' }}>
            📅 {dayjs(record.matchDate).format('MMM DD')} ⏰ {record.matchTime}
          </div>
          {record.homeScore !== null && record.awayScore !== null && (
            <div className="match-score">
              ⚽ Score: {record.homeScore} - {record.awayScore}
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Match Result',
      dataIndex: 'matchResult',
      key: 'matchResult',
      width: 150,
      render: (_, record) => {
        const prediction = record.predictions?.find(p => p.category === 'MATCH_RESULT');
        const result = record.results?.find(r => r.category === 'MATCH_RESULT');
        return renderPredictionCell(prediction, result);
      },
    },
    {
      title: 'Handicap',
      dataIndex: 'handicap',
      key: 'handicap',
      width: 150,
      render: (_, record) => {
        const prediction = record.predictions?.find(p => p.category === 'HANDICAP');
        const result = record.results?.find(r => r.category === 'HANDICAP');
        return renderPredictionCell(prediction, result);
      },
    },
    {
      title: 'Over/Under',
      dataIndex: 'overUnder',
      key: 'overUnder',
      width: 150,
      render: (_, record) => {
        const prediction = record.predictions?.find(p => p.category === 'OVER_UNDER');
        const result = record.results?.find(r => r.category === 'OVER_UNDER');
        return renderPredictionCell(prediction, result);
      },
    },
    {
      title: 'Corners',
      dataIndex: 'corners',
      key: 'corners',
      width: 150,
      render: (_, record) => {
        const prediction = record.predictions?.find(p => p.category === 'CORNERS');
        const result = record.results?.find(r => r.category === 'CORNERS');
        return renderPredictionCell(prediction, result);
      },
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={matches}
      loading={loading}
      rowKey="id"
      pagination={false}
      size="middle"
      scroll={{ x: 800 }}
      locale={{
        emptyText: type === 'upcoming' ? 'No upcoming matches' : 'No previous matches'
      }}
      style={{
        backgroundColor: 'transparent'
      }}
      className="dark-table"
      rowClassName={(record, index) => 
        index % 2 === 0 ? 'table-row-even' : 'table-row-odd'
      }
    />
  );
};

export default MatchTable;
