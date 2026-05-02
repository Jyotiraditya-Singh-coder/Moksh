const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_COLLABORATION_URL);

exports.formGroups = (data) => client.post('/form-groups', data);
exports.detectEmotion = (data) => client.post('/detect-emotion', data);
// WebSocket handled separately (direct connection)