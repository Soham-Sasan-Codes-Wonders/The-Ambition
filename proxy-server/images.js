const express = require('express');
const cors = require('cors');
const http = require('http');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3002;

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        const uploadDir = 'uploads';
        // Create uploads directory if it doesn't exist
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir);
        }
        cb(null, uploadDir);
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ 
    storage: storage,
    limits: {
        fileSize: 5 * 1024 * 1024 // 5MB limit
    },
    fileFilter: function(req, file, cb) {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.mimetype)) {
            cb(new Error('Only .png, .jpg and .gif files are allowed'));
            return;
        }
        cb(null, true);
    }
});

app.use(cors());
app.use(express.json());
app.use('/uploads', express.static('uploads')); // Serve uploaded files

// Regular chat completion endpoint
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

// File upload endpoint
app.post('/upload', upload.single('image'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    // Return the file URL
    const fileUrl = `http://localhost:${PORT}/uploads/${req.file.filename}`;
    res.json({ 
        success: true, 
        fileUrl: fileUrl,
        filename: req.file.filename
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    if (err instanceof multer.MulterError) {
        return res.status(400).json({ error: err.message });
    }
    res.status(500).json({ error: err.message });
});

app.listen(PORT, () => {
    console.log(`Server running on http://127.0.0.1:${PORT}`);
});