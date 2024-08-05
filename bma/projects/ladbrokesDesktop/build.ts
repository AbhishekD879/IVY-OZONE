import budgets from './budgets';
import lazyModules from './lazyModules';

export default {
  'builder': '@angular-devkit/build-angular:browser',
  'options': {
    'outputPath': 'dist/ladbrokesDesktop',
    'index': 'src/index.html',
    'main': 'src/platforms/ladbrokesDesktop/main.ts',
    'polyfills': 'src/polyfills-vanilla.ts',
    'tsConfig': 'src/tsconfig.ladbrokesDesktop.json',
    'assets': [
      'src/buildInfo.json',
      'src/platforms/ladbrokesDesktop/assets/favicon.ico',
      'src/assets',
      'src/iframe-response.html'
    ],
    'styles': [
      'src/platforms/ladbrokesDesktop/assets/styles/global.variables.scss',
      'src/assets/styles/main.scss',
      'src/platforms/ladbrokesDesktop/assets/styles/index.scss',
      'src/platforms/ladbrokesDesktop/assets/styles/fonts/roboto.scss'
    ],
    'stylePreprocessorOptions': {
      'includePaths': [
        'src/platforms/ladbrokesDesktop/assets/styles'
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