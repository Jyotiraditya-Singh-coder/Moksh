const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_SUBJECT_TRAINING_URL);

exports.generateProblem = async (data) => client.post('/generate-problem', data);
exports.analyzeSolution = async (data) => client.post('/analyze-solution', data);
exports.validateMath = async (data) => client.post('/validate-math', data);
exports.validateNumerical = async (data) => client.post('/validate-numerical', data);
exports.compareAlgorithms = async (data) => client.post('/compare-algorithms', data);
exports.analyzeAlgorithm = async (data) => client.post('/analyze-algorithm', data);
exports.searchApproaches = async (data) => client.post('/search-approaches', data);
exports.getWeaknessProfile = async (data) => client.post('/weakness-profile', data);
exports.getPersonalizedSequence = async (data) => client.post('/personalized-sequence', data);