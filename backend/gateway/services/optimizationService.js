const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_OPTIMIZE_URL);

exports.getOptimizedPlan = async (input) => {
  return client.post('/optimize', input);
};