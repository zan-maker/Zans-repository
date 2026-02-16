#!/usr/bin/env node
/**
 * Simple HTTP Webhook Server for Lead Magnet Submissions
 * Receives POST requests from lead magnet forms
 * 
 * Usage: node webhook-server.js
 * Port: 3000 (configurable via PORT env var)
 */

const http = require('http');
const url = require('url');
const { processSubmission } = require('./process-submission');

const PORT = process.env.PORT || 3000;

// Simple CORS headers
const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
};

const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    
    // Handle CORS preflight
    if (req.method === 'OPTIONS') {
        res.writeHead(200, corsHeaders);
        res.end();
        return;
    }
    
    // Health check endpoint
    if (parsedUrl.pathname === '/health' && req.method === 'GET') {
        res.writeHead(200, corsHeaders);
        res.end(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));
        return;
    }
    
    // Lead submission endpoint
    if (parsedUrl.pathname === '/api/submit-lead' && req.method === 'POST') {
        let body = '';
        
        req.on('data', chunk => {
            body += chunk.toString();
        });
        
        req.on('end', async () => {
            try {
                const submissionData = JSON.parse(body);
                
                // Validate required fields
                if (!submissionData.email || !submissionData.companyName) {
                    res.writeHead(400, corsHeaders);
                    res.end(JSON.stringify({ 
                        error: 'Missing required fields: email, companyName' 
                    }));
                    return;
                }
                
                console.log('📥 Received lead submission:', submissionData.email);
                
                // Process submission
                const result = await processSubmission(submissionData);
                
                res.writeHead(200, corsHeaders);
                res.end(JSON.stringify({
                    success: true,
                    leadId: result.lead.id,
                    message: 'Lead processed successfully'
                }));
                
            } catch (error) {
                console.error('❌ Error processing submission:', error);
                res.writeHead(500, corsHeaders);
                res.end(JSON.stringify({ 
                    error: 'Internal server error',
                    message: error.message 
                }));
            }
        });
        
        return;
    }
    
    // 404 for unknown routes
    res.writeHead(404, corsHeaders);
    res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, () => {
    console.log(`🚀 Lead Magnet Webhook Server running on port ${PORT}`);
    console.log(`\nEndpoints:`);
    console.log(`  GET  /health          - Health check`);
    console.log(`  POST /api/submit-lead - Submit lead data`);
    console.log(`\nPress Ctrl+C to stop`);
});

module.exports = server;
