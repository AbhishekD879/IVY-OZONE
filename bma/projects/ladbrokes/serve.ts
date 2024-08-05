export default {
  'builder': '@angular-devkit/build-angular:dev-server',
  'options': {
    'browserTarget': 'ladbrokesDesktop:build',
    'port': 9999,
    'host': 'bm-tst1.ladbrokes.com',
    'open': true
  },
  'configurations': {
    'production': {
      'browserTarget': 'ladbrokesDesktop:build:production'
    },
    'dev0': {
      'browserTarget': 'ladbrokesDesktop:build:dev0'
    },
    'stg0': {
      'browserTarget': 'ladbrokesDesktop:build:stg-'
    },
    'hlv0': {
      'browserTarget': 'ladbrokesDesktop:build:hiddenProd'
    },
    'hlv2': {
      'browserTarget': 'ladbrokesDesktop:build:hlv2'
    },
    'hiddenStage': {
      'browserTarget': 'ladbrokesDesktop:build:hiddenStage'
    }
  }
};
