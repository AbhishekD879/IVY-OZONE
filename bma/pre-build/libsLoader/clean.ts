'use strict';

const fs = require('fs-extra'),
  path = require('path'),
  dist = path.resolve(__dirname, '../../src/assets/lib/');

export default {
  run() {
    if (fs.existsSync(dist)) {
      fs.removeSync(dist);
      fs.mkdirSync(dist);
    }
  }
};
