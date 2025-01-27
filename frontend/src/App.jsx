import React from 'react';
import ReportDashboard from './ReportDashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="container mx-auto py-4 px-4">
          <h1 className="text-2xl font-bold text-gray-900">AI/ML Opportunity Report Generator</h1>
        </div>
      </header>
      <main>
        <ReportDashboard />
      </main>
    </div>
  );
}

export default App;