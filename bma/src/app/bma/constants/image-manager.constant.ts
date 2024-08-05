import environment from '@environment/oxygenEnvConfig';

const cmsApi = environment.CMS_ENDPOINT;
const brand = environment.brand;
const cmsImagesPath = `${cmsApi}/${brand}/svg-images/sprite`;

export const SPRITE_PATH = {
  initial: `${cmsImagesPath}/initial`, // always included to /initial-data
  featured: `${cmsImagesPath}/featured`, // included to /initial-data/desktop
  additional: `${cmsImagesPath}/additional`,
  virtual: `${cmsImagesPath}/virtual`,
  timeline: `${cmsImagesPath}/timeline`
};
