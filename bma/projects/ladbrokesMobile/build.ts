import budgets from './budgets';
import lazyModules from './lazyModules';

export default {
  'builder': '@angular-devkit/build-angular:browser',
  'options': {
    'outputPath': 'dist/ladbrokesMobile',
    'index': 'src/index.html',
    'main': 'src/platforms/ladbrokesMobile/main.ts',
    'polyfills': 'src/polyfills-vanilla.ts',
    'tsConfig': 'src/tsconfig.ladbrokesMobile.json',
    'assets': [
      'src/buildInfo.json',
      'src/platforms/ladbrokesMobile/assets/favicon.ico',
      { 'glob': '**/*', 'input': 'src/platforms/ladbrokesMobile/assets/fonts', 'output': '/assets/fonts' },
      'src/assets',
      'src/iframe-response.html'
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
