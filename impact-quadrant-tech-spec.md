# Impact Quadrant React Web App
## Technical Specification Document

**Version:** 1.0  
**Date:** February 10, 2026  
**Status:** Implementation-Ready

---

## 1. Executive Overview

### Project Goal
Build a modern React web application for Impact Quadrant that positions the company as the AI-native fractional CFO firm. The website will showcase AI agents working with legacy ERP systems (specifically Netsuite) to modernize finance operations without replacement.

### Target Users
- CFOs and VP Finance at growth-stage companies ($5M-$100M ARR)
- CEOs evaluating finance function improvements
- Private equity and venture capital firms (referral sources)

### Success Metrics
- Page load time: < 2 seconds
- Time on site: > 3 minutes
- Demo requests: > 5% of visitors
- Mobile traffic: Fully responsive

---

## 2. Technology Stack

### Core Framework
```
Frontend Framework: React 18.2+
Language: TypeScript 5.0+
Build Tool: Vite 5.0+ (recommended) or Next.js 14+
Package Manager: pnpm (faster, disk efficient)
```

**Why Vite over Next.js:**
- Faster development server (native ESM)
- Simpler configuration for static sites
- Better for marketing sites without heavy SSR needs
- Can add SSR later if needed

### Styling & UI
```
CSS Framework: Tailwind CSS 3.4+
UI Components: shadcn/ui (Tailwind-based, customizable)
Animation: Framer Motion 10+
Icons: Lucide React (consistent, tree-shakeable)
Charts: Recharts (React-native) or Tremor (Tailwind-based)
```

### State Management
```
Primary: React Query (TanStack Query) 5+
Server State: React Query caching
Client State: Zustand (lightweight) or React Context
Forms: React Hook Form + Zod validation
```

### Development Tools
```
Linting: ESLint with TypeScript
Formatting: Prettier
Testing: Vitest (unit) + React Testing Library
E2E Testing: Playwright
Git Hooks: Husky + lint-staged
```

---

## 3. Application Architecture

### Folder Structure
```
src/
├── app/                          # App-level components
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page
│   ├── providers.tsx            # Context providers
│   └── globals.css              # Global styles
│
├── components/                   # Reusable components
│   ├── ui/                      # shadcn/ui components
│   ├── layout/                  # Layout components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Container.tsx
│   ├── sections/                # Page sections
│   │   ├── Hero.tsx
│   │   ├── ProblemSolution.tsx
│   │   ├── AgentShowcase.tsx
│   │   ├── HowItWorks.tsx
│   │   ├── SocialProof.tsx
│   │   └── CTASection.tsx
│   └── shared/                  # Shared components
│       ├── AgentCard.tsx
│       ├── MetricCard.tsx
│       ├── TestimonialCard.tsx
│       └── ROICalculator.tsx
│
├── hooks/                        # Custom React hooks
│   ├── useAgents.ts
│   ├── useScrollAnimation.ts
│   └── useROICalculator.ts
│
├── lib/                          # Utilities and configs
│   ├── utils.ts                 # General utilities
│   ├── constants.ts             # App constants
│   └── animations.ts            # Framer Motion configs
│
├── types/                        # TypeScript types
│   ├── agent.ts
│   ├── testimonial.ts
│   └── index.ts
│
├── styles/                       # Additional styles
│   └── animations.css
│
└── public/                       # Static assets
    ├── images/
    ├── videos/
    └── fonts/
```

### Component Architecture

#### Atomic Design Approach
```
Atoms: Button, Input, Card, Icon
Molecules: AgentCard, MetricCard, TestimonialCard
Organisms: Hero, AgentShowcase, ROICalculator
Templates: Page layouts
Pages: Route components
```

#### Component Example Structure
```typescript
// components/sections/Hero.tsx
interface HeroProps {
  headline: string;
  subheadline: string;
  primaryCTA: { text: string; href: string };
  secondaryCTA: { text: string; href: string };
}

export function Hero({ headline, subheadline, primaryCTA, secondaryCTA }: HeroProps) {
  return (
    <section className="relative min-h-screen flex items-center">
      {/* Content */}
    </section>
  );
}
```

