import { fakeAsync, tick } from '@angular/core/testing';
import {
  LiveEventsCarouselComponent
} from '@app/bigCompetitions/components/liveEventsCarousel/live-events-carousel.component';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';

describe('LiveEventsCarouselComponent', () => {

  let component: LiveEventsCarouselComponent;

  let pubSubService;
  let inplaySubscriptionService;
  let participantsService;
  let bigCompetitionsService;
  let changeDetectorRef;
  let events;
  let participants;

  beforeEach(() => {
    events = [{
      name: 'name',
      id: 1
    }, {
      name: 'name2',
      id: '2'
    }] as IBigCompetitionSportEvent[];

    participants = {
      HOME: {
        name: '',
        abbreviation: ''
      },
      AWAY: {
        name: '',
        abbreviation: ''
      }
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: {
        MOVE_EVENT_TO_INPLAY: 'MOVE_EVENT_TO_INPLAY',
        WS_EVENT_LIVE_UPDATE: 'WS_EVENT_LIVE_UPDATE',
        WS_EVENT_DELETE: 'WS_EVENT_DELETE'
      }
    };
    inplaySubscriptionService = {
      loadCompetitionEvents: jasmine.createSpy('loadCompetitionEvents').and.returnValue(Promise.resolve(events)),
      unsubscribeForLiveUpdates: jasmine.createSpy('unsubscribeForLiveUpdates'),
      subscribeForLiveUpdates: jasmine.createSpy('subscribeForLiveUpdates')
    };
    participantsService = {
      parseParticipantsFromName: jasmine.createSpy('parseParticipantsFromName').and.returnValue(participants)
    };
    bigCompetitionsService = {
      addOutcomeMeaningMinorCode: jasmine.createSpy('addOutcomeMeaningMinorCode')
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new LiveEventsCarouselComponent(
      pubSubService,
      inplaySubscriptionService,
      participantsService,
      bigCompetitionsService,
      changeDetectorRef
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should perform init commands', () => {
      component.carouselId = 'id';
      component['loadCompetitionEvents'] = jasmine.createSpy('loadCompetitionEvents');
      component.ngOnInit();
      expect(component.name).toBe(`liveCarousel-${component.carouselId}`);
      expect(component['loadCompetitionEvents']).toHaveBeenCalled();
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(component.name, pubSubService.API.MOVE_EVENT_TO_INPLAY, jasmine.any(Function));
    });

    it('should handle MOVE_EVENT_TO_INPLAY pubsub event and add event if it is not in list and is of same typeId', fakeAsync(() => {
      const typeId = 123;
      const mockEvent = {
        id: '3',
        typeId: `${typeId}`
      };
      let callback;

      pubSubService.subscribe.and.callFake((name, eventName, cb) => {
        if (eventName === pubSubService.API.MOVE_EVENT_TO_INPLAY) {
          callback = cb;
        }
      });
      component.typeId = typeId;

      component.ngOnInit();
      tick();
      callback && callback(mockEvent);

      expect(component.events.length).toEqual(3);
      expect(bigCompetitionsService.addOutcomeMeaningMinorCode).toHaveBeenCalled();
      expect(inplaySubscriptionService.subscribeForLiveUpdates).toHaveBeenCalledWith([mockEvent.id]);
    }));

    it('should handle MOVE_EVENT_TO_INPLAY pubsub event and not add event if it is already in list', fakeAsync(() => {
      const typeId = 123;
      const mockEvent = {
        id: +events[1].id,
        typeId: `${typeId}`
      };
      let callback;

      pubSubService.subscribe.and.callFake((name, eventName, cb) => {
        if (eventName === pubSubService.API.MOVE_EVENT_TO_INPLAY) {
          callback = cb;
        }
      });
      component.typeId = typeId;

      component.ngOnInit();
      tick();
      callback && callback(mockEvent);

      expect(component.events.length).toEqual(2);
      expect(bigCompetitionsService.addOutcomeMeaningMinorCode).not.toHaveBeenCalled();
      expect(inplaySubscriptionService.subscribeForLiveUpdates).not.toHaveBeenCalledWith([mockEvent.id]);
    }));

    it('should handle MOVE_EVENT_TO_INPLAY pubsub event and not add event if type Ids are different', fakeAsync(() => {
      const typeId = 123;
      const mockEvent = {
        id: '3',
        typeId: `124`
      };
      let callback;

      pubSubService.subscribe.and.callFake((name, eventName, cb) => {
        if (eventName === pubSubService.API.MOVE_EVENT_TO_INPLAY) {
          callback = cb;
        }
      });
      component.typeId = typeId;

      component.ngOnInit();
      tick();
      callback && callback(mockEvent);

      expect(component.events.length).toEqual(2);
      expect(bigCompetitionsService.addOutcomeMeaningMinorCode).not.toHaveBeenCalled();
      expect(inplaySubscriptionService.subscribeForLiveUpdates).not.toHaveBeenCalledWith([mockEvent.id]);
    }));
  });

  it('#ngOnDestroy', () => {
    const sportEvents = [
      { id: 12 }
    ] as IBigCompetitionSportEvent[];
    component.events = sportEvents;
    component.name = 'name';
    component.ngOnDestroy();
    expect(inplaySubscriptionService.unsubscribeForLiveUpdates)
      .toHaveBeenCalledWith(jasmine.arrayContaining([12]));
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component.name);
  });

  it('#ngOnDestroy when eventIds is undefined', () => {
    const sportEvents = [] as IBigCompetitionSportEvent[];
    component.events = sportEvents;
    component.ngOnDestroy();
    expect(inplaySubscriptionService.unsubscribeForLiveUpdates).not.toHaveBeenCalled();
  });

  it('should call correct methods', fakeAsync(() => {
    component.categoryId = 10;
    component.typeId = 12;
    component['addLiveUpdatesHandler'] = jasmine.createSpy('addLiveUpdatesHandler');
    component['loadCompetitionEvents']();

    tick();

    expect(inplaySubscriptionService.loadCompetitionEvents)
      .toHaveBeenCalledWith(true, component.categoryId, component.typeId, false);
    expect(participantsService.parseParticipantsFromName).toHaveBeenCalledWith(events[0].name);
    expect(component.events[0].participants).toBe(participants);
    expect(component['addLiveUpdatesHandler']).toHaveBeenCalled();
  }));

  it('should call correct methods', () => {
    const sportEvents = [
      { id: 15 }
    ] as IBigCompetitionSportEvent[];
    component['handleLiveUpdate'] = jasmine.createSpy('handleLiveUpdate');
    pubSubService.subscribe.and.callFake((name, eventName, cb) => {
        cb();
    });
    component['deleteEvent'] = jasmine.createSpy('deleteEvent');
    component.events = sportEvents;
    component.name = 'name';
    component['addLiveUpdatesHandler']();

    expect(pubSubService.subscribe).toHaveBeenCalledTimes(2);
    expect(component['handleLiveUpdate']).toHaveBeenCalled();
    expect(inplaySubscriptionService.subscribeForLiveUpdates)
      .toHaveBeenCalledWith(jasmine.arrayContaining([15]));
    expect(component['deleteEvent']).toHaveBeenCalled();
  });

  it('should call correct methods', () => {
    const updatedItemId = 10;
    const messageBody = 'message';
    const sportEvents = [
      { id: 10 }
    ] as IBigCompetitionSportEvent[];
    component.events = sportEvents;
    component['handleLiveUpdate'](updatedItemId, messageBody);
    expect(pubSubService.publish)
      .toHaveBeenCalledWith(pubSubService.API.WS_EVENT_UPDATE, jasmine.objectContaining({
        events: [sportEvents[0]],
        update: messageBody
      }), false);
  });

  it('should call correct methods without eventToUpdate', () => {
    const updatedItemId = 10;
    const messageBody = 'message';
    const sportEvents = [] as IBigCompetitionSportEvent[];
    component.events = sportEvents;
    component['handleLiveUpdate'](updatedItemId, messageBody);
    expect(pubSubService.publish).not.toHaveBeenCalledWith();
  });

  describe('deleteEvent', () => {
    it('should remove event from the stored list if id of passed event exists in list', () => {
      const id = '2';

      component.events = [{ id: '1' }, { id: +id }] as any;
      component['deleteEvent'](id);

      expect(component.events.length).toEqual(1);
    });

    it('should not remove event from the stored list if id of passed event does not exist in list', () => {
      const id = '3';

      component.events = [{ id: '1' }, { id: 2 }] as any;
      component['deleteEvent'](id);

      expect(component.events.length).toEqual(2);
    });
  });
});
