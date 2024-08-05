import logger from './logger';
import profileBuilder from './profileBuilder';

const brand = process.env['npm_config_env.brand'] || 'coral';
const profile = process.env['npm_config_env.environment'] || 'dev0';
const platform = process.env['npm_config_env.platform'] || 'Mobile';

class ProfileSwitcher {
  run(brand: string, profile: string, platform: string): void {
    logger.log(`Switching profile to ${brand}${platform} ${profile}.`);

    profileBuilder.run(brand, platform, profile)
      .then(() => logger.log('Profile was switched successfully.'));
  }
}

new ProfileSwitcher().run(brand, profile, platform);