---

## 4. Page Structure & Routes

### Route Map
```
/                          # Home (all sections)
/agents                    # Agent details page
/agents/:agentId           # Individual agent showcase
/demo                      # Interactive demo
/case-studies              # Case studies list
/case-studies/:id          # Individual case study
/pricing                   # Pricing page
/about                     # About page
/contact                   # Contact form
/blog                      # Blog list
/blog/:slug                # Blog post
```

### Home Page Sections (Single Page Scroll)
1. **Navigation** - Sticky header with smooth scroll links
2. **Hero** - Animated value proposition
3. **Problem/Solution** - Before/after comparison
4. **Agents Showcase** - Digital finance team cards
5. **How It Works** - 4-step process timeline
6. **Social Proof** - Testimonials + metrics
7. **ROI Calculator** - Interactive calculator
8. **CTA Section** - Final call-to-action
9. **Footer** - Links and contact info

---

## 5. Key Features Implementation

### 5.1 Hero Section with Animated Agents

#### Visual Concept
Central dashboard with 5 animated "agent orbs" orbiting around Netsuite/ERP interface. Each orb pulses when active. Data flows from chaos (disconnected) to clarity (unified).

#### Technical Implementation
```typescript
// Using Framer Motion for orbital animation
const orbitVariants = {
  animate: (i: number) => ({
    rotate: 360,
    transition: {
      duration: 20 + i * 5,
      repeat: Infinity,
      ease: "linear"
    }
  })
};

// Agent orbs with pulse effect
const pulseVariants = {
  pulse: {
    scale: [1, 1.1, 1],
    opacity: [0.7, 1, 0.7],
    transition: {
      duration: 2,
      repeat: Infinity
    }
  }
};
```

#### Components Needed
- `AgentOrb` - Animated agent representation
- `DataFlow` - SVG animation of data transformation
- `HeroBackground` - Particle effect or gradient

### 5.2 Interactive Problem/Solution Slider

#### User Interaction
Drag slider to reveal transformation from "The Old Way" to "The Agent Way"

#### Technical Implementation
```typescript
// components/sections/ProblemSolution.tsx
import { useState, useRef } from 'react';
import { motion, useMotionValue, useTransform } from 'framer-motion';

export function ComparisonSlider() {
  const [sliderPosition, setSliderPosition] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);
  
  const handleDrag = (event: any, info: any) => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      const x = info.point.x - rect.left;
      const percentage = (x / rect.width) * 100;
      setSliderPosition(Math.max(0, Math.min(100, percentage)));
    }
  };
  
  return (
    <div ref={containerRef} className="relative overflow-hidden">
      {/* Before Image (The Old Way) */}
      <div className="absolute inset-0">
        <OldWayImage />
      </div>
      
      {/* After Image (The Agent Way) - clipped */}
      <motion.div 
        className="absolute inset-0 overflow-hidden"
        style={{ width: `${sliderPosition}%` }}
      >
        <NewWayImage />
      </motion.div>
      
      {/* Draggable Slider Handle */}
      <motion.div
        drag="x"
        dragConstraints={containerRef}
        onDrag={handleDrag}
        className="absolute top-0 bottom-0 w-1 bg-white cursor-ew-resize"
        style={{ left: `${sliderPosition}%` }}
      />
    </div>
  );
}
```

### 5.3 Agent Showcase Cards

#### Card Design
- 3D tilt effect on hover
- Expandable details
- Animated icon transitions

