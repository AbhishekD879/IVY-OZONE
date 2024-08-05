import { ImgService } from './img.service';
import { of } from 'rxjs';
import { IImgQueryParams } from '@lazy-modules/eventVideoStream/services/imgService/img.model';

describe('ImgService', () => {
  let service: ImgService;

  let http;
  let timeService;
  let timeSyncService;

  beforeEach(() => {
    http = {
      get: jasmine.createSpy('get').and.returnValue(of({
        body: {
          hlsUrl: 'videoLink'
        }
      }))
    };
    timeService = {
      fiveMinutsInMiliseonds: 300000
    };
    timeSyncService = {
      getUserSessionTime: jasmine.createSpy('getUserSessionTime').and.returnValue(of({}))
    };

    service = new ImgService(http, timeService, timeSyncService);
  });

  it('setConfigParams, should set "operatorId" and "secret"', () => {
    const operatorId = 'operatorId',
      secret = 'secret';
    service.setConfigParams(operatorId, secret);

    expect(service['IMGOperatorId']).toEqual(operatorId);
    expect(service['IMGSecretKey']).toEqual(secret);
  });

  describe('isEventStarted', () => {
    it('should return "true" if event started', () => {
      const eventEntity = {
        startTime: Date.now()
      } as any;

      expect(service.isEventStarted(eventEntity)).toEqual(true);
    });

    it('should return "false" if the event has NOT started yet.', () => {
      const eventEntity = {
        startTime: Date.now() + timeService.fiveMinutsInMiliseonds + 1
      } as any;

      expect(service.isEventStarted(eventEntity)).toEqual(false);
    });
  });

  it('getVideoUrl, should return url', () => {
    const providerInfo = {} as any,
      queryParams = {
        eventId: 0
      };
    service['getIMGEventId'] = jasmine.createSpy('getIMGEventId').and.returnValue(of({}));
    service['prepareQueryParams'] = jasmine.createSpy('prepareQueryParams').and.returnValue(of(queryParams));
    service['getIMGStreamingUrls'] = jasmine.createSpy('getIMGStreamingUrls').and.returnValue(of('url'));

    service.getVideoUrl(providerInfo).subscribe((result: string) => {
      expect(service['getIMGEventId']).toHaveBeenCalledWith(providerInfo);
      expect(service['timeSyncService'].getUserSessionTime).toHaveBeenCalledWith(true, false);
      expect(service['prepareQueryParams']).toHaveBeenCalled();
      expect(service['getIMGStreamingUrls']).toHaveBeenCalledWith(queryParams as any);
      expect(result).toEqual('url');
    });
  });


  describe('getIMGEventId', () => {
    const eventId = 'eventId';

    beforeEach(() => {
      service['getEventId'] = jasmine.createSpy('').and.returnValue('eventId');
    });

    it('should return eventId from streamProvider by SSResponse is exist', () => {
      const response = {
        SSResponse: {
          children: [{
            mediaProvider: {
              children: [],
              name: 'IMG Video Streaming'
            }
          }]
        }
      } as any;

      service['getIMGEventId'](response).subscribe((result: string) => {
        expect(service['getEventId']).toHaveBeenCalledWith(response.SSResponse.children[0].mediaProvider.children);
        expect(service['IMGEventId']).toEqual(eventId);
        expect(result).toEqual(eventId);
      });
    });

    it('should return eventId from streamProvider, listOfMediaProviders is exist', () => {
      const response = {
        listOfMediaProviders: [{
          children: [{}],
          name: 'name'
        }]
      } as any;

      service['getIMGEventId'](response).subscribe((result: string) => {
        expect(service['getEventId']).toHaveBeenCalledWith(response.listOfMediaProviders[0].children);
        expect(service['IMGEventId']).toEqual(eventId);
        expect(result).toEqual(eventId);
      });
    });

    it('should throw error - mediaProvider.name !== "IMG Video Streaming"', () => {
      const response = {
        SSResponse: {
          children: [{
            mediaProvider: {
              children: [],
              name: 'name'
            }
          }]
        }
      } as any,
        servicesCrashed = 'servicesCrashed';

      service['getIMGEventId'](response).subscribe(null, (error: string) => {
        expect(service['getEventId']).not.toHaveBeenCalled();
        expect(service['IMGEventId']).toEqual(undefined);
        expect(error).toEqual(servicesCrashed);
      });
    });

    it('should throw error - listOfMediaProviders.children is empty', () => {
      const response = {
          listOfMediaProviders: [{
            children: [],
            name: 'name'
          }]
        } as any,
        servicesCrashed = 'servicesCrashed';

      service['getIMGEventId'](response).subscribe(null, (error: string) => {
        expect(service['getEventId']).not.toHaveBeenCalled();
        expect(service['IMGEventId']).toEqual(undefined);
        expect(error).toEqual(servicesCrashed);
      });
    });
  });

  it('getEventId, should return eventId', () => {
    const accessProperty = 'accessProperties',
      children = [{
      media: {
        accessProperties: `test:${accessProperty}`
      }
    }];

    expect(service['getEventId'](children)).toEqual(accessProperty);
  });

  it('getEventId, should return eventId', () => {
      const children = [{
        media: {
          accessProperties: ''
        }
      }];

    expect(service['getEventId'](children)).toEqual(undefined);
  });

  it('prepareQueryParams, should return ', () => {
    const serverData = {
      'x-forward-for': 'x-forward-for',
      timestamp: 1
    },
      queryParams  = {
        eventId: 'IMGEventId',
        operatorId: 'IMGOperatorId',
        auth: '3c7eb83a8768a70932e49811631a6028',
        timeStamp: 1
    };
    service['IMGEventId'] = queryParams.eventId;
    service['IMGOperatorId'] = queryParams.operatorId;
    service['IMGSecretKey'] = 'IMGSecretKey';

    service['prepareQueryParams'](serverData).subscribe((result: IImgQueryParams) => {
      expect(result).toEqual(queryParams);
    });
  });

  it('getIMGStreamingUrls', () => {
    service['getIMGStreamingUrls']({
      eventId: '123',
      timeStamp: 1231231231,
      operatorId: '26',
      auth: 'asedas'
    }).subscribe((res) => {
      expect(http.get).toHaveBeenCalledTimes(1);
      expect(res).toEqual('videoLink');
    });
  });
});
