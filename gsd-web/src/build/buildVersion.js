// Uses code from https://stackoverflow.com/a/34518749

const fs = require('fs');

const rev = fs.readFileSync('../.git/HEAD').toString().trim();
let sha
if (rev.indexOf(':') === -1) {
    sha = rev;
} else {
    sha = fs.readFileSync('../.git/' + rev.substring(5)).toString().trim();
}

module.exports = { rev, sha }
