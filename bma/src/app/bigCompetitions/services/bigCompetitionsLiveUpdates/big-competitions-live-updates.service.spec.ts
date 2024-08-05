import { of } from 'rxjs';

import {
  BigCompetitionsLiveUpdatesService
} from '@app/bigCompetitions/services/bigCompetitionsLiveUpdates/big-competitions-live-updates.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('BigCompetitionsLiveUpdatesService', () => {
  let service;
  let pubSubService;
  let liveServService;

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    liveServService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({})),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    service = new BigCompetitionsLiveUpdatesService(
      pubSubService,
      liveServService
    );
  });

  describe('liveServeUpdateHandler', () => {
    let update;

    beforeEach(() => {
      update = {
          type: 'MESSAGE',
          message: 'testMessage',
          channel: {
            name: 'test',
            id: 'testId'
          },
          event: {
            id: 'testEventId'
          },
          subChannel: {
            type: 'subChannelType'
          }
        };
    });

    it('should handle live Serve Update and trigger Publish', () => {
        service['liveServeUpdateHandler'](update);

        expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.LIVE_SERVE_MS_UPDATE, {
          channel: update.channel.name,
          channel_number: update.event.id,
          payload: update.message,
          subject_number: update.channel.id,
          subject_type: update.subChannel.type
        });
    });

    it('should not handle live Serve Update and trigger Publish', () => {
      update = {};
      service['liveServeUpdateHandler'](update);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });


  describe('reconnect', () => {
    it('should call liveServService', () => {
      service.reconnect();

      expect(liveServService.connect).toHaveBeenCalled();
    });
  });

  describe('subscribe', () => {
    let events;

    beforeEach(() => {
      service.getIds = jasmine.createSpy('getIds');
    });

    it('should call getIds with undefined', () => {
      service.subscribe(events);
    });

    it('should call getIds with []', () => {
      events = [];
      service.subscribe(events);
    });

    it('should call getIds with [{}, {}]', () => {
      events = [{}, {}];
      service.subscribe(events);
    });

    afterEach(() => {
      expect(liveServService.connect).toHaveBeenCalled();
      expect(liveServService.subscribe).toHaveBeenCalled();
      expect(service.getIds).toHaveBeenCalledWith(events);
    });
  });

  describe('unsubscribe', () => {
    let events;

    beforeEach(() => {
      service.getIds = jasmine.createSpy('getIds');
    });

    it('should call getIds with undefined', () => {
      service.unsubscribe(events);
    });

    it('should call getIds with []', () => {
      events = [];
      service.unsubscribe(events);
    });

    it('should call getIds with [{}, {}]', () => {
      events = [{}, {}];
      service.unsubscribe(events);
    });

    afterEach(() => {
      expect(liveServService.unsubscribe).toHaveBeenCalled();
      expect(service.getIds).toHaveBeenCalledWith(events);
    });
  });

  describe('removeEventEntity', () => {
    let events;

    beforeEach(() => {
      service.isUndisplayed = jasmine.createSpy('isUndisplayed').and.returnValue(true);
      service.deleteAndUnsubscribe = jasmine.createSpy('deleteAndUnsubscribe');
      service.isAllOutcomesUndisplayed = jasmine.createSpy('isAllOutcomesUndisplayed');
    });

    it('should not remove event entity', () => {
      service.removeEventEntity();

      expect(service.isUndisplayed).not.toHaveBeenCalled();
      expect(service.deleteAndUnsubscribe).not.toHaveBeenCalled();
      expect(service.isAllOutcomesUndisplayed).not.toHaveBeenCalled();
    });

    it('should not remove event from events', () => {
      events = [];
      service.removeEventEntity(events);

      expect(service.isUndisplayed).not.toHaveBeenCalled();
      expect(service.deleteAndUnsubscribe).not.toHaveBeenCalled();
      expect(service.isAllOutcomesUndisplayed).not.toHaveBeenCalled();
    });

    it('should not remove event from events', () => {
      events = [undefined];
      service.removeEventEntity(events);

      expect(service.isUndisplayed).not.toHaveBeenCalled();
      expect(service.deleteAndUnsubscribe).not.toHaveBeenCalled();
      expect(service.isAllOutcomesUndisplayed).not.toHaveBeenCalled();
    });

    it('should remove events list where all undisplayed events', () => {
      events = [{}];
      service.removeEventEntity(events);

      expect(service.deleteAndUnsubscribe).toHaveBeenCalledWith(events, 0);
      expect(service.isUndisplayed).toHaveBeenCalledWith(events[0]);
      expect(service.isAllOutcomesUndisplayed).not.toHaveBeenCalled();
    });

    it('should remove events list where all undisplayed events', () => {
      events = [{
        markets: []
      }];
      service.removeEventEntity(events);

      expect(service.deleteAndUnsubscribe).toHaveBeenCalledWith(events, 0);
      expect(service.isUndisplayed).toHaveBeenCalledWith(events[0]);
      expect(service.isAllOutcomesUndisplayed).not.toHaveBeenCalled();
    });

    it('should remove events list where all undisplayed markets', () => {
      events = [{
        markets: [
          {
            outcomes: {}
          }
        ]
      }];
      service.removeEventEntity(events);

      expect(service.isUndisplayed).toHaveBeenCalledWith(events[0]);
      expect(service.deleteAndUnsubscribe).toHaveBeenCalledWith(events, 0);
      expect(service.isAllOutcomesUndisplayed).not.toHaveBeenCalled();
    });

    it('should remove events list where all undisplayed markets', () => {
      events = [{
        markets: [{}]
      }];
      service.removeEventEntity(events);

      expect(service.isUndisplayed).toHaveBeenCalledWith(events[0]);
      expect(service.deleteAndUnsubscribe).toHaveBeenCalledWith(events, 0);
      expect(service.isAllOutcomesUndisplayed).not.toHaveBeenCalled();
    });

    it('should remove events list where all undisplayed outcomes', () => {
      events = [{
        markets: [
          {
            outcomes: {}
          }
        ]
      }];
      service.isUndisplayed = jasmine.createSpy('isUndisplayed').and.returnValue(false);
      service.isAllOutcomesUndisplayed = jasmine.createSpy('isAllOutcomesUndisplayed').and.returnValue(true);
      service.removeEventEntity(events);

      expect(service.isUndisplayed).toHaveBeenCalledWith(events[0]);
      expect(service.isAllOutcomesUndisplayed).toHaveBeenCalledWith(events[0].markets[0].outcomes);
      expect(service.deleteAndUnsubscribe).toHaveBeenCalledWith(events, 0);
    });

    it('should not remove events list where outcomes is displayed', () => {
      events = [{
        markets: [
          {
            outcomes: {}
          }
        ]
      }];
      service.isUndisplayed = jasmine.createSpy('isUndisplayed').and.returnValue(false);
      service.isAllOutcomesUndisplayed = jasmine.createSpy('isAllOutcomesUndisplayed').and.returnValue(false);
      service.removeEventEntity(events);

      expect(service.isUndisplayed).toHaveBeenCalledWith(events[0]);
      expect(service.isAllOutcomesUndisplayed).toHaveBeenCalledWith(events[0].markets[0].outcomes);
      expect(service.deleteAndUnsubscribe).not.toHaveBeenCalled();
    });
  });

  describe('isUndisplayed', () => {
    let result,
      entity;

    it('should return false', () => {
      entity = {
        isDisplayed: ''
      };
      result = service['isUndisplayed'](entity);

      expect(result).toEqual(false);
    });

    it('should return true', () => {
      entity = {
        isDisplayed: false
      };
      result = service['isUndisplayed'](entity);

      expect(result).toEqual(true);
    });
  });

  describe('deleteAndUnsubscribe', () => {
    it('should unsubcribe from LP updates', () => {
      const events = [{}, {}];

      service.unsubscribe = jasmine.createSpy('unsubscribe');
      service['deleteAndUnsubscribe'](events, 0);

      expect(service.unsubscribe).toHaveBeenCalledWith([events[0]]);
    });
  });

  describe('getIds', () => {
    let result,
      events;

    it('should return []', () => {
      result = service['getIds']();

      expect(result).toEqual([]);
    });

    it('should return []', () => {
      events = [];
      result = service['getIds'](events);

      expect(result).toEqual(events);
    });

    it('should return markets.liveServChannels and outcomes.liveServChannels', () => {
      events = [{
        liveServChannels: '',
        markets: [{
          liveServChannels: 'liveServChannels',
          outcomes: [{
            liveServChannels: 'liveServChannels'
          }]
        }]
      }];

      result = service['getIds'](events);

      expect(result).toEqual(['', 'liveServChannel', 'liveServChannel']);
    });

    it('should return outcomes.liveServChannels', () => {
      events = [{
        liveServChannels: 'liveServChannels',
        markets: [{
          liveServChannels: '',
          outcomes: [{
            liveServChannels: 'liveServChannels'
          }]
        }]
      }];

      result = service['getIds'](events);

      expect(result).toEqual(['liveServChannel', '', 'liveServChannel']);
    });
  });

  describe('isAllOutcomesUndisplayed', () => {
    let result,
      outcomes;

    beforeEach(() => {
      outcomes = [{
        isDisplayed: true
      }];
    });

    it('should return false', () => {
      result = service['isAllOutcomesUndisplayed'](outcomes);

      expect(result).toEqual(false);
    });

    it('should return true', () => {
      outcomes[0].isDisplayed = false;
      result = service['isAllOutcomesUndisplayed'](outcomes);

      expect(result).toEqual(true);
    });
  });
});
