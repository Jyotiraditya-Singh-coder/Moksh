const skillService = require('../services/skillNavigatorService');

exports.createProfile = async (req, res, next) => {
  try {
    const payload = { ...req.body, student_id: req.user.id };
    const result = await skillService.createProfile(payload);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.getOptimalPath = async (req, res, next) => {
  try {
    const payload = { ...req.body, student_id: req.user.id };
    const result = await skillService.getOptimalPath(payload);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.getCareerReadiness = async (req, res, next) => {
  try {
    const payload = { ...req.body, student_id: req.user.id };
    // Need skill_mastery from somewhere - could be passed in body or fetched from profile
    const result = await skillService.getCareerReadiness(payload);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.updateKT = async (req, res, next) => {
  try {
    const result = await skillService.updateKT(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};