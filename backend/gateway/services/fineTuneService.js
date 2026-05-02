const httpClient = require('../utils/httpClient');

// Dropout model
const dropoutClient = httpClient(process.env.AI_DROPOUT_URL);
exports.fineTuneDropout = (data) => dropoutClient.post('/fine-tune', data);

// Recommendation engine
const recClient = httpClient(process.env.AI_RECOMMEND_URL);
exports.fineTuneRecommendation = (data) => recClient.post('/fine-tune', data);

// Skill navigator
const skillClient = httpClient(process.env.AI_SKILL_NAVIGATOR_URL);
exports.fineTuneKT = (data) => skillClient.post('/fine-tune-kt', data);