export default {
  'builder': '@angular-devkit/build-angular:dev-server',
  'options': {
    'browserTarget': 'coralDesktop:build',
    'port': 9999,
    'host': 'bm-tst1.coral.co.uk',
    'open': true
  },
  'configurations': {
    'production': {
      'browserTarget': 'coralDesktop:build:production'
    },
    'dev0': {
      'browserTarget': 'coralDesktop:build:dev0'
    },
    'hlv0': {
      'browserTarget': 'coralDesktop:build:hlv0'
    },
    'hlv1': {
      'browserTarget': 'coralDesktop:build:hlv1'
    },
    'stg0': {
      'browserTarget': 'coralDesktop:build:stg0'
    },
    'tst0': {
      'browserTarget': 'coralDesktop:build:tst0'
    },
    'hiddenStage': {
      'browserTarget': 'ladbrokesDesktop:build:hiddenStage'
    }
  }
};
