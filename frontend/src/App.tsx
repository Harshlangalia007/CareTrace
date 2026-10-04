import React from 'react';
import { BrowserRouter, Routes, Route, useParams } from 'react-router-dom';
import Sidebar from './components/ui/Sidebar';
import Dashboard from './pages/Dashboard';
import PatientPage from './pages/PatientPage';
import './index.css';

const AppLayout: React.FC<{ children: React.ReactNode; currentPatientId?: string }> = ({
  children, currentPatientId
}) => (
  <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
    <Sidebar currentPatientId={currentPatientId} />
    <main style={{ flex: 1, overflow: 'auto', background: 'var(--bg)' }}>
      {children}
    </main>
  </div>
);

const PatientRoute: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>();
  return (
    <AppLayout currentPatientId={patientId}>
      <PatientPage />
    </AppLayout>
  );
};

const App: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={
        <AppLayout>
          <Dashboard />
        </AppLayout>
      } />
      <Route path="/patients" element={
        <AppLayout>
          <Dashboard />
        </AppLayout>
      } />
      <Route path="/patient/:patientId/*" element={<PatientRoute />} />
    </Routes>
  </BrowserRouter>
);

export default App;
