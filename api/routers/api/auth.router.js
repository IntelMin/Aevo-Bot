
const express = require('express');
const router = express.Router();
const controller = require('../../controllers/api/auth.controller');

router.post('/auth', controller.auth);

module.exports = router;
