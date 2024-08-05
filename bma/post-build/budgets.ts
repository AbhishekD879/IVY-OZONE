declare const require: any;
declare const __filename: string;
declare const process: any;

import logger from '../pre-build/logger';
import angularJson from '../projects/angular.json';

const fs = require('fs-extra');
const path = require('path');
const filenamePath = `${path.dirname(__filename)}/../../../../build/Web/ClientDist`;

class Budgets {
  public static PLATFORMS = ['coralMobile', 'coralDesktop', 'ladbrokesMobile', 'ladbrokesDesktop'];
  private budgetError: boolean = false;

  run(): void {
    Budgets.PLATFORMS.map((platform: string) => {
      logger.log(`Budgets comprasion for ${platform} started...`);
      const platformPath = `${filenamePath}/${platform}`;

      if (fs.existsSync(platformPath)) {
        const budgets = angularJson.projects[platform].architect.build.configurations.production.budgets;
        const files = fs.readdirSync(platformPath);

        budgets.map((config) => this.checkBudgets(config, platform, files));
      } else {
        logger.error(`Dist folder for ${platform} not found.`);
      }
    });

    if (this.budgetError) {
      process.exit(-1);
    } else {
      logger.log('Budgets passed.');
      process.exit(0);
    }
  }

  private checkBudgets(config, platform: string, files: string[]): void {
    const fileName = this.findFile(files, config.name);
    const filePath = `${filenamePath}/${platform}/${fileName}`;

    if (fs.existsSync(filePath)) {
      const stats = fs.statSync(filePath);
      this.compareSize(stats.size, fileName, config, platform);
    } else {
      logger.error(`File not found: ${config.name}`);
    }
  }

  private findFile(files: string[], name: string): string {
    const regex: RegExp = new RegExp(`^${name}.*\.js$`, 'i');
    return files.find((fileName: string) => !!fileName.match(regex));
  }

  private compareSize(size: number, fileName: string, config, platform: string): void {
    const { baseline, minimumError, maximumError } = config;
    const multiplier = this.getMultiplier(baseline);
    const baseSize = this.filterSymbols(baseline) * multiplier.coefficient;
    const min = baseSize - (baseSize * this.filterSymbols(minimumError) / 100);
    const max = baseSize + (baseSize * this.filterSymbols(maximumError) / 100);
    if (fileName.indexOf('main') > -1) {
      logger.log(`Below is budgets check for filename: ${fileName}`);
      logger.log(`Min. value: ${min} ; baseline: ${baseSize} ; Max. value: ${max}`);
      logger.log(`Main.js file Size with latest commit: ${size}`);
    }
    if (size < min || size > max) {
      logger.error(`ERROR in ${platform} budgets, file size is out of baseline for ${fileName}.
      Budget ${baseline}, new size: ${(size/multiplier.coefficient).toFixed(3)}${multiplier.value}`);
      this.budgetError = true;
    }
  }

  private getMultiplier(baseline: string): { value: string; coefficient: number } {
    const value = baseline.includes('Mb') ? 'Mb' : baseline.includes('kb') ? 'kb' : 'bytes';
    const coefficient = baseline.includes('Mb') ? 1000 * 1000 : baseline.includes('kb') ? 1000 : 1;
    return { value, coefficient };
  }

  private filterSymbols(val: string): number {
    return +val.replace(/[^0-9.,]+/, '');
  }
}

new Budgets().run();