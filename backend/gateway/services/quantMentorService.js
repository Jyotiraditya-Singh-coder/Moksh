const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_QUANT_MENTOR_URL);

exports.getQuantGuide = async (data) => client.post('/guide', data);
exports.getTopicInfo = async (data) => client.post('/topic-info', data);
exports.listTopics = async () => client.get('/topics');