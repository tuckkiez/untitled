import React from 'react';
import { Row, Col, Card, Statistic, Progress, Tag } from 'antd';
import { 
  TrophyOutlined, 
  RiseOutlined, 
  AimOutlined, 
  HomeOutlined,
  MinusOutlined,
  CarOutlined
} from '@ant-design/icons';

const LeagueStats = ({ data, leagueName, loading }) => {
  const getStatColor = (value) => {
    if (value >= 80) return '#52c41a';  // เขียวเข้ม - ดีเยี่ยม
    if (value >= 70) return '#73d13d';  // เขียวกลาง - ดีมาก
    if (value >= 60) return '#95de64';  // เขียวอ่อน - ดี
    if (value >= 50) return '#b7eb8f';  // เขียวอ่อนมาก - ผ่านเกณฑ์
    return '#ff4d4f';                   // แดง - ต้องปรับปรุง
  };

  const getProgressStatus = (value) => {
    if (value >= 50) return 'success';  // เขียว - ผ่านเกณฑ์
    return 'exception';                 // แดง - ไม่ผ่านเกณฑ์
  };

  // Handle mock data structure
  const stats = data?.accuracy || {
    overall: 0,
    homeWin: 0,
    draw: 0,
    awayWin: 0,
    handicap: 0,
    overUnder: 0,
    corners: 0
  };

  const matchStats = {
    total: data?.totalMatches || 0,
    completed: data?.completedMatches || 0,
    upcoming: data?.upcomingMatches || 0
  };

  const overallAccuracy = Math.round(stats.overall || 0);

  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
      <Col xs={24} sm={12} md={6}>
        <Card loading={loading} style={{ 
          textAlign: 'center',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid rgba(255, 255, 255, 0.08)'
        }}>
          <Statistic
            title={
              <span>
                <TrophyOutlined style={{ marginRight: 6, color: '#faad14' }} />
                Overall Accuracy
              </span>
            }
            value={overallAccuracy}
            suffix="%"
            valueStyle={{ 
              color: getStatColor(overallAccuracy),
              fontSize: '24px',
              fontWeight: 'bold'
            }}
          />
          <Progress 
            percent={overallAccuracy} 
            showInfo={false} 
            status={getProgressStatus(overallAccuracy)}
            strokeWidth={8}
            style={{ marginTop: 12 }}
          />
          {overallAccuracy >= 80 && (
            <Tag color="success" style={{ marginTop: 8 }}>🔥 EXCELLENT</Tag>
          )}
          {overallAccuracy >= 60 && overallAccuracy < 80 && (
            <Tag color="success" style={{ marginTop: 8 }}>⭐ GOOD</Tag>
          )}
          {overallAccuracy < 50 && (
            <Tag color="error" style={{ marginTop: 8 }}>⚠️ NEEDS IMPROVEMENT</Tag>
          )}
        </Card>
      </Col>
      
      <Col xs={24} sm={12} md={6}>
        <Card loading={loading} style={{ 
          textAlign: 'center',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid rgba(255, 255, 255, 0.08)'
        }}>
          <Statistic
            title={
              <span>
                <HomeOutlined style={{ marginRight: 6, color: '#52c41a' }} />
                Home Win
              </span>
            }
            value={Math.round(stats.homeWin)}
            suffix="%"
            valueStyle={{ 
              color: getStatColor(stats.homeWin),
              fontSize: '20px',
              fontWeight: 'bold'
            }}
          />
          <Progress 
            percent={Math.round(stats.homeWin)} 
            showInfo={false} 
            status={getProgressStatus(stats.homeWin)}
            strokeWidth={6}
            style={{ marginTop: 12 }}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={12} md={6}>
        <Card loading={loading} style={{ 
          textAlign: 'center',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid rgba(255, 255, 255, 0.08)'
        }}>
          <Statistic
            title={
              <span>
                <AimOutlined style={{ marginRight: 6, color: '#1890ff' }} />
                Handicap
              </span>
            }
            value={Math.round(stats.handicap)}
            suffix="%"
            valueStyle={{ 
              color: getStatColor(stats.handicap),
              fontSize: '20px',
              fontWeight: 'bold'
            }}
          />
          <Progress 
            percent={Math.round(stats.handicap)} 
            showInfo={false} 
            status={getProgressStatus(stats.handicap)}
            strokeWidth={6}
            style={{ marginTop: 12 }}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={12} md={6}>
        <Card loading={loading} style={{ 
          textAlign: 'center',
          background: 'rgba(255, 255, 255, 0.02)',
          border: '1px solid rgba(255, 255, 255, 0.08)'
        }}>
          <Statistic
            title={
              <span>
                <RiseOutlined style={{ marginRight: 6, color: '#722ed1' }} />
                Over/Under
              </span>
            }
            value={Math.round(stats.overUnder)}
            suffix="%"
            valueStyle={{ 
              color: getStatColor(stats.overUnder),
              fontSize: '20px',
              fontWeight: 'bold'
            }}
          />
          <Progress 
            percent={Math.round(stats.overUnder)} 
            showInfo={false} 
            status={getProgressStatus(stats.overUnder)}
            strokeWidth={6}
            style={{ marginTop: 12 }}
          />
        </Card>
      </Col>

      {/* Match Statistics Row */}
      <Col xs={24} sm={8}>
        <Card loading={loading} style={{ 
          textAlign: 'center', 
          background: 'rgba(24, 144, 255, 0.06)',
          border: '1px solid rgba(24, 144, 255, 0.15)'
        }}>
          <Statistic
            title="Total Matches"
            value={matchStats.total}
            valueStyle={{ color: '#69c0ff', fontSize: '18px', fontWeight: 'bold' }}
            prefix={<TrophyOutlined />}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={8}>
        <Card loading={loading} style={{ 
          textAlign: 'center', 
          background: 'rgba(82, 196, 26, 0.06)',
          border: '1px solid rgba(82, 196, 26, 0.15)'
        }}>
          <Statistic
            title="Completed"
            value={matchStats.completed}
            valueStyle={{ color: '#95de64', fontSize: '18px', fontWeight: 'bold' }}
            prefix={<TrophyOutlined />}
          />
        </Card>
      </Col>
      
      <Col xs={24} sm={8}>
        <Card loading={loading} style={{ 
          textAlign: 'center', 
          background: 'rgba(250, 173, 20, 0.06)',
          border: '1px solid rgba(250, 173, 20, 0.15)'
        }}>
          <Statistic
            title="Upcoming"
            value={matchStats.upcoming}
            valueStyle={{ color: '#ffc53d', fontSize: '18px', fontWeight: 'bold' }}
            prefix={<RiseOutlined />}
          />
        </Card>
      </Col>
    </Row>
  );
};

export default LeagueStats;
