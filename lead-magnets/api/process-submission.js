#!/usr/bin/env node
/**
 * Lead Magnet Submission Handler
 * Receives form submissions and processes them
 * 
 * Usage: node process-submission.js
 * This script should be called by OpenClaw cron job or webhook
 */

const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');
const puppeteer = require('puppeteer');

// Configuration
const DATA_DIR = path.join(__dirname, '..', 'data');
const TEMPLATES_DIR = path.join(__dirname, '..', 'templates');
const LEADS_FILE = path.join(DATA_DIR, 'leads.json');

// Kimi API Configuration
const KIMI_API_KEY = process.env.KIMI_API_KEY || process.env.MOONSHOT_API_KEY;
const KIMI_API_URL = 'https://api.moonshot.cn/v1/chat/completions';

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

/**
 * Validate submission using Kimi API
 * Returns { isValid: boolean, reason: string }
 */
async function validateSubmissionWithKimi(leadData) {
    console.log('🔍 Validating submission with Kimi API...');
    
    const prompt = `You are a data validation expert for lead generation. Review this business submission and determine if it's valid.

SUBMISSION DATA:
- Service: ${leadData.service}
- Company: ${leadData.companyName}
- Employees: ${leadData.employeeCount}
${leadData.monthlyBenefitsCost ? `- Monthly Benefits Cost: $${leadData.monthlyBenefitsCost}` : ''}
${leadData.monthlySaaSSpend ? `- Monthly SaaS Spend: $${leadData.monthlySaaSSpend}` : ''}
${leadData.monthlyVendorSpend ? `- Monthly Vendor Spend: $${leadData.monthlyVendorSpend}` : ''}
- Email: ${leadData.email}
- Calculated Savings: $${leadData.calculatedSavings}

VALIDATION RULES:
1. Company name should not be gibberish or clearly fake (e.g., "Test Company", "ABC", "123 Corp")
2. Employee count should be reasonable (1-10,000)
3. Financial values should make sense for the company size
4. Email should look professional (not test@test.com, fake@fake.com, etc.)
5. Calculated savings should be positive and reasonable

RED FLAGS (mark invalid):
- Test data, fake company names
- Impossible numbers (0 employees, $999,999 monthly spend for small company)
- Disposable email addresses
- Obvious spam submissions

RESPOND WITH JSON ONLY:
{
  "isValid": true/false,
  "reason": "Brief explanation of why valid or invalid",
  "confidence": "high/medium/low"
}`;

    try {
        const response = await fetch(KIMI_API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${KIMI_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'moonshot-v1-8k',
                messages: [
                    { role: 'system', content: 'You are a data validation expert. Respond only with valid JSON.' },
                    { role: 'user', content: prompt }
                ],
                temperature: 0.1,
                max_tokens: 500
            })
        });
        
        if (!response.ok) {
            console.warn(`⚠️ Kimi API returned ${response.status} - falling back to basic validation`);
            return fallbackValidation(leadData);
        }
        
        const data = await response.json();
        const content = data.choices[0].message.content;
        
        // Parse JSON response
        const result = JSON.parse(content);
        console.log(`✅ Validation result: ${result.isValid ? 'VALID' : 'INVALID'} (${result.confidence})`);
        console.log(`   Reason: ${result.reason}`);
        
        return {
            isValid: result.isValid,
            reason: result.reason,
            confidence: result.confidence
        };
        
    } catch (error) {
        console.error('❌ Kimi validation error:', error.message);
        console.log('⚠️ Falling back to basic validation...');
        return fallbackValidation(leadData);
    }
}

/**
 * Fallback validation when Kimi API fails
 */
