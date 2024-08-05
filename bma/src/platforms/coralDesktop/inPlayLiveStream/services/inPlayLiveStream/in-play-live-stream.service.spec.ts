import { InPlayLiveStreamService } from './in-play-live-stream.service';

const testStr = 'TestString';

describe('InPlayLiveStreamService', () => {
  let service: InPlayLiveStreamService;

  let inplayHelperService;
  let timeSyncService;
  let liveEventClockProviderService;
  let storageService;
  let userService;
  let eventService;
  let routingHelperService;

  beforeEach(() => {
    inplayHelperService = {
      unsubscribeForLiveUpdates: jasmine.createSpy('unsubscribeForLiveUpdates')
    };
    timeSyncService = {};
    liveEventClockProviderService = {};
    storageService = {};
    userService = {};
    eventService = {};
    routingHelperService = {
      getLastUriSegment: jasmine.createSpy('getLastUriSegment')
    };

    service = new InPlayLiveStreamService(
      inplayHelperService,
      timeSyncService,
      liveEventClockProviderService,
      storageService,
      userService,
      eventService,
      eventService,
      routingHelperService
    );
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('prepareFooter', () => {
    const items = [{ categoryName: '123', targetUri: '/test1'  }, { categoryName: testStr, targetUri: '/test' }] as any;

    it('should find menuItem with same categoryName in menuItems', () => {
      expect(service.prepareFooter(testStr.toLowerCase(), items, testStr)).not.toBeUndefined();
    });
    it('should return undefined if Not find menuItem with same categoryName in menuItems', () => {
      expect(service.prepareFooter(testStr, items, testStr)).toBeUndefined();
    });

    it('should find menuItem with same categoryName in menuItems', () => {
      routingHelperService.getLastUriSegment.and.returnValue('test');
      expect(service.prepareFooter(testStr.toLowerCase(), items, 'LIVE_EVENT')).not.toBeUndefined();
      expect(routingHelperService.getLastUriSegment).toHaveBeenCalledWith('/test');
    });
  });

  describe('removeCompetitionFromCollection', () => {
    it('should remove competition from collection', () => {
    const competitionsExpect = [
      {
        categoryName: '2',
        events: [{
          typeId: '124'
        }]
      }
    ] as any;
    const competitionsInput = competitionsExpect.slice();
    competitionsInput.push({
      categoryName: '1',
      events: [{
        typeId: '123'
      }]
    });
    const typeIds = ['123'];
    service.removeCompetitionFromCollection(competitionsInput, typeIds);
      expect(competitionsInput).toEqual(competitionsExpect);
    });
  });

  it('should unsubscribe for undisplayed events', () => {
    const competitions = [
      {
        categoryName: '2',
        events: [{
           id: 123
        }]
      }
    ] as any;
    service.removeEventFromCollection(competitions, 123);
    expect(inplayHelperService.unsubscribeForLiveUpdates).toHaveBeenCalledWith([{ id: 123 }]);
  });
});
