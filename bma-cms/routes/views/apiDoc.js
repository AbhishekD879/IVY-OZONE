const keystone = require('../../bma-betstone');

exports = module.exports = function(req, res) {
  const view = new keystone.View(req, res);
  view.render('apiDoc');
};
