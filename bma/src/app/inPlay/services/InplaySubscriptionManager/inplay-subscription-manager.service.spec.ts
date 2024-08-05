import { InplaySubscriptionManagerService } from './inplay-subscription-manager.service';
import { inplayConfig } from '@app/inPlay/constants/config';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { SUBSCRIBE_MESSAGES } from '@app/inPlay/constants/messages';

describe('InplaySubscriptionManagerService', () => {
  let service: InplaySubscriptionManagerService;
  let pubSubService;
  let subscriptionsManagerService;
  let inPlayConnectionService;
  let inPlayStorageService;

  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy()
    };

    subscriptionsManagerService = {
      create: jasmine.createSpy().and.returnValue({})
    };

    inPlayConnectionService = {
      emitSocket: jasmine.createSpy(),
      addEventListener: jasmine.createSpy(),
      removeEventListener: jasmine.createSpy()
    };

    inPlayStorageService = {
      onVirtualsUpdate: jasmine.createSpy()
    };

    service = new InplaySubscriptionManagerService(
      pubSubService,
      subscriptionsManagerService,
      inPlayConnectionService,
      inPlayStorageService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service.subscriptionsManager).toBeTruthy();
  });

  it('addEventListeners', () => {
    service.addEventListeners();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'inplaySubscription', `${inplayConfig.moduleName}.${EVENTS.SOCKET_DISCONNECT}`, jasmine.any(Function)
    );
  });

  it('#virtualSportsListener', () => {
    const data = {
      categoryId: 1,
      categoryName: 'football',
      liveEventCount: 2,
      liveStreamEventCount: 4,
      showInPlay: true,
      svgId: '34324234234',
      targetUri: '',
      targetUriCopy: '',
      upcomingEventCount: 5,
      imageTitle: 'sample',
      upcommingLiveStreamEventCount: 4 // allsports typo in property on backend
    }
    service.virtualSportsListener(data as any);
    expect(inPlayStorageService.onVirtualsUpdate).toHaveBeenCalled();
  });

  it('subscribeForLiveUpdates', () => {
    const eventsIds = [1, 2];
    const eventsToSubscribe = [3];
    service.subscriptionsManager.checkForSubscribe = jasmine.createSpy().and.returnValue(eventsToSubscribe);

    service.subscribeForLiveUpdates(eventsIds);

    expect(service.subscriptionsManager.checkForSubscribe).toHaveBeenCalledWith(eventsIds);
    expect(inPlayConnectionService.emitSocket).toHaveBeenCalledWith(
      SUBSCRIBE_MESSAGES.SUBSCRIBE, eventsToSubscribe
    );
  });

  it('unsubscribeForLiveUpdates', () => {
    const eventsIds = [1, 2];
    const eventsToUnsubscribe = [3];
    service.subscriptionsManager.checkForUnsubscribe = jasmine.createSpy().and.returnValue(eventsToUnsubscribe);

    service.unsubscribeForLiveUpdates(eventsIds);

    expect(service.subscriptionsManager.checkForUnsubscribe).toHaveBeenCalledWith(eventsIds);
    expect(inPlayConnectionService.emitSocket).toHaveBeenCalledWith(
      SUBSCRIBE_MESSAGES.UNSUBSCRIBE, eventsToUnsubscribe
    );
  });

  describe('subscribe4RibbonUpdates', () => {
    beforeEach(() => {
      service.subscribe = jasmine.createSpy('subscribe');
    });
    it('should subscribe', () => {
      service.wsEventsHandlers[SUBSCRIBE_MESSAGES.RIBBON_CHANGE] = [];
      service.subscribe4RibbonUpdates();
      expect(service.subscribe).toHaveBeenCalledWith(
        SUBSCRIBE_MESSAGES.RIBBON_CHANGE, jasmine.any(Function)
      );
    });

    it('should not subscribe', () => {
      service.wsEventsHandlers[SUBSCRIBE_MESSAGES.RIBBON_CHANGE] = [() => 1];
      service.subscribe4RibbonUpdates();
      expect(service.subscribe).not.toHaveBeenCalled();
    });
  });

  describe('subscribeForStructureUpdates', () => {
    beforeEach(() => {
      service.subscribe = jasmine.createSpy();
    });

    it('subscribeForStructureUpdates', () => {
      service.subscribeForStructureUpdates();

      expect(service.subscribe).toHaveBeenCalledWith(
        SUBSCRIBE_MESSAGES.STRUCTURE_CHANGE, jasmine.any(Function)
      );
    });

    it(`should subscribe for liveStream structure updates if call with true`, () => {
      service.subscribeForStructureUpdates(true);

      expect(service.subscribe).toHaveBeenCalledWith(
        SUBSCRIBE_MESSAGES.LS_STRUCTURE_CHANGE, jasmine.any(Function)
      );
    });
  });

  it('subscribeForSportCompetitionChanges', () => {
    const sportId = 'SID';
    const topLevelType = 'TLT';
    let markerSelector = '';
    service.subscribe = jasmine.createSpy();

    service.subscribeForSportCompetitionChanges(sportId, topLevelType, markerSelector, () => { });
    expect(service.subscribe).toHaveBeenCalledWith(
      `${SUBSCRIBE_MESSAGES.COMPETITION_CHANGE}::${sportId}::${topLevelType}`,
      jasmine.any(Function)
    );

    markerSelector = 'MS';
    service.subscribeForSportCompetitionChanges(sportId, topLevelType, markerSelector, () => { });
    expect(service.subscribe).toHaveBeenCalledWith(
      `${SUBSCRIBE_MESSAGES.COMPETITION_CHANGE}::${sportId}::${topLevelType}::${markerSelector}`,
      jasmine.any(Function)
    );
  });

  it('unsubscribeForSportCompetitionChanges', () => {
    const sportId = 'SID';
    const topLevelType = 'TLT';
    let markerSelector = '';
    service.unSubscribe = jasmine.createSpy();

    service.unsubscribeForSportCompetitionChanges(sportId, topLevelType, markerSelector);
    expect(service.unSubscribe).toHaveBeenCalledWith(
      `${SUBSCRIBE_MESSAGES.COMPETITION_CHANGE}::${sportId}::${topLevelType}`
    );

    markerSelector = 'MS';
    service.unsubscribeForSportCompetitionChanges(sportId, topLevelType, markerSelector);
    expect(service.unSubscribe).toHaveBeenCalledWith(
      `${SUBSCRIBE_MESSAGES.COMPETITION_CHANGE}::${sportId}::${topLevelType}::${markerSelector}`
    );
  });

  it('unsubscribe4RibbonUpdates', () => {
    service.unSubscribe = jasmine.createSpy();
    service.unsubscribe4RibbonUpdates();
    expect(service.unSubscribe).toHaveBeenCalledWith(SUBSCRIBE_MESSAGES.RIBBON_CHANGE);
  });

  it('unsubscribeForStructureUpdates', () => {
    service.unSubscribe = jasmine.createSpy();
    service.unsubscribeForStructureUpdates();
    expect(service.unSubscribe).toHaveBeenCalledWith(SUBSCRIBE_MESSAGES.STRUCTURE_CHANGE);
  });

  it('unsubscribe4VRLiveEventUpdates', () => {
    service.unSubscribe = jasmine.createSpy();
    service.unsubscribe4VRLiveEventUpdates();
    expect(service.unSubscribe).toHaveBeenCalledWith(SUBSCRIBE_MESSAGES.VIRTUALS_CHANGE);
  });

  it('subscribe', () => {
    const eventName = 'EN';
    const handler = () => { };

    service.subscribe(eventName, handler);

    expect(service.wsEventsHandlers[eventName]).toEqual(jasmine.any(Array));
    expect(service.wsEventsHandlers[eventName][0]).toBe(handler);
    expect(inPlayConnectionService.addEventListener).toHaveBeenCalledWith(eventName, handler);
    expect(inPlayConnectionService.emitSocket).toHaveBeenCalledWith(SUBSCRIBE_MESSAGES.SUBSCRIBE, eventName);
  });

  it('subscribe with exist eventName', () => {
    const eventName = 'EN';
    const handler = () => { };
    service.wsEventsHandlers[eventName] = [1, 2] as any;

    service.subscribe(eventName, handler);

    expect(service.wsEventsHandlers[eventName].length).toEqual(3);
    expect(service.wsEventsHandlers[eventName][2]).toBe(handler);
    expect(inPlayConnectionService.addEventListener).toHaveBeenCalledWith(eventName, handler);
    expect(inPlayConnectionService.emitSocket).toHaveBeenCalledWith(SUBSCRIBE_MESSAGES.SUBSCRIBE, eventName);
  });

  it('unSubscribe', () => {
    const eventName = 'EN';
    const handler = [() => { }];
    service.wsEventsHandlers[eventName] = handler;

    service.unSubscribe(eventName);

    expect(inPlayConnectionService.removeEventListener).toHaveBeenCalledWith(
      eventName, handler
    );
    expect(inPlayConnectionService.emitSocket).toHaveBeenCalledWith(
      SUBSCRIBE_MESSAGES.UNSUBSCRIBE, eventName
    );
    expect(service.wsEventsHandlers[eventName]).toBeUndefined();
  });

  it('should not unSubscribe', () => {
    const eventName = 'EN';
    service.wsEventsHandlers[eventName] = null;

    service.unSubscribe(eventName);

    expect(inPlayConnectionService.removeEventListener).not.toHaveBeenCalled();
    expect(inPlayConnectionService.emitSocket).not.toHaveBeenCalled();
  });

  it('clearAllListeners', () => {
    service.wsEventsHandlers['EVENT'] = [() => { }];
    service.clearAllListeners();
    expect(service.wsEventsHandlers).toEqual({});
  });

  describe('subscribe4VirtualsUpdates', () => {
    it('subscribe4VirtualsUpdates', () => {
      service.wsEventsHandlers = {GET_VIRTUAL_SPORTS_RIBBON: [1,2] as any}
      service.subscribe4VirtualsUpdates()
    })
    it('subscribe4VirtualsUpdates', () => {
      service.wsEventsHandlers = {GET_VIRTUAL_SPORTS_RIBBON: [] as any}
      service.subscribe4VirtualsUpdates()
      service.wsEventsHandlers.GET_VIRTUAL_SPORTS_RIBBON[0]()
    })
  })
});
