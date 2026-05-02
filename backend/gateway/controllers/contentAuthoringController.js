const contentService = require('../services/contentAuthoringService');

exports.generateLesson = async (req, res, next) => {
  try {
    const result = await contentService.generateLesson(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.extractSkills = async (req, res, next) => {
  try {
    const result = await contentService.extractSkills(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};