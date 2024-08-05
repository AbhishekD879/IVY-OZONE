const Countries = require('../../models/Countries'),
  Logger = require('../../lib/logger');

exports = module.exports = function(req, res) {
  const newModel = req.body.data;

  Countries.findOne({ _id: req.body.data._id }, (err, doc) => {
    if (err) {
      res.end(err);
    } else {
      doc.countriesData = newModel.countriesData;
      doc.save(
        error => {
          Logger.error(
            'AKAMAI',
            'countries-settings user',
            req.user.email,
            req.headers['x-forwarded-for'] || req.connection.remoteAddress || req.socket.remoteAddress ||
              req.connection.socket.remoteAddress,
            '\t module:',
            req.body._id
          );
          if (error) {
            res.sendStatus(500);
            res.end(error);
          } else {
            res.sendStatus(200);
            res.end();
          }
        }
      );
    }
  });
};
