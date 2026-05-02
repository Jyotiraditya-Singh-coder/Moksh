const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_DROPOUT_URL);

exports.predictDropoutRisk = async (features) => {
  return client.post('/predict', features);
};