#### Implementation
```typescript
// components/shared/AgentCard.tsx
import { motion } from 'framer-motion';
import { useState } from 'react';

interface AgentCardProps {
  name: string;
  tagline: string;
  icon: React.ReactNode;
  capabilities: string[];
  color: string;
}

export function AgentCard({ name, tagline, icon, capabilities, color }: AgentCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <motion.div
      className="relative p-6 rounded-2xl bg-white shadow-lg"
      whileHover={{ 
        scale: 1.02,
        rotateX: 5,
        rotateY: 5,
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)"
      }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      style={{ transformStyle: "preserve-3d" }}
    >
      {/* Animated Icon */}
      <motion.div
        animate={isHovered ? { rotate: 360, scale: 1.1 } : {}}
        transition={{ duration: 0.5 }}
        className={`w-16 h-16 rounded-full flex items-center justify-center ${color}`}
      >
        {icon}
      </motion.div>
      
      {/* Content */}
      <h3 className="mt-4 text-xl font-bold">{name}</h3>
      <p className="text-gray-600">{tagline}</p>
      
      {/* Capabilities - expand on hover */}
      <motion.ul
        initial={{ height: 0, opacity: 0 }}
        animate={isHovered ? { height: "auto", opacity: 1 } : {}}
        className="mt-4 space-y-2"
      >
        {capabilities.map((cap, i) => (
          <li key={i} className="flex items-center text-sm">
            <CheckIcon className="w-4 h-4 mr-2 text-green-500" />
            {cap}
          </li>
        ))}
      </motion.ul>
    </motion.div>
  );
}
```

### 5.4 ROI Calculator

#### Functionality
Interactive calculator where users input:
- Current month-end close time
- Number of finance team members
- Average hourly rate
- Current forecasting method

Outputs:
- Projected time savings
- Cost savings (annual)
- Payback period
- 3-year NPV

#### Implementation
```typescript
// components/shared/ROICalculator.tsx
import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface CalculatorState {
  closeTimeDays: number;
  teamSize: number;
  avgHourlyRate: number;
  monthlyTransactions: number;
}

export function ROICalculator() {
  const [inputs, setInputs] = useState<CalculatorState>({
    closeTimeDays: 12,
    teamSize: 3,
    avgHourlyRate: 75,
    monthlyTransactions: 5000
  });
  
  const results = useMemo(() => {
    // Current state calculations
    const currentHoursPerClose = inputs.closeTimeDays * 8 * inputs.teamSize;
    const currentAnnualHours = currentHoursPerClose * 12;
    const currentAnnualCost = currentAnnualHours * inputs.avgHourlyRate;
    
    // With Impact Quadrant (80% reduction)
    const newCloseTimeDays = Math.max(3, inputs.closeTimeDays * 0.2);
    const newHoursPerClose = newCloseTimeDays * 8 * inputs.teamSize;
    const newAnnualHours = newHoursPerClose * 12;
    const hoursSaved = currentAnnualHours - newAnnualHours;
    const annualSavings = hoursSaved * inputs.avgHourlyRate;
    
    // Additional forecasting savings (estimate)
    const forecastingSavings = inputs.teamSize * 520 * inputs.avgHourlyRate * 0.3; // 30% of time
    
    const totalAnnualSavings = annualSavings + forecastingSavings;
    const impactQuadrantCost = 150000; // Average annual cost
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
  }, [inputs]);
  
  return (
    <div className="bg-white rounded-2xl p-8 shadow-xl">
      {/* Input Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <InputSlider
          label="Current Month-End Close (days)"
          value={inputs.closeTimeDays}
          min={3}
          max={20}
          onChange={(v) => setInputs({ ...inputs, closeTimeDays: v })}
        />
        {/* More inputs... */}
      </div>
      
      {/* Results Section */}
      <AnimatePresence mode="wait">
        <motion.div
          key={JSON.stringify(results)}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          <ResultCard
            label="Annual Savings"
            value={formatCurrency(results.totalAnnualSavings)}
            color="green"
          />
          <ResultCard
            label="ROI"
            value={`${results.roi.toFixed(0)}%`}
            color="blue"
          />
          <ResultCard
            label="Payback Period"
            value={`${results.paybackMonths.toFixed(1)} months`}
            color="purple"
          />
          <ResultCard
            label="3-Year Value"
            value={formatCurrency(results.threeYearValue)}
            color="gold"
          />
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
```

### 5.5 How It Works Timeline

#### Scroll-Triggered Animations
As user scrolls, each step reveals with animation

