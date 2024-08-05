export default {
  'extract-i18n': {
    'builder': '@angular-devkit/build-angular:extract-i18n',
    'options': {
      'browserTarget': 'coralDesktop:build'
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
        'src/assets/testStyles/global.variables.scss',
        'src/assets/styles/main.scss',
        'src/platforms/coralDesktop/assets/styles/index.scss'
      ],
      'stylePreprocessorOptions': {
        'includePaths': [
          'src/assets/testStyles'
        ]
      },
      'scripts': [],
      'assets': [
        'src/favicon.ico',
        'src/assets'
      ]
    }
  }
};
