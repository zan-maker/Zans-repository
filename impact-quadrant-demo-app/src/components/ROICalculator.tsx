import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { 
  ChevronLeft, DollarSign, Clock, Users, 
  TrendingUp, Calculator, CheckCircle
} from 'lucide-react';

export function ROICalculator({ onBack }: { onBack: () => void }) {
  const [closeTime, setCloseTime] = useState(12);
  const [teamSize, setTeamSize] = useState(3);
  const [hourlyRate, setHourlyRate] = useState(75);
  const [showResults, setShowResults] = useState(false);

  const results = useMemo(() => {
    // Current state
    const currentHoursPerClose = closeTime * 8 * teamSize;
    const currentAnnualHours = currentHoursPerClose * 12;
    const currentAnnualCost = currentAnnualHours * hourlyRate;
    
    // With Impact Quadrant (80% reduction)
    const newCloseTime = Math.max(3, closeTime * 0.2);
    const newHoursPerClose = newCloseTime * 8 * teamSize;
    const newAnnualHours = newHoursPerClose * 12;
    const hoursSaved = currentAnnualHours - newAnnualHours;
    const annualSavings = hoursSaved * hourlyRate;
    
    // Additional forecasting savings
    const forecastingSavings = teamSize * 520 * hourlyRate * 0.3;
    
    const totalAnnualSavings = annualSavings + forecastingSavings;
    const impactQuadrantCost = 150000;
    const netSavings = totalAnnualSavings - impactQuadrantCost;
    const roi = (netSavings / impactQuadrantCost) * 100;
    const paybackMonths = (impactQuadrantCost / totalAnnualSavings) * 12;
    
    return {
      currentAnnualCost,
      hoursSaved,
      totalAnnualSavings,
      netSavings,
      roi,
      paybackMonths,
      threeYearValue: netSavings * 3
    };
  }, [closeTime, teamSize, hourlyRate]);

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
            <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
              <Calculator className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">ROI Calculator</h2>
              <p className="text-gray-500">Calculate your potential savings</p>
            </div>
          </div>
          <div className="w-24" />
        </div>

        {/* Calculator */}
        <div className="bg-white rounded-2xl p-8 shadow-lg mb-6">
          <h3 className="text-lg font-semibold mb-6">Enter your current finance operations</h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Clock className="w-4 h-4 inline mr-1" />
                Month-End Close (days)
              </label>
              <div className="flex items-center space-x-3">
                <input
                  type="range"
                  min="3"
                  max="20"
                  value={closeTime}
                  onChange={(e) => setCloseTime(parseInt(e.target.value))}
                  className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                />
                <span className="w-12 text-right font-bold">{closeTime}</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Users className="w-4 h-4 inline mr-1" />
                Finance Team Size
              </label>
              <div className="flex items-center space-x-3">
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={teamSize}
                  onChange={(e) => setTeamSize(parseInt(e.target.value))}
                  className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                />
                <span className="w-12 text-right font-bold">{teamSize}</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <DollarSign className="w-4 h-4 inline mr-1" />
                Avg Hourly Rate ($)
              </label>
              <div className="flex items-center space-x-3">
                <input
                  type="range"
                  min="30"
                  max="200"
                  step="5"
                  value={hourlyRate}
                  onChange={(e) => setHourlyRate(parseInt(e.target.value))}
                  className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                />
                <span className="w-16 text-right font-bold">${hourlyRate}</span>
              </div>
            </div>
          </div>

          <button 
            onClick={() => setShowResults(true)} 
            className="btn-primary w-full"
          >
            <Calculator className="w-5 h-5 mr-2 inline" />
            Calculate ROI
          </button>
        </div>

        {/* Results */}
        {showResults && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            {/* Key Metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-green-500">
                <p className="text-sm text-gray-500 mb-1">Annual Savings</p>
                <p className="text-2xl font-bold text-green-600">
                  ${(results.totalAnnualSavings / 1000).toFixed(0)}K
                </p>
              </div>
              <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-blue-500">
                <p className="text-sm text-gray-500 mb-1">ROI</p>
                <p className="text-2xl font-bold text-blue-600">
                  {results.roi.toFixed(0)}%
                </p>
              </div>
              <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-purple-500">
                <p className="text-sm text-gray-500 mb-1">Payback Period</p>
                <p className="text-2xl font-bold text-purple-600">
                  {results.paybackMonths.toFixed(1)} months
                </p>
              </div>
              <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-amber-500">
                <p className="text-sm text-gray-500 mb-1">3-Year Value</p>
                <p className="text-2xl font-bold text-amber-600">
                  ${(results.threeYearValue / 1000000).toFixed(1)}M
                </p>
              </div>
            </div>

            {/* Detailed Breakdown */}
            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <h3 className="text-xl font-bold mb-6">Detailed Breakdown</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                  <div>
                    <p className="font-medium">Current Annual Close Cost</p>
                    <p className="text-sm text-gray-500">{closeTime} days × 12 months × {teamSize} people × ${hourlyRate}/hr</p>
                  </div>
                  <p className="text-xl font-bold text-gray-700">
                    ${(results.currentAnnualCost / 1000).toFixed(0)}K
                  </p>
                </div>

                <div className="flex items-center justify-between p-4 bg-green-50 rounded-xl border border-green-200">
                  <div className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    <div>
                      <p className="font-medium">Hours Saved Annually</p>
                      <p className="text-sm text-green-600">80% reduction in manual reconciliation & reporting</p>
                    </div>
                  </div>
                  <p className="text-xl font-bold text-green-700">
                    {results.hoursSaved.toLocaleString()} hrs
                  </p>
                </div>

                <div className="flex items-center justify-between p-4 bg-blue-50 rounded-xl border border-blue-200">
                  <div className="flex items-center">
                    <TrendingUp className="w-5 h-5 text-blue-500 mr-3" />
                    <div>
                      <p className="font-medium">Additional Forecasting Value</p>
                      <p className="text-sm text-blue-600">Better decisions from accurate predictions</p>
                    </div>
                  </div>
                  <p className="text-xl font-bold text-blue-700">
                    ${((results.totalAnnualSavings - (results.hoursSaved * hourlyRate)) / 1000).toFixed(0)}K
                  </p>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-100 rounded-xl">
                  <div>
                    <p className="font-medium">Impact Quadrant Investment</p>
                    <p className="text-sm text-gray-500">Annual subscription + implementation</p>
                  </div>
                  <p className="text-xl font-bold text-gray-700">
                    $150K
                  </p>
                </div>

                <div className="border-t-2 border-gray-200 pt-4">
                  <div className="flex items-center justify-between p-4 bg-primary-50 rounded-xl border border-primary-200">
                    <div>
                      <p className="font-bold text-primary-900">Net Annual Benefit</p>
                      <p className="text-sm text-primary-700">Total savings minus investment</p>
                    </div>
                    <p className="text-3xl font-bold text-primary-600">
                      ${(results.netSavings / 1000).toFixed(0)}K
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* CTA */}
            <div className="bg-primary-600 rounded-2xl p-8 text-white text-center">
              <h3 className="text-2xl font-bold mb-4">Ready to achieve these results?</h3>
              <p className="text-primary-100 mb-6 max-w-2xl mx-auto">
                Join 30+ growth-stage companies who've transformed their finance operations with Impact Quadrant.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold hover:bg-primary-50 transition-colors">
                  Schedule Free Assessment
                </button>
                <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white/10 transition-colors">
                  Download Full Report
                </button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Back Button */}
        <div className="mt-6">
          <button onClick={onBack} className="btn-secondary">
            <ChevronLeft className="w-4 h-4 mr-2 inline" />
            Back to Demos
          </button>
        </div>
      </div>
    </div>
  );
}