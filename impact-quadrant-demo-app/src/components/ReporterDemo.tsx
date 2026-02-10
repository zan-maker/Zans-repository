import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, ChevronRight, ChevronLeft, Search, 
  BarChart3, TrendingUp, DollarSign, Users
} from 'lucide-react';

const sampleQueries = [
  "Show me Q3 burn by entity with MoM comparison",
  "What's our customer acquisition cost by channel?",
  "Compare gross margin this quarter vs last year",
  "Show me overdue invoices over $10K"
];

export function ReporterDemo({ onNext, onBack }: { onNext: () => void; onBack: () => void }) {
  const [query, setQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [selectedQuery, setSelectedQuery] = useState('');

  const submitQuery = (q: string) => {
    setQuery(q);
    setSelectedQuery(q);
    setIsProcessing(true);
    setShowResults(false);
    
    setTimeout(() => {
      setIsProcessing(false);
      setShowResults(true);
    }, 2000);
  };

  const mockData = {
    entities: [
      { name: 'Parent Entity', july: 420000, august: 435000, september: 410000, total: 1265000 },
      { name: 'US Subsidiary', july: 180000, august: 195000, september: 188000, total: 563000 },
      { name: 'EU Subsidiary', july: 145000, august: 152000, september: 148000, total: 445000 },
      { name: 'APAC Sub', july: 95000, august: 102000, september: 98000, total: 295000 },
    ],
    total: { july: 840000, august: 884000, september: 844000, grandTotal: 2568000 }
  };

  return (
    <div className="section-container py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button onClick={onBack} className="btn-secondary text-sm">
            <ChevronLeft className="w-4 h-4 mr-1 inline" />
            Back
          </button>
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-amber-500 rounded-xl flex items-center justify-center">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Reporter Demo</h2>
              <p className="text-gray-500">Natural Language Reporting</p>
            </div>
          </div>
          <div className="w-24" />
        </div>

        {/* Query Input */}
        <div className="bg-white rounded-2xl p-8 shadow-lg mb-6">
          <h3 className="text-lg font-semibold mb-4">Ask Reporter anything about your finances</h3>
          
          <div className="relative mb-4">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && query && submitQuery(query)}
              placeholder="e.g., Show me Q3 burn by entity..."
              className="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent text-lg"
            />
            <button
              onClick={() => query && submitQuery(query)}
              disabled={!query || isProcessing}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-amber-500 text-white px-4 py-2 rounded-lg disabled:opacity-50"
            >
              Ask
            </button>
          </div>

          {/* Sample Queries */}
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-500 mr-2">Try:</span>
            {sampleQueries.map((q, idx) => (
              <button
                key={idx}
                onClick={() => submitQuery(q)}
                className="text-sm bg-gray-100 hover:bg-amber-100 text-gray-700 hover:text-amber-700 px-3 py-1 rounded-full transition-colors"
              >
                {q.length > 40 ? q.substring(0, 40) + '...' : q}
              </button>
            ))}
          </div>
        </div>

        {/* Processing State */}
        <AnimatePresence>
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="bg-white rounded-2xl p-8 shadow-lg mb-6"
            >
              <div className="flex items-center justify-center space-x-3 mb-4">
                <div className="w-8 h-8 border-4 border-amber-200 border-t-amber-500 rounded-full animate-spin" />
                <span className="text-lg font-medium">Reporter is analyzing...</span>
              </div>
              <div className="space-y-2 text-sm text-gray-600">
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}>
                  • Parsing: &quot;{selectedQuery}&quot;
                </motion.p>
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 }}>
                  • Identifying entities and metrics...
                </motion.p>
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.9 }}>
                  • Querying Netsuite data...
                </motion.p>
                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }}>
                  • Generizing visualization...
                </motion.p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {showResults && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-xl font-bold">Q3 2024 Burn by Entity</h3>
                  <p className="text-sm text-gray-500">Generated in 2.3 seconds • Live data from Netsuite</p>
                </div>
                <div className="flex space-x-2">
                  <button className="text-sm bg-gray-100 hover:bg-gray-200 px-3 py-2 rounded-lg">
                    Export to Sheets
                  </button>
                  <button className="text-sm bg-amber-500 text-white hover:bg-amber-600 px-3 py-2 rounded-lg">
                    Add to Deck
                  </button>
                </div>
              </div>

              {/* Chart Visualization */}
              <div className="bg-gray-50 rounded-xl p-6 mb-6">
                <div className="flex items-end justify-between h-48 space-x-4">
                  {mockData.entities.map((entity, idx) => (
                    <div key={idx} className="flex-1 flex flex-col items-center">
                      <div className="w-full flex space-x-1 h-40 items-end">
                        <motion.div
                          initial={{ height: 0 }}
                          animate={{ height: `${(entity.july / 450000) * 100}%` }}
                          transition={{ delay: idx * 0.1 }}
                          className="flex-1 bg-blue-300 rounded-t"
                          title={`July: $${entity.july.toLocaleString()}`}
                        />
                        <motion.div
                          initial={{ height: 0 }}
                          animate={{ height: `${(entity.august / 450000) * 100}%` }}
                          transition={{ delay: idx * 0.1 + 0.1 }}
                          className="flex-1 bg-blue-500 rounded-t"
                          title={`August: $${entity.august.toLocaleString()}`}
                        />
                        <motion.div
                          initial={{ height: 0 }}
                          animate={{ height: `${(entity.september / 450000) * 100}%` }}
                          transition={{ delay: idx * 0.1 + 0.2 }}
                          className="flex-1 bg-amber-500 rounded-t"
                          title={`September: $${entity.september.toLocaleString()}`}
                        />
                      </div>
                      <p className="text-xs mt-2 text-center font-medium">{entity.name}</p>
                    </div>
                  ))}
                </div>
                <div className="flex justify-center space-x-6 mt-4 text-sm">
                  <div className="flex items-center"><div className="w-3 h-3 bg-blue-300 rounded mr-2" /> July</div>
                  <div className="flex items-center"><div className="w-3 h-3 bg-blue-500 rounded mr-2" /> August</div>
                  <div className="flex items-center"><div className="w-3 h-3 bg-amber-500 rounded mr-2" /> September</div>
                </div>
              </div>

              {/* Data Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="text-left p-3 font-semibold">Entity</th>
                      <th className="text-right p-3 font-semibold">July</th>
                      <th className="text-right p-3 font-semibold">August</th>
                      <th className="text-right p-3 font-semibold">September</th>
                      <th className="text-right p-3 font-semibold">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mockData.entities.map((entity, idx) => (
                      <tr key={idx} className="border-b border-gray-100">
                        <td className="p-3 font-medium">{entity.name}</td>
                        <td className="text-right p-3">${(entity.july / 1000).toFixed(0)}K</td>
                        <td className="text-right p-3">${(entity.august / 1000).toFixed(0)}K</td>
                        <td className="text-right p-3">${(entity.september / 1000).toFixed(0)}K</td>
                        <td className="text-right p-3 font-bold">${(entity.total / 1000).toFixed(0)}K</td>
                      </tr>
                    ))}
                    <tr className="bg-gray-50 font-bold">
                      <td className="p-3">TOTAL</td>
                      <td className="text-right p-3">${(mockData.total.july / 1000).toFixed(0)}K</td>
                      <td className="text-right p-3">${(mockData.total.august / 1000).toFixed(0)}K</td>
                      <td className="text-right p-3">${(mockData.total.september / 1000).toFixed(0)}K</td>
                      <td className="text-right p-3 text-amber-600">${(mockData.total.grandTotal / 1000000).toFixed(2)}M</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Insights */}
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mt-6">
                <h4 className="font-semibold text-amber-800 mb-2 flex items-center">
                  <TrendingUp className="w-4 h-4 mr-2" />
                  AI-Generated Insights
                </h4>
                <ul className="space-y-2 text-sm text-amber-700">
                  <li>• EU burn increased 4.8% in August (new office lease)</li>
                  <li>• Parent entity burn down 5.7% in September (cost optimization)</li>
                  <li>• Q3 total burn 2.3% under budget</li>
                </ul>
              </div>

              {/* Time Saved */}
              <div className="bg-green-50 border border-green-200 rounded-xl p-4 mt-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
                      <span className="text-green-600 font-bold">⚡</span>
                    </div>
                    <div>
                      <p className="font-semibold text-green-800">Time Saved vs. Traditional Reporting</p>
                      <p className="text-sm text-green-600">What took 2-3 days now takes 2.3 seconds</p>
                    </div>
                  </div>
                  <p className="text-2xl font-bold text-green-700">99.9% faster</p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Navigation */}
        <div className="flex justify-between mt-6">
          <button onClick={onBack} className="btn-secondary">
            <ChevronLeft className="w-4 h-4 mr-2 inline" />
            Back: Reconciler
          </button>
          <button onClick={onNext} className="btn-primary">
            Next: Forecaster
            <ChevronRight className="w-4 h-4 ml-2 inline" />
          </button>
        </div>
      </div>
    </div>
  );
}