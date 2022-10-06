var express = require('express');
var router = express.Router();

router.get('/', async function(req, res, next) {

	req.session.github_login = undefined;
	res.redirect('/');
});

module.exports = router;
