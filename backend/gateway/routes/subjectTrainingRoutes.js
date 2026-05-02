const express = require('express');
const {
  generateProblem,
  analyzeSolution,
  validateMath,
  validateNumerical,
  compareAlgorithms,
  analyzeAlgorithm,
  searchApproaches,
  getWeaknessProfile,
  getPersonalizedSequence
} = require('../controllers/subjectTrainingController');
const { protect } = require('../middleware/auth');
const router = express.Router();

router.use(protect);
router.post('/generate-problem', generateProblem);
router.post('/analyze-solution', analyzeSolution);
router.post('/validate-math', validateMath);
router.post('/validate-numerical', validateNumerical);
router.post('/compare-algorithms', compareAlgorithms);
router.post('/analyze-algorithm', analyzeAlgorithm);
router.post('/search-approaches', searchApproaches);
router.get('/weakness-profile', getWeaknessProfile); // GET for simplicity
router.post('/personalized-sequence', getPersonalizedSequence);

module.exports = router;