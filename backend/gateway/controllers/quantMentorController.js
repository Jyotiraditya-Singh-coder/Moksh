const quantService = require('../services/quantMentorService');

exports.getQuantGuide = async (req, res, next) => {
  try {
    const result = await quantService.getQuantGuide(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.getTopicInfo = async (req, res, next) => {
  try {
    const result = await quantService.getTopicInfo(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.listTopics = async (req, res, next) => {
  try {
    const result = await quantService.listTopics();
    res.json(result);
  } catch (err) {
    next(err);
  }
};