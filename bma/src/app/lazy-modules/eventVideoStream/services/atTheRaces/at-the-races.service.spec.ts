import { of as observableOf } from 'rxjs';
import { fakeAsync } from '@angular/core/testing';

import { TimeService } from '@core/services/time/time.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { UserService } from '@core/services/user/user.service';
import { IStreamProvidersResponse } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { AtTheRacesService } from '@lazy-modules/eventVideoStream/services/atTheRaces/at-the-races.service';
import { IAtrRequestParamsModel, IAtrStreamModel } from '@lazy-modules/eventVideoStream/services/atTheRaces/at-the-races.models';

describe('AtTheRacesService', () => {
  let service: AtTheRacesService;
  let timeServiceStub: TimeService;
  let httpStub;
  let device;
  const userServiceStub = { username: 'testName' };

  const testStr: string = 'testStr';
  const testPartnerCode: string = 'testAtrPartnerCode';
  const testSectetKey: string = 'testAtrSectetKey';


  beforeEach(() => {
    httpStub = {
      get: jasmine.createSpy().and.returnValue(observableOf({ body: {} }))
    };
    timeServiceStub = jasmine.createSpyObj({
      fiveMinutsInMiliseonds: 300000
    });
    device = {
      browserName: 'Chrome',
      get isDesktopSafari() {
        return this.isDesktop && this.browserName.toLowerCase() === 'safari';
      }
    };

    service = new AtTheRacesService(httpStub, timeServiceStub, userServiceStub as UserService,
      device);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('setConfigParams', () => {
    it('should set partnerCode', () => {
      service.setConfigParams(testPartnerCode, null);
      expect(service['partnerCode']).toEqual(testPartnerCode);
    });

    it('should set secretKey', () => {
      service.setConfigParams(null, testSectetKey);
      expect(service['secretKey']).toEqual(testSectetKey);
    });
  });

  describe('parseStreamResponse', () => {
    it('should throw a standard error', () => {
      const response = {
        IsOK: false,
        Error: {
          ErrorCode: 'EVENT_OVER',
          ErrorMessage: 'eventFinished'
        }
      };

      service['parseStreamResponse'](response).subscribe(null, (error: string) => {
        expect(error).toEqual(response.Error.ErrorMessage);
      });
    });

    it('should throw a servicesCrashed error', () => {
      const response = {
        IsOK: false,
        Error: {
          ErrorCode: 'UNKNOWN_ERROR',
          ErrorMessage: 'error'
        }
      };

      service['parseStreamResponse'](response).subscribe(null, (error: string) => {
        expect(error).toEqual('servicesCrashed');
      });
    });

    it('should return url', () => {
      service['getAtrStream'] = jasmine.createSpy('getAtrStream').and.returnValue({ Url: 'url' });
      const response = {
        IsOK: true,
        EventInfo: {
          Streams: ['streams']
        }
      } as any;

      service['parseStreamResponse'](response).subscribe((result: Object) => {
        expect(service['getAtrStream']).toHaveBeenCalledWith(response.EventInfo.Streams);
        expect(result).toEqual('url');
      });
    });

    it('should throw a servicesCrashed error if stream has no url', () => {
      service['getAtrStream'] = jasmine.createSpy('getAtrStream').and.returnValue({ Url: undefined });
      const response = {
        IsOK: true,
        EventInfo: {
          Streams: ['streams']
        }
      } as any;

      service['parseStreamResponse'](response).subscribe(null, (result: Object) => {
        expect(service['getAtrStream']).toHaveBeenCalledWith(response.EventInfo.Streams);
        expect(result).toEqual('servicesCrashed');
      });
    });

    it('should throw a servicesCrashed error if EventInfo is undefined', () => {
      const response = {
        IsOK: true,
        EventInfo: undefined
      } as any;

      service['parseStreamResponse'](response).subscribe(null, (result: Object) => {
        expect(result).toEqual('servicesCrashed');
      });
    });
  });

  describe('isEventStarted', () => {
    const yesterday = new Date(new Date().setDate(new Date().getDate() - 1)).toString();
    const tomorrow = new Date(new Date().setDate(new Date().getDate() + 1)).toString();
    let event;

    it('should return true if event has been started', () => {
      event = { startTime: yesterday };
      expect(service.isEventStarted(event as ISportEvent)).toBeFalsy();
    });

    it('should return false if event don\'t start yet', () => {
      event = { startTime: tomorrow };
      expect(service.isEventStarted(event as ISportEvent)).toBeFalsy();
    });
  });

  describe('getVideoUrl', () => {
    const providerInfo = {};

    beforeEach(() => {
      service['getStreamUrl'] = jasmine.createSpy().and.returnValue(observableOf({}));
      service['parseStreamResponse'] = jasmine.createSpy().and.returnValue(observableOf('testStr'));
    });

    it('should call getStreamUrl', () => {
      service.getVideoUrl(providerInfo as IStreamProvidersResponse);
      expect(service['getStreamUrl']).toHaveBeenCalledWith(providerInfo as any);
    });

    it('should call parseStreamResponse', () => {
      service.getVideoUrl(providerInfo as IStreamProvidersResponse).subscribe(() => {
        expect(service['parseStreamResponse']).toHaveBeenCalledTimes(1);
      });
    });

  });

  describe('getStreamUrl', () => {
    it('should call getATRStriaminUrls with proper params', () => {
      service['getATRStriaminUrls'] = jasmine.createSpy();
      spyOn<any>(service, 'getATREventId').and.returnValue(123);
      spyOn<any>(service, 'createAccessKey').and.returnValue('key');

      service['getStreamUrl']({} as any);
      expect(service['getATRStriaminUrls']).toHaveBeenCalledWith({
        eventId: 123 as any,
        userId: service['userId'],
        key: 'key',
        partnerCode: service['partnerCode'],
        mediaFormat: 'HLS'
      } as any);
    });

    it('should call getATRStriaminUrls with proper params for desktop', () => {
      service['getATRStriaminUrls'] = jasmine.createSpy();
      spyOn<any>(service, 'getATREventId').and.returnValue(123);
      spyOn<any>(service, 'createAccessKey').and.returnValue('key');
      service['device'].isDesktop = true;

      service['getStreamUrl']({} as any);
      expect(service['getATRStriaminUrls']).toHaveBeenCalledWith(jasmine.objectContaining({
        mediaFormat: 'FLV'
      }));
    });

    it('should call getATRStriaminUrls with proper params for Safari desktop', () => {
      service['getATRStriaminUrls'] = jasmine.createSpy();
      spyOn<any>(service, 'getATREventId').and.returnValue(123);
      spyOn<any>(service, 'createAccessKey').and.returnValue('key');
      service['device'].isDesktop = true;
      service['device'].browserName = 'Safari';

      service['getStreamUrl']({} as any);
      expect(service['getATRStriaminUrls']).toHaveBeenCalledWith(jasmine.objectContaining({
        mediaFormat: 'HLS'
      }));
    });

    it('should raise error if no event id', fakeAsync(() => {
      service['getStreamUrl']({} as any).subscribe(
        () => {},
        (err) => { expect(err).toEqual('servicesCrashed'); }
      );
    }));
  });

  describe('userId', () => {
    it('should return userId', () => {
      expect(service['userId']).toEqual('testName');
    });
  });

  describe('getAtrStream', () => {
    const bitrateLevels = ['Adaptive', 'High', 'Medium', 'Low'];
    const streams = [];

    bitrateLevels.forEach(el => {
      streams.push({ BitrateLevel: el });
    });

    streams.forEach(el => {
      it(`should return ${el['BitrateLevel']} element if BitrateLevel: ${el['BitrateLevel']} is the highest`, () => {
        expect(service['getAtrStream'](streams)).toEqual(el as IAtrStreamModel);
        el['BitrateLevel'] = null;
      });
    });

    it(`should return first element if didn't find some BitrateLevel property`, () => {
      expect(service['getAtrStream'](streams)).toEqual(streams[0] as IAtrStreamModel);
    });
  });

  describe('getATREventId', () => {
    const providerId = '16389';
    const SSResponseId = '654321';

    let ATRStreamMapping;

    beforeEach(() => {
      ATRStreamMapping = {
        listOfMediaProviders: [{
          name: testStr,
          children: [{
            media: {
              id: 'V46381',
              refRecordId: '1397869',
              refRecordType: 'event',
              accessProperties: `ATRStream:${providerId}`,
              siteChannels: 'd,e,i,o,v,'
            }
          }]
        }],
        SSResponse: {
          children: [{
            mediaProvider: {
              name: 'At The Races',
              children: [{ media: { accessProperties: `ATRStream:${SSResponseId}` } }]
            }
          }]
        },
        priorityProviderName: testStr,
        priorityProviderCode: testStr,
        stream: testStr,
        error: testStr
      };
    });

    it('should return undefined EventId ', () => {
      ATRStreamMapping.SSResponse.children[0].mediaProvider.name = 'name';
      expect(service['getATREventId'](ATRStreamMapping as IStreamProvidersResponse)).toEqual(undefined);
    });

    it('should return undefined EventId ', () => {
      ATRStreamMapping.SSResponse = undefined;
      ATRStreamMapping.listOfMediaProviders[0].children = [];
      expect(service['getATREventId'](ATRStreamMapping as IStreamProvidersResponse)).toEqual(undefined);
    });

    it('should return EventId of SSResponse if SSResponse children has it', () => {
      expect(service['getATREventId'](ATRStreamMapping as IStreamProvidersResponse)).toEqual(SSResponseId);
    });

    it('should return EventId of listOfMediaProviders if SSResponse children don\'t has it', () => {
      ATRStreamMapping.SSResponse = null;
      expect(service['getATREventId'](ATRStreamMapping as IStreamProvidersResponse)).toEqual(providerId);
    });
  });

  describe('createAccessKey', () => {
    const accessKey = 'f5e7ddd9896427b15565b7be642867ad';

    it('should create md5 coded access key', () => {
      service.setConfigParams(testPartnerCode, testSectetKey);
      expect(service['createAccessKey'](testStr)).toEqual(accessKey);
    });
  });

  it('getEventId, should return ""', () => {
    const media = {} as any;
    expect(service['getEventId'](media)).toEqual('');
  });

  describe('getATRStriaminUrls', () => {
    const params = {
      mediaFormat: testStr,
      eventId: testStr,
      userId: testStr,
      partnerCode: testStr,
      key: testStr,
    };

    it('should call http.get method', () => {
      service['getATRStriaminUrls'](params as IAtrRequestParamsModel).subscribe((result: Object) => {
        expect(result).toEqual({} as any);
      });
      expect(service['http']['get']).toHaveBeenCalledTimes(1);

    });
  });

});
