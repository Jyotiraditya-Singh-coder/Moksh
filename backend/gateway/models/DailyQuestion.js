const mongoose = require('mongoose');

const dailyQuestionSchema = new mongoose.Schema({
  studentId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  question: String,
  difficulty: { type: String, enum: ['easy', 'medium', 'hard'] },
  topic: String,
  solution: String,
  alternateApproach: String,
  explanation: String,
  learningTip: String,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('DailyQuestion', dailyQuestionSchema);