import { of } from 'rxjs';
import { NewRelicService } from './new-relic.service';
import { HttpErrorResponse } from '@angular/common/http';
import environment from '@environment/oxygenEnvConfig';

const packageData = require('../../../../../package.json');

describe('NewRelicService', () => {
  let service: NewRelicService,
    windowRef,
    userService,
    cmsService,
    deviceService,
    cookiesLength,
    savedProductionState;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        newrelic: {
          addPageAction: jasmine.createSpy(),
          noticeError: jasmine.createSpy()
        },
        document: {
          cookie: 'cookie'
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
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        newRelic: { interceptAjax: true }
      }))
    };

    deviceService = {
      parsedUA: 'device',
      isWrapper: true,
    };

    cookiesLength = windowRef.nativeWindow.document.cookie.length;
    savedProductionState = environment.production;

    service = new NewRelicService(windowRef, userService, cmsService, deviceService);
  });

  it('constructor', () => {
    expect(service['isInterceptAjax']).toBeTruthy();
  });

  it('addPageAction', () => {
    service.addPageAction('rememberMeLoginSequence', { test: 'action' });

      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledTimes(1);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'rememberMeLoginSequence', {
          test: 'action',
          username: 'oxygenUser',
          token: 'ajhsdgu',
          isWrapper: true,
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
  });

  it('addPageAction should save each action to newRelicEvents in window if newRelicEvents is defined in window', () => {
    windowRef.nativeWindow.newRelicEvents = {};
    service.addPageAction('logout', { test: 'action' });

    expect(windowRef.nativeWindow.newRelicEvents['logout']).toBeDefined();
    expect(windowRef.nativeWindow.newRelicEvents['logout'].length).toBe(1);
    expect(windowRef.nativeWindow.newRelicEvents['logout'][0]).toEqual({
      test: 'action',
      username: 'oxygenUser',
      token: 'ajhsdgu',
      isWrapper: true,
      bppToken: 'testBpp',
      appVersion: packageData.version
    });

    environment.production = savedProductionState;
  });

  it('addPageAction should NOT called', () => {
    windowRef.nativeWindow.newrelic = '';
    const result = service.addPageAction('rememberMeLoginSequence', { test: 'action' });
    expect(result).toBe(undefined);
  });

  describe('#noticeError', () => {
    it('should call noticeError', () => {
      const error = new Error('Error');
      service.noticeError(error);

      expect(windowRef.nativeWindow.newrelic.noticeError).toHaveBeenCalledTimes(1);
      expect(windowRef.nativeWindow.newrelic.noticeError).toHaveBeenCalledWith(error);
    });

    it('should not call noticeError', () => {
      windowRef.nativeWindow.newrelic = '';

      const error = new Error('Error'),
        result = service.noticeError(error);

      expect(result).toBe(undefined);
    });
  });

  describe('trackOxygenRequest', () => {
    it('success request no payload', () => {
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, <any>{
        status: 201
      }, 100);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'Ajax Call', {
          url: 'https://backoffice-tst2.coral.co.uk/test',
          level: 'success',
          time: 100,
          requestMethod: 'GET',
          cookiesLength,
          isWrapper: true,
          status: 201,
          payloadSize: 0,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });

    it('success request with payload', () => {
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, <any>{
        status: 201,
        body: '1234567'
      }, 100);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'Ajax Call', {
          url: 'https://backoffice-tst2.coral.co.uk/test',
          level: 'success',
          time: 100,
          requestMethod: 'GET',
          cookiesLength,
          isWrapper: true,
          status: 201,
          payloadSize: 9,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });

    it('error request with payload', () => {
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, new HttpErrorResponse({
        status: 404,
        error: '1234567'
      }), 100);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'Ajax Call', {
          url: 'https://backoffice-tst2.coral.co.uk/test',
          level: 'error',
          time: 100,
          requestMethod: 'GET',
          cookiesLength,
          isWrapper: true,
          status: 404,
          payloadSize: 9,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });

    it('error request with payload', () => {
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, new HttpErrorResponse({
        status: 404
      }), 100);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'Ajax Call', {
          url: 'https://backoffice-tst2.coral.co.uk/test',
          level: 'error',
          time: 100,
          isWrapper: true,
          requestMethod: 'GET',
          cookiesLength,
          status: 404,
          payloadSize: 0,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });
  });

  describe('addRouletteJourneySpecificPageAction', () => {

    it('should call addPageAction if RouletteJourney', () => {
      const actionName = 'name';
      const params = { error: 'error' };
      spyOn(service['userService'], 'isRouletteJourney').and.returnValue(true);
      const spy = spyOn(service, 'addPageAction');

      service.addRouletteJourneySpecificPageAction(actionName, params);

      expect(spy).toHaveBeenCalledWith(actionName, params);
    });

    it('should not call addPageAction if !RouletteJourney', () => {
      const actionName = 'name';
      const params = { error: 'error' };
      const spy = spyOn(service, 'addPageAction');

      service.addRouletteJourneySpecificPageAction(actionName, params);

      expect(spy).not.toHaveBeenCalled();
    });
  });

  describe('trackOxygenRequest', () => {
    it('success request no payload', () => {
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, <any>{
        status: 201
      }, 100);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'Ajax Call', {
          url: 'https://backoffice-tst2.coral.co.uk/test',
          level: 'success',
          time: 100,
          requestMethod: 'GET',
          cookiesLength,
          status: 201,
          isWrapper: true,
          payloadSize: 0,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });

    it('success request with payload', () => {
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, <any>{
        status: 201,
        body: '1234567'
      }, 100);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'Ajax Call', {
          url: 'https://backoffice-tst2.coral.co.uk/test',
          level: 'success',
          time: 100,
          requestMethod: 'GET',
          cookiesLength,
          isWrapper: true,
          status: 201,
          payloadSize: 9,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });

    it('error request with payload', () => {
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, new HttpErrorResponse({
        status: 404,
        error: '1234567'
      }), 100);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'Ajax Call', {
          url: 'https://backoffice-tst2.coral.co.uk/test',
          level: 'error',
          time: 100,
          requestMethod: 'GET',
          cookiesLength,
          isWrapper: true,
          status: 404,
          payloadSize: 9,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });

    it('error request with payload', () => {
      service.trackOxygenRequest(<any>{
        url: 'https://backoffice-tst2.coral.co.uk/test',
        method: 'GET',
      }, new HttpErrorResponse({
        status: 404
      }), 100);
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith(
        'Ajax Call', {
          url: 'https://backoffice-tst2.coral.co.uk/test',
          level: 'error',
          time: 100,
          requestMethod: 'GET',
          cookiesLength,
          status: 404,
          isWrapper: true,
          payloadSize: 0,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });
  });

  describe('tracking browser', () => {
    it('should not add browser info', () => {
      service.addPageAction('someAction');
      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith('someAction',
        {
          token: 'ajhsdgu',
          isWrapper: true,
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });

    it('should add browser info for ui_message tracking ', () => {
      service.addPageAction('someAction=>UI_Message=>Error');

      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith('someAction=>UI_Message=>Error',
        {
          device: 'device',
          isWrapper: true,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });
    it('should add browser info for betslip tracking ', () => {
      service.addPageAction('someAction=>Betslip=>Error');

      expect(windowRef.nativeWindow.newrelic.addPageAction).toHaveBeenCalledWith('someAction=>Betslip=>Error',
        {
          device: 'device',
          isWrapper: true,
          token: 'ajhsdgu',
          username: 'oxygenUser',
          bppToken: 'testBpp',
          appVersion: packageData.version
        }
      );
    });
  });
});