#### Implementation
```typescript
// components/sections/HowItWorks.tsx
import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';

const steps = [
  { week: "Week 1", title: "Connect", icon: PlugIcon, description: "..." },
  { week: "Week 2", title: "Calibrate", icon: SlidersIcon, description: "..." },
  { week: "Week 3", title: "Activate", icon: ZapIcon, description: "..." },
  { week: "Week 4+", title: "Optimize", icon: TrendingUpIcon, description: "..." }
];

export function HowItWorks() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"]
  });
  
  return (
    <section ref={containerRef} className="py-24">
      <div className="max-w-4xl mx-auto">
        {/* Timeline */}
        <div className="relative">
          {/* Progress Line */}
          <motion.div
            className="absolute left-8 top-0 bottom-0 w-1 bg-gradient-to-b from-blue-500 to-purple-500"
            style={{ 
              scaleY: scrollYProgress,
              transformOrigin: "top"
            }}
          />
          
          {/* Steps */}
          {steps.map((step, index) => (
            <TimelineStep
              key={index}
              step={step}
              index={index}
              scrollYProgress={scrollYProgress}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

function TimelineStep({ step, index, scrollYProgress }) {
  const start = index / 4;
  const end = (index + 1) / 4;
  
  const opacity = useTransform(
    scrollYProgress,
    [start - 0.1, start, end, end + 0.1],
    [0.3, 1, 1, 0.3]
  );
  
  const scale = useTransform(
    scrollYProgress,
    [start - 0.1, start, end, end + 0.1],
    [0.9, 1, 1, 0.9]
  );
  
  return (
    <motion.div
      style={{ opacity, scale }}
      className="relative flex items-start mb-16 ml-20"
    >
      {/* Step Number/Icon */}
      <div className="absolute -left-20 flex items-center justify-center w-16 h-16 rounded-full bg-white shadow-lg border-2 border-blue-500">
        <step.icon className="w-8 h-8 text-blue-500" />
      </div>
      
      {/* Content */}
      <div className="bg-white rounded-xl p-6 shadow-md">
        <span className="text-sm font-semibold text-blue-500">{step.week}</span>
        <h3 className="text-xl font-bold mt-1">{step.title}</h3>
        <p className="text-gray-600 mt-2">{step.description}</p>
      </div>
    </motion.div>
  );
}
```

---

## 6. Integration Architecture

### Netsuite Integration

#### Connection Methods
```typescript
// lib/integrations/netsuite.ts

// Method 1: REST API (preferred for new integrations)
interface NetsuiteConfig {
  accountId: string;
  consumerKey: string;
  consumerSecret: string;
  tokenId: string;
  tokenSecret: string;
}

// Method 2: ODBC (for complex queries)
interface ODBCC config {
  driver: string;
  server: string;
  port: number;
  database: string;
  username: string;
  password: string;
}

// Method 3: SuiteTalk Web Services (for SOAP needs)
```

#### Data Sync Strategy
```typescript
// hooks/useNetsuiteSync.ts
import { useQuery, useMutation } from '@tanstack/react-query';

export function useNetsuiteSync() {
  // Initial full sync
  const { data: initialSync } = useQuery({
    queryKey: ['netsuite', 'initial'],
    queryFn: fetchAllFinancialData,
    staleTime: 5 * 60 * 1000 // 5 minutes
  });
  
  // Real-time webhook updates
  const mutation = useMutation({
    mutationFn: processWebhookUpdate,
    onSuccess: (data) => {
      // Update React Query cache
      queryClient.invalidateQueries({ queryKey: ['netsuite'] });
    }
  });
  
  return { initialSync, processUpdate: mutation.mutate };
}
```

### Agent Orchestration Layer

