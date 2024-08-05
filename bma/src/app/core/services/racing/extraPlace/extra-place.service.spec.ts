import { ExtraPlaceService } from './extra-place.service';

import { ISportEvent } from '@core/models/sport-event.model';

import { extraPlaceConfig } from '@core/services/racing/extraPlace/extra-place.constant';

describe('#ExtraPlaceService', () => {
  let service;
  let pubSubService;
  let siteServerService;
  let timeService;
  let cacheEventsService;
  let gtmService;
  let events;
  let channelService;

  beforeEach(() => {
    events = [
      { name: 'event1', liveServChannels: 'event1', drilldownTagNames: 'EVFLAG_FRT' },
      { name: 'event2', liveServChannels: 'event2', drilldownTagNames: '' },
      { name: 'event3', liveServChannels: 'event3', drilldownTagNames: ''},
    ];
    siteServerService = {
      getExtraPlaceEvents: jasmine.createSpy('getExtraPlaceEvents').and.returnValue(Promise.resolve(null))
    };
    timeService = {
      apiDataCacheInterval: {},
      selectTimeRangeStart: jasmine.createSpy('selectTimeRangeStart')
    };
    cacheEventsService = {
      storedData: {},
      stored: jasmine.createSpy('stored'),
      store: jasmine.createSpy('store'),
      async: jasmine.createSpy('async')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    channelService = {
      getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray').and.returnValue([{}, {}])
    };

    service = new ExtraPlaceService(
      siteServerService as any,
      timeService as any,
      cacheEventsService as any,
      gtmService as any,
      pubSubService as any,
      channelService as any
    );
  });

  it('#constructor', () => {
    expect(service).toBeTruthy();
    expect(timeService.apiDataCacheInterval['extraPlaceEventsHR']).toEqual(extraPlaceConfig.cacheInterval);
    expect(cacheEventsService.storedData['extraPlaceEventsHR']).toEqual({});
  });

  describe('#getEvents', () => {
    it('should Get extra place events from SS', () => {
      service.getEvents({}).then(null, () => {});

      expect(siteServerService.getExtraPlaceEvents).toHaveBeenCalled();
      expect(timeService.selectTimeRangeStart).toHaveBeenCalled();
      expect(cacheEventsService.stored).toHaveBeenCalledWith('extraPlaceEventsHR');
    });
  });

  describe('#subscribeForUpdates', () => {
    it('should subscribe from updates', () => {
      const result = service.subscribeForUpdates(events);

      expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith(events as ISportEvent[]);
      expect(pubSubService.publish).toHaveBeenCalled();

      expect(result).not.toBe('');
    });

    describe('should NOT subscribe from updates', () => {
      beforeEach(() => {
        channelService.getLSChannelsFromArray.and.returnValue([]);
      });

      it('should subscribe for updates when no channels', () => {
        const result = service.subscribeForUpdates();

        expect(result).toEqual('');
      });
    });
  });

  describe('#unSubscribeForUpdates', () => {
    it('should unsubscribe from updates', () => {
      service.unSubscribeForUpdates('extra-place-1565879224866');

      expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'extra-place-1565879224866');
    });
    it('should not unsubscribe for updates if channel ids dosen"t exists', () => {
      service.unSubscribeForUpdates();

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  describe('#cachedEvents', () => {
    it('should Store events or get new', () => {
      service.cachedEvents(siteServerService.getExtraPlaceEvents, 'extraPlaceEventsHR')({});

      expect(cacheEventsService.stored).toHaveBeenCalledWith('extraPlaceEventsHR');
    });
  });

  describe('#sendGTM', () => {
    it('should send GTM tracking, when user click on extra place card', () => {
      service.sendGTM('extra');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'horse racing',
        eventAction: 'extra place',
        eventLabel: 'extra'
      });
    });
  });
});
