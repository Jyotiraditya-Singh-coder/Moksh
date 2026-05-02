const express = require('express');
const {
  fineTuneDropout,
  fineTuneRecommendation,
  fineTuneKT
} = require('../controllers/fineTuneController');
const { protect, authorize } = require('../middleware/auth');
const router = express.Router();

// Only teachers/admins can fine-tune models
router.use(protect, authorize('teacher', 'admin'));

router.post('/dropout', fineTuneDropout);
router.post('/recommendation', fineTuneRecommendation);
router.post('/kt', fineTuneKT);

module.exports = router;