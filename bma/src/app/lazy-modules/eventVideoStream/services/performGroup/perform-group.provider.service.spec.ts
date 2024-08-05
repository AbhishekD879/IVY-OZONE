import { of as observableOf } from 'rxjs';
import { PerformGroupProviderService } from './perform-group.provider.service';
import environment from '@environment/oxygenEnvConfig';
import * as xml2js from 'xml2js';

describe('PerformGroupProviderService', () => {
  let service: PerformGroupProviderService;
  let http;
  let deviceService;
  let requestParams;

  beforeEach(() => {
    http = {
        get: jasmine.createSpy('get').and.returnValue(observableOf({data: 'data'}))
    };
    deviceService = {
        performProviderIsMobile: jasmine.createSpy('performProviderIsMobile').and.returnValue(true)
    };
    requestParams = {
      userId: 'userId',
      partnerId: 'partnerId',
      eventId: 'eventId',
      key: 'key'
    };
    service = new PerformGroupProviderService(http, deviceService);
  });

  describe('#addPerformUserToPull', () => {
    it('should add perform user to pull for case perfom provider is mobile', () => {
        const result = service.addPerformUserToPull(requestParams);
        result.subscribe();
        expect(http.get).toHaveBeenCalledWith(
          `${environment.PERFORM_GROUP_END_POINT}/validation/addUser/index.html?userId=userId&partnerId=partnerId&eventId=eventId&key=key`,
          { responseType: 'text' }
        );
    });
    it('should add perform user to pull for case perfom provider is desktop', () => {
      deviceService.performProviderIsMobile.and.returnValue(false);
      const result = service.addPerformUserToPull(requestParams);
      result.subscribe();
      expect(http.get).toHaveBeenCalledWith(
        /* eslint-disable max-len */
        `${environment.PERFORM_GROUP_END_POINT_DESKTOP}/validation/addUser/index.html?userId=userId&partnerId=partnerId&eventId=eventId&key=key`,
        { responseType: 'text' }
      );
    });
  });

  describe('#getNativeUrls', () => {
    beforeEach(() => {
      spyOn(xml2js, 'parseString').and.callThrough();
    });
    it('should get native urls', () => {
      const params = <any>{
        baseUrl: 'baseUrl',
        queryString: 'queryString'
      };
      http.get.and.returnValue(observableOf('some string'));
      service['generateRequestParams'] = jasmine.createSpy('generateRequestParams').and.returnValue(params);
      service.getNativeUrls(requestParams).subscribe((data) => {
        expect(data).toEqual('some string');
      });
      expect(http.get).toHaveBeenCalledWith(
        `baseUrl/wab/multiformat/index.html?queryString`,
        { responseType: 'text' }
      );
      expect(xml2js.parseString).toHaveBeenCalled();
    });

    it('should return parsed response', () => {
      http.get.and.returnValue(observableOf(''));
      service.getNativeUrls(requestParams).subscribe((data) => {
        expect(data).toBeNull();
      });
      expect(xml2js.parseString).toHaveBeenCalled();
    });
  });

  describe('#getNativeCSBUrl', () => {
    let params;
    beforeEach(() => {
      params = <any>{
        baseUrl: 'baseUrl',
        queryString: 'queryString'
      };
      service['generateRequestParams'] = jasmine.createSpy('generateRequestParams').and.returnValue(params);
    });
    it('should get native CSB url: iframe dimensions is defined', () => {
      const iframeDimensions = {
        width: 100,
        height: 100
      };
      const result = service.getNativeCSBUrl(requestParams, iframeDimensions);
      expect(result).toBe(`baseUrl/watch/event/index.html?queryString&rmg=true&width=100&height=100`);
    });
    it('should get native CSB url: iframe dimensions is not defined', () => {
      const result = service.getNativeCSBUrl(requestParams);
      expect(result).toBe(`baseUrl/watch/event/index.html?queryString&rmg=true`);
    });
  });

  describe('#generateRequestParams', () => {
    it('should generate baseUrl & queryString for case perfom provider is mobile', () => {
      const result = service['generateRequestParams'](requestParams);
      expect(result).toEqual({
        baseUrl: environment.PERFORM_GROUP_END_POINT,
        queryString: `userId=userId&partnerId=partnerId&eventId=eventId&key=key`
      });
    });
    it('should generate baseUrl & queryString for case perfom provider is desktop', () => {
      deviceService.performProviderIsMobile.and.returnValue(false);
      const result = service['generateRequestParams'](requestParams);
      expect(result).toEqual({
        baseUrl: environment.PERFORM_GROUP_END_POINT_DESKTOP,
        queryString: `userId=userId&partnerId=partnerId&eventId=eventId&key=key`
      });
    });
    it('should generate queryString according to available request params', () => {
      delete requestParams.key;
      const result = service['generateRequestParams'](requestParams);
      expect(result).toEqual({
        baseUrl: environment.PERFORM_GROUP_END_POINT,
        queryString: `userId=userId&partnerId=partnerId&eventId=eventId`
      });
    });
  });
});
