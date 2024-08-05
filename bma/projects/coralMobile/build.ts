import budgets from './budgets';
import lazyModules from './lazyModules';

export default {
  'builder': '@angular-devkit/build-angular:browser',
  'options': {
    'outputPath': 'dist/coralMobile',
    'index': 'src/index.html',
    'main': 'src/platforms/coralMobile/main.ts',
    'polyfills': 'src/polyfills-vanilla.ts',
    'tsConfig': 'src/tsconfig.coralMobile.json',
    'assets': [
      'src/buildInfo.json',
      'src/assets/favicon.ico',
      'src/assets',
      'src/iframe-response.html'
    ],
    'styles': [
      'src/assets/styles/global.variables.scss',
      'src/assets/styles/main.scss'
    ],
    'stylePreprocessorOptions': {
      'includePaths': [
        'src/assets/styles'
      ]
    },
    'scripts': [
      './node_modules/socket.io.exec/src/socket.io.exec.js',
      './node_modules/smoothscroll-polyfill/dist/smoothscroll.js'
    ],
    'lazyModules': lazyModules
  },
  'configurations': {
    'production': {
      'optimization': true,
      'sourceMap': false,
      'extractCss': true,
      'namedChunks': false,
      'outputHashing': 'bundles',
      'aot': true,
      'extractLicenses': true,
      'vendorChunk': true,
      'commonChunk': false,
      'buildOptimizer': true,
      'budgets': budgets.production
    }
  }
};
