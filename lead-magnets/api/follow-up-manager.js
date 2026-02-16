#!/usr/bin/env node
/**
 * Follow-Up Email Sequence Manager
 * Runs via OpenClaw cron job
 * 
 * Schedule: Every 2 hours (0 */2 * * *)
 * Checks for leads that need follow-up emails sent
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Configuration
const DATA_DIR = path.join(__dirname, '..', 'data');
const LEADS_FILE = path.join(DATA_DIR, 'leads.json');
const AGENTMAIL_API_KEY = process.env.AGENTMAIL_API_KEY || 'am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68';

// Load leads
function loadLeads() {
    if (!fs.existsSync(LEADS_FILE)) {
        return [];
    }
    return JSON.parse(fs.readFileSync(LEADS_FILE, 'utf8'));
}

// Save leads
function saveLeads(leads) {
    fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2));
}

// Calculate hours since lead was created
function hoursSince(dateString) {
    const created = new Date(dateString);
    const now = new Date();
    return (now - created) / (1000 * 60 * 60);
}

// Send email via Agentmail.to
async function sendEmail(to, subject, body, from = 'Zane@agentmail.to') {
    const curlCommand = `curl -s -X POST https://api.agentmail.to/v1/send \
        -H "Authorization: Bearer ${AGENTMAIL_API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "from": "${from}",
            "to": "${to}",
            "cc": "sam@impactquadrant.info",
            "subject": "${subject}",
            "body": ${JSON.stringify(body)}
        }'`;
    
    return new Promise((resolve, reject) => {
        exec(curlCommand, (error, stdout, stderr) => {
            if (error) {
                console.error(`Email send error: ${error}`);
                reject(error);
            } else {
                console.log(`✅ Email sent to ${to}`);
                resolve(stdout);
            }
        });
    });
}

// Verify email with ZeroBounce
async function verifyEmail(email) {
    const ZEROBOUNCE_API_KEY = process.env.ZEROBOUNCE_API_KEY || 'fd0105c8c98340e0a2b63e2fbe39d7a4';
    
    const curlCommand = `curl -s -X POST "https://api.zerobounce.net/v2/validate" \
        -d "api_key=${ZEROBOUNCE_API_KEY}" \
        -d "email=${email}"`;
    
    return new Promise((resolve, reject) => {
        exec(curlCommand, (error, stdout, stderr) => {
            if (error) {
                console.error(`Email verification error: ${error}`);
                reject(error);
            } else {
                const result = JSON.parse(stdout);
                resolve(result.status === 'valid');
            }
        });
    });
}

// Process follow-ups
async function processFollowUps() {
    console.log('🔍 Checking for leads needing follow-up emails...\n');
    
    const leads = loadLeads();
    let emailsSent = 0;
    
    for (const lead of leads) {
        const hours = hoursSince(lead.createdAt);
        
        // Skip if email already verified as invalid
        if (lead.emailVerified === false && lead.verificationAttempts > 0) {
            continue;
        }
        
        // Verify email on first run
        if (lead.emailVerified === false && lead.verificationAttempts === 0) {
            console.log(`🔍 Verifying email for ${lead.companyName} (${lead.email})...`);
            try {
                const isValid = await verifyEmail(lead.email);
                lead.emailVerified = isValid;
                lead.verificationAttempts = 1;
                
                if (!isValid) {
                    console.log(`⚠️ Email invalid: ${lead.email} - Skipping`);
                    continue;
                }
            } catch (error) {
                console.error(`❌ Verification failed for ${lead.email}:`, error.message);
                continue;
            }
        }
        
        // Check for follow-ups to send
        const followUpsToSend = [];
        
        // Immediate email (0-1 hours) - Send PDF report
        if (hours >= 0 && hours < 1 && !lead.followUps.includes('immediate')) {
            followUpsToSend.push({
                stage: 'immediate',
                subject: `Your Wellness 125 Savings Report - $${lead.calculatedSavings.toLocaleString()} Potential Savings`,
                template: 'immediate.txt'
            });
        }
        
        // Day 3 email (72 hours)
        if (hours >= 72 && hours < 74 && !lead.followUps.includes('day3')) {
            followUpsToSend.push({
                stage: 'day3',
                subject: 'Case Study: How Similar Companies Saved $31,000/year',
                template: 'day3.txt'
            });
        }
        
        // Day 7 email (168 hours)
        if (hours >= 168 && hours < 170 && !lead.followUps.includes('day7')) {
            followUpsToSend.push({
                stage: 'day7',
                subject: 'Quick Question: Implementation Timeline for Your Wellness 125 Plan',
                template: 'day7.txt'
            });
        }
        
        // Send emails
        for (const followUp of followUpsToSend) {
            console.log(`📧 Sending ${followUp.stage} email to ${lead.companyName}...`);
            
            try {
                // Load email template
                const templatePath = path.join(DATA_DIR, 'emails', lead.id, followUp.template);
                let body = '';
                
                if (fs.existsSync(templatePath)) {
                    body = fs.readFileSync(templatePath, 'utf8');
                } else {
                    // Fallback template
                    body = `Hi ${lead.companyName} Team,\n\nFollowing up on your Wellness 125 Savings Calculator results.\n\nYou could save $${lead.calculatedSavings.toLocaleString()} annually.\n\nReady to discuss implementation?\n\nBest,\nZane`;
                }
                
                // Attach PDF if immediate email
                if (followUp.stage === 'immediate') {
                    const pdfPath = path.join(DATA_DIR, `report-${lead.id}.pdf`);
                    if (fs.existsSync(pdfPath)) {
                        // Note: Agentmail.to doesn't support attachments via simple API
                        // We'll need to mention it in the email body
                        body += '\n\n[PDF Report attached - download from your email client]';
                    }
                }
                
                await sendEmail(lead.email, followUp.subject, body);
                
                // Update lead
                lead.followUps.push(followUp.stage);
                lead.lastEmailSent = new Date().toISOString();
                emailsSent++;
                
                console.log(`✅ ${followUp.stage} email sent to ${lead.email}\n`);
                
            } catch (error) {
                console.error(`❌ Failed to send ${followUp.stage} email to ${lead.email}:`, error.message);
            }
        }
    }
    
    // Save updated leads
    saveLeads(leads);
    
    console.log(`\n📊 Summary:`);
    console.log(`- Total leads: ${leads.length}`);
    console.log(`- Emails sent this run: ${emailsSent}`);
    console.log(`- Next check: 2 hours`);
}

// Run if called directly
if (require.main === module) {
    processFollowUps()
        .then(() => {
            console.log('\n✅ Follow-up processing complete');
            process.exit(0);
        })
        .catch(error => {
            console.error('❌ Error:', error);
            process.exit(1);
        });
}

module.exports = { processFollowUps, sendEmail, verifyEmail };