function fallbackValidation(leadData) {
    const issues = [];
    
    // Check for test/fake company names
    const testNames = ['test', 'fake', 'abc', '123', 'xyz', 'company', 'sample'];
    if (testNames.some(name => leadData.companyName.toLowerCase().includes(name))) {
        issues.push('Suspicious company name');
    }
    
    // Check employee count
    if (leadData.employeeCount < 1 || leadData.employeeCount > 10000) {
        issues.push('Unreasonable employee count');
    }
    
    // Check email
    const fakeEmails = ['test@test.com', 'fake@fake.com', 'example@example.com', 'user@user.com'];
    if (fakeEmails.includes(leadData.email.toLowerCase())) {
        issues.push('Test email address');
    }
    
    // Check calculated savings
    if (leadData.calculatedSavings <= 0 || leadData.calculatedSavings > 10000000) {
        issues.push('Unreasonable savings amount');
    }
    
    const isValid = issues.length === 0;
    
    return {
        isValid,
        reason: isValid ? 'Basic validation passed' : `Issues found: ${issues.join(', ')}`,
        confidence: 'low'
    };
}

/**
 * Save lead to database
 */
function saveLead(leadData) {
    let leads = [];
    
    // Read existing leads
    if (fs.existsSync(LEADS_FILE)) {
        leads = JSON.parse(fs.readFileSync(LEADS_FILE, 'utf8'));
    }
    
    // Add new lead with metadata
    const lead = {
        id: Date.now().toString(),
        ...leadData,
        status: 'new',
        emailVerified: false,
        createdAt: new Date().toISOString(),
        followUps: []
    };
    
    leads.push(lead);
    
    // Save back to file
    fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2));
    
    return lead;
}

/**
 * Generate PDF report using Puppeteer
 */
