const express = require('express');
const cors = require('cors');
const http = require('http');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

app.post('/v1/chat/completions', (req, res) => {
    const requestData = JSON.stringify(req.body);
    
    const options = {
        hostname: '127.0.0.1',
        port: 1234,
        path: '/v1/chat/completions',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(requestData)
        }
    };

    const proxyReq = http.request(options, (proxyRes) => {
        let responseData = '';
        
        proxyRes.on('data', chunk => {
            responseData += chunk;
        });
        
        proxyRes.on('end', () => {
            console.log('Response from LM Studio:', responseData);
            res.status(proxyRes.statusCode).send(responseData);
        });
    });

    proxyReq.on('error', (error) => {
        console.error('Error:', error);
        res.status(500).json({ error: error.message });
    });

    proxyReq.write(requestData);
    proxyReq.end();
});

app.listen(PORT, () => {
    console.log(`Server running on http://127.0.0.1:${PORT}`);
});