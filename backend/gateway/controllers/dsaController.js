exports.getTrendingTopics = async (req, res, next) => {
  try {
    const result = await dsaService.getTrendingTopics(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

exports.updateTrendingTopics = async (req, res, next) => {
  try {
    // Only allow admins/teachers to update trends
    if (!['admin', 'teacher'].includes(req.user.role)) {
      return res.status(403).json({ message: 'Forbidden' });
    }
    const result = await dsaService.updateTrendingTopics(req.body);
    res.json(result);
  } catch (err) {
    next(err);
  }
};