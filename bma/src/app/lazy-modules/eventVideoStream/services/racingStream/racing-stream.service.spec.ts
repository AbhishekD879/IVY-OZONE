import { fakeAsync, flush } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import * as md5 from 'blueimp-md5';

import { RacingStreamService } from './racing-stream.service';

describe('RacingStreamService', () => {
  let service: RacingStreamService,
    timeService,
    userService,
    performGroupService,
    performGroupProviderService,
    datePipe,
    errorHandler,
    successHandler;

  let requestConfig;
  const key = 'someKey';
  const userId = 'someName';
  const partnerId = '1';
  const performGroupId = '345';
  const isNormalInteger = true;
  const providerInfo = { listOfMediaProviders: [] } as any;
  const performConfig = { CSBIframeEnabled: true, partnerId } as any;
  const url = 'url';

  beforeEach(() => {
    userService = { username: userId };
    timeService = {
      threeMinutsInMiliseonds: 180000
    };
    performGroupService = { getPerformGroupId: jasmine.createSpy().and.returnValue(performGroupId) };
    performGroupProviderService = {
      getNativeUrls: jasmine.createSpy().and.returnValue(of(null)),
      getNativeCSBUrl: jasmine.createSpy().and.returnValue(url),
    };
    datePipe = {
      transform: jasmine.createSpy('transform')
    };

    successHandler = jasmine.createSpy('successHandler');
    errorHandler = jasmine.createSpy('errorHandler');
    requestConfig = { key, userId, partnerId, performGroupId, isNormalInteger };

    service = new RacingStreamService(timeService,
      userService,
      performGroupService,
      performGroupProviderService,
      datePipe);
  });

  it('should properly parse response from streaming service ', () => {
    const response = {
      eventInfo: {
        availableMediaFormats: [{
          mediaFormat: [{
            playerAlias: 'hlsmed',
            stream: [{
              streamLaunchCode: ['test']
            }]
          }]
        }]
      }
    } as any;
    service.rejectAndThrowError = jasmine.createSpy();
    const result = service.parseResponseDataObject(response);
    result.subscribe((stream) => {
      expect(stream).toEqual('test');
    });
    response.eventInfo.availableMediaFormats[0].mediaFormat[0].playerAlias = 'incorrect value';
    service.parseResponseDataObject(response);
    expect(service.rejectAndThrowError).toHaveBeenCalled();
  });

  describe('getVideoUrl', () => {
    const parsedUrl = 'parsedUrl';

    beforeEach(() => {
      spyOn(service, 'generateRequestConfig').and.returnValue(requestConfig);
      spyOn(service, 'parseResponse').and.returnValue(of(parsedUrl));
    });

    it(`should throw error if isNormalInteger equal false`, fakeAsync(() => {
      requestConfig.isNormalInteger = false;
      (service.generateRequestConfig as any).and.returnValue(requestConfig);

      service.getVideoUrl(providerInfo, performConfig).subscribe(null, errorHandler);
      flush();

      expect(service.generateRequestConfig).toHaveBeenCalledWith(providerInfo, performConfig);
      expect(errorHandler).toHaveBeenCalledWith(performGroupId);
    }));

    it(`should getNativeUrls`, fakeAsync(() => {
      service.getVideoUrl(providerInfo, performConfig).subscribe(successHandler);
      flush();

      expect(performGroupProviderService.getNativeUrls)
        .toHaveBeenCalledWith({ key, userId, partnerId, eventId: performGroupId });
      expect(successHandler).toHaveBeenCalled();
    }));

    it(`should concatMap to parseResponse`, fakeAsync(() => {
      performGroupProviderService.getNativeUrls.and.returnValue(of(url));
      service.getVideoUrl(providerInfo, performConfig).subscribe(successHandler);
      flush();

      expect(service.parseResponse).toHaveBeenCalledWith(url);
      expect(successHandler).toHaveBeenCalledWith(parsedUrl);
    }));

    it(`should catchError`, fakeAsync(() => {
      const error = 'error';
      performGroupProviderService.getNativeUrls.and.returnValue(throwError(error));
      service.getVideoUrl(providerInfo, performConfig).subscribe(null, errorHandler);
      flush();

      expect(errorHandler).toHaveBeenCalledWith(error);
    }));

    it(`should return default msg`, fakeAsync(() => {
      performGroupProviderService.getNativeUrls.and.returnValue(throwError(null));
      service.getVideoUrl(providerInfo, performConfig).subscribe(null, errorHandler);
      flush();

      expect(errorHandler).toHaveBeenCalledWith('servicesCrashed');
    }));
  });

  describe('getVideoCSBUrl', () => {
    beforeEach(() => {
      spyOn(service, 'generateRequestConfig').and.returnValue(requestConfig);
    });

    it(`should return null if isNormalInteger equal false`, () => {
      requestConfig.isNormalInteger = false;
      (service.generateRequestConfig as any).and.returnValue(requestConfig);

      const res = service.getVideoCSBUrl(providerInfo, performConfig);

      expect(service.generateRequestConfig).toHaveBeenCalledWith(providerInfo, performConfig, false);
      expect(res).toBeNull();
    });

    it(`should return NativeCSBUrl`, () => {
      const res = service.getVideoCSBUrl(providerInfo, performConfig);

      expect(performGroupProviderService.getNativeCSBUrl)
        .toHaveBeenCalledWith({ userId, partnerId, eventId: performGroupId }, undefined);
      expect(res).toEqual(url);
    });

    it(`should return NativeCSBUrl with Dimensions`, () => {
      const iframeDimensions = { width: 200, height: 100 };
      const res = service.getVideoCSBUrl(providerInfo, performConfig, iframeDimensions);

      expect(performGroupProviderService.getNativeCSBUrl)
        .toHaveBeenCalledWith({ userId, partnerId, eventId: performGroupId }, iframeDimensions);
      expect(res).toEqual(url);
    });
  });

  describe('generateRequestConfig', () => {
    let requesrConfig;
    beforeEach(() => {
      spyOn(service, 'generateKeyURLS').and.returnValue(key);
      spyOn(service, 'isNormalInteger').and.returnValue(true);

      requesrConfig = { performGroupId, key, isNormalInteger, partnerId: partnerId, userId };
    });

    it(`should return RequestConfig`, () => {
      expect(service.generateRequestConfig(providerInfo, performConfig)).toEqual(requesrConfig);
    });

    it(`should return RequestConfig without key property`, () => {
      requesrConfig = { performGroupId, key: false, isNormalInteger, partnerId, userId };
      expect(service.generateRequestConfig(providerInfo, performConfig, false)).toEqual(requesrConfig);
    });
  });

  describe('@generateKeyURLS', () => {
    let config;
    const date = '2020/03/24';

    beforeEach(() => {
      config = {
        partnerId,
        seed: '123'
      };
      datePipe.transform.and.returnValue(date);
    });

    it('should return encoded key with mobilePartnerId and mobileSeed', () => {
      const toEncrypt: string = `${date + date + date}_1_someName_123`;
      const md5String: string = md5(toEncrypt + config.seed, null, true);
      const base64: string = btoa(md5String);
      const encodedKey: string = encodeURIComponent(base64);
      const actualResult = service.generateKeyURLS('123', config);

      expect(actualResult).toEqual(encodedKey);
    });
  });

  it('@rejectAndThrowError', fakeAsync(() => {
    service.rejectAndThrowError('error').subscribe(successHandler, errorHandler);
    flush();
    expect(errorHandler).toHaveBeenCalledWith('error');
  }));

  it('@isNormalInteger', () => {
    expect(service.isNormalInteger('123')).toEqual(true);
  });

  describe('isEventStarted', () => {
    it('should return true', () => {
      expect(service.isEventStarted({ startTime: '2010-01-01' } as any)).toBeTruthy();
    });

    it('should return false', () => {
      expect(service.isEventStarted({ startTime: '2099-01-01' } as any)).toBeFalsy();
    });
  });

  describe('parseResponse', () => {
    beforeEach(() => {
      spyOn(service, 'parseResponseDataString').and.returnValue(of(null));
      spyOn(service, 'parseResponseDataObject').and.returnValue(of(null));
    });

    it('should parse data as string', () => {
      service.parseResponse('data').subscribe();
      expect(service.parseResponseDataString).toHaveBeenCalledWith('data');
    });

    it('should parse data as object', () => {
      const data: any = {
        eventInfo: { availableMediaFormats: [{ mediaFormat: 'format' }] }
      };
      service.parseResponse(data).subscribe();
      expect(service.parseResponseDataObject).toHaveBeenCalledWith(data);
    });

    it('should throw error', () => {
      service.parseResponse(null).subscribe(null, err => {
        expect(err).toBe('servicesCrashed');
      });
    });
  });

  describe('parseResponseDataString', () => {
    it('shoud throw error message', () => {
      service.parseResponseDataString('eventnotstarted').subscribe(null, err => {
        expect(err).toBe('eventNotStarted');
      });
    });

    it(`shoud throw error "servicesCrashed"`, () => {
      service.parseResponseDataString('unknownerror').subscribe(null, err => {
        expect(err).toBe('servicesCrashed');
      });
    });
  });
});
