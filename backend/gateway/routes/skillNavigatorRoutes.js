const express = require('express');
const {
  createProfile,
  getOptimalPath,
  getCareerReadiness,
  updateKT
} = require('../controllers/skillNavigatorController');
const { protect } = require('../middleware/auth');
const router = express.Router();

router.use(protect);
router.post('/profile', createProfile);
router.post('/optimal-path', getOptimalPath);
router.post('/career-readiness', getCareerReadiness);
router.post('/kt-update', updateKT);

module.exports = router;