#### OpenClaw-Style Architecture
```typescript
// lib/agents/orchestrator.ts

interface Agent {
  id: string;
  name: string;
  capabilities: string[];
  execute: (task: Task) => Promise<Result>;
}

interface Task {
  type: 'reconciliation' | 'forecasting' | 'reporting' | 'compliance';
  parameters: Record<string, any>;
  priority: 'low' | 'medium' | 'high';
  deadline?: Date;
}

class AgentOrchestrator {
  private agents: Map<string, Agent> = new Map();
  
  registerAgent(agent: Agent) {
    this.agents.set(agent.id, agent);
  }
  
  async dispatch(task: Task): Promise<Result> {
    // Route to appropriate agent
    const agent = this.selectAgent(task);
    
    // Execute with monitoring
    const result = await this.executeWithMonitoring(agent, task);
    
    // Store result for audit trail
    await this.logExecution(task, agent, result);
    
    return result;
  }
  
  private selectAgent(task: Task): Agent {
    // Logic to select best agent for task
    // Could use ML model for optimal routing
  }
}
```

---

## 7. Performance Requirements

### Core Web Vitals Targets
```
LCP (Largest Contentful Paint): < 2.5s
FID (First Input Delay): < 100ms
CLS (Cumulative Layout Shift): < 0.1
FCP (First Contentful Paint): < 1.8s
TTFB (Time to First Byte): < 600ms
```

### Optimization Strategies

#### 1. Image Optimization
```typescript
// Use Next.js Image component or similar
import Image from 'next/image';

<Image
  src="/hero-illustration.png"
  alt="AI Agents Visualization"
  width={1200}
  height={800}
  priority // For above-fold images
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

#### 2. Code Splitting
```typescript
// Lazy load below-fold sections
const ROICalculator = lazy(() => import('./ROICalculator'));
const CaseStudies = lazy(() => import('./CaseStudies'));

// Use Suspense for loading states
<Suspense fallback={<SectionSkeleton />}>
  <ROICalculator />
</Suspense>
```

#### 3. Animation Performance
```typescript
// Use transform and opacity only
// Avoid animating layout properties
const optimizedVariants = {
  animate: {
    x: 0,        // Good - compositor layer
    opacity: 1,  // Good - compositor layer
    // height: 'auto',  // Bad - causes layout
    // top: 0,          // Bad - causes layout
  }
};

// Use will-change for heavy animations
<motion.div style={{ willChange: 'transform' }} />

// Respect reduced motion preferences
const prefersReducedMotion = 
  typeof window !== 'undefined' && 
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

### Bundle Size Budgets
```
Initial JS: < 200KB (gzipped)
Total JS: < 500KB (gzipped)
CSS: < 50KB (gzipped)
Images: < 2MB total, WebP format
```

---

## 8. SEO Strategy

### Technical SEO
```typescript
// app/layout.tsx or similar
export const metadata = {
  title: 'Impact Quadrant | AI-Native Fractional CFO Services',
  description: 'Transform your finance function with AI agents...',
  keywords: ['fractional CFO', 'AI agents', 'Netsuite', 'finance automation'],
  openGraph: {
    title: 'Impact Quadrant',
    description: '...',
    images: ['/og-image.png']
  },
  twitter: {
    card: 'summary_large_image',
    title: '...',
    description: '...'
  }
};
```

### Structured Data
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Impact Quadrant",
  "description": "AI-native fractional CFO services",
  "url": "https://impactquadrant.info",
  "logo": "https://impactquadrant.info/logo.png",
  "sameAs": [
    "https://linkedin.com/company/impactquadrant",
    "https://twitter.com/impactquadrant"
  ],
  "offers": {
    "@type": "Service",
    "name": "Fractional CFO Services",
    "description": "AI-augmented finance leadership"
  }
}
```

---

## 9. Testing Strategy

### Unit Tests
```typescript
// __tests__/ROICalculator.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ROICalculator } from '../ROICalculator';

describe('ROICalculator', () => {
  it('calculates ROI correctly', () => {
    render(<ROICalculator />);
    
    // Set inputs
    fireEvent.change(screen.getByLabelText(/close time/i), {
      target: { value: '12' }
    });
    
    // Check output
    expect(screen.getByText(/\$350,000/)).toBeInTheDocument();
  });
});
```

### E2E Tests (Playwright)
```typescript
// e2e/demo.spec.ts
import { test, expect } from '@playwright/test';

