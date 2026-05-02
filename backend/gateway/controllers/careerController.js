const careerService = require('../services/careerService');

/**
 * Analyze skill gap
 */
exports.analyzeSkillGap = async (req, res, next) => {
  try {
    const result = await careerService.analyzeSkillGap(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

/**
 * Add a new job role (teacher/admin only)
 */
exports.addJobRole = async (req, res, next) => {
  try {
    const result = await careerService.addJobRole(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

/**
 * List all job roles
 */
exports.listJobRoles = async (req, res, next) => {
  try {
    const result = await careerService.listJobRoles();
    res.json(result);
  } catch (err) {
    next(err);
  }
};

/**
 * Rebuild FAISS index (admin only)
 */
exports.rebuildIndex = async (req, res, next) => {
  try {
    const result = await careerService.rebuildIndex();
    res.json(result);
  } catch (err) {
    next(err);
  }
};