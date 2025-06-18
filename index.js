const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 3000;
const FLASK_API_URL = 'http://localhost:5000/trigger';

app.use(express.static('public'));
app.use(express.json());

app.post('/trigger-logger', async (req, res) => {
  try {
    const response = await axios.post(FLASK_API_URL, {
      mode: req.body.mode || 'text'
    });
    res.json(response.data);
  } catch (err) {
    console.error('[ERROR] Flask API gagal:', err.message);
    res.status(500).json({ status: 'error', message: 'Gagal menghubungi Flask API' });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Express frontend aktif di http://localhost:${PORT}`);
});