test('user can run ROI calculator', async ({ page }) => {
  await page.goto('/');
  await page.click('text=Calculate ROI');
  await page.fill('[name="closeTime"]', '12');
  await page.fill('[name="teamSize"]', '3');
  
  await expect(page.locator('[data-testid="annual-savings"]'))
    .toContainText('$350,000');
});
```

### Visual Regression
```typescript
// Use Chromatic or similar
// Snapshots taken on every PR
// Review UI changes in Storybook
```

---

## 10. Deployment & CI/CD

### Build Configuration
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true }) // Bundle analysis
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom'],
          'vendor-motion': ['framer-motion'],
          'vendor-charts': ['recharts']
        }
      }
    },
    sourcemap: true
  }
});
```

### CI/CD Pipeline (GitHub Actions)
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          
      - name: Install pnpm
        uses: pnpm/action-setup@v2
        
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Run tests
        run: pnpm test
        
      - name: Build
        run: pnpm build
        
      - name: Deploy to Vercel/Netlify
        uses: vercel/action-deploy@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
```

### Hosting Recommendations
**Primary:** Vercel (best for React, edge network)
**Alternative:** Netlify (great for static sites)
**Enterprise:** AWS CloudFront + S3 (for custom infrastructure)

---

## 11. Security Considerations

### Data Protection
```typescript
// Environment variables
VITE_NETSUITE_CLIENT_ID=xxx      // Never commit
VITE_API_BASE_URL=https://api.impactquadrant.info
VITE_ANALYTICS_KEY=xxx
```

### Content Security Policy
```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' 'unsafe-eval';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.impactquadrant.info;
  font-src 'self';
">
```

### Form Security
```typescript
// Rate limiting on API routes
// CSRF protection
// Input sanitization with Zod
const contactSchema = z.object({
  email: z.string().email(),
  company: z.string().min(2).max(100),
  message: z.string().min(10).max(5000)
});
```

---

## 12. Implementation Roadmap

### Phase 1: MVP (Weeks 1-2)
- [ ] Set up project structure and tooling
- [ ] Build layout components (Header, Footer, Container)
- [ ] Implement Hero section with basic animation
- [ ] Create Problem/Solution section
- [ ] Deploy to staging

### Phase 2: Core Features (Weeks 3-4)
- [ ] Build Agent Showcase cards
- [ ] Implement How It Works timeline
- [ ] Create Social Proof section
- [ ] Add responsive navigation
- [ ] Performance optimization

### Phase 3: Interactive Elements (Weeks 5-6)
- [ ] Build ROI Calculator
- [ ] Implement Problem/Solution slider
- [ ] Add scroll-triggered animations
- [ ] Create demo page structure
- [ ] Add form handling

### Phase 4: Polish & Launch (Weeks 7-8)
- [ ] Add comprehensive tests
- [ ] SEO optimization
- [ ] Accessibility audit
- [ ] Performance benchmarking
- [ ] Launch to production

---

## 13. Appendix

### Dependencies to Install
```bash
# Core
pnpm add react react-dom
pnpm add -D typescript @types/react @types/react-dom

# Build
pnpm add -D vite @vitejs/plugin-react

# Styling
pnpm add tailwindcss postcss autoprefixer
pnpm add -D @tailwindcss/forms @tailwindcss/typography

# Animation
pnpm add framer-motion

# UI Components
pnpm add lucide-react
pnpm add -D @shadcn/ui

# State Management
pnpm add @tanstack/react-query zustand

# Forms
pnpm add react-hook-form zod @hookform/resolvers

# Charts
pnpm add recharts

# Utilities
pnpm add clsx tailwind-merge date-fns
```

### File Templates
See accompanying files for:
- `tsconfig.json` configuration
- `tailwind.config.ts` with custom theme
- Component boilerplates
- Test examples

---

*This specification provides a complete blueprint for building the Impact Quadrant React application. All sections are implementation-ready with code examples, architecture diagrams, and clear requirements.*
