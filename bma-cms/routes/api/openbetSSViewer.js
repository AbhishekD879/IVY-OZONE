const request = require('request');

exports = module.exports = function(req, res) {
  const proxyTarget = `http://backoffice-tst2.coral.co.uk${req.url.replace('/api', '')}`;
  request({ url: proxyTarget, headers: { Accept: 'application/json, text/plain, */*' } }, (error, response, body) => {
    if (!error && response.statusCode === 200) {
      res.send(body);
      res.end();
    } else {
      res.status(500);
      res.send({ error });
      res.end();
    }
  });
};
