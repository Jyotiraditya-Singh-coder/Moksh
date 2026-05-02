const mongoose = require('mongoose');

const dropoutPredictionSchema = new mongoose.Schema({
  studentId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  riskScore: Number,
  factors: [{
    feature: String,
    impact: Number
  }],
  recommendations: [String],
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('DropoutPrediction', dropoutPredictionSchema);