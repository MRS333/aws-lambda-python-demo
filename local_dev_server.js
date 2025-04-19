import express from 'express';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(cors());

// Simple test route
app.get('/', (req, res) => {
  res.json({ message: 'Server is running!' });
});

app.get('/users/:userId', (req, res) => {
  const { userId } = req.params;
  const { name = 'World' } = req.query;
  res.json({
    message: `Hello, ${name}!`,
    userId,
    timestamp: new Date().toISOString()
  });
});

app.post('/users/:userId', (req, res) => {
  const { userId } = req.params;
  const { name = 'World', message = '' } = req.body;
  res.json({
    message: `Hello, ${name}! You said: ${message}`,
    userId,
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(port, '0.0.0.0', () => {
  console.log(`Server running at http://localhost:${port}`);
  console.log(`Try these endpoints:`);
  console.log(`  GET  http://localhost:${port}/users/12345?name=TestUser`);
  console.log(`  POST http://localhost:${port}/users/12345 with body: {"name": "TestUser", "message": "Hello!"}`);
});