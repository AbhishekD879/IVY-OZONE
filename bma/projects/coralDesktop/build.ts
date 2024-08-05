import budgets from './budgets';
import lazyModules from './lazyModules';

export default {
  'builder': '@angular-devkit/build-angular:browser',
  'options': {
    'outputPath': 'dist/coralDesktop',
    'index': 'src/index.html',
    'main': 'src/platforms/coralDesktop/main.ts',
    'polyfills': 'src/polyfills-vanilla.ts',
    'tsConfig': 'src/tsconfig.coralDesktop.json',
    'assets': [
      'src/buildInfo.json',
      'src/assets/favicon.ico',
      'src/assets',
      'src/iframe-response.html'
    ],
    'styles': [
      'src/platforms/coralDesktop/assets/styles/global.variables.scss',
      'src/assets/styles/main.scss',
      'src/platforms/coralDesktop/assets/styles/index.scss',
      'src/platforms/coralDesktop/assets/styles/lato.scss'
    ],
    'stylePreprocessorOptions': {
      'includePaths': [
        'src/platforms/coralDesktop/assets/styles'
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
