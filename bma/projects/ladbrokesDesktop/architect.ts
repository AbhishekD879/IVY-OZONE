export default {
  'extract-i18n': {
    'builder': '@angular-devkit/build-angular:extract-i18n',
    'options': {
      'browserTarget': 'ladbrokesDesktop:build'
    }
  },
  'test': {
    'builder': '@angular-devkit/build-angular:karma',
    'options': {
      'include': [
        '**/*.spec.ts'
      ],
      'main': 'src/test.ts',
      'polyfills': 'src/polyfills.ts',
      'tsConfig': 'src/tsconfig.spec.json',
      'karmaConfig': 'src/karma.conf.js',
      'styles': [
        'src/assets/styles/main.scss'
      ],
      'scripts': [],
      'assets': [
        'src/favicon.ico',
        'src/assets'
      ]
    }
  }
};
