const fineTuneService = require('../services/fineTuneService');

exports.fineTuneDropout = async (req, res, next) => {
  try {
    const result = await fineTuneService.fineTuneDropout(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.fineTuneRecommendation = async (req, res, next) => {
  try {
    const result = await fineTuneService.fineTuneRecommendation(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.fineTuneKT = async (req, res, next) => {
  try {
    const result = await fineTuneService.fineTuneKT(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};