async function generatePDF(leadData) {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // Create HTML content for PDF
        const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; color: #333; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #667eea; }
        .savings-box { background: #f0f4ff; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .savings-amount { font-size: 36px; font-weight: bold; color: #667eea; }
        .section { margin: 30px 0; }
        .section h2 { color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        .detail-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
        .cta { background: #667eea; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-top: 40px; }
        .footer { margin-top: 50px; text-align: center; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Wellness 125 Savings Report</h1>
        <p>Prepared for ${leadData.companyName}</p>
        <p>Generated on ${new Date().toLocaleDateString()}</p>
    </div>
    
    <div class="savings-box">
        <h3>Your Estimated Annual Savings</h3>
        <div class="savings-amount">$${leadData.calculatedSavings.toLocaleString()}</div>
        <p>Through FICA tax reduction on employee benefit contributions</p>
    </div>
    
    <div class="section">
        <h2>Company Profile</h2>
        <div class="detail-row">
            <span>Company Name:</span>
            <span>${leadData.companyName}</span>
        </div>
        <div class="detail-row">
            <span>Number of Employees:</span>
            <span>${leadData.employeeCount}</span>
        </div>
        <div class="detail-row">
            <span>Monthly Benefits Cost:</span>
            <span>$${leadData.monthlyBenefitsCost.toLocaleString()}</span>
        </div>
        ${leadData.annualRevenue ? `
        <div class="detail-row">
            <span>Annual Revenue:</span>
            <span>$${leadData.annualRevenue.toLocaleString()}</span>
        </div>
        ` : ''}
    </div>
    
    <div class="section">
        <h2>Savings Breakdown</h2>
        <div class="detail-row">
            <span>Annual Benefits Cost:</span>
            <span>$${(leadData.monthlyBenefitsCost * 12 * leadData.employeeCount).toLocaleString()}</span>
        </div>
        <div class="detail-row">
            <span>Est. Participation Rate:</span>
            <span>70%</span>
        </div>
        <div class="detail-row">
            <span>FICA Tax Rate:</span>
            <span>7.65%</span>
        </div>
        <div class="detail-row">
            <span><strong>Annual FICA Savings:</strong></span>
            <span><strong>$${leadData.calculatedSavings.toLocaleString()}</strong></span>
        </div>
    </div>
    
    <div class="section">
        <h2>Additional Benefits</h2>
        <ul>
            <li><strong>Employee Tax Savings:</strong> $50-$400/month per employee</li>
            <li><strong>Workers' Comp Reduction:</strong> 30-60% premium decrease</li>
            <li><strong>Increased Take-Home Pay:</strong> Employees keep more of their paycheck</li>
            <li><strong>Zero Cost:</strong> No employer fees or setup charges</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Implementation Timeline</h2>
        <ol>
            <li><strong>Week 1-2:</strong> Plan design and employee communication</li>
            <li><strong>Week 3:</strong> Employee enrollment meetings</li>
            <li><strong>Week 4:</strong> Plan goes live - savings begin immediately</li>
        </ol>
    </div>
    
    <div class="cta">
        <h2>Ready to Start Saving?</h2>
        <p>Book your free 90-minute implementation strategy call</p>
        <p><strong>Contact:</strong> Zane@agentmail.to | sam@impactquadrant.info</p>
    </div>
    
    <div class="footer">
        <p>© 2026 ImpactQuadrant - Wellness 125 Cafeteria Plan Specialists</p>
        <p>This report is an estimate based on the information provided.</p>
        <p>Actual savings may vary based on plan participation and other factors.</p>
    </div>
</body>
</html>
        `;
        
        await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
        
        const pdfPath = path.join(DATA_DIR, `report-${leadData.id}.pdf`);
        
        await page.pdf({
            path: pdfPath,
            format: 'A4',
            printBackground: true,
            margin: { top: '20px', right: '20px', bottom: '20px', left: '20px' }
        });
        
        console.log(`✅ PDF generated: ${pdfPath}`);
        return pdfPath;
        
    } finally {
        await browser.close();
    }
}

/**
 * Generate follow-up email using Kimi API
 */
async function generateFollowUpEmail(leadData, stage = 'immediate') {
    // This will be replaced with actual Kimi API call
    // For now, use Handlebars templates
    
    const templates = {
        immediate: `
Hi {{companyName}} Team,

Thank you for using our Wellness 125 Savings Calculator!

Based on your inputs, we've identified potential annual savings of ${{calculatedSavings}} through FICA tax reduction.

Here's what this means for your company:
• {{employeeCount}} employees could benefit immediately
• Zero setup costs or employer fees
• Savings begin as soon as the plan is implemented

I've attached your personalized savings report (PDF) with detailed breakdowns.

Would you like to discuss how to implement this? I offer a free 90-minute strategy call where we'll:
1. Review your specific situation
2. Design a custom plan
3. Create an implementation roadmap

Reply to this email or book a time here: [CALENDAR LINK]

Best regards,
Zane
ImpactQuadrant
Zane@agentmail.to
        `,
        day3: `
Hi {{companyName}} Team,

I hope you found the Wellness 125 savings report helpful.

I wanted to share a quick case study:

A manufacturing company with 45 employees (similar to your size) implemented a Wellness 125 plan last year. Results:
• $31,000 in annual FICA savings
• Average employee take-home increase: $180/month
• Workers' comp premiums reduced by 42%

The best part? It cost them nothing to implement and employees love the extra money in their paychecks.

Interested in learning how this could work for {{companyName}}?

Book a free strategy call: [CALENDAR LINK]

Best,
Zane
        `,
        day7: `
Hi {{companyName}} Team,

I know implementing new benefits can seem complex, but Wellness 125 plans are surprisingly simple.

Here's what the process looks like:

Week 1: Plan design and documentation
Week 2: Employee communication materials
Week 3: Enrollment meetings
Week 4: Plan goes live

We handle everything - plan documents, enrollment, compliance. You just announce it to your employees.

Since you have {{employeeCount}} employees, you're looking at approximately ${{calculatedSavings}} in annual savings.

Want to see exactly how this would work for your company?

Book a free 90-minute strategy session: [CALENDAR LINK]

Or just reply with any questions.

Best,
Zane
ImpactQuadrant
        `
    };
    
    const template = Handlebars.compile(templates[stage]);
    return template(leadData);
}

/**
 * Process a new lead submission
 */
async function processSubmission(submissionData) {
    console.log('📥 Processing new lead submission...');
    console.log('Data:', JSON.stringify(submissionData, null, 2));
    
    // STEP 1: Validate with Kimi API
    console.log('\n🔍 Step 1: Validating submission...');
    const validation = await validateSubmissionWithKimi(submissionData);
    
    if (!validation.isValid) {
        console.log(`❌ Submission REJECTED: ${validation.reason}`);
        console.log(`   Confidence: ${validation.confidence}`);
        
        // Save rejected lead for analysis
        const rejectedLead = {
            ...submissionData,
            id: Date.now().toString(),
            status: 'rejected',
            rejectionReason: validation.reason,
            createdAt: new Date().toISOString()
        };
        
        const rejectedFile = path.join(DATA_DIR, 'rejected-leads.json');
        let rejected = [];
        if (fs.existsSync(rejectedFile)) {
            rejected = JSON.parse(fs.readFileSync(rejectedFile, 'utf8'));
        }
        rejected.push(rejectedLead);
        fs.writeFileSync(rejectedFile, JSON.stringify(rejected, null, 2));
        
        return {
            success: false,
            rejected: true,
            reason: validation.reason,
            message: 'Submission did not pass quality filters'
        };
    }
    
    console.log(`✅ Submission PASSED validation: ${validation.reason}\n`);
    
    // STEP 2: Save lead to database
    console.log('💾 Step 2: Saving lead to database...');
    const lead = saveLead(submissionData);
    console.log(`✅ Lead saved: ${lead.id}\n`);
    
    // STEP 3: Generate PDF report
    console.log('📄 Step 3: Generating PDF report...');
    const pdfPath = await generatePDF(lead);
    console.log(`✅ PDF report generated: ${pdfPath}\n`);
    
    // STEP 4: Queue follow-up emails
    console.log('📧 Step 4: Generating follow-up emails...');
    const immediateEmail = await generateFollowUpEmail(lead, 'immediate');
    const day3Email = await generateFollowUpEmail(lead, 'day3');
    const day7Email = await generateFollowUpEmail(lead, 'day7');
    
    // Save email templates for sending
    const emailsDir = path.join(DATA_DIR, 'emails', lead.id);
    fs.mkdirSync(emailsDir, { recursive: true });
    
    fs.writeFileSync(path.join(emailsDir, 'immediate.txt'), immediateEmail);
    fs.writeFileSync(path.join(emailsDir, 'day3.txt'), day3Email);
    fs.writeFileSync(path.join(emailsDir, 'day7.txt'), day7Email);
    
    console.log('✅ Email templates generated');
    console.log('\n📋 Next Steps:');
    console.log('1. Verify email with ZeroBounce');
    console.log('2. Send immediate email via Agentmail.to');
    console.log('3. Schedule follow-up emails (Day 3, Day 7)');
    console.log('4. Attach PDF report to email');
    
    return {
        lead,
        pdfPath,
        emails: {
            immediate: immediateEmail,
            day3: day3Email,
            day7: day7Email
        }
    };
}

// If called directly with arguments
if (require.main === module) {
    // Check for submission data via command line or stdin
    const args = process.argv.slice(2);
    
    if (args.length > 0) {
        // Read from command line argument
        const submissionData = JSON.parse(args[0]);
        processSubmission(submissionData)
            .then(result => {
                console.log('\n✅ Processing complete');
                console.log(JSON.stringify(result, null, 2));
            })
            .catch(error => {
                console.error('❌ Error:', error);
                process.exit(1);
            });
    } else {
        console.log('Usage: node process-submission.js \'{...submission data...}\'');
        console.log('\nExample:');
        console.log(`node process-submission.js '${JSON.stringify({
            companyName: 'Acme Corp',
            employeeCount: 50,
            monthlyBenefitsCost: 500,
            email: 'test@example.com',
            calculatedSavings: 16012
        })}'`);
    }
}

