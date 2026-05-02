const { requireAuth } = require('@clerk/express');
const { logger } = require('./logger');
const MysqlUser = require('../models/MysqlUser');

// Use Clerk's requireAuth to protect routes
const protect = requireAuth();

// Authorization by Role: relies on MySQL synced user role or Clerk metadata
const authorize = (...roles) => {
  return async (req, res, next) => {
    try {
      const clerkId = req.auth.userId;
      if (!clerkId) {
        return res.status(401).json({ message: 'Not authenticated' });
      }

      // Fetch user role from our database to check authorization
      const user = await MysqlUser.findOne({ where: { clerkId } });
      
      if (!user || !roles.includes(user.role)) {
        return res.status(403).json({ message: 'Forbidden' });
      }

      // Attach user object to request so subsequent controllers don't have to refetch
      req.dbUser = user;
      next();
    } catch (error) {
      logger.error('Authorization error:', error);
      res.status(500).json({ message: 'Server error during authorization' });
    }
  };
};

module.exports = { protect, authorize };