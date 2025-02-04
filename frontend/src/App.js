import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
// import SlugSeiCoach from './components/SlugSeiCoach';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        {/* <Route path="/baseball-ai" element={<SlugSeiCoach />} /> */}
      </Routes>
    </Router>
  );
};

export default App;
