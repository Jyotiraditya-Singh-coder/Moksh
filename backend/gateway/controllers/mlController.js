const DropoutPrediction = require('../models/DropoutPrediction');
const StudentProfile = require('../models/StudentProfile');
const { predictDropoutRisk } = require('../services/dropoutService');

exports.predictDropout = async (req, res, next) => {
  try {
    const clerkId = req.auth.userId; // Changed to Clerk's user id
    // Gather features from request body or from other sources
    const profile = await StudentProfile.findOne({ userId: clerkId });
    const features = {
      attendance_rate: req.body.attendance_rate || 0.9,
      test_scores: req.body.test_scores || [85, 90, 78],
      engagement_time: req.body.engagement_time || 120,
      assignment_completion: req.body.assignment_completion || 0.85,
      weak_topics_count: profile?.weakTopics?.length || 0,
    };
    const result = await predictDropoutRisk(features);
    // Store result
    const prediction = await DropoutPrediction.create({
      studentId: clerkId,
      ...result
    });
    res.json(prediction);
  } catch (err) {
    next(err);
  }
};