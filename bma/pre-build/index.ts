import angularJsonBuilder from './builders/angularJsonBuilder';
import logger from './logger';
import ThirdPartyLibsLoader from './libsLoader/3rd-party';
import profileBuilder from './profileBuilder';

// overwrite environment parameter
const brand = process.env['npm_config_env.brand'] ? process.env['npm_config_env.brand'] : 'coral';

const environmentName = process.env['npm_config_env.environment'] || 'dev0' || process.env['npm_package_config_environment'];
process.env.npm_build_environment = environmentName;

const platform = process.env['npm_config_env.platform'] || 'mobile';
process.env.npm_build_platform = platform;

const forceProfile: boolean = process.env.npm_config_env_forceProfile && process.env.npm_config_env_forceProfile === 'true' ? true : false;

logger.log('Pre build is about to start');
// Making job with 3rd party libs
ThirdPartyLibsLoader.run();
// Creating angular json
angularJsonBuilder.run();
// Builds profile
profileBuilder.run(brand, platform, environmentName, null, forceProfile)
  .then(() => {
    logger.log(`Profile build is completed for brand: ${brand}, platform: ${platform}, profile: ${environmentName}`)
  }, (error: string) => {
    logger.error(error);
  });