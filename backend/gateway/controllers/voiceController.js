const { askVoiceTutor } = require('../services/voiceService');

exports.askVoice = async (req, res, next) => {
  try {
    // Expect multipart form with audio file
    if (!req.file) {
      return res.status(400).json({ message: 'Audio file required' });
    }
    const audioBase64 = req.file.buffer.toString('base64');
    const language = req.body.language || 'en';
    const answer = await askVoiceTutor({ audioBase64, language });
    res.json({ answer });
  } catch (err) {
    next(err);
  }
};