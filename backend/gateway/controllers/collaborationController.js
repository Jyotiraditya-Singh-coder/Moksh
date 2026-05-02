const collabService = require('../services/collaborationService');

exports.formGroups = async (req, res, next) => {
  try {
    const result = await collabService.formGroups(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.detectEmotion = async (req, res, next) => {
  try {
    const result = await collabService.detectEmotion(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};