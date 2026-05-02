const express = require('express');
const multer = require('multer');
const { askVoice } = require('../controllers/voiceController');
const { protect } = require('../middleware/auth');
const router = express.Router();
const upload = multer({ storage: multer.memoryStorage() });

router.use(protect);
router.post('/ask', upload.single('audio'), askVoice);

module.exports = router;