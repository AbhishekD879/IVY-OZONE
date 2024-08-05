'use strict';

const sendResponse = require('../../../routes/api/sendResponse');
const sendError = require('../../../routes/api/sendError');
const path = require('path');
const fs = require('fs');
const keystone = require('../../');
const imagemin = require('../../../lib/imagemin');
const akamai = require('../../lib/akamai');

exports = module.exports = (req, res) => {
  const allowedTypes = ['image/jpeg','image/png','image/jpg'];
  const file = req.files.image;
  const filetype = file.mimetype || file.type;
  const dirAbsolute = path.join('public', '/images/uploads/wysiwyg_uploads', req.body.listId, req.body.itemId);

  if (allowedTypes.indexOf(filetype) === -1) {
    req.flash('error', 'Unsupported File Type: ' + filetype);
    return res.status(415).end();
  }

  imagemin.min(file.path, dirAbsolute, (err, minPath) => {
    if (err) {
      sendError(err, res);
    } else {

      // Remove /public part
      const apiPath = minPath.substring(6);
      const stream = fs.createReadStream(minPath);
      const model = keystone.mongoose.model(req.body.listId);

      model.findOne({ _id: req.body.itemId }, { brand: true }).exec()
        .then(
          m => {
            akamai.upload(m.brand, stream, apiPath, (err, _, akamaiFilePath) => {
              if (err) {
                sendError(err, res);
              } else {
                sendResponse({ path: akamaiFilePath }, res);
              }
            });
          },
          err => sendError(err, res)
        )
    }
  });
};
