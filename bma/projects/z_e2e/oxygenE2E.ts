export default {
  'root': 'e2e/',
  'projectType': 'application',
  'architect': {
    'e2e': {
      'builder': '@angular-devkit/build-angular:protractor',
      'options': {
        'protractorConfig': 'e2e/protractor.conf.js',
        'devServerTarget': 'coralMobile:serve'
      },
      'configurations': {
        'production': {
          'devServerTarget': 'coralMobile:serve:production'
        }
      }
    },
    'lint': {
      'builder': '@angular-devkit/build-angular:tslint',
      'options': {
        'tsConfig': 'e2e/tsconfig.e2e.json',
        'exclude': [
          '**/node_modules/**'
        ]
      }
    }
  }
};
