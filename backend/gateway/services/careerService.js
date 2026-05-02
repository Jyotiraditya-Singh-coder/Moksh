const httpClient = require('../utils/httpClient');
const client = httpClient(process.env.AI_CAREER_URL);

/**
 * Analyze skill gap between resume and target role
 * @param {Object} data - { resumeText, targetRole }
 * @returns {Promise<Object>} - { missingSkills, roadmap }
 */
exports.analyzeSkillGap = (data) => client.post('/analyze', data);

/**
 * Add a new job role to the skill gap database (fine‑tuning)
 * @param {Object} data - { job_title, skills }
 * @returns {Promise<Object>} - { title, skills }
 */
exports.addJobRole = (data) => client.post('/add-job-role', data);

/**
 * List all stored job roles
 * @returns {Promise<Array>} - Array of { title, skills }
 */
exports.listJobRoles = () => client.get('/job-roles');

/**
 * Rebuild the FAISS index (admin only)
 * @returns {Promise<Object>} - { message }
 */
exports.rebuildIndex = () => client.post('/rebuild-index');