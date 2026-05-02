const express = require('express');
const { getUserProfile, updateUserProfile, syncUser } = require('../controllers/authController');
const { requireAuth } = require('@clerk/express');
const router = express.Router();

// Protected routes using Clerk
router.get('/profile', requireAuth(), getUserProfile);
router.put('/profile', requireAuth(), updateUserProfile);

router.post('/sync', requireAuth(), syncUser);

module.exports = router;
