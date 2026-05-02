const DailyQuestion = require('../models/DailyQuestion');
const StudentProfile = require('../models/StudentProfile');
const { generateQuestion } = require('../services/questionService');

exports.getTodayQuestion = async (req, res, next) => {
  try {
    // Check if already generated today
    const today = new Date().setHours(0,0,0,0);
    const existing = await DailyQuestion.findOne({
      studentId: req.user.id,
      createdAt: { $gte: today }
    });
    if (existing) return res.json(existing);

    // Fetch student profile for weaknesses
    const profile = await StudentProfile.findOne({ userId: req.user.id });
    if (!profile) return res.status(400).json({ message: 'Complete profile first' });

    // Call AI service
    const questionData = await generateQuestion(profile);
    const saved = await DailyQuestion.create({
      studentId: req.user.id,
      ...questionData
    });
    res.json(saved);
  } catch (err) {
    next(err);
  }
};

exports.submitAnswer = async (req, res, next) => {
  try {
    const { questionId, answer } = req.body;
    // Evaluate answer, update learning history, etc.
    // For now, just acknowledge
    res.json({ message: 'Answer recorded' });
  } catch (err) {
    next(err);
  }
};