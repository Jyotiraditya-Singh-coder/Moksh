const OptimizationPlan = require('../models/OptimizationPlan');
const StudentProfile = require('../models/StudentProfile');
const DropoutPrediction = require('../models/DropoutPrediction');
const { getOptimizedPlan } = require('../services/optimizationService');

exports.getStudyPlan = async (req, res, next) => {
  try {
    const profile = await StudentProfile.findOne({ userId: req.user.id });
    const dropout = await DropoutPrediction.findOne({ studentId: req.user.id }).sort({ createdAt: -1 });
    const input = {
      weakTopics: profile?.weakTopics || [],
      strongTopics: profile?.strongTopics || [],
      availableHours: req.body.availableHours || 10,
      difficultyPreference: req.body.difficultyPreference || 'medium',
      dropoutRisk: dropout?.riskScore || 0,
      careerGoal: profile?.careerGoal || ''
    };
    const plan = await getOptimizedPlan(input);
    const saved = await OptimizationPlan.create({
      studentId: req.user.id,
      ...plan
    });
    res.json(saved);
  } catch (err) {
    next(err);
  }
};