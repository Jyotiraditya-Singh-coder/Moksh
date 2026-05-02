const express = require('express');
const {
  analyzeSkillGap,
  addJobRole,
  listJobRoles,
  rebuildIndex
} = require('../controllers/careerController');
const { protect, authorize } = require('../middleware/auth');
const router = express.Router();

// All routes require authentication
router.use(protect);

// POST /api/career/analyze - analyze resume (any authenticated user)
router.post('/analyze', analyzeSkillGap);

// POST /api/career/add-job-role - add new job role (teacher or admin only)
router.post('/add-job-role', authorize('teacher', 'admin'), addJobRole);

// GET /api/career/job-roles - list all job roles (any authenticated user)
router.get('/job-roles', listJobRoles);

// POST /api/career/rebuild-index - rebuild FAISS index (admin only)
router.post('/rebuild-index', authorize('admin'), rebuildIndex);

module.exports = router;