const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_VOICE_URL);

exports.askVoiceTutor = async ({ audioBase64, language }) => {
  return client.post('/ask', { audio: audioBase64, language });
};