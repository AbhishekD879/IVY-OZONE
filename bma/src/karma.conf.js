process.env.CHROME_BIN = require('puppeteer').executablePath();

module.exports = function (config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-chrome-launcher'),
      require('karma-mocha-reporter'),
      require('karma-jasmine-html-reporter'),
      require('karma-coverage-istanbul-reporter'),
      require('@angular-devkit/build-angular/plugins/karma'),
    ],
    client: {
      clearContext: false, // leave Jasmine Spec Runner output visible in browser
      jasmine: {
        random: false
      }
    },
    coverageIstanbulReporter: {
      dir: 'coverage', // write in project root, relatively to ../webpack folder (local npm tasks)
      reports: ['lcovonly', 'html', 'json-summary'],
      fixWebpackSourcePaths: true,
      combineBrowserReports: true
    },
    reporters: ['mocha', 'kjhtml', 'coverage-istanbul'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: false,
    browsers: ['ChromeNoSandboxHeadless'],
    customLaunchers: {
      ChromeNoSandboxHeadless: {
        base: 'ChromeHeadless',
        flags: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-gpu',
        ],
      }
    },
    singleRun: true,
    captureTimeout: 910000,
    browserDisconnectTolerance: 3,
    retryLimit: 3,
    browserDisconnectTimeout : 910000,
    browserNoActivityTimeout : 910000,
    processKillTimeout: 910000,
    reportSlowerThan: 500
  });
};
