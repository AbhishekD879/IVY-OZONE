import environment from '@environment/oxygenEnvConfig';

export const addActionMock = {
      test: 'action',
      username: 'oxygenUser',
      token: 'ajhsdgu',
      isWrapper: true,
      bppToken: 'testBpp',
      appVersion: environment.version,
      logTime: new Date().getTime(),
      actionName: 'betslipLogui_message',
      currentUrl: '/',
      referralUrl: '/',
      product: 'bm-tst1.coral.co.uk',
      userAgent: 'Mozilla/5.0'
};

export const trackOxySucPayload = {
      url: 'https://backoffice-tst2.coral.co.uk/test',
      level: 'success',
      time: 100,
      requestMethod: 'GET',
      cookiesLength: 6,
      isWrapper: true,
      status: 201,
      payloadSize: 0,
      token: 'ajhsdgu',
      username: 'oxygenUser',
      bppToken: 'testBpp',
      appVersion: environment.version,
      logTime: new Date().getTime(),
      actionName: 'Ajax Call',
      currentUrl: '/',
      referralUrl: '/',
      product: 'bm-tst1.coral.co.uk',
      userAgent: 'Mozilla/5.0'
};

export const trackOxyErrPayload = {
      url: 'https://backoffice-tst2.coral.co.uk/test',
      level: 'error',
      time: 100,
      requestMethod: 'GET',
      cookiesLength: 6,
      isWrapper: true,
      status: 404,
      payloadSize: 9,
      token: 'ajhsdgu',
      username: 'oxygenUser',
      bppToken: 'testBpp',
      appVersion: environment.version,
      logTime: new Date().getTime(),
      actionName: 'Ajax Call',
      currentUrl: '/',
      referralUrl: '/',
      product: 'bm-tst1.coral.co.uk',
      userAgent: 'Mozilla/5.0'
};

export const COGNITO_CREDENTIALS = {
      'accessKey': 'yu89kknmm',
      needsRefresh: () => { },
      get: () => { },
      refresh: () => { },
      expired: false
};

export const CONFIG = {
      region: 'eu-west-2',
      IdentityPoolId: 'jdukjlcdfhkjds'
};

