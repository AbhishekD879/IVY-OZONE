import { of as observableOf, throwError } from 'rxjs';

import { InplayMainService } from './inplay-main.service';

describe('InplayMainService', () => {
  let service: InplayMainService;

  let route;
  let router;
  let location;

  let pubSubService;
  let inPlayDataService;
  let inPlayStorageService;
  let inPlaySubscriptionManagerService;
  let timeSyncService;
  let liveEventClockProviderService;
  let cashOutLabelService;
  let userService;
  let storageService;
  let cmsService;
  let windowRefService;
  let isPropertyAvailableService;
  let commentsService;
  let routingStateService, getSportInstanceService, germanSupportInPlayService;
  const getSportError = false;
  const ribbonData = {
    items: [
      { id: 1, categoryId: 19 }, // GH
      { id: 2, categoryId: 21 }, // HR
      { id: 3, categoryId: 161 }, // INT Tote
      { id: 4, categoryId: 16 }, // football
    ]
  };


  beforeEach(() => {
    route = {
      snapshot: {}
    };

    router = {
      navigateByUrl: jasmine.createSpy()
    };

    location = {
      path: jasmine.createSpy()
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      API: {
        EVENT_COUNT: 'EVENT_COUNT',
        WS_EVENT_LIVE_UPDATE: 'WS_EVENT_LIVE_UPDATE'
      }
    };

    inPlayDataService = {
      loadData: jasmine.createSpy('loadData').and.returnValue(observableOf([1, 2, 3]))
    };

    inPlayStorageService = {
      isOutdatedRibbon: jasmine.createSpy('isOutdatedRibbon'),
      isOutdatedStructure: jasmine.createSpy().and.returnValue(false),
      initSportsCache: jasmine.createSpy(),
      ribbonCache: {},
      structureCache: {},
      cacheStructure: jasmine.createSpy(),
      addCompetition: jasmine.createSpy(),
      removeCompetition: jasmine.createSpy(),
      getSportCompetition: jasmine.createSpy(),
      storeSport: jasmine.createSpy('storeSport'),
      clearLink: jasmine.createSpy('clearLink'),
      cacheRibbon: jasmine.createSpy('cacheRibbon')
    };

    inPlaySubscriptionManagerService = {
      subscribe4RibbonUpdates: jasmine.createSpy('subscribe4RibbonUpdates'),
      unsubscribe4RibbonUpdates: jasmine.createSpy(),
      subscribeForStructureUpdates: jasmine.createSpy(),
      unsubscribeForStructureUpdates: jasmine.createSpy(),
      subscribeForLiveUpdates: jasmine.createSpy(),
      unsubscribeForLiveUpdates: jasmine.createSpy(),
      unsubscribeForSportCompetitionChanges: jasmine.createSpy(),
      subscribeForSportCompetitionChanges: jasmine.createSpy('subscribeForSportCompetitionChanges')
    };

    timeSyncService = {
      getTimeDelta: jasmine.createSpy()
    };

    liveEventClockProviderService = {
      create: jasmine.createSpy()
    };

    cashOutLabelService = {
      checkCondition: jasmine.createSpy()
    };

    isPropertyAvailableService = {
      isPropertyAvailable: jasmine.createSpy().and.returnValue(() => { })
    };

    userService = {
      status: true,
      username: 'user1'
    };

    storageService = {
      set: jasmine.createSpy(),
      remove: jasmine.createSpy()
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig')
    };

    windowRefService = {
      nativeWindow: {
        location: {
          search: ''
        }
      }
    };

    getSportInstanceService = {
      getSport: jasmine.createSpy().and.callFake(() => {
        return getSportError ? throwError({}) :
          observableOf({
            config: {
              tier: 1
            }
          });
      })
    };

    commentsService = {};

    routingStateService = {
      getRouteParam: jasmine.createSpy(),
      getPathName: jasmine.createSpy().and.returnValue('football')
    };

    germanSupportInPlayService = {
      getGeFilteredRibbonItemsForInPlay: jasmine.createSpy().and.returnValue(ribbonData),
      getGeFilteredRibbonItems: jasmine.createSpy().and.returnValue(ribbonData),
      applyFiltersToStructureData: jasmine.createSpy().and.returnValue(ribbonData),
      isNewUserFromOtherCountry: jasmine.createSpy().and.returnValue(ribbonData)
    };

    service = new InplayMainService(
      pubSubService,
      inPlayDataService,
      inPlayStorageService,
      inPlaySubscriptionManagerService,
      timeSyncService,
      liveEventClockProviderService,
      cashOutLabelService,
      location,
      userService,
      storageService,
      cmsService,
      windowRefService,
      isPropertyAvailableService,
      commentsService,
      router,
      routingStateService,
      route,
      getSportInstanceService,
      germanSupportInPlayService
    );
  });

  it('#getFiltersForRibbonData - should run german support filters for Ribbon and run inherited filters from baseClass', () => {
    const [fnInCurrentServiceNo1, ...baseServiceFunctions] = service['getFiltersForRibbonData']();

    expect(fnInCurrentServiceNo1 === service['getGeFilteredRibbonItemsForInPlay']).toBeTruthy();
    expect(baseServiceFunctions.length).toEqual(1);

    baseServiceFunctions.forEach(baseServiceFn => {
      expect(typeof baseServiceFn === 'function').toBeTruthy();
    });
  });

  it('#getStructureDataModifiers - should run german support filters for StructureData and run inherited filters from baseClass', () => {
    const [fnInCurrentServiceNo1, ...baseServiceFunctions] = service['getStructureDataModifiers']();

    expect(fnInCurrentServiceNo1 === service['applyFiltersToStructureData']).toBeTruthy();
    expect(baseServiceFunctions.length).toEqual(2);

    baseServiceFunctions.forEach(baseServiceFn => {
      expect(typeof baseServiceFn === 'function').toBeTruthy();
    });
  });

  it(`#getLiveStreamStructureDataModifiers - should run german support filters for LiveStreamStructure and run inherited
      filters from baseClass`, () => {
    const [fnInCurrentServiceNo1, ...baseServiceFunctions] = service['getLiveStreamStructureDataModifiers']();

    expect(fnInCurrentServiceNo1 === service['applyFiltersToStructureData']).toBeTruthy();
    expect(baseServiceFunctions.length).toEqual(2);

    baseServiceFunctions.forEach(baseServiceFn => {
      expect(typeof baseServiceFn === 'function').toBeTruthy();
    });
  });

});
