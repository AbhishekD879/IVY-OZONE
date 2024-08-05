import { RacingSpecialsCarouselService } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.service';

describe('RacingSpecialsCarouselService', () => {

  let service: RacingSpecialsCarouselService;

  let siteServerService;
  let timeService;
  let cacheEventsService;
  let pubSubService;
  let channelService;

  const orderedEvents = [
    { displayOrder: 1, name: 'Event A' },
    { displayOrder: 3, name: 'Event B' },
    { displayOrder: 5, name: 'Event C' }] as any;

  describe('RacingSpecialsCarouselService', () => {
    beforeEach(() => {
      siteServerService = {
        getRacingSpecialsEvents: jasmine.createSpy().and.returnValue(Promise.resolve(orderedEvents))
      };
      timeService = {
        apiDataCacheInterval: {}
      };
      cacheEventsService = {
        store: jasmine.createSpy(),
        stored: jasmine.createSpy(),
        async: jasmine.createSpy(),
        clearByName: jasmine.createSpy(),
        storedData: {}
      };
      pubSubService = {
        publish: jasmine.createSpy()
      };
      channelService = jasmine.createSpyObj(['getLSChannelsFromArray']);

      service = new RacingSpecialsCarouselService(siteServerService, timeService,
        cacheEventsService, pubSubService, channelService);
    });

    describe('subscribeForUpdates', () => {
      it(`should subscribe on subscribeForUpdates`, () => {
        const channel = ['sEVENT1'];
        const events = [{ liveServChannels: 'EV1234555', liveServChildrenChannels: 'EVC1234555' },
          { liveServChannels: 'EV9984234', liveServChildrenChannels: 'EVC1234555' }] as any;
        channelService.getLSChannelsFromArray.and.returnValue(channel);

        service.subscribeForUpdates(events);

        expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith(events);
        expect(pubSubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', {
          channel,
          module: 'racing-specials'
        });
      });
    });

    it('unSubscribeForUpdates - should unsubscribe from updates', () => {
      service.unSubscribeForUpdates();
      expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'racing-specials');
    });

    it('clearCache - should clear Cache', () => {
      service.clearCache(1234);
      expect(cacheEventsService.clearByName).toHaveBeenCalledWith('racingSpecialsEvents1234');
    });

    it('orderEvents - should order event by displayOrder', () => {
      const events = [
        { displayOrder: 3, name: 'Event B' },
        { displayOrder: 1, name: 'Event A' },
        { displayOrder: 5, name: 'Event C' }] as any;
      expect(service.orderEvents(events)).toEqual(orderedEvents);
    });

    it('getEvents - should load linked events by event id', () => {
      const eventId = 546346;
      service.getEvents(eventId);
      expect(siteServerService.getRacingSpecialsEvents).toHaveBeenCalled();
      expect(timeService.apiDataCacheInterval['racingSpecialsEvents546346']).toEqual(5 * 60 * 1000);
      expect(cacheEventsService.storedData['racingSpecialsEvents546346']).toEqual({});
    });

    it('extendCacheParams - should extend cache Params', () => {
      const eventId = 12345;
      service['extendCacheParams'](eventId);
      expect(timeService.apiDataCacheInterval['racingSpecialsEvents12345']).toEqual(5 * 60 * 1000);
      expect(cacheEventsService.storedData['racingSpecialsEvents12345']).toEqual({});
    });
  });
});
