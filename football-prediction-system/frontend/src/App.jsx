import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider, theme } from 'antd';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

// Pages
import Dashboard from './pages/Dashboard';
import Admin from './pages/Admin';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Dark theme configuration
const darkTheme = {
  algorithm: theme.darkAlgorithm,
  token: {
    colorPrimary: '#64b5f6',
    colorBgBase: '#1a1a2e',
    colorBgContainer: '#16213e',
    colorBgElevated: '#0f3460',
    colorText: '#e0e0e0',
    colorTextSecondary: '#b0b0b0',
    colorBorder: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 12,
    fontSize: 14,
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
  },
  components: {
    Layout: {
      bodyBg: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
      headerBg: 'rgba(20, 20, 30, 0.95)',
      siderBg: 'rgba(20, 20, 30, 0.8)',
    },
    Card: {
      colorBgContainer: 'rgba(20, 20, 30, 0.8)',
      colorBorderSecondary: 'rgba(255, 255, 255, 0.1)',
    },
    Table: {
      colorBgContainer: 'rgba(20, 20, 30, 0.8)',
      colorBorderSecondary: 'rgba(255, 255, 255, 0.1)',
      headerBg: 'rgba(255, 255, 255, 0.05)',
    },
    Button: {
      colorPrimary: '#64b5f6',
      colorPrimaryHover: '#42a5f5',
      colorPrimaryActive: '#2196f3',
    },
    Select: {
      colorBgContainer: 'rgba(255, 255, 255, 0.1)',
      colorBorder: 'rgba(255, 255, 255, 0.2)',
    },
    Input: {
      colorBgContainer: 'rgba(255, 255, 255, 0.1)',
      colorBorder: 'rgba(255, 255, 255, 0.2)',
    },
    Modal: {
      colorBgElevated: 'rgba(20, 20, 30, 0.98)',
      colorBgMask: 'rgba(0, 0, 0, 0.7)',
    },
    Tabs: {
      colorBgContainer: 'rgba(255, 255, 255, 0.1)',
      colorBorderSecondary: 'rgba(255, 255, 255, 0.2)',
    }
  }
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider theme={darkTheme}>
        <Router>
          <div className="App" style={{ 
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)'
          }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/admin" element={<Admin />} />
            </Routes>
            
            {/* Toast notifications */}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: 'rgba(20, 20, 30, 0.95)',
                  color: '#e0e0e0',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '12px',
                  backdropFilter: 'blur(10px)',
                },
                success: {
                  iconTheme: {
                    primary: '#4caf50',
                    secondary: '#ffffff',
                  },
                },
                error: {
                  iconTheme: {
                    primary: '#f44336',
                    secondary: '#ffffff',
                  },
                },
              }}
            />
          </div>
        </Router>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

export default App;
