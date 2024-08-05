/**
 * Builds angular.json with build projects data
 */

const fs = require('fs-extra');
const path = require('path');

import angularJson from './../../projects/angular.json';
import logger from '../logger';

export default {
  /**
   * Main process method
   */
  run() {
    const destFile = path.resolve(__dirname, '../../angular.json');
    let data = JSON.stringify(angularJson, null, 2);
    logger.log('save Angular JSON');
    fs.writeFileSync(destFile, data);
  }
};
