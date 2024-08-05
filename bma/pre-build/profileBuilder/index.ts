declare const require: any;
declare const __filename: string;

const path = require('path');
import logger from '../logger';
import gtmConfig from './environments/configs/gtmConfig';
import { writeFile, readFile } from 'fs-extra';
import buildInfoBuilder from '../builders/buildInfoBuilder';

class ProfileBuilder {
  private static PATH_TO_PROFILES: string = `${path.dirname(__filename)}/environments`;
  constructor() {}

  run(brand: string, platform: string, profile: string, allProfilesPath?: string, forceProfile?: boolean): Promise<void> {
    return new Promise((resolve: () => void, reject: (error: string) => void) => {
      const pathToFile: string = `${ProfileBuilder.PATH_TO_PROFILES}/${brand}/environment.${profile}.ts`;
      logger.log(`Fetching profile from: ${pathToFile}`);
      import(pathToFile).then(data => {
        const envConfig = data.default;
        // Update profile in case this is desktop for better definning of
        if (platform === 'desktop') {
          logger.log(`Platform is changed to: desktop`);
          envConfig.CURRENT_PLATFORM = platform;
        }

        envConfig.googleTagManagerID = this.getGTMIds(brand, envConfig.ENVIRONMENT);
        envConfig.CSS_Lazy_loadash = Array.from({ length: 20 }, () => Math.random().toString(36).charAt(2)).join('');
        if (allProfilesPath) {
          this.writeProfile(allProfilesPath, envConfig, resolve, reject);
        } else {
          this.createBuildInfo(envConfig, `${brand} ${platform} ${profile}`, resolve, reject);
          this.modifyPathOfDefaultProductionProfileBasedOnBrand(envConfig, forceProfile);
        }
      });
    });
  }

  private modifyPathOfDefaultProductionProfileBasedOnBrand(config: any, forceProfile: boolean = false): void {
    const pathToOXEnvFile: string = `${path.dirname(__filename)}/../../src/environments/oxygenEnvConfig.ts`;
    readFile(pathToOXEnvFile).then((data) => {
      let profileStr: string = data.toString().replace('//', '').replace('${config}', JSON.stringify(config));
      if (forceProfile) {
        logger.log('Force Profile is DONE');
        profileStr = profileStr.replace('(window as any).oxygenEnvConfig || ', '');
      }
      writeFile(pathToOXEnvFile, profileStr).then(() => {
        logger.log(`Path to default profile set`);
        logger.log('Check oxygen Env Config, do not commit this file');
      });
    })
  }

  private getGTMIds(brand: string, environment: string): string[] {
    const gtmIdsData: string | string[] = gtmConfig && gtmConfig[brand] && gtmConfig[brand][environment];
    logger.log(`Config for GTM for brand: ${brand} and profile: ${environment}, ${gtmIdsData}`);

    return gtmIdsData ? [].concat(gtmIdsData) : [];
  }

  private writeProfile(pathTo, envConfig, resolve: () => void, reject: (error: string) => void): void {
    logger.log('Write profile File, ENVIRONMENT=', envConfig.ENVIRONMENT);
    writeFile(pathTo, `window.oxygenEnvConfig=${JSON.stringify(envConfig)}`)
      .then(() => {
        logger.log('Write File done');
        resolve();
      })
      .catch((error: string) => reject(error));
  }

  private createBuildInfo(envConfig: string, profileInfo: string, resolve: () => void, reject: (error: string) => void): void {
    buildInfoBuilder.run(envConfig)
      .then(() => {
        logger.log(`Build Info is created for: ${profileInfo}`);
        const profilePath = `${path.dirname(__filename)}/../../src/profile.js`;
        this.writeProfile(profilePath, envConfig, resolve, reject);
      }, (error) => {
        reject(`Build Info is not created. ${error}`);
      });
  }
}

export default new ProfileBuilder();
