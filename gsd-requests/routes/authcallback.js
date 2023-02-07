var express = require('express');
var axios = require('axios');
var router = express.Router();

var clientId = process.env.GH_CLIENT_ID;
var clientSecret = process.env.GH_OAUTH_SECRET;

/* GET home page. */
router.get('/', async function(req, res, next) {

	if (process.env.GSD_VIEW_EDIT == "true") {
        // Form view only dev mode
		req.session.github_login = "dev-user";
		req.session.github_id = 0;
		res.redirect('/');

	} else {

		var body = {
			client_id: clientId,
			client_secret: clientSecret,
			code: req.query.code
		};
		var opts = { headers: { accept: 'application/json' } };

		try {
			var resp = await axios.post(`https://github.com/login/oauth/access_token`, body, opts);
			const token = resp.data['access_token'];

			body = { };
			opts = { headers:
					{
					accept: 'application/json',
					authorization: `token ${token}`
					}
			};

			resp = await axios.get(`https://api.github.com/user`, opts);

			const user_login = resp['data']['login'];
			const user_id = resp['data']['id'];
			req.session.github_login = user_login;
			req.session.github_id = user_id;
			res.redirect('/');
		} catch(err) {
			console.log(err)
			res.status(500).json({ message: "A bad thing happened" });
		}
	}

});

module.exports = router;
