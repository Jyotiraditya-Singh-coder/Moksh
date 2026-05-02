const subjectService = require('../services/subjectTrainingService');

exports.generateProblem = async (req, res, next) => {
  try {
    const result = await subjectService.generateProblem(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.analyzeSolution = async (req, res, next) => {
  try {
    // Add studentId from auth
    const payload = { ...req.body, studentId: req.user.id };
    const result = await subjectService.analyzeSolution(payload);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.validateMath = async (req, res, next) => {
  try {
    const result = await subjectService.validateMath(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.validateNumerical = async (req, res, next) => {
  try {
    const result = await subjectService.validateNumerical(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.compareAlgorithms = async (req, res, next) => {
  try {
    const result = await subjectService.compareAlgorithms(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.analyzeAlgorithm = async (req, res, next) => {
  try {
    const result = await subjectService.analyzeAlgorithm(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.searchApproaches = async (req, res, next) => {
  try {
    const result = await subjectService.searchApproaches(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.getWeaknessProfile = async (req, res, next) => {
  try {
    const result = await subjectService.getWeaknessProfile({ studentId: req.user.id });
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.getPersonalizedSequence = async (req, res, next) => {
  try {
    const payload = { ...req.body, studentId: req.user.id };
    const result = await subjectService.getPersonalizedSequence(payload);
    res.json(result);
  } catch (err) {
    next(err);
  }
};