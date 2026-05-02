const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_CONTENT_AUTHORING_URL);

exports.generateLesson = (data) => client.post('/generate-lesson', data);
exports.extractSkills = (data) => client.post('/extract-skills', data);