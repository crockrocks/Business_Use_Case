import React, { useState } from 'react';

const ReportDashboard = () => {
  const [companyName, setCompanyName] = useState('');
  const [industry, setIndustry] = useState('');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const generateReport = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await fetch('http://localhost:5000/api/generate-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company_name: companyName, industry }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      setReport(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-bold mb-4">AI/ML Opportunity Report Generator</h2>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Enter company name"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
          />
          <input
            type="text"
            placeholder="Enter industry"
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
          />
          <button
            onClick={generateReport}
            disabled={loading || !companyName || !industry}
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Generating...' : 'Generate Report'}
          </button>

          {error && (
            <div className="text-red-500 text-sm">
              {error}
            </div>
          )}
        </div>
      </div>
      {report && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-6">Report for {report.metadata.company_name}</h2>
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-2">Executive Summary</h3>
            <div className="bg-gray-50 p-4 rounded">
              <p>Industry: {report.metadata.industry}</p>
              <p>Generated: {new Date(report.metadata.generated_at).toLocaleString()}</p>
            </div>
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-2">Market Analysis</h3>
            <div className="space-y-4">
              <div className="bg-gray-50 p-4 rounded">
                <h4 className="font-medium mb-2">Key Findings</h4>
                <ul className="list-disc pl-6 space-y-2">
                  {report.research_summary.market_analysis.key_findings.map((finding, index) => (
                    <li key={index} className="text-gray-700">{finding}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-gray-50 p-4 rounded">
                <h4 className="font-medium mb-2">Sources</h4>
                <ul className="list-disc pl-6 space-y-2">
                  {report.research_summary.market_analysis.sources.map((source, index) => (
                    <li key={index}>
                      <a
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 hover:underline"
                      >
                        {source}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-2">Key Findings</h3>
            <ul className="list-disc pl-6 space-y-2">
              {report.research_summary.market_analysis.key_findings.map((finding, index) => (
                <li key={index} className="text-gray-700">{finding}</li>
              ))}
            </ul>
          </div>
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4">Use Cases</h3>
            <div className="space-y-4">
              {report.use_cases.map((useCase, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <h4 className="font-semibold mb-2">{useCase.title}</h4>
                  <p className="text-gray-600 mb-4">{useCase.description}</p>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div className="bg-gray-50 p-2 rounded">
                      <span className="font-medium">Priority:</span> {useCase.priority}
                    </div>
                    <div className="bg-gray-50 p-2 rounded">
                      <span className="font-medium">Complexity:</span> {useCase.complexity}
                    </div>
                    <div className="bg-gray-50 p-2 rounded">
                      <span className="font-medium">Timeline:</span> {useCase.estimated_timeline}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Available Resources</h3>
            <div className="space-y-4">
              {Object.entries(report.resources).map(([title, resources], index) => (
                <div key={index} className="border rounded-lg p-4">
                  <h4 className="font-semibold mb-2">{title}</h4>
                  {resources.datasets.length > 0 && (
                    <div className="mb-4">
                      <h5 className="font-medium mb-2">Datasets:</h5>
                      <ul className="list-disc pl-6">
                        {resources.datasets.map((dataset, i) => (
                          <li key={i} className="text-gray-700">{dataset.title}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {resources.research_papers.length > 0 && (
                    <div>
                      <h5 className="font-medium mb-2">Research Papers:</h5>
                      <ul className="list-disc pl-6">
                        {resources.research_papers.map((paper, i) => (
                          <li key={i} className="text-gray-700">{paper.title}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportDashboard;