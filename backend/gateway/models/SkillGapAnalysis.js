const mongoose = require('mongoose');

const skillGapSchema = new mongoose.Schema({
  studentId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  targetRole: String,
  missingSkills: [String],
  roadmap: [{
    skill: String,
    resources: [String],
    estimatedHours: Number
  }],
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('SkillGapAnalysis', skillGapSchema);