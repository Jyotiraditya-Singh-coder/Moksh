const StudentProfile = require('../models/StudentProfile');

exports.getProfile = async (req, res, next) => {
  try {
    const profile = await StudentProfile.findOne({ userId: req.user.id });
    res.json(profile || {});
  } catch (err) {
    next(err);
  }
};

exports.updateProfile = async (req, res, next) => {
  try {
    const profile = await StudentProfile.findOneAndUpdate(
      { userId: req.user.id },
      req.body,
      { new: true, upsert: true, runValidators: true }
    );
    res.json(profile);
  } catch (err) {
    next(err);
  }
};