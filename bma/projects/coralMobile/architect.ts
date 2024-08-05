export default {
  'extract-i18n': {
    'builder': '@angular-devkit/build-angular:extract-i18n',
    'options': {
      'browserTarget': 'coralMobile:build'
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
        'src/assets/styles/main.scss'
      ],
      'stylePreprocessorOptions': {
        'includePaths': [
          'src/assets/testStyles'
        ]
      },
      'fileReplacements': [
        {
          'replace': 'src/environments/oxygenEnvConfig.ts',
          'with': 'src/environments/environment.mock.ts'
        }
      ],
      'scripts': [],
      'assets': [
        'src/favicon.ico',
        'src/assets'
      ]
    }
  },
  'lint': {
    'builder': '@angular-eslint/builder:lint',
    'options': {
      'lintFilePatterns': [
        'src/**/*.ts',
        'src/**/*.html'
      ]
    }
  }
};
