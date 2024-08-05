exports = module.exports = function(result, res) {
  /**
  * Sends Response
  * @param {result} json
  * @param {res} res
  */

  // cache-control:max-age=3600
  res.setHeader('Strict-Transport-Security', 'max-age=63072000; includeSubDomains');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.json(result);
};
