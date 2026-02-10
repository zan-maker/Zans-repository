import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  TrendingUp, ChevronRight, ChevronLeft, Users, 
  DollarSign, Clock, AlertTriangle, CheckCircle
} from 'lucide-react';

export function ForecasterDemo({ onNext, onBack }: { onNext: () => void; onBack: () => void }) {
  const [hires, setHires] = useState(10);
  const [salary, setSalary] = useState(165000);
  const [showResults, setShowResults] = useState(false);

  const calculateScenario = () => {
    setShowResults(true);
  };

  const monthlyBurnIncrease = (hires * (salary * 1.25)) / 12;
  const newMonthlyBurn = 310000 + monthlyBurnIncrease;
  const currentCash = 4200000;
  const newRunway = currentCash / newMonthlyBurn;
  const runwayReduction = 14 - newRunway;

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
            <div className="w-10 h-10 bg-blue-500 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Forecaster Demo</h2>
              <p className="text-gray-500">Scenario Modeling & Predictions</p>
            </div>
          </div>
          <div className="w-24" />
        </div>

        {/* Scenario Builder */}
        <div className="bg-white rounded-2xl p-8 shadow-lg mb-6">
          <h3 className="text-lg font-semibold mb-2">What if we hire more engineers?</h3>
          <p className="text-gray-500 mb-6">Model the impact of hiring decisions on your cash runway</p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of New Hires: <span className="text-blue-600 font-bold">{hires}</span>
              </label>
              <input
                type="range"
                min="0"
                max="20"
                value={hires}
                onChange={(e) => { setHires(parseInt(e.target.value)); setShowResults(false); }}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0</span>
                <span>10</span>
                <span>20</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Average Salary: <span className="text-blue-600 font-bold">${(salary / 1000).toFixed(0)}K</span>
              </label>
              <input
                type="range"
                min="80000"
                max="250000"
                step="5000"
                value={salary}
                onChange={(e) => { setSalary(parseInt(e.target.value)); setShowResults(false); }}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>$80K</span>
                <span>$165K</span>
                <span>$250K</span>
              </div>
            </div>
          </div>

          {/* Base Assumptions */}
          <div className="bg-gray-50 rounded-xl p-4 mb-6">
            <h4 className="font-semibold mb-3">Current State</h4>
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <p className="text-gray-500">Current Cash</p>
                <p className="text-xl font-bold">$4.2M</p>
              </div>
              <div>
                <p className="text-gray-500">Monthly Burn</p>
                <p className="text-xl font-bold">$310K</p>
              </div>
              <div>
                <p className="text-gray-500">Current Runway</p>
                <p className="text-xl font-bold">14 months</p>
              </div>
            </div>
          </div>

          <button onClick={calculateScenario} className="btn-primary w-full">
            <TrendingUp className="w-5 h-5 mr-2 inline" />
            Model Scenario
          </button>
        </div>

        {/* Results */}
        <AnimatePresence>
          {showResults && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <h3 className="text-xl font-bold mb-6">Scenario Results</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div className="flex items-center">
                      <DollarSign className="w-5 h-5 text-gray-400 mr-3" />
                      <span>Additional Monthly Burn</span>
                    </div>
                    <span className="text-xl font-bold text-red-600">
                      +${(monthlyBurnIncrease / 1000).toFixed(0)}K
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div className="flex items-center">
                      <TrendingUp className="w-5 h-5 text-gray-400 mr-3" />
                      <span>New Total Monthly Burn</span>
                    </div>
                    <span className="text-xl font-bold">
                      ${(newMonthlyBurn / 1000).toFixed(0)}K
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-blue-50 rounded-xl border border-blue-200">
                    <div className="flex items-center">
                      <Clock className="w-5 h-5 text-blue-500 mr-3" />
                      <span className="font-medium">New Runway</span>
                    </div>
                    <span className="text-xl font-bold text-blue-600">
                      {newRunway.toFixed(1)} months
                    </span>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-red-50 rounded-xl border border-red-200">
                    <div className="flex items-center">
                      <AlertTriangle className="w-5 h-5 text-red-500 mr-3" />
                      <span className="font-medium">Runway Reduction</span>
                    </div>
                    <span className="text-xl font-bold text-red-600">
                      -{runwayReduction.toFixed(1)} months
                    </span>
                  </div>
                </div>

                {/* Visualization */}
                <div className="bg-gray-50 rounded-xl p-4">
                  <h4 className="font-semibold mb-4">Cash Runway Comparison</h4>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span>Current (14 months)</span>
                        <span className="text-gray-500">Oct 2025</span>
                      </div>
                      <div className="h-8 bg-gray-200 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: '100%' }}
                          className="h-full bg-green-500 rounded-full"
                        />
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span>With {hires} hires ({newRunway.toFixed(1)} months)</span>
                        <span className="text-gray-500">
                          {new Date(Date.now() + newRunway * 30 * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
                        </span>
                      </div>
                      <div className="h-8 bg-gray-200 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${(newRunway / 14) * 100}%` }}
                          transition={{ delay: 0.2 }}
                          className="h-full bg-amber-500 rounded-full"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Confidence Interval */}
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm text-blue-800">
                      <strong>65% Confidence:</strong> This projection assumes current revenue growth continues. 
                      If Q4 revenue exceeds plan by 20%, runway extends to {(newRunway * 1.2).toFixed(1)} months.
                    </p>
                  </div>
                </div>
              </div>

              {/* Alternatives */}
              <div className="bg-gray-50 rounded-xl p-4">
                <h4 className="font-semibold mb-3 flex items-center">
                  <CheckCircle className="w-4 h-4 mr-2 text-green-500" />
                  Alternatives to Consider
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between p-2 bg-white rounded-lg">
                    <span>Hire {Math.floor(hires * 0.6)} now, {hires - Math.floor(hires * 0.6)} in Q2</span>
                    <span className="font-semibold text-green-600">{(newRunway + 2).toFixed(1)} months runway</span>
                  </div>
                  <div className="flex items-center justify-between p-2 bg-white rounded-lg">
                    <span>Mix FTE ({Math.floor(hires * 0.7)}) and contractors ({hires - Math.floor(hires * 0.7)})</span>
                    <span className="font-semibold text-green-600">{(newRunway + 1.5).toFixed(1)} months runway</span>
                  </div>
                  <div className="flex items-center justify-between p-2 bg-white rounded-lg">
                    <span>Deferred comp for senior hires</span>
                    <span className="font-semibold text-green-600">{(newRunway + 1).toFixed(1)} months runway</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Navigation */}
        <div className="flex justify-between mt-6">
          <button onClick={onBack} className="btn-secondary">
            <ChevronLeft className="w-4 h-4 mr-2 inline" />
            Back: Reporter
          </button>
          <button onClick={onNext} className="btn-primary">
            Next: ROI Calculator
            <ChevronRight className="w-4 h-4 ml-2 inline" />
          </button>
        </div>
      </div>
    </div>
  );
}