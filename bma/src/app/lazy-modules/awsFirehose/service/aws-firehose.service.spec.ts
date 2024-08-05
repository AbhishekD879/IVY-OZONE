import { of as observableOf } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import environment from '@environment/oxygenEnvConfig';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { addActionMock, trackOxySucPayload, trackOxyErrPayload } from '@lazy-modules/awsFirehose/test/data/awsFirehose.mock';

describe('AWSFirehoseService', () => {
  let service: AWSFirehoseService,
    windowRef,
    userService,
    cmsService,
    deviceService,
    pubSubService,
    router;
  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        document: {
          cookie: 'cookie'
        },
        AWS: {
          Firehose: jasmine.createSpy().and.returnValue({ putRecord: () => { } }),
          config: {
            region: 'eu-west',
            IdentityPoolId: 'jdukjlcdfhkjds',
            credentials: {
              expired: false
            }
          }
        },
        navigator: {
          userAgent: 'Google Chrome'
        },
        location: {
          host: 'bm-tst1.coral.co.uk'
        }
      }
    };

    userService = {
      username: 'oxygenUser',
      sessionToken: 'ajhsdguyq87119816asljka',
      isRouletteJourney() { },
      bppToken: 'testBppLongToken'
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        awsLog: { interceptAjax: true }
      }))
    };

    deviceService = {
      parsedUA: 'device',
      isWrapper: true,
    };
    pubSubService = {
      API: {
        INIT_AWS: 'INIT_AWS'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, callback) => callback())
    };

    router = {
      getCurrentUrl: jasmine.createSpy('getCurrentUrl'),
      getPreviousUrl: jasmine.createSpy('getPreviousUrl')
    };
    service = new AWSFirehoseService(windowRef, userService, cmsService, deviceService, pubSubService, router);
  });
  it('should return prod env', () => {
    const env = service['getEnvironment']('prod');
    expect(env).toEqual('prod');
  });
  it('should return nonprod env', () => {
    const env = service['getEnvironment']('dev');
    expect(env).toEqual('nonprod');
  });
  it('constructor', () => {
    expect(service['isInterceptAjax']).toBeTruthy();
  });
  describe('performAddAction', () => {
    it('should call performAddAction', () => {
      spyOn<any>(service, 'firehosePutRecord');
      service['analyticsParams.device'] = deviceService.parsedUA;
      service.performAddAction('betslipLogui_message', addActionMock);
      expect(service['firehosePutRecord']).toHaveBeenCalled();
    });
    it('should not call performAddAction', () => {
      spyOn<any>(service, 'firehosePutRecord');
      service['analyticsParams.device'] = deviceService.parsedUA;
      const data = addActionMock;
      service.performAddAction('', data);
      expect(service['firehosePutRecord']).toHaveBeenCalled();
    });
  });
  describe('firehosePutRecord', () => {
    it('should call firehose', () => {
      const firehose = windowRef.nativeWindow.AWS.Firehose();
      spyOn(firehose, 'putRecord');
      spyOn<any>(service, 'getEnvironment');
      service.recordData = {
        test: 'action',
        username: 'oxygenUser',
        token: 'ajhsdgu',
        isWrapper: true,
        bppToken: 'testBpp',
        appVersion: environment.version,
        actionName: 'betslipLogui_message',
        currentUrl: '/',
        referralUrl: '/',
        product: 'bm-tst1.coral.co.uk',
        logTime: new Date().getTime(),
        userAgent: 'Mozilla/5.0'
      } as any;
      service['firehosePutRecord']();
      expect(firehose.putRecord).toHaveBeenCalled();
    });
    it('should not call firehose', () => {
      const firehose = windowRef.nativeWindow.AWS.Firehose();
      environment.ENVIRONMENT = 'prod';
      spyOn(firehose, 'putRecord');
      spyOn<any>(service, 'getEnvironment');
      service['recordData'] = {} as any;
      Object.keys(service.recordData).length = 0;
      service['firehosePutRecord']();
      expect(Object.keys(service.recordData).length).toEqual(0);
      expect(firehose.putRecord).not.toHaveBeenCalled();
    });
  });
  describe('check Action Name', () => {
    it('should check action name', () => {
      spyOn<any>(service, 'checkActionName');
      service.checkActionName('betslipLogui_message', addActionMock);
      service['analyticsParams.device'] = deviceService.parsedUA;
    });
    it('should not have action name', () => {
      spyOn<any>(service, 'checkActionName');
      service.checkActionName('', addActionMock);
      service['analyticsParams.device'] = deviceService.parsedUA;
    });
  });
  describe('addAction', () => {
    it('should call performAddAction', () => {
      spyOn<any>(service, 'performAddAction');
      windowRef.nativeWindow.AWS.config.credentials.expired = false;
      service.addAction('betslipLogui_message', addActionMock);
      service.performAddAction('betslipLogui_message', addActionMock);
      service['analyticsParams.device'] = deviceService.parsedUA;
      expect(service.performAddAction).toHaveBeenCalled();
    });
    it('should push data to queue when AWS is undefined', () => {
      spyOn<any>(service, 'performAddAction');
      windowRef.nativeWindow.AWS = undefined;
      service.addAction('betslipLogui_message', addActionMock, 'aws_12346');
      expect(pubSubService.subscribe).toHaveBeenCalledWith('aws_12346', pubSubService.API.INIT_AWS, jasmine.any(Function));
      expect(service.performAddAction).toHaveBeenCalledWith('betslipLogui_message', addActionMock);
    });
    it('should push data to queue when config is undefined', () => {
      spyOn<any>(service, 'performAddAction');
      windowRef.nativeWindow.AWS.config = undefined;
      service.addAction('betslipLogui_message', addActionMock, 'aws_12346');
      expect(pubSubService.subscribe).toHaveBeenCalledWith('aws_12346', pubSubService.API.INIT_AWS, jasmine.any(Function));
      expect(service.performAddAction).toHaveBeenCalledWith('betslipLogui_message', addActionMock);
    });
    it('should push data to queue when expired is true', () => {
      spyOn<any>(service, 'performAddAction');
      windowRef.nativeWindow.AWS.config.credentials.expired = true;
      service.addAction('betslipLogui_message', addActionMock, 'aws_12346');
      expect(pubSubService.subscribe).toHaveBeenCalledWith('aws_12346', pubSubService.API.INIT_AWS, jasmine.any(Function));
      expect(service.performAddAction).toHaveBeenCalledWith('betslipLogui_message', addActionMock);
    });
  });
  describe('trackOxygenRequest', () => {
    it('success request no payload', () => {
      spyOn(service, 'addAction');
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, <any>{
        status: 201
      }, 100);
      service.addAction(
        'Ajax Call', trackOxySucPayload, 'aws_12345');
    });

    it('success request no payload and status set to 200', () => {
      spyOn(service, 'addAction');
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, <any>{
        status: undefined
      }, 100);
      service.addAction(
        'Ajax Call', trackOxySucPayload, 'aws_12345');
    });

    it('success request with payload', () => {
      spyOn(service, 'addAction');
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, <any>{
        status: 201,
        body: '1234567'
      }, 100);
      const data = trackOxySucPayload;
      data.payloadSize = 9;
      service.addAction(
        'Ajax Call', data);
    });

    it('error request with payload', () => {
      spyOn(service, 'addAction');
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, new HttpErrorResponse({
        status: 404,
        error: '1234567'
      }), 100);
      service.addAction(
        'Ajax Call', trackOxyErrPayload);
    });

    it('error request no payload', () => {
      spyOn(service, 'addAction');
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, new HttpErrorResponse({
        status: 404
      }), 100);
      const data = trackOxySucPayload;
      data.payloadSize = 0;
      data.appVersion = environment.version;
      service.addAction(
        'Ajax Call', data);
    });
    it('should not call trackOxygen request', () => {
      spyOn(service, 'addAction');
      service['isInterceptAjax'] = false;
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, new HttpErrorResponse({
        status: 404
      }), 100);
      expect(service['isInterceptAjax']).toBe(false);
      expect(service.addAction).not.toHaveBeenCalled();
    });
  });

  describe('#errorLog', () => {
    it('should call errorLog', () => {
      spyOn<any>(service, 'firehosePutRecord');
      const error = new Error('Error');
      service.errorLog(error);
      expect(service['firehosePutRecord']).toHaveBeenCalled();
    });
  });

  describe('#getUniqueSubscriberName', () => {
    it('should get unique subscriber name', () => {
      const subscribername = service['getUniqueSubscriberName']();
      expect(subscribername.includes('awsFirSubscr')).toBe(true);
    });
  });

  describe('addRouletteJourneySpecificPageAction', () => {
    it('should call addAction if RouletteJourney', () => {
      const actionName = 'name';
      const params = { error: 'error' };
      spyOn(service['userService'], 'isRouletteJourney').and.returnValue(true);
      const spy = spyOn(service, 'addAction');
      service['analyticsParams.device'] = deviceService.parsedUA;

      service.addRouletteJourneySpecificPageAction(actionName, params);

      expect(spy).toHaveBeenCalledWith(actionName, params);
    });

    it('should not call addAction if !RouletteJourney', () => {
      const actionName = 'name';
      const params = { error: 'error' };
      const spy = spyOn(service, 'addAction');

      service.addRouletteJourneySpecificPageAction(actionName, params);

      expect(spy).not.toHaveBeenCalled();
    });
  });

  describe('tracking browser', () => {
    it('should not add browser info', () => {
      spyOn(service, 'addAction');
      service.addAction('someAction',
        {
          token: 'ajhsdgu',
          isWrapper: true,
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: environment.version
        }
      );
    });

    it('should add browser info for ui_message tracking ', () => {
      spyOn(service, 'addAction');
      service.addAction('someAction=>UI_Message=>Error',
        {
          device: 'device',
          isWrapper: true,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: environment.version
        }
      );
    });
    it('should add browser info for betslip tracking ', () => {
      spyOn(service, 'addAction');
      service.addAction('someAction=>Betslip=>Error',
        {
          device: 'device',
          isWrapper: true,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: environment.version
        }
      );
    });
  });

  describe('checkAWS', () => {
    it('check aws case undefined', () => {
      windowRef.nativeWindow.AWS = undefined;
      service['checkAWS']();
    });
    it('check aws case config undefined ', () => {
      windowRef.nativeWindow.AWS.config = undefined;
      service['checkAWS']();
    });
    it('check aws case config credentials true case', () => {
      windowRef.nativeWindow.AWS.config.credentials.expired = false;
      service['checkAWS']();
    });
    it('check aws case config credentials false case', () => {
      windowRef.nativeWindow.AWS.config.credentials.expired = true;
      service['checkAWS']();
    });
  });

  describe('addRouletteJourneySpecificPageAction', () => {
    it('addRouletteJourneySpecificPageAction else case', () => {
      const actionName = 'name';
      const params = { error: 'error' };
      spyOn(service['userService'], 'isRouletteJourney').and.returnValue(false);
      service.addRouletteJourneySpecificPageAction(actionName, params);
    });
  });
});
