const express = require('express');
const { predictDropout } = require('../controllers/mlController');
const { protect } = require('../middleware/auth');
const router = express.Router();

router.use(protect);
router.post('/predict-risk', predictDropout);

module.exports = router;