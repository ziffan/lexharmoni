import React from 'react';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 text-gray-900 p-8">
      <header className="text-center mb-12">
        <h1 className="text-6xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
          LexHarmoni
        </h1>
        <p className="text-2xl font-semibold mb-2">
          AI-Powered Regulatory Stress-Testing
        </p>
        <p className="text-lg text-gray-600">
          Test the impact, before it's enacted.
        </p>
      </header>

      <main className="max-w-xl text-center">
        <div className="bg-white rounded-xl shadow-lg p-10 border border-gray-100">
          <p className="text-xl font-medium text-gray-500 italic">
            Demo coming soon
          </p>
        </div>
      </main>

      <footer className="mt-16 text-sm text-gray-400">
        © 2026 LexHarmoni • Built for Regulatory Compliance Analysis
      </footer>
    </div>
  );
}
