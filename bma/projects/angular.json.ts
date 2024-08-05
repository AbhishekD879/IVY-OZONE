import coralMobile from './coralMobile/coralMobile';
import coralDesktop from './coralDesktop/coralDesktop';
import ladbrokesMobile from './ladbrokesMobile/ladbrokesMobile';
import ladbrokesDesktop from './ladbrokesDesktop/ladbrokesDesktop';
import oxygenE2E from './z_e2e/oxygenE2E';

export default {
  '$schema': './node_modules/@angular/cli/lib/config/schema.json',
  'version': 1,
  'newProjectRoot': 'projects',
  'projects': {
    'coralMobile': coralMobile,
    'coralDesktop': coralDesktop,
    'ladbrokesMobile': ladbrokesMobile,
    'ladbrokesDesktop': ladbrokesDesktop,
    'oxygen-e2e': oxygenE2E
  },
  'defaultProject': 'coralMobile'
};
