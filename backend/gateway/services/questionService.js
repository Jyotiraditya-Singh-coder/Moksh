const httpClient = require('../utils/httpClient');

const client = httpClient(process.env.AI_QUESTION_URL);

exports.generateQuestion = async (profile) => {
  return client.post('/generate', profile);
};