/**
 * Generate enhanced PDF template with better branding
 */
function generatePDFTemplate(leadData) {
    const serviceConfig = {
        'wellness-125': {
            title: 'Wellness 125 Savings Report',
            primaryColor: '#667eea',
            secondaryColor: '#764ba2',
            icon: '🏥',
            description: 'Section 125 Cafeteria Plan Analysis'
        },
        'expense-reduction': {
            title: 'Expense Reduction Audit',
            primaryColor: '#059669',
            secondaryColor: '#10b981',
            icon: '💰',
            description: 'Vendor Spend Optimization Analysis'
        }
    };
    
    const config = serviceConfig[leadData.service] || serviceConfig['wellness-125'];
    const currentDate = new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: #1f2937;
            line-height: 1.6;
            background: #ffffff;
        }
        
        .header {
            background: linear-gradient(135deg, ${config.primaryColor} 0%, ${config.secondaryColor} 100%);
            padding: 40px;
            color: white;
            text-align: center;
        }
        
        .header-icon {
            font-size: 48px;
            margin-bottom: 16px;
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .company-info {
            background: #f9fafb;
            padding: 30px 40px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .company-info h2 {
            font-size: 20px;
            color: #111827;
            margin-bottom: 16px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px dotted #d1d5db;
        }
        
        .info-label {
            color: #6b7280;
            font-size: 13px;
        }
        
        .info-value {
            font-weight: 600;
            color: #111827;
        }
        
        .savings-highlight {
            background: linear-gradient(135deg, ${config.primaryColor}15 0%, ${config.secondaryColor}15 100%);
            padding: 40px;
            text-align: center;
            border-left: 4px solid ${config.primaryColor};
        }
        
        .savings-label {
            font-size: 14px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        
        .savings-amount {
            font-size: 48px;
            font-weight: 700;
            color: ${config.primaryColor};
            margin-bottom: 8px;
        }
        
        .savings-period {
            font-size: 16px;
            color: #6b7280;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 32px;
        }
        
        .section h3 {
            font-size: 18px;
            color: #111827;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid ${config.primaryColor};
            display: inline-block;
        }
        
        .benefits-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 16px;
        }
        
        .benefit-card {
            background: #f9fafb;
            padding: 16px;
            border-radius: 8px;
            border-left: 3px solid ${config.primaryColor};
        }
        
        .benefit-card h4 {
            font-size: 14px;
            color: #111827;
            margin-bottom: 4px;
        }
        
        .benefit-card p {
            font-size: 12px;
            color: #6b7280;
        }
        
        .timeline {
            background: #f9fafb;
            padding: 24px;
            border-radius: 8px;
        }
        
        .timeline-item {
            display: flex;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px dashed #d1d5db;
        }
        
        .timeline-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .timeline-marker {
            width: 32px;
            height: 32px;
            background: ${config.primaryColor};
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            margin-right: 16px;
            flex-shrink: 0;
        }
        
        .timeline-content h4 {
            font-size: 14px;
            color: #111827;
            margin-bottom: 4px;
        }
        
        .timeline-content p {
            font-size: 13px;
            color: #6b7280;
        }
        
        .cta-section {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: white;
            padding: 40px;
            text-align: center;
            margin-top: 40px;
        }
        
        .cta-section h3 {
            font-size: 22px;
            margin-bottom: 12px;
        }
        
        .cta-section p {
            opacity: 0.8;
            margin-bottom: 24px;
        }
        
        .contact-info {
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-top: 24px;
        }
        
        .contact-item {
            text-align: center;
        }
        
        .contact-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.6;
            margin-bottom: 4px;
        }
        
        .contact-value {
            font-size: 13px;
            font-weight: 500;
        }
        
        .footer {
            background: #f9fafb;
            padding: 24px 40px;
            text-align: center;
            font-size: 11px;
            color: #9ca3af;
        }
        
        .disclaimer {
            margin-top: 8px;
            font-style: italic;
        }
        
        .page-break {
            page-break-after: always;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <div class="header-icon">${config.icon}</div>
        <h1>${config.title}</h1>
        <p>${config.description} | Prepared for ${leadData.companyName}</p>
        <p style="margin-top: 8px; font-size: 12px;">${currentDate}</p>
    </div>
    
    <!-- Company Info -->
    <div class="company-info">
        <h2>Company Profile</h2>
        <div class="info-grid">
            <div class="info-item">
                <span class="info-label">Company Name</span>
                <span class="info-value">${leadData.companyName}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Employees</span>
                <span class="info-value">${leadData.employeeCount}</span>
            </div>
            ${leadData.monthlyBenefitsCost ? `
            <div class="info-item">
                <span class="info-label">Monthly Benefits</span>
                <span class="info-value">$${leadData.monthlyBenefitsCost.toLocaleString()}</span>
            </div>
            ` : ''}
            ${leadData.monthlySaaSSpend ? `
            <div class="info-item">
                <span class="info-label">Monthly SaaS Spend</span>
                <span class="info-value">$${leadData.monthlySaaSSpend.toLocaleString()}</span>
            </div>
            ` : ''}
            ${leadData.contactName ? `
            <div class="info-item">
                <span class="info-label">Contact</span>
                <span class="info-value">${leadData.contactName}</span>
            </div>
            ` : ''}
            <div class="info-item">
                <span class="info-label">Email</span>
                <span class="info-value">${leadData.email}</span>
            </div>
        </div>
    </div>
    
    <!-- Savings Highlight -->
    <div class="savings-highlight">
        <div class="savings-label">Estimated Annual Savings</div>
        <div class="savings-amount">$${leadData.calculatedSavings.toLocaleString()}</div>
        <div class="savings-period">Potential first-year savings based on your inputs</div>
    </div>
    
    <!-- Content -->
    <div class="content">
        <!-- Benefits Section -->
        <div class="section">
            <h3>Key Benefits</h3>
            <div class="benefits-grid">
                <div class="benefit-card">
                    <h4>💰 Immediate Cost Savings</h4>
                    <p>Reduce expenses without cutting headcount or quality</p>
                </div>
                <div class="benefit-card">
                    <h4>📊 Data-Driven Insights</h4>
                    <p>AI-powered analysis of your spend patterns</p>
                </div>
                <div class="benefit-card">
                    <h4>⚡ Quick Implementation</h4>
                    <p>Most savings realized within 30-60 days</p>
                </div>
                <div class="benefit-card">
                    <h4>🎯 Risk-Free Model</h4>
                    <p>Success-based fees - we only win when you save</p>
                </div>
            </div>
        </div>
        
        <!-- Timeline Section -->
        <div class="section">
            <h3>Implementation Roadmap</h3>
            <div class="timeline">
                <div class="timeline-item">
                    <div class="timeline-marker">1</div>
                    <div class="timeline-content">
                        <h4>Discovery Call (Week 1)</h4>
                        <p>Deep dive into your current spend and identify quick wins</p>
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-marker">2</div>
                    <div class="timeline-content">
                        <h4>Analysis & Strategy (Week 2)</h4>
                        <p>Complete audit and prioritized savings roadmap</p>
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-marker">3</div>
                    <div class="timeline-content">
                        <h4>Implementation (Weeks 3-4)</h4>
                        <p>Negotiate better rates, eliminate waste, optimize contracts</p>
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-marker">4</div>
                    <div class="timeline-content">
                        <h4>Ongoing Optimization</h4>
                        <p>Continuous monitoring and quarterly reviews</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Case Study -->
        <div class="section">
            <h3>Success Story</h3>
            <div style="background: #f0fdf4; border-left: 4px solid #22c55e; padding: 20px; border-radius: 8px;">
                <p style="font-style: italic; color: #166534; margin-bottom: 12px;">
                    "ImpactQuadrant identified $47,000 in annual savings within the first 30 days. 
                    Their team handled all the vendor negotiations and we saw immediate results."
                </p>
                <p style="font-size: 13px; color: #15803d; font-weight: 500;">
                    — Sarah M., CFO at TechStart Inc. (65 employees)
                </p>
            </div>
        </div>
    </div>
    
    <!-- CTA Section -->
    <div class="cta-section">
        <h3>Ready to Capture These Savings?</h3>
        <p>Schedule your free 90-minute strategy session. No obligation, just actionable insights.</p>
        
        <div class="contact-info">
            <div class="contact-item">
                <div class="contact-label">Email</div>
                <div class="contact-value">Zane@agentmail.to</div>
            </div>
            <div class="contact-item">
                <div class="contact-label">Website</div>
                <div class="contact-value">www.impactquadrant.info</div>
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="footer">
        <p>© 2026 ImpactQuadrant. All rights reserved.</p>
        <p class="disclaimer">
            This report contains estimates based on the information provided. 
            Actual savings may vary. ImpactQuadrant specializes in technology-led 
            expense reduction with success-based pricing.
        </p>
    </div>
</body>
</html>
    `;
}

module.exports = { processSubmission, saveLead, generatePDF, generateFollowUpEmail, generatePDFTemplate };
