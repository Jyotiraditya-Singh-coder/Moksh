const express = require('express');
const { getTodayQuestion, submitAnswer } = require('../controllers/questionController');
const { protect } = require('../middleware/auth');
const router = express.Router();

router.use(protect);
router.get('/today', getTodayQuestion);
router.post('/submit', submitAnswer);

module.exports = router;