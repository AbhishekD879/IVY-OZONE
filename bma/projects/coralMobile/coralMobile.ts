import architect from './architect';
import base from '../base';
import build from './build';
import serve from '../coral/serve';

export default {
  ...base,
  'architect': {
    'build': build,
    'serve': serve,
    'extract-i18n': architect['extract-i18n'],
    'test': architect.test,
    'lint': architect.lint
  }
};
