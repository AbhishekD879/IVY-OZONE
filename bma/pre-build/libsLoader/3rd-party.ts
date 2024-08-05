'use strict';

declare const require: any;
declare const __dirname: string;

import logger from '../logger';

const fs = require('fs-extra');

const path = require('path');

class ThirdPartyLibsLoader {

  private run_env = (process.env['npm_config_env.environment'] === 'production-prem' ? 'prod/' : 'beta/');
  private pathTo3rdParty: string = '../../node_modules/oxygen-3rd-party-libs/src/'+this.run_env;
  private assetsPath: string = '../../src/assets/';

  private readonly loggerPrefix: string = '3rd Party: ';
  public run(): void {
    logger.log('OXYGEN-Environment', process.env['npm_config_env.environment']);
    logger.log('OXYGEN-Running in', this.pathTo3rdParty);
    this.pathTo3rdParty = path.resolve(__dirname, `../../../${this.pathTo3rdParty}`);
    this.assetsPath = path.resolve(__dirname, `../coralsports/${this.assetsPath}`);

    logger.log(`${this.loggerPrefix}Start insertion of 3rd party libs`);
    fs.readdir(this.pathTo3rdParty, (err, res: string[]) => {
      if (err) {
        logger.log(err);
        return;
      }

      logger.log(`${this.loggerPrefix}Libraries present in oxygen-3rd-party-libs: ${res.join(',')}`);
      res.forEach((folderName: string) => {
        const pathToCopy: string = `${this.pathTo3rdParty}/${folderName}`;
        logger.log(`${this.loggerPrefix}Try to copy: "${pathToCopy}" into "${this.assetsPath}"`);

        fs.copy(`${pathToCopy}`, `${this.assetsPath}/${folderName}`, (copyErr) => {
          if (copyErr) {
            logger.log(copyErr);
            return;
          }
          logger.log(`${this.loggerPrefix}${folderName} is copied to ${this.assetsPath}`);
        });
      });
    });
  }
}

export default new ThirdPartyLibsLoader();
