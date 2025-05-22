require('dotenv').config();
const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static('public'));

app.get('/api/stock', async (req, res) => {
  const { symbol } = req.query;
  const apiKey = process.env.ALPHAVANTAGE_KEY;
  try {
    const response = await axios.get(`https://www.alphavantage.co/query`, {
      params: {
        function: 'TIME_SERIES_MONTHLY_ADJUSTED',
        symbol,
        apikey: apiKey
      }
    });
    res.json(response.data);
  } catch (error) {
    console.error('Stock API error:', error.response?.data || error.message);
    res.status(500).json({ error: 'Failed to fetch stock data' });
  }
});

app.get('/api/weather-tile', async (req, res) => {
  const { layer, z, x, y } = req.query;
  const apiKey = process.env.OPENWEATHERMAP_KEY;

  if (!layer || !z || !x || !y) {
    return res.status(400).json({ error: 'Missing tile parameters: layer, z, x, y' });
  }

  const tileUrl = `https://tile.openweathermap.org/map/${layer}/${z}/${x}/${y}.png?appid=${apiKey}`;
  try {
    const response = await axios.get(tileUrl, { responseType: 'arraybuffer' });
    res.set('Content-Type', 'image/png');
    res.send(response.data);
  } catch (error) {
    console.error('Weather tile error:', error.message);
    res.status(500).json({ error: 'Failed to fetch weather tile' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});