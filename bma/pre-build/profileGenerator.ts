import logger from './logger';
import profileBuilder from './profileBuilder';

declare var require: any;
const fs = require('fs');
const path = require('path');
const DIST_DIR = `${path.dirname(__filename)}/../../../../build/Web/ClientDist/`;
class ProfileGenerator {
  public static PROFILES_TYPES: { brand: string; profiles: string[]; platform: string }[] = [{
    brand: 'coral',
    profiles: ['dev0', 'stg0-prem', 'hlv1-stress',
                'production', 'production-prem', 'hlv0-prem', 'tst0-prem','dev0-prem'],
    platform: 'Mobile'
  }, {
    brand: 'coral',
    profiles: ['dev0', 'stg0-prem', 'hlv1-stress',
                'production', 'production-prem', 'hlv0-prem', 'tst0-prem','dev0-prem'],
    platform: 'Desktop'
  }, {
    brand: 'ladbrokes',
    profiles: ['dev0', 'stg0-prem', 'production', 'production-prem', 'hlv1-stress',
                'hlv0-prem', 'tst0-prem','dev0-prem'],
    platform: 'Mobile'
  }, {
    brand: 'ladbrokes',
    profiles: ['dev0', 'stg0-prem', 'production', 'production-prem', 'hlv1-stress',
                'hlv0-prem', 'tst0-prem','dev0-prem'],
    platform: 'Desktop'
  }];

  run(): void {
    const commands = [];
    ProfileGenerator.PROFILES_TYPES.forEach((item: { brand: string; profiles: string[]; platform: string }) => {
      this.createFolder(`${DIST_DIR}${item.brand}${item.platform}`);
      item.profiles.forEach((profile: string) => {
        commands.push({
          brand: item.brand,
          platform: item.platform.toLowerCase(),
          profile: profile,
          path: this.distPath(profile, item.brand, item.platform)
        });
      });
    });
    this.iterator(commands, 0);
  }

  private iterator(commands, index): void {
    profileBuilder.run(
      commands[index].brand,
      commands[index].platform,
      commands[index].profile,
      commands[index].path
    ).then(() => {
      if (commands.length > index + 1) {
        this.iterator(commands, index + 1);
      }
    });
  }

  private createFolder(profileFolder: string): void {
    if (!fs.existsSync(`${profileFolder}`)) {
      fs.mkdirSync(`${profileFolder}`, { recursive: true } as any);
    }
  }

  private distPath(profile: string, brand: string, platform: string): string {
    return `${DIST_DIR}${brand}${platform}/profile.${profile}.js`;
  }
}
new ProfileGenerator().run();
