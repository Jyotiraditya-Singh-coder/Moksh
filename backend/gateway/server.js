require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const connectDB = require('./config/db'); // keep mongo if needed by other services
const { connectMysqlDB } = require('./config/mysqlDb'); // Add MySQL
const { logger, expressLogger } = require('./middleware/logger');
const errorHandler = require('./middleware/errorHandler');
const { clerkMiddleware } = require('@clerk/express'); // Clerk integration

const app = express();

connectDB();
connectMysqlDB(); // Initialize MySQL database

app.use(helmet());
app.use(cors());

// Add clerk middleware globally for auth context
app.use(clerkMiddleware());

// Webhook route needs raw body, mount it BEFORE express.json()
const { clerkWebhook } = require('./controllers/authController');
app.post('/api/auth/webhook', express.raw({ type: 'application/json' }), clerkWebhook);

app.use(express.json({ limit: '10mb' }));
app.use(expressLogger);

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use('/api', limiter);

// Routes
app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/student', require('./routes/studentRoutes'));
app.use('/api/questions', require('./routes/questionRoutes'));
app.use('/api/ml', require('./routes/mlRoutes'));
app.use('/api/career', require('./routes/careerRoutes'));
app.use('/api/voice', require('./routes/voiceRoutes'));
app.use('/api/optimize', require('./routes/optimizeRoutes'));
app.use('/api/subject', require('./routes/subjectTrainingRoutes'));
app.use('/api/skill-navigator', require('./routes/skillNavigatorRoutes'));
app.use('/api/quant-mentor', require('./routes/quantMentorRoutes'));
app.use('/api/content-authoring', require('./routes/contentAuthoringRoutes'));
app.use('/api/collaboration', require('./routes/collaborationRoutes'));
app.use('/api/resources', require('./routes/resourceRoutes'));
app.use('/api/fine-tune', require('./routes/fineTuneRoutes'));

app.get('/health', (req, res) => res.send('OK'));

app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => logger.info(`Gateway running on port ${PORT}`));