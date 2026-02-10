import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, TrendingUp, FileText, Shield, Scale, 
  ChevronRight, Clock, DollarSign, Users, BarChart3,
  Play, CheckCircle, AlertCircle, Sparkles
} from 'lucide-react';
import { ReconcilerDemo } from './components/ReconcilerDemo';
import { ReporterDemo } from './components/ReporterDemo';
import { ForecasterDemo } from './components/ForecasterDemo';
import { ROICalculator } from './components/ROICalculator';

type Section = 'intro' | 'reconciler' | 'reporter' | 'forecaster' | 'roi';

const agents = [
  {
    id: 'reconciler',
    name: 'Reconciler',
    tagline: 'The Error Hunter',
    icon: Scale,
    color: 'bg-emerald-500',
    description: 'Auto-matches 95% of transactions across bank, ERP, and payment systems',
    metric: '95%',
    metricLabel: 'Auto-match rate'
  },
  {
    id: 'forecaster',
    name: 'Forecaster',
    tagline: 'The Crystal Ball',
    icon: TrendingUp,
    color: 'bg-blue-500',
    description: '13-week rolling cash flow forecasts updated daily with ML predictions',
    metric: '±5%',
    metricLabel: 'Forecast accuracy'
  },
  {
    id: 'reporter',
    name: 'Reporter',
    tagline: 'The Storyteller',
    icon: FileText,
    color: 'bg-amber-500',
    description: 'Natural language queries become board-ready reports in 30 seconds',
    metric: '30s',
    metricLabel: 'Report generation'
  },
  {
    id: 'watchdog',
    name: 'Watchdog',
    tagline: 'The Guardian',
    icon: Shield,
    color: 'bg-red-500',
    description: 'Real-time anomaly detection and compliance monitoring',
    metric: '24/7',
    metricLabel: 'Monitoring'
  },
  {
    id: 'advisor',
    name: 'Advisor',
    tagline: 'The Strategist',
    icon: Brain,
    color: 'bg-purple-500',
    description: 'Pattern recognition and strategic recommendations',
    metric: '10x',
    metricLabel: 'More insights'
  }
];

function App() {
  const [currentSection, setCurrentSection] = useState<Section>('intro');
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  const renderSection = () => {
    switch (currentSection) {
      case 'intro':
        return <IntroSection onStart={() => setCurrentSection('reconciler')} />;
      case 'reconciler':
        return <ReconcilerDemo onNext={() => setCurrentSection('reporter')} onBack={() => setCurrentSection('intro')} />;
      case 'reporter':
        return <ReporterDemo onNext={() => setCurrentSection('forecaster')} onBack={() => setCurrentSection('reconciler')} />;
      case 'forecaster':
        return <ForecasterDemo onNext={() => setCurrentSection('roi')} onBack={() => setCurrentSection('reporter')} />;
      case 'roi':
        return <ROICalculator onBack={() => setCurrentSection('forecaster')} />;
      default:
        return <IntroSection onStart={() => setCurrentSection('reconciler')} />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="section-container py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Impact Quadrant</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">AI Agent Demo</span>
              <div className="flex space-x-1">
                {['intro', 'reconciler', 'reporter', 'forecaster', 'roi'].map((section, idx) => (
                  <div
                    key={section}
                    className={`w-8 h-1 rounded-full transition-colors ${
                      currentSection === section ? 'bg-primary-600' : 'bg-gray-200'
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentSection}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.3 }}
        >
          {renderSection()}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

function IntroSection({ onStart }: { onStart: () => void }) {
  return (
    <div className="section-container py-12">
      {/* Hero */}
      <div className="text-center mb-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Your Netsuite Has Limits.
            <br />
            <span className="text-primary-600">Your CFO Shouldn't.</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Meet the AI-powered finance team that works inside your existing ERP. 
            No rip-and-replace. No disruption. Just smarter decisions, faster.
          </p>
          <button onClick={onStart} className="btn-primary text-lg px-8 py-4 inline-flex items-center">
            <Play className="w-5 h-5 mr-2" />
            See AI Agents in Action
            <ChevronRight className="w-5 h-5 ml-2" />
          </button>
        </motion.div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
        {[
          { label: 'Month-End Close', before: '15 days', after: '3 days', metric: '80% faster' },
          { label: 'Forecast Accuracy', before: '±20%', after: '±5%', metric: '4x better' },
          { label: 'Board Prep Time', before: '20+ hours', after: '2 hours', metric: '90% faster' },
          { label: 'Auto-Reconciliation', before: '0%', after: '95%', metric: 'Fully automated' },
        ].map((stat, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-white rounded-xl p-6 shadow-md"
          >
            <p className="text-sm text-gray-500 mb-2">{stat.label}</p>
            <div className="flex items-baseline space-x-2 mb-1">
              <span className="text-gray-400 line-through">{stat.before}</span>
              <span className="text-2xl font-bold text-primary-600">{stat.after}</span>
            </div>
            <p className="text-sm font-semibold text-green-600">{stat.metric}</p>
          </motion.div>
        ))}
      </div>

      {/* Agents Grid */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-8">Meet Your Digital Finance Team</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, idx) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.1 }}
              whileHover={{ scale: 1.02 }}
              className="agent-card cursor-pointer"
              onClick={onStart}
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 ${agent.color} rounded-xl flex items-center justify-center`}>
                  <agent.icon className="w-6 h-6 text-white" />
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-gray-900">{agent.metric}</p>
                  <p className="text-xs text-gray-500">{agent.metricLabel}</p>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-1">{agent.name}</h3>
              <p className="text-sm text-gray-500 mb-3">{agent.tagline}</p>
              <p className="text-gray-600 text-sm">{agent.description}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* CTA */}
      <div className="text-center bg-primary-600 rounded-2xl p-12 text-white">
        <h2 className="text-3xl font-bold mb-4">Ready to Meet Your Digital Finance Team?</h2>
        <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
          See how AI agents transform your existing ERP from a system of record into a strategic command center.
        </p>
        <button onClick={onStart} className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-primary-50 transition-colors inline-flex items-center">
          <Play className="w-5 h-5 mr-2" />
          Start Interactive Demo
        </button>
      </div>
    </div>
  );
}

export default App;