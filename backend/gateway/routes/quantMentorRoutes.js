const express = require('express');
const {
  getQuantGuide,
  getTopicInfo,
  listTopics
} = require('../controllers/quantMentorController');
const { protect } = require('../middleware/auth');
const router = express.Router();

router.use(protect);
router.post('/guide', getQuantGuide);
router.post('/topic-info', getTopicInfo);
router.get('/topics', listTopics);

module.exports = router;