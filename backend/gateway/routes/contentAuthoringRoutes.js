const express = require('express');
const { generateLesson, extractSkills } = require('../controllers/contentAuthoringController');
const { protect } = require('../middleware/auth');
const router = express.Router();

router.use(protect);
router.post('/generate-lesson', generateLesson);
router.post('/extract-skills', extractSkills);

module.exports = router;