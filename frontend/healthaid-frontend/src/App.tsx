import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Landing from './pages/Landing';
import Layout from './components/layout';
import AuthLayout from './components/auth/authLayout';

function App() {
  return (
      <Routes>
        <Route path="/" element={<Landing />} />

      <Route element={<AuthLayout />}>
        <Route path="signup" element={<Signup />} />
        <Route path="login" element={<Login />} />
      </Route>

        {/* Protected/nested routes using Layout */}
      <Route path="/app" element={<Layout />}>
        <Route path="dashboard" element={<Dashboard />} />
      </Route>

      </Routes>
  );
}

export default App;
