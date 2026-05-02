const express = require('express');
const { getStudyPlan } = require('../controllers/optimizeController');
const { protect } = require('../middleware/auth');
const router = express.Router();

router.use(protect);
router.post('/study-plan', getStudyPlan);

module.exports = router;