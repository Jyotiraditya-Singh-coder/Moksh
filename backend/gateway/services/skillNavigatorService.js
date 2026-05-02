const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_SKILL_NAVIGATOR_URL);

exports.createProfile = async (data) => client.post('/profile', data);
exports.getOptimalPath = async (data) => client.post('/optimal-path', data);
exports.getCareerReadiness = async (data) => client.post('/career-readiness', data);
exports.updateKT = async (data) => client.post('/kt-update', data);