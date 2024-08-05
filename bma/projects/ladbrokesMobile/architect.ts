export default {
  'extract-i18n': {
    'builder': '@angular-devkit/build-angular:extract-i18n',
    'options': {
      'browserTarget': 'ladbrokesMobile:build'
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
      'assets': [
        'src/platforms/ladbrokesMobile/assets/favicon.ico',
        'src/assets'
      ],
      'styles': [
        'src/platforms/ladbrokesMobile/assets/styles/global.variables.scss',
        'src/assets/styles/main.scss',
        'src/platforms/ladbrokesMobile/assets/styles/main.scss'
      ],
      'stylePreprocessorOptions': {
        'includePaths': [
          'src/platforms/ladbrokesMobile/assets/styles'
        ]
      },
      'scripts': []
    }
  }
};
