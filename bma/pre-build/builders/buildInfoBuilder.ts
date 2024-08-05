/**
 * Builds buildInfo.json with build related data
 */
declare const require: any;
declare const __filename: string;

const fs = require('fs-extra');
const git = require('git-rev-sync');
const packageData = require('./../../package.json');
const path = require('path');
import logger from '../logger';

export default {
  /**
   * Main process method
   */
  run(environment): Promise<void> {
    const gitDir = './';
    const destFile = `${path.dirname(__filename)}/../../src/buildInfo.json`,
      output = {
        appVersion: packageData.version,
        git: {
          short: git.short(gitDir),
          long: git.long(gitDir),
          branch: git.branch(gitDir),
          tag: git.tag(),
          isTagDirty: git.isTagDirty(),
          message: git.message(),
          count: git.count()
        },
        environment: environment
      };
    logger.log(`Build info writing started, path: ${destFile}`);
    return fs.writeJson(destFile, output);
  }
};
