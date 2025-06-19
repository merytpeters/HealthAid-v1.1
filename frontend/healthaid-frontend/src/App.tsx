import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Landing from './pages/Landing';
import Layout from './components/layout';

function App() {
  return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/" element={<Landing />} />

        {/* Protected/nested routes using Layout */}
      <Route path="/app" element={<Layout />}>
        <Route path="dashboard" element={<Dashboard />} />
      </Route>

      </Routes>
  );
}

export default App;
