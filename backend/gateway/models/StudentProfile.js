const mongoose = require('mongoose');

const studentProfileSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, unique: true },
  educationLevel: { type: String, enum: ['high school', 'bachelor', 'master', 'phd'] },
  careerGoal: String,
  preferredLanguage: { type: String, default: 'en' },
  weakTopics: [String],
  strongTopics: [String],
  learningHistory: [{
    topic: String,
    score: Number,
    date: Date
  }]
});

module.exports = mongoose.model('StudentProfile', studentProfileSchema);