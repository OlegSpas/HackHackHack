import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import HomePage from './components/pages/HomePage';
import LoadingPage from './components/pages/LoadingPage';
import VulnerabilityListPage from './components/pages/VulnerabilityListPage';
import VulnerabilityPage from './components/pages/VulnerabilityPage';

function App() {
  const VULNERABILITIES_LINK = "vulnerabilities"

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<HomePage />} />
        <Route path='/loading' element={<LoadingPage />} />
        <Route path='/vulnerabilities' element={<VulnerabilityListPage />} />
        <Route path={`${VULNERABILITIES_LINK}/:id`} element={<VulnerabilityPage />} />
      </Routes>
    </BrowserRouter>

  );
}

export default App;
