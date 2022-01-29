var express = require('express');
var axios = require('axios');
var csrf = require('csurf');
var router = express.Router();

const csrfProtection = csrf({ cookie: true });

/* GET home page. */
router.get('/', csrfProtection, function(req, res, next) {

	const the_username = req.session.github_login || undefined;

	if (the_username == undefined) {
		res.redirect("/");
	}

	res.render('gsdform', {
		title: 'Actual GSD Form',
		username: the_username,
		csrfToken: req.csrfToken()
	});
});

router.post('/formsubmit', csrfProtection, function(req, res, next) {

	if (process.env.GSD_VIEW_EDIT == "true") {
		// form fiew only dev mode
		res.redirect("/");
	} else {

		var redirect = "/";
		const the_username = req.session.github_login || undefined;

		if (the_username == undefined) {
			res.redirect("/");
		}

		const the_github_id = req.session.github_id;

		var refs = [];
		if (Array.isArray(req.body.references)) {
			refs = req.body.references;
		} else {
			refs = [req.body.references];
		}

		// We need to turn the form data into a structure, then into json
		gsd_data = {
			vendor_name: req.body.vendorName,
			product_name: req.body.productName,
			product_version: req.body.productVersion,
			vulnerability_type: req.body.vulnType,
			affected_component: req.body.affectedComponent,
			attack_vector: req.body.attackVector,
			impact: req.body.impact,
			credit: req.body.credit,
			references: refs,
			reporter: the_username,
			reporter_id: the_github_id,
			notes: req.body.notes,
			description: req.body.description
		};

		gsd_json = JSON.stringify(gsd_data, null, 2);

		//Create issue
		var body = {
			title: "GSD Request",
			body: `\`\`\`\n--- GSD JSON ---\n${gsd_json}\n--- GSD JSON ---\n\`\`\`\n/cc @${the_username}`,
			labels: ['new', 'check']
		};
		var opts = {
			headers: { accept: 'application/json' },
			auth: {
				username: process.env.GH_USERNAME,
				password: process.env.GH_TOKEN,
			}
		};
		var repo = process.env.GH_REPO
		axios.post(`https://api.github.com/repos/${repo}/issues`, body, opts)
		.then((resp) => {
			redirect = resp['data']['html_url'];
			res.redirect(redirect);
		})
		.catch((err) => {
					console.log(err)
					res.status(500).json({ message: "A bad thing happened" });
			})
	}

});

module.exports = router;
