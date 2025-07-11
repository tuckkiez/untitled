import React, { useState } from 'react';
import {
  Layout,
  Typography,
  Tabs,
  Card,
  Row,
  Col,
  Statistic,
  Button,
  Space,
  FloatButton
} from 'antd';
import {
  TrophyOutlined,
  BarChartOutlined,
  SettingOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';

// Components
import MatchTable from '../components/MatchTable/MatchTable';
import PreviousResults from '../components/MatchTable/PreviousResults';
import AdminPanel from '../components/AdminPanel/AdminPanel';
import LeagueStats from '../components/Dashboard/LeagueStats';

// Services
import { leaguesAPI, matchesAPI } from '../services/api';
import { mockAPI } from '../services/mockData';

const { Header, Content } = Layout;
const { Title, Text } = Typography;

const Dashboard = () => {
  const [activeLeague, setActiveLeague] = useState('PL');
  const [adminVisible, setAdminVisible] = useState(false);

  // Fetch leagues
  const { data: leaguesData, isLoading: leaguesLoading } = useQuery({
    queryKey: ['leagues'],
    queryFn: mockAPI.getAllLeagues
  });

  // Fetch league data
  const { data: leagueData, isLoading: leagueLoading, refetch } = useQuery({
    queryKey: ['league-data', activeLeague],
    queryFn: () => mockAPI.getLeagueData(activeLeague),
    enabled: !!activeLeague
  });

  // Fetch upcoming matches
  const { data: upcomingMatches, isLoading: upcomingLoading } = useQuery({
    queryKey: ['upcoming-matches', activeLeague],
    queryFn: () => mockAPI.getUpcomingMatches({ leagueId: activeLeague }),
    enabled: !!activeLeague
  });

  // Fetch previous matches
  const { data: previousMatches, isLoading: previousLoading } = useQuery({
    queryKey: ['previous-matches', activeLeague],
    queryFn: () => mockAPI.getPreviousMatches({ leagueId: activeLeague }),
    enabled: !!activeLeague
  });

  const leagues = [
    { key: 'PL', label: '👑 Premier League', icon: '🏴󠁧󠁢󠁥󠁮󠁧󠁿' },
    { key: 'PD', label: '⭐ La Liga', icon: '🇪🇸' },
    { key: 'BL1', label: '🛡️ Bundesliga', icon: '🇩🇪' },
    { key: 'SA', label: '🏆 Serie A', icon: '🇮🇹' },
    { key: 'FL1', label: '🥇 Ligue 1', icon: '🇫🇷' }
  ];

  const currentLeague = leagues.find(l => l.key === activeLeague);

  return (
    <Layout style={{ minHeight: '100vh', background: 'transparent' }}>
      {/* Header */}
      <Header style={{
        background: 'rgba(20, 20, 30, 0.95)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        padding: '0 24px',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <Row justify="space-between" align="middle" style={{ height: '100%' }}>
          <Col>
            <Space size="large">
              <TrophyOutlined style={{ fontSize: '32px', color: '#64b5f6' }} />
              <Title level={2} style={{ margin: 0, color: '#e0e0e0' }}>
                Football Prediction Dashboard
              </Title>
            </Space>
          </Col>
          <Col>
            <Space>
              <Text style={{ color: '#b0b0b0' }}>1,750 Total Matches</Text>
              <Text style={{ color: '#b0b0b0' }}>•</Text>
              <Text style={{ color: '#b0b0b0' }}>5 Major Leagues</Text>
              <Text style={{ color: '#b0b0b0' }}>•</Text>
              <Text style={{ color: '#64b5f6', fontWeight: 'bold' }}>75% Best Accuracy</Text>
            </Space>
          </Col>
        </Row>
      </Header>

      {/* Content */}
      <Content style={{ padding: '24px' }}>
        {/* League Tabs */}
        <Card style={{ marginBottom: 24, background: 'rgba(20, 20, 30, 0.8)' }}>
          <Tabs
            activeKey={activeLeague}
            onChange={setActiveLeague}
            size="large"
            items={leagues.map(league => ({
              key: league.key,
              label: (
                <Space>
                  <span style={{ fontSize: '18px' }}>{league.icon}</span>
                  <span>{league.label}</span>
                </Space>
              )
            }))}
          />
        </Card>

        {/* League Statistics */}
        {leagueData && (
          <LeagueStats 
            data={leagueData.data} 
            leagueName={currentLeague?.label}
            loading={leagueLoading}
          />
        )}

        {/* Upcoming Matches */}
        <Card 
          title={
            <Space>
              <BarChartOutlined />
              <span>{currentLeague?.label} - Upcoming Predictions</span>
            </Space>
          }
          extra={
            <Button 
              icon={<ReloadOutlined />} 
              onClick={() => refetch()}
              loading={upcomingLoading}
            >
              Refresh
            </Button>
          }
          style={{ 
            marginBottom: 24,
            background: 'rgba(20, 20, 30, 0.8)',
            border: '1px solid rgba(255,255,255,0.1)'
          }}
        >
          <MatchTable 
            matches={upcomingMatches?.data || []}
            loading={upcomingLoading}
            type="upcoming"
          />
        </Card>

        {/* Previous Results */}
        <Card 
          title={
            <Space>
              <TrophyOutlined />
              <span>Previous Results (Last 2 Weeks)</span>
            </Space>
          }
          style={{ 
            background: 'rgba(20, 20, 30, 0.8)',
            border: '1px solid rgba(255,255,255,0.1)'
          }}
        >
          <PreviousResults 
            matches={previousMatches?.data || []}
            loading={previousLoading}
          />
        </Card>
      </Content>

      {/* Floating Admin Button */}
      <FloatButton
        icon={<SettingOutlined />}
        type="primary"
        style={{
          right: 24,
          bottom: 24,
          width: 60,
          height: 60,
          background: 'linear-gradient(45deg, #ff6b6b, #ee5a52)',
          border: 'none',
          boxShadow: '0 4px 15px rgba(255, 107, 107, 0.4)'
        }}
        onClick={() => setAdminVisible(true)}
        tooltip="Admin Panel"
      />

      {/* Admin Panel Modal */}
      <AdminPanel 
        visible={adminVisible}
        onClose={() => setAdminVisible(false)}
      />
    </Layout>
  );
};

export default Dashboard;
