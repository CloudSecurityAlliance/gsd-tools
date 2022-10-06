var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {

	const the_username = req.session.github_login || undefined;

	res.render('index', {
		title: 'GSD Form',
		client_id: process.env.GH_CLIENT_ID,
		username: the_username
	});
});

module.exports = router;
