import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Scale, ChevronRight, ChevronLeft, Clock, 
  CheckCircle, AlertTriangle, RefreshCw
} from 'lucide-react';

export function ReconcilerDemo({ onNext, onBack }: { onNext: () => void; onBack: () => void }) {
  const [step, setStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [matchedCount, setMatchedCount] = useState(0);
  const [showResults, setShowResults] = useState(false);

  const startReconciliation = () => {
    setIsProcessing(true);
    setStep(1);
    
    // Simulate processing
    let prog = 0;
    const interval = setInterval(() => {
      prog += 2;
      setProgress(prog);
      setMatchedCount(Math.floor((prog / 100) * 4789));
      
      if (prog >= 100) {
        clearInterval(interval);
        setIsProcessing(false);
        setShowResults(true);
        setStep(2);
      }
    }, 80);
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
            <div className="w-10 h-10 bg-emerald-500 rounded-xl flex items-center justify-center">
              <Scale className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Reconciler Demo</h2>
              <p className="text-gray-500">Month-End Close Transformation</p>
            </div>
          </div>
          <div className="w-24" />
        </div>

        {/* Content */}
        <AnimatePresence mode="wait">
          {step === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <h3 className="text-xl font-bold mb-4">The Problem: Month-End Takes 8 Days</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className="bg-red-50 rounded-xl p-4 border border-red-100">
                  <h4 className="font-semibold text-red-800 mb-2">Before Reconciler</h4>
                  <ul className="space-y-2 text-sm text-red-700">
                    <li className="flex items-center"><AlertTriangle className="w-4 h-4 mr-2" /> 5,000+ transactions manually matched</li>
                    <li className="flex items-center"><AlertTriangle className="w-4 h-4 mr-2" /> 200+ exceptions to investigate</li>
                    <li className="flex items-center"><AlertTriangle className="w-4 h-4 mr-2" /> 3 systems, 12 Excel files</li>
                    <li className="flex items-center"><AlertTriangle className="w-4 h-4 mr-2" /> 8 days of manual work</li>
                  </ul>
                </div>
                <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
                  <h4 className="font-semibold text-emerald-800 mb-2">With Reconciler</h4>
                  <ul className="space-y-2 text-sm text-emerald-700">
                    <li className="flex items-center"><CheckCircle className="w-4 h-4 mr-2" /> 95% auto-matched instantly</li>
                    <li className="flex items-center"><CheckCircle className="w-4 h-4 mr-2" /> 245 exceptions flagged with context</li>
                    <li className="flex items-center"><CheckCircle className="w-4 h-4 mr-2" /> Single dashboard view</li>
                    <li className="flex items-center"><CheckCircle className="w-4 h-4 mr-2" /> 3 minutes to complete</li>
                  </ul>
                </div>
              </div>
              <button onClick={startReconciliation} className="btn-primary w-full text-lg">
                <RefreshCw className="w-5 h-5 mr-2 inline" />
                Start Reconciliation
              </button>
            </motion.div>
          )}

          {step === 1 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <h3 className="text-xl font-bold mb-6 text-center">Reconciliation in Progress...</h3>
              
              {/* Progress Bar */}
              <div className="mb-8">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Processing transactions...</span>
                  <span>{progress}%</span>
                </div>
                <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                  <motion.div 
                    className="h-full bg-emerald-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.1 }}
                  />
                </div>
              </div>

              {/* Live Stats */}
              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="text-center p-4 bg-gray-50 rounded-xl">
                  <p className="text-3xl font-bold text-gray-900">5,034</p>
                  <p className="text-sm text-gray-500">Total Transactions</p>
                </div>
                <div className="text-center p-4 bg-emerald-50 rounded-xl">
                  <p className="text-3xl font-bold text-emerald-600">{matchedCount.toLocaleString()}</p>
                  <p className="text-sm text-emerald-600">Auto-Matched</p>
                </div>
                <div className="text-center p-4 bg-amber-50 rounded-xl">
                  <p className="text-3xl font-bold text-amber-600">{245}</p>
                  <p className="text-sm text-amber-600">Need Review</p>
                </div>
              </div>

              {/* Animated Transaction Stream */}
              <div className="bg-gray-900 rounded-xl p-4 font-mono text-sm text-green-400 h-48 overflow-hidden">
                <div className="space-y-1">
                  {Array.from({ length: 8 }).map((_, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1, repeat: Infinity, repeatDelay: 2 }}
                      className="flex items-center space-x-2"
                    >
                      <CheckCircle className="w-4 h-4" />
                      <span>TXN-{Math.random().toString(36).substr(2, 9).toUpperCase()}</span>
                      <span className="text-gray-500">→</span>
                      <span className="text-blue-400">Matched (${(Math.random() * 10000).toFixed(2)})</span>
                      <span className="text-gray-500 ml-auto">{Math.floor(Math.random() * 98 + 1)}% confidence</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <div className="text-center mb-6">
                <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-emerald-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900">Reconciliation Complete!</h3>
                <p className="text-gray-500">Time elapsed: 3 minutes 12 seconds</p>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="text-center p-4 bg-gray-50 rounded-xl">
                  <p className="text-2xl font-bold">5,034</p>
                  <p className="text-xs text-gray-500">Total</p>
                </div>
                <div className="text-center p-4 bg-emerald-50 rounded-xl">
                  <p className="text-2xl font-bold text-emerald-600">4,789</p>
                  <p className="text-xs text-emerald-600">Auto-Matched (95.1%)</p>
                </div>
                <div className="text-center p-4 bg-amber-50 rounded-xl">
                  <p className="text-2xl font-bold text-amber-600">245</p>
                  <p className="text-xs text-amber-600">Need Review</p>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-xl">
                  <p className="text-2xl font-bold text-red-600">12</p>
                  <p className="text-xs text-red-600">Anomalies</p>
                </div>
              </div>

              {/* Exceptions List */}
              <div className="bg-gray-50 rounded-xl p-4 mb-6">
                <h4 className="font-semibold mb-3">Top Exceptions Requiring Review</h4>
                <div className="space-y-2">
                  {[
                    { type: 'Wire Transfer', amount: '$47,000', issue: 'Unusual pattern', priority: 'high' },
                    { type: 'Duplicate', amount: '$12,500', issue: 'Possible double pay', priority: 'high' },
                    { type: 'FX Variance', amount: '€12,400', issue: 'Rate mismatch', priority: 'medium' },
                  ].map((exc, idx) => (
                    <div key={idx} className="flex items-center justify-between bg-white p-3 rounded-lg">
                      <div>
                        <p className="font-medium">{exc.type}</p>
                        <p className="text-sm text-gray-500">{exc.issue}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">{exc.amount}</p>
                        <span className={`text-xs px-2 py-1 rounded ${exc.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'}`}>
                          {exc.priority}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Time Saved */}
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 mb-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-emerald-700">Time Saved</p>
                    <p className="text-2xl font-bold text-emerald-800">7 days, 4 hours</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-emerald-700">Efficiency Gain</p>
                    <p className="text-2xl font-bold text-emerald-800">87% faster</p>
                  </div>
                </div>
              </div>

              <div className="flex space-x-4">
                <button onClick={() => setStep(0)} className="btn-secondary flex-1">
                  Run Again
                </button>
                <button onClick={onNext} className="btn-primary flex-1">
                  Next: Reporter Demo
                  <ChevronRight className="w-4 h-4 ml-2 inline" />
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}