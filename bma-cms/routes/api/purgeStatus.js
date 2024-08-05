'use strict';

const request = require('request');

exports = module.exports = function(req, res) {
  request({
    method: 'get',
    json: true,
    url: `https://api.ccu.akamai.com/ccu/v2/purges/${req.params.progressUri}`,
    auth: {
      user: process.env.AKAMAI_CRED_USER,
      pass: process.env.AKAMAI_CRED_PASS
    }
  }, function(err, response, body) {
    res.json(err || body);
  });
};
