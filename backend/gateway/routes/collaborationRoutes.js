const express = require('express');
const { formGroups, detectEmotion } = require('../controllers/collaborationController');
const { protect } = require('../middleware/auth');
const router = express.Router();

router.use(protect);
router.post('/form-groups', formGroups);
router.post('/detect-emotion', detectEmotion);

module.exports = router;