const mongoose = require('mongoose');

const optimizationPlanSchema = new mongoose.Schema({
  studentId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  recommendedStudyHours: Number,
  optimizedTopicSequence: [String],
  dailyPlan: [{
    day: Number,
    topic: String,
    hours: Number
  }],
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('OptimizationPlan', optimizationPlanSchema);