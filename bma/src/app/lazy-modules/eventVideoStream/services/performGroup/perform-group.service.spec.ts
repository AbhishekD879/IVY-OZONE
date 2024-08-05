import { PerformGroupService } from './perform-group.service';
import {
  IPerformGroupConfig,
  IStreamProvidersResponse
} from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { throwError, of as observableOf } from 'rxjs';

describe('PerformGroupService', () => {
  let service: PerformGroupService;

  let userService;
  let timeService;
  let performGroupProviderService;
  let domToolsService;
  let awsService;

  beforeEach(() => {
    userService = {
      username: 'testName'
    };
    timeService = {
      oneDayInMiliseconds: 86400000,
      additionalTimeForSteamStartEnd: 0,
      getCurrentTime: jasmine.createSpy('getCurrentTime'),
      dateToString: jasmine.createSpy('dateToString')
    };
    performGroupProviderService = {
      addPerformUserToPull: jasmine.createSpy('addPerformUserToPull')
    };
    domToolsService = jasmine.createSpyObj(['getWidth', 'css']);
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };

    service = new PerformGroupService(userService, timeService, performGroupProviderService,
      domToolsService, awsService);
  });

  describe('isPerformStreamStarted', () => {
    const event = { startTime: '2018-06-30T16:57:12Z' } as any;

    describe('should return true', () => {
      it(`if 8PM day before`, () => {
        timeService.getCurrentTime.and.returnValue(new Date('2018-06-29T20:00:00Z').getTime());
      });

      it(`if 11PM day before`, () => {
        timeService.getCurrentTime.and.returnValue(new Date('2018-06-29T23:19:00Z').getTime());
      });

      it(`if today`, () => {
        timeService.getCurrentTime.and.returnValue(new Date('2018-06-30T09:57:00Z').getTime());
      });

      afterEach(() => {
        expect(service.isPerformStreamStarted(event)).toBeTruthy();
      });
    });

    describe('should return false', () => {
      it(`if 7PM day before`, () => {
        timeService.getCurrentTime.and.returnValue(new Date('2018-06-29T19:57:00Z').getTime());
      });

      it(`if 1AM day before`, () => {
        timeService.getCurrentTime.and.returnValue(new Date('2018-06-29T01:03:59Z').getTime());
      });

      it(`if couple days before`, () => {
        timeService.getCurrentTime.and.returnValue(new Date('2018-06-15T19:59:59Z').getTime());
      });

      afterEach(() => {
        expect(service.isPerformStreamStarted(event)).toBeFalsy();
      });
    });
  });

  describe('getElementWidth', () => {
    let elementRef;
    let parentNode;
    const elementWidth = 100;

    beforeEach(() => {
      elementRef = { nativeElement: {} } as any;

      parentNode = { tag: 'div' };
      elementRef.nativeElement.parentNode = parentNode;
      domToolsService.getWidth.and.returnValue(elementWidth);

    });

    it('should handle case when element does not have parentElement', () => {
      expect(service['getElementWidth'](elementRef)).toEqual(elementWidth);
      expect(domToolsService.getWidth).toHaveBeenCalledWith(parentNode);
    });

    it('should handle case when parentElement does not have parentNode', () => {

      elementRef.nativeElement.parentElement = {
        parentElement: null
      };
      elementRef.nativeElement.parentNode = parentNode;

      expect(service['getElementWidth'](elementRef)).toEqual(elementWidth);
      expect(domToolsService.getWidth).toHaveBeenCalledWith(parentNode);
    });

    it('should set display block', () => {
      const parentElement = { tag: 'body' };

      elementRef.nativeElement.parentElement = {
        parentElement: {
          parentNode: parentElement
        }
      };

      expect(service['getElementWidth'](elementRef)).toEqual(elementWidth);
      expect(domToolsService.css).toHaveBeenCalledWith(parentNode, 'display', 'block');
    });
  });

  describe('@performGroupId', () => {
    let successHandler,
      errorHandler;
    beforeEach(() => {
      successHandler = jasmine.createSpy('successHandler');
      errorHandler = jasmine.createSpy('errorHandler');
    });

    it('should return error if perform group id is not integer', () => {
      spyOn(service, 'getPerformGroupId').and.returnValue(false as any);

      service.performGroupId({} as IStreamProvidersResponse, {} as IPerformGroupConfig, 111)
        .subscribe(successHandler, errorHandler);

      expect(errorHandler).toHaveBeenCalledWith(false);
    });

    it('should return error if perform group provider throw error', () => {
      spyOn(service, 'getPerformGroupId').and.returnValue('123');
      performGroupProviderService.addPerformUserToPull.and.returnValue(throwError(''));

      service.performGroupId({} as IStreamProvidersResponse, {} as IPerformGroupConfig, 111)
        .subscribe(successHandler, errorHandler);

      expect(errorHandler).toHaveBeenCalledWith('servicesCrashed');
      expect(performGroupProviderService.addPerformUserToPull).toHaveBeenCalled();
      expect(awsService.addAction).toHaveBeenCalledWith('STREAM_TOKENISATION_ERROR', jasmine.objectContaining({
        eventId: 111,
        performEventId: '123',
        response: 'servicesCrashed'
      }));
    });

    it('should return empty string if perform group provider does not send success', () => {
      spyOn(service, 'getPerformGroupId').and.returnValue('123');
      performGroupProviderService.addPerformUserToPull.and.returnValue(observableOf(['test', {}]));

      service.performGroupId({} as IStreamProvidersResponse, {} as IPerformGroupConfig, 111)
        .subscribe(successHandler, errorHandler);

      expect(errorHandler).not.toHaveBeenCalled();
      expect(successHandler).toHaveBeenCalledWith('');
      expect(performGroupProviderService.addPerformUserToPull).toHaveBeenCalled();
      expect(awsService.addAction).toHaveBeenCalledWith('STREAM_TOKENISATION_ERROR', jasmine.objectContaining({
        eventId: 111,
        performEventId: '123',
        response: 'test'
      }));
    });

    it('should return performGroupId if perform group provider send success', () => {
      spyOn(service, 'getPerformGroupId').and.returnValue('123');
      performGroupProviderService.addPerformUserToPull.and.returnValue(observableOf('success'));

      service.performGroupId({} as IStreamProvidersResponse, {} as IPerformGroupConfig, 111)
        .subscribe(successHandler, errorHandler);

      expect(errorHandler).not.toHaveBeenCalled();
      expect(successHandler).toHaveBeenCalledWith('123');
      expect(performGroupProviderService.addPerformUserToPull).toHaveBeenCalled();
      expect(awsService.addAction).not.toHaveBeenCalled();
    });

    it('should return undefined', () => {
      service.getPerformGroupId = () => null;
      service['isNormalInteger'] = () => true;
      expect(service.performGroupId({} as any, {} as any, 0)).toBeUndefined();
    });
  });

  describe('@sendAwsData', () => {
    it('should send to AWS eventId, performEventId and default response', () => {
      service['sendAwsData'](111, '123');

      expect(awsService.addAction).toHaveBeenCalledWith('STREAM_TOKENISATION_ERROR', jasmine.objectContaining({
        eventId: 111,
        performEventId: '123',
        response: 'servicesCrashed'
      }));
    });

    it('should send to AWS eventId, performEventId and response', () => {
      service['sendAwsData'](111, '123', 'test');

      expect(awsService.addAction).toHaveBeenCalledWith('STREAM_TOKENISATION_ERROR', jasmine.objectContaining({
        eventId: 111,
        performEventId: '123',
        response: 'test'
      }));
    });
  });

  describe('isEventStarted', () => {
    beforeEach(() => {
      timeService.getCurrentTime.and.returnValue(new Date(2020, 0, 1));
    });

    it('should return true', () => {
      expect(
        service.isEventStarted({ startTime: '2019-01-01' } as any)
      ).toBeTruthy();
    });
    it('should return false', () => {
      const today = new Date();
      const eventTime = new Date(today.setDate(today.getDate() + 1));
      expect(
        service.isEventStarted({ startTime: eventTime } as any)
      ).toBeFalsy();
    });
  });

  describe('getPerformGroupId', () => {
    it('should get perform id from SSResponse', () => {
      const providerInfo: any = {
        SSResponse: {
          children: [{}, {
            mediaProvider: {
              children: [{}, {
                media: { accessProperties: 'provider:id1,info' }
              }]
            }
          }]
        }
      };
      expect(service.getPerformGroupId(providerInfo)).toBe('id1');
    });

    it('should get perform id from listOfMediaProviders', () => {
      const providerInfo: any = {
        listOfMediaProviders: [{ children: [] }, {
          children: [{
            media: { accessProperties: 'provider:id2,info' }
          }]
        }]
      };
      expect(service.getPerformGroupId(providerInfo)).toBe('id2');
    });

    it(`should return 'servicesCrashed'`, () => {
      expect(service.getPerformGroupId({} as any)).toBe('servicesCrashed');
    });
  });

  describe('generateMD5', () => {
    it('should create code', () => {
      expect(
        service['generateMD5']('1', { partnerId: 'dkid', seed: 'dkseed' })
      ).toBe('GN49IN%2FoSQJqVKpWO43wGw%3D%3D');
    });

    it('should create code', () => {
      expect(service['generateMD5']('1', {})).toBe('aiPr2wmL0i5LHtqUXji6Eg%3D%3D');
    });
  });
});
