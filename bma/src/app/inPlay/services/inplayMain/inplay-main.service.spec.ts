import * as _ from 'underscore';
import { of as observableOf, Observable, throwError, Subject } from 'rxjs';
import { fakeAsync, flush, tick } from '@angular/core/testing';
import { delay } from 'rxjs/operators';

import { InplayMainService } from './inplay-main.service';
import { IInplayAllSports } from '@app/inPlay/models/inplay-all-sports.model';
import { watchLiveItem } from '@app/inPlay/constants/watch-live-ribbon.constant';
import { EVENT_TYPES } from '@app/inPlay/constants/event-types.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import * as env from '@environment/oxygenEnvConfig';

describe('InplayMainService', () => {
  const environment = env as any;
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
  let routingStateService, getSportInstanceService,
    getSportError = false;

  let ribbonCacheData;

  beforeEach(() => {
    ribbonCacheData = {
      data: [{
        alt: 'alt',
        categoryId: 10,
        disabled: false,
        hasLiveNow: false,
        hasLiveStream: false,
        targetUriCopy: 'allsports'
      }, {
        alt: 'alt',
        categoryId: 12,
        disabled: false,
        hasLiveNow: false,
        hasLiveStream: false,
        targetUriCopy: 'tennis'
      }, {
        alt: 'alt2',
        categoryId: 14,
        disabled: false,
        hasLiveNow: false,
        hasLiveStream: false,
        targetUriCopy: 'football'
      }],
      lastUpdated: 0
    } as any;

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
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      API: {
        EVENT_COUNT: 'EVENT_COUNT',
        WS_EVENT_LIVE_UPDATE: 'WS_EVENT_LIVE_UPDATE',
        WS_EVENT_UPDATE: 'WS_EVENT_UPDATE',
        INPLAY_COMPETITION_REMOVED: 'INPLAY_COMPETITION_REMOVED',
        INPLAY_DATA_RELOADED: 'INPLAY_DATA_RELOADED',
        EVENT_BY_SPORTS_CHANNEL: 'EVENT_BY_SPORTS_CHANNEL'
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
      resetCompetitionEvents: jasmine.createSpy(),
      getSportCompetition: jasmine.createSpy(),
      storeSport: jasmine.createSpy('storeSport'),
      clearLink: jasmine.createSpy('clearLink'),
      cacheRibbon: jasmine.createSpy('cacheRibbon'),
      removeEvents: jasmine.createSpy('removeEvents')
    };

    inPlaySubscriptionManagerService = {
      subscribe4RibbonUpdates: jasmine.createSpy('subscribe4RibbonUpdates'),
      unsubscribe4RibbonUpdates: jasmine.createSpy(),
      unsubscribe4VRLiveEventUpdates:jasmine.createSpy('unsubscribe4VRLiveEventUpdates'),
      subscribeForStructureUpdates: jasmine.createSpy(),
      unsubscribeForStructureUpdates: jasmine.createSpy(),
      subscribeForLiveUpdates: jasmine.createSpy(),
      unsubscribeForLiveUpdates: jasmine.createSpy(),
      unsubscribeForSportCompetitionChanges: jasmine.createSpy(),
      subscribeForSportCompetitionChanges: jasmine.createSpy('subscribeForSportCompetitionChanges'),
      subscribe4VirtualsUpdates: jasmine.createSpy()
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
      getSportInstanceService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('isCashoutAvailable', () => {
    expect(service.isCashoutAvailable(null)).toBeFalsy();

    service.isCashoutAvailable([]);
    expect(isPropertyAvailableService.isPropertyAvailable).toHaveBeenCalled();
  });

  describe('getSportId', () => {
    let result;
    let ribbonCache;

    beforeEach(() => {
      ribbonCache = {
        data: [{
          targetUriCopy: 'targetUriCopy',
          categoryId: 1
        }, {
          targetUriCopy: 'targetUriCopy2',
          categoryId: 2
        }]
      };
    });

    it('getSportId', (done: DoneFn) => {
      const ribbonItemMock = {
        targetUriCopy: 'targetUriCopy2',
        categoryId: 2
      };
      service['_getRibbon'] = jasmine.createSpy('_getRibbon').and.returnValue(observableOf(ribbonCache));
      spyOn(_, 'findWhere').and.returnValue(ribbonItemMock);
      result = service.getSportId('targetUriCopy2');
      result.subscribe(() => {
        done();
        expect(inPlayStorageService.clearLink).toHaveBeenCalledWith(jasmine.anything());
        expect(inPlayStorageService.clearLink).toHaveBeenCalledTimes(2);
        expect(_.findWhere).toHaveBeenCalledWith(ribbonCache.data, { targetUriCopy: 'targetUriCopy2' });
      });
      expect(result).toEqual(jasmine.any(Observable));
      expect(service['_getRibbon']).toHaveBeenCalled();
    });
  });

  it('initSportsCache', () => {
    service.initSportsCache();
    expect(inPlayStorageService.initSportsCache).toHaveBeenCalled();
  });

  it('setSportUri', () => {
    location.path = jasmine.createSpy().and.returnValue('/in-play');

    service.setSportUri('/');
    expect(location.path).toHaveBeenCalled();
    expect(storageService.set).toHaveBeenCalledWith(`inPlay-${userService.username}`, '/');

    service.setSportUri(null);
    expect(location.path).toHaveBeenCalled();
    expect(storageService.remove).toHaveBeenCalledWith(`inPlay-${userService.username}`);
  });

  it('getSportUri', () => {
    storageService.get = jasmine.createSpy().and.returnValue('football');
    expect(service.getSportUri()).toEqual('football');
    expect(storageService.get).toHaveBeenCalledWith(`inPlay-${userService.username}`);

    userService.status = false;
    expect(service.getSportUri()).toEqual('');
  });

  it('#getFiltersForRibbonData - should run filters for Ribbon', () => {
    expect(service['getFiltersForRibbonData']()[0] === service['filterAllSportsRibbonItems']).toBeTruthy();
    expect(service['getFiltersForRibbonData']().length).toEqual(1);
  });

  it('#getStructureDataModifiers - should run filters for StructureData', () => {
    expect(service['getStructureDataModifiers']()[0] === service['_filterShowInPlay']).toBeTruthy();
    expect(service['getStructureDataModifiers']()[1] === service['_addExpandProperties']).toBeTruthy();
    expect(service['getStructureDataModifiers']().length).toEqual(2);
  });

  it('#getLiveStreamStructureDataModifiers - should run filters for LiveStreamStructure', () => {
    expect(service['getLiveStreamStructureDataModifiers']()[0] === service['filterLiveStreamInPlay']).toBeTruthy();
    expect(service['getLiveStreamStructureDataModifiers']()[1] === service['addExpandLiveStream']).toBeTruthy();
    expect(service['getLiveStreamStructureDataModifiers']().length).toEqual(2);
  });

  describe('#addRibbonURLHandler', () => {
    beforeEach(() => {
      service['_getRibbon'] = jasmine.createSpy('_getRibbon').and.returnValue(observableOf(ribbonCacheData));
    });

    it('should navigate to last remember sport', fakeAsync(() => {
      storageService.get = jasmine.createSpy().and.returnValue('football');
      service.addRibbonURLHandler();
      tick(200);
      expect(router.navigateByUrl).toHaveBeenCalledWith('/in-play/football');
    }));

    it('should navigate to first sport', fakeAsync(() => {
      userService.status = false;
      service.addRibbonURLHandler();
      tick(200);
      expect(router.navigateByUrl).toHaveBeenCalledWith('/in-play/tennis');
    }));
  });

  describe('getRibbonData', () => {
    beforeEach(() => {
      service['_getRibbon'] = jasmine.createSpy('_getRibbon').and.returnValue(observableOf(ribbonCacheData));
      cmsService.getSystemConfig.and.returnValue(observableOf({
        InPlayWatchLive: {
          enabled: false
        }
      }));
    });

    describe('watchlive is enabled', () => {
      beforeEach(() => {
        cmsService.getSystemConfig.and.returnValue(observableOf({
          InPlayWatchLive: {
            enabled: true
          }
        }));

        inPlayStorageService.ribbonCache = ribbonCacheData;
      });

      it('isOutdatedRibbon = true', (done: DoneFn) => {
        service.getRibbonData().subscribe(() => {
          done();
        });
        expect(inPlaySubscriptionManagerService.subscribe4RibbonUpdates).toHaveBeenCalled();
        expect(inPlayStorageService.ribbonCache).toEqual(ribbonCacheData);
      });

      it(`should Not remove all sports if removeAllSportsItem equal false`, () => {
        service.getRibbonData(false).subscribe((res) => {
          expect(res.data.find(el => el.targetUriCopy === 'allsports')).toBeTruthy();
        });
      });

      it(`should remove all sports by default`, () => {
        service.getRibbonData().subscribe((res) => {
          expect(res.data.find(el => el.targetUriCopy === 'allsports')).toBeFalsy();
        });
      });

      it(`should add watchlive`, () => {
        service.getRibbonData().subscribe((res) => {
          // expect(res.data[0].targetUriCopy).toEqual('watchlive');
        });
      });
    });

    it('watchlive is not added: isOutdatedRibbon = true, watchlive item is already present', fakeAsync(() => {
      ribbonCacheData.data.unshift(watchLiveItem);
      inPlayStorageService.ribbonCache = ribbonCacheData;
      service.getRibbonData();

      expect(inPlayStorageService.ribbonCache).toEqual(ribbonCacheData);
    }));

    it('watchlive is not added: isOutdatedRibbon = true, watchlive feature is disabled', fakeAsync(() => {
      inPlayStorageService.ribbonCache = ribbonCacheData;
      service.getRibbonData();

      expect(inPlayStorageService.ribbonCache).toEqual(ribbonCacheData);
    }));
  });
  it('unsubscribeForUpdates', () => {
    service['isWidgetEnabled'] = false;
    service.unsubscribeForUpdates();
    expect(inPlaySubscriptionManagerService.unsubscribe4RibbonUpdates).toHaveBeenCalled();
    expect(inPlaySubscriptionManagerService.unsubscribeForStructureUpdates).toHaveBeenCalled();
  });

  it('unsubscribe4VRLiveEventUpdates', () => {
    service.unsubscribeForVRUpdates();
    expect(inPlaySubscriptionManagerService.unsubscribe4VRLiveEventUpdates).toHaveBeenCalled();
  });

  describe('getLiveStreamStructureData', () => {
    it('getLiveStreamStructureData with useCache', () => {
      service['getLiveStreamStructure'] = jasmine.createSpy().and.returnValue(observableOf(null));
      service.getLiveStreamStructureData(true);

      expect(inPlayStorageService.isOutdatedStructure).toHaveBeenCalled();
      expect(service['getLiveStreamStructure']).not.toHaveBeenCalled();
      expect(inPlaySubscriptionManagerService.subscribeForStructureUpdates).toHaveBeenCalledWith(true);
    });

    it('getLiveStreamStructureData without useCache', () => {
      service['getLiveStreamStructure'] = jasmine.createSpy().and.returnValue(observableOf(null));
      service.getLiveStreamStructureData(false);

      expect(service['getLiveStreamStructure']).toHaveBeenCalled();
    });
  });

  describe('#getStructureData', () => {
    it('for not outdated structure', () => {
      service['_getStructure'] = jasmine.createSpy().and.returnValue(observableOf(null));
      expect(service.getStructureData()).toEqual(jasmine.any(Observable));
      expect(service['_getStructure']).toHaveBeenCalled();
      expect(service.getStructureData(true)).toEqual(jasmine.any(Observable));
      expect(inPlaySubscriptionManagerService.subscribeForStructureUpdates).toHaveBeenCalled();
    });
    it('for outdated structure', () => {
      inPlayStorageService.isOutdatedStructure = jasmine.createSpy().and.returnValue(true);
      service['_getStructure'] = jasmine.createSpy().and.returnValue(observableOf({}));
      service.getStructureData().subscribe();
      expect(service['_getStructure']).toHaveBeenCalledWith(false);
      expect(inPlayStorageService.cacheStructure).toHaveBeenCalled();
      expect(inPlaySubscriptionManagerService.subscribeForStructureUpdates).toHaveBeenCalled();
    });
    it('should expand upcomming', () => {
      service['_getStructure'] = jasmine.createSpy().and.returnValue(observableOf({}));
      service.getStructureData(false, true).subscribe();
      expect(service['_getStructure']).toHaveBeenCalledWith(true);
    });
  });

  it('getTopLevelTypeParameter', () => {
    expect(service.getTopLevelTypeParameter('upcoming')).toEqual('UPCOMING_EVENT');
    expect(service.getTopLevelTypeParameter('other')).toEqual('LIVE_EVENT');
  });

  it('getExpandedLeaguesCount', () => {
    service.expandedLeaguesCount = 0;
    cmsService.getSystemConfig.and.returnValue(observableOf({}));
    expect(service.getExpandedLeaguesCount()).toEqual(jasmine.any(Observable));

    service.expandedLeaguesCount = 1;
    expect(service.getExpandedLeaguesCount()).toEqual(jasmine.any(Observable));
    expect(cmsService.getSystemConfig).toHaveBeenCalledWith(null);
  });

  describe('getSportData', () => {
    beforeEach(() => {
      cmsService.getSystemConfig.and.returnValue(observableOf({}));
    });

    describe('general flow', () => {
      const params = {};
      const sportData = {
        eventsByTypeName: [{}]
      };
      beforeEach(() => {
        service['_getSport'] = jasmine.createSpy('_getSport').and.returnValue(observableOf(sportData));
        service['_addLiveUpdatesHandler'] = jasmine.createSpy('_addLiveUpdatesHandler');
        service.initialSubscribeForMultipleCompetitions = jasmine.createSpy('initialSubscribeForMultipleCompetitions')
          .and.returnValue(observableOf(sportData));
      });

      it('should get competition events and subscribe', (done: DoneFn) => {
        const result = service.getSportData(params, false, false, true,true);
        result.subscribe(() => {
          done();
          expect(params['emptyTypes']).toEqual('Yes');
          expect(params['autoUpdates']).toEqual('No');
          expect(params['topLevelType']).toEqual('UPCOMING_EVENT');
          expect(service['_getSport']).toHaveBeenCalledWith(params);
          expect(service.initialSubscribeForMultipleCompetitions).toHaveBeenCalledWith(jasmine.anything(), params, false,true);
        });
        expect(result).toEqual(jasmine.any(Observable));
      });

      it('should not get competition events and subscribe', (done: DoneFn) => {
        const result = service.getSportData(params, false, false, false);
        result.subscribe(() => {
          done();
          expect(service.initialSubscribeForMultipleCompetitions).not.toHaveBeenCalledWith(jasmine.anything(), params, false);
        });
        expect(result).toEqual(jasmine.any(Observable));
        expect(inPlayStorageService.storeSport).toHaveBeenCalledWith(params,sportData);
      });
      it('should call _addLiveUpdatesHandler and make isLiveUpdatesHandlerAdded', (done: DoneFn) => {
        service.isLiveUpdatesHandlerAdded = false;
        const result = service.getSportData(params, false, false, false);
        result.subscribe(() => {
          done();
          expect(service.initialSubscribeForMultipleCompetitions).not.toHaveBeenCalledWith(jasmine.anything(), params, false);
        });
        expect(service.isLiveUpdatesHandlerAdded).toBeTrue();
        expect(service['_addLiveUpdatesHandler']).toHaveBeenCalled();
      });
      it('should not call _addLiveUpdatesHandler and make isLiveUpdatesHandlerAdded', (done: DoneFn) => {
        service.isLiveUpdatesHandlerAdded = true
        const result = service.getSportData(params, false, false, false);
        result.subscribe(() => {
          done();
          expect(service.initialSubscribeForMultipleCompetitions).not.toHaveBeenCalledWith(jasmine.anything(), params, false);
        });
        expect(service['_addLiveUpdatesHandler']).not.toHaveBeenCalled();
      });
    });

    it('isLiveNowType', () => {
      const params = {
        isLiveNowType: true
      };
      service.getSportData(params);

      expect(params['topLevelType']).toEqual('LIVE_EVENT');
    });

    it('RequestParamsWithTennisId', () => {
      const params = {
        topLevelType: 'STREAM_EVENT',
        categoryId: '34',
        isLiveNowType:true
      };
      environment.CATEGORIES_DATA = { tierOne: ['34', '16'] };
      service.getSportData(params);
      expect(params['marketSelector']).toEqual('Main Market');
    });
    it('RequestParamsWithTennisId when marketSelector has value', () => {
      const params = {
        topLevelType: 'STREAM_EVENT',
        categoryId: '34',
        isLiveNowType:true,
        marketSelector: 'someValue'
      };
      environment.CATEGORIES_DATA = { tierOne: ['34', '16'] };
      service.getSportData(params);
      expect(params['marketSelector']).toEqual('someValue');
    });
    it('RequestParamsWithTennisId when category is not tierone', () => {
      const params = {
        topLevelType: 'STREAM_EVENT',
        categoryId: '14',
        isLiveNowType:true
      };
      environment.CATEGORIES_DATA = { tierOne: ['34', '16'] };
      service.getSportData(params);
      expect(params['marketSelector']).toEqual(undefined);
    });
    it('RequestParamsWithTennisId when isLiveNowType is false', () => {
      const params = {
        topLevelType: 'STREAM_EVENT',
        categoryId: '34',
        isLiveNowType:false
      };
      environment.CATEGORIES_DATA = { tierOne: ['34', '16'] };
      service.getSportData(params);
      expect(params['marketSelector']).toEqual(undefined);
    });
    it('isStreamEventType', () => {
      const params = {
        topLevelType: 'STREAM_EVENT'
      };
      service.getSportData(params);

      expect(params['topLevelType']).toEqual('STREAM_EVENT');
      expect(params['isLiveNowType']).not.toBeDefined();
    });

    it('isUpcomingType', () => {
      const params = {
        isLiveNowType: false
      };
      service.getSportData(params);

      expect(params['topLevelType']).toEqual('UPCOMING_EVENT');
    });

    it(`should subscribe For Sport Competition Changes`, fakeAsync(() => {
      const params = { topLevelType: EVENT_TYPES.LIVE_EVENT };

      spyOn(service as any, '_getSport').and.returnValue(observableOf({ eventsByTypeName: [] }));

      service.getSportData(params).subscribe(() => {
        expect(service['inPlaySubscriptionManagerService'].subscribeForSportCompetitionChanges).toHaveBeenCalled();
      });

      flush();
    }));

    it(`should return sportData with 'categoryId' and 'topLevelType' if sportData do Not have them`, fakeAsync(() => {
      const requestParams = {
        categoryId: '13',
        topLevelType: EVENT_TYPES.UPCOMING_EVENT
      };

      spyOn(service as any, '_getSport').and.returnValue(observableOf({ eventsByTypeName: [] }));

      service.getSportData(requestParams).subscribe((data) => {
        expect(data).toEqual(jasmine.objectContaining({ categoryId: '13', topLevelType: EVENT_TYPES.UPCOMING_EVENT }));
      });

      flush();
    }));

    it(`should return sportData with 'categoryId' and 'topLevelType'`, fakeAsync(() => {
      const sportData = {
        categoryId: '13',
        topLevelType: EVENT_TYPES.UPCOMING_EVENT
      };

      service.expandedLeaguesCount = 0;
      spyOn(service as any, '_getSport').and.returnValue(observableOf({ eventsByTypeName: [sportData] }));

      service.getSportData({}).subscribe((data) => {
        expect(data).toEqual(jasmine.objectContaining({
          eventsByTypeName: [{ categoryId: '13', topLevelType: EVENT_TYPES.UPCOMING_EVENT }]
        } as any));
      });

      flush();
    }));
  });

  describe('initialSubscribeForMultipleCompetitions', () => {
    let sportData, events, params;

    beforeEach(() => {
      sportData = {
        eventsByTypeName: [
          {}, {}
        ]
      };

      events = [{ id: 1 }, { id: 2 }];

      params = { marketSelector: '->' };

      service.expandedLeaguesCount = 2;
      service['_getCompetitionData'] = jasmine.createSpy('_getCompetitionData').and.returnValue(observableOf(events));
    });
    it('should call subscribeForLiveUpdates', fakeAsync(() => {
      const result = service.initialSubscribeForMultipleCompetitions(sportData, params, true);
      result.subscribe();
      tick();
      expect(inPlaySubscriptionManagerService.subscribeForLiveUpdates).toHaveBeenCalledWith([1, 2]);
      expect(service['_getCompetitionData']).toHaveBeenCalledTimes(2);
      expect(result).toEqual(jasmine.any(Observable));
      sportData.eventsByTypeName.forEach(
        item => expect(item.marketSelector).toBe(params.marketSelector)
      );
    }));

    it('should not call subscribeForLiveUpdates', fakeAsync(() => {
      const result = service.initialSubscribeForMultipleCompetitions(sportData, params, false);
      result.subscribe();
      tick();
      expect(inPlaySubscriptionManagerService.subscribeForLiveUpdates).not.toHaveBeenCalled();
      expect(service['_getCompetitionData']).toHaveBeenCalledTimes(2);
      expect(result).toEqual(jasmine.any(Observable));
      sportData.eventsByTypeName.forEach(
        item => expect(item.marketSelector).toBe(params.marketSelector)
      );
    }));

    it('should not call subscribeForLiveUpdates', fakeAsync(() => {
      const callbackFn = jasmine.createSpy('callbackFn');
      service.expandedLeaguesCount = 0;

      service.initialSubscribeForMultipleCompetitions(sportData, params, false).subscribe(callbackFn);
      tick();

      expect(callbackFn).toHaveBeenCalledWith(sportData);
      expect(inPlayDataService.loadData).not.toHaveBeenCalled();
      expect(inPlaySubscriptionManagerService.subscribeForLiveUpdates).not.toHaveBeenCalled();
    }));
    it('should push data to HREvents if isFetch is true', fakeAsync(() => {
      sportData = {
        eventsByTypeName: [
          { events: [{ eventEntity: { startTime: '1:00' } }, { eventEntity: { startTime: '2:00' } }] }
        ]
      };
      const result = service.initialSubscribeForMultipleCompetitions(sportData, params, true, true);
      result.subscribe();
      tick();
      expect(result).toEqual(jasmine.any(Observable));
    }));
  });

  describe('subscribeForUpdates', () => {
    it('should subscribe For Updates', () => {
      const events: any[] = [{ id: 1 }, { id: 2 }];
      service.subscribeForUpdates(events);
      expect(inPlaySubscriptionManagerService.subscribeForLiveUpdates).toHaveBeenCalledWith(
        events.map(i => i.id)
      );
    });

    it(`should Not subscribe For Updates `, () => {
      service.subscribeForUpdates(undefined);
      expect(inPlaySubscriptionManagerService.subscribeForLiveUpdates).not.toHaveBeenCalled();
    });
  });

  describe('unsubscribeForSportCompetitionUpdates', () => {
    it('unsubscribeForSportCompetitionUpdates', () => {
      const data: any = { categoryId: 1, topLevelType: 'FF', eventsIds: [1, 2] };
      service.unsubscribeForSportCompetitionUpdates(data);

      expect(inPlaySubscriptionManagerService.unsubscribeForSportCompetitionChanges)
        .toHaveBeenCalledWith(data.categoryId, data.topLevelType);

      expect(inPlayStorageService.removeEvents).toHaveBeenCalledWith(data.eventsIds);
    });

    it('unsubscribeForSportCompetitionUpdates eventsIds is missed in sportData', () => {
      const data: any = { categoryId: 1, topLevelType: 'FF'};
      service.unsubscribeForSportCompetitionUpdates(data);

      expect(inPlaySubscriptionManagerService.unsubscribeForSportCompetitionChanges)
        .toHaveBeenCalledWith(data.categoryId, data.topLevelType);
      expect(inPlayStorageService.removeEvents).not.toHaveBeenCalled();
    });
    it('should not fail in edge case', () => {
      service.unsubscribeForSportCompetitionUpdates(undefined as any);
    });
  });

  it('unsubscribeForEventsUpdates when there are eventsIds', () => {
    const data: any = { eventsIds: [1, 2, 3] };
    service.unsubscribeForEventsUpdates(data);

    expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalledWith(data.eventsIds);
    expect(inPlayStorageService.removeEvents).toHaveBeenCalledWith(data.eventsIds);
  });

  it('unsubscribeForEventsUpdates when there are eventsIds and not clear storage', () => {
    const data: any = { eventsIds: [1, 2, 3] };
    service.unsubscribeForEventsUpdates(data, false);

    expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalledWith(data.eventsIds);
    expect(inPlayStorageService.removeEvents).not.toHaveBeenCalled();
  });

  it('unsubscribeForEventsUpdates when there are no eventsIds', () => {
    const data: any = {};
    service.unsubscribeForEventsUpdates(data);

    expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).not.toHaveBeenCalled();
    expect(inPlayStorageService.removeEvents).not.toHaveBeenCalled();
  });

  it('clearDeletedEventFromSport', () => {
    const data: any = {
      EA: { eventsIds: [1], eventsBySports: [{ eventsByTypeName: [{}, {}], eventsIds: ['1', '2'] }] }
    };
    const sport = { eventsByTypeName: [{}, {}], eventsIds: ['1', '2'] };
    spyOn(service, 'getLevelIndex').and.returnValue(0);
    spyOn(service, 'clearDeletedEventFromType');

    service.clearDeletedEventFromSport(data, 1, ['EA']);
    expect(service.getLevelIndex).toHaveBeenCalledWith(data.EA.eventsBySports, 'eventsIds', 1);
    expect(service.clearDeletedEventFromType).toHaveBeenCalledWith(sport as any, 1);
  });
  describe('#unsubscribeForEventUpdates', () => {
    it('unsubscribeForEventsUpdates when there are eventsId', () => {
      const data: any = { id: 1 };
      service.unsubscribeForEventUpdates(data);
      expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalledWith([1]);
      expect(inPlayStorageService.removeEvents).toHaveBeenCalledWith([1]);
    });

    it('unsubscribeForEventsUpdates when there are eventsId and not clear storage', () => {
      const data: any = { id: 1 };
      service.unsubscribeForEventUpdates(data, false);
      expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalledWith([1]);
      expect(inPlayStorageService.removeEvents).not.toHaveBeenCalled();
    });
  });
  describe('#clearDeletedEventFromType', () => {
    it('should call clearDeletedEventFromType method if data present', () => {
      const data: any = {
        eventsByTypeName: {
          '0': { events: [], eventsIds: [1], typeId: 'TID' }
        },
        topLevelType: 'TLP',
        categoryId: 'CID',
        eventsIds: []
      };

      service['unsubscribeAndRemoveCompetition'] = jasmine.createSpy();
      service['_deleteEntity'] = jasmine.createSpy();
      service.getLevelIndex = jasmine.createSpy().and.returnValue(0);

      service.clearDeletedEventFromType(data, 0);
      expect(service.getLevelIndex).toHaveBeenCalledWith(
        data.eventsByTypeName, 'eventsIds', 0
      );
      expect(service['unsubscribeAndRemoveCompetition']).toHaveBeenCalledWith(
        data.topLevelType, data.categoryId, data.eventsByTypeName['0'].typeId
      );
      expect(service.clearDeletedEventFromType(data, 1)).toEqual(undefined);
    });
  });


  it('getLevelIndex', () => {
    const entities: any[] = [
      { 'ppt': 1 },
      { 'sdc': [1, 2, 3] }
    ];
    expect(service.getLevelIndex(entities, 'ppt', 1)).toBe(0);
    expect(service.getLevelIndex(entities, 'sdc', 2)).toBe(1);
    expect(service.getLevelIndex(entities, 'other', 2)).toBe(undefined);
  });

  it('getFilter', () => {
    windowRefService.nativeWindow.location.search = '/';
    routingStateService.getRouteParam.and.returnValue('');
    expect(service.getFilter(['A', 'B'])).toBe('A');
    expect(routingStateService.getRouteParam).toHaveBeenCalledWith('sport', route.snapshot);

    windowRefService.nativeWindow.location.search = '/?tab=InPLay';
    routingStateService.getRouteParam.and.returnValue('inplay');
    expect(service.getFilter(['A', 'B'])).toBe('B');
    expect(routingStateService.getRouteParam).toHaveBeenCalledWith('sport', route.snapshot);
  });

  it('areEventsAvailable', () => {
    const data: any = {};
    const filters = ['F1', 'F2'];
    service['_isEventsInViewAvailable'] = jasmine.createSpy();

    service.areEventsAvailable(data, filters);
    filters.forEach(filter => {
      expect(service['_isEventsInViewAvailable']).toHaveBeenCalledWith(data, filter);
    });
  });

  it('publishEventCount', () => {
    service.publishEventCount('FLR');
    expect(pubSubService.publish).toHaveBeenCalledWith('EVENT_COUNT', 'FLR');
  });

  it('generateSwitchers', () => {
    service['_getEventsCounter'] = jasmine.createSpy().and.returnValue({
      livenow: 2,
      upcoming: 3
    });

    const viewByFilters = ['F', 'S'];
    const data = [];
    const result = service.generateSwitchers(() => { }, viewByFilters, data);

    expect(service['_getEventsCounter']).toHaveBeenCalled();
    expect(result).toEqual([
      {
        onClick: jasmine.any(Function),
        viewByFilters: viewByFilters[0],
        name: 'inplay.byLiveNow',
        eventCount: 2
      },
      {
        onClick: jasmine.any(Function),
        viewByFilters: viewByFilters[1],
        name: 'inplay.byUpcoming',
        eventCount: 3
      }
    ] as any);
  });

  it('saveWidgetState', () => {
    service.saveWidgetState(true);
    expect(service.isWidgetEnabled).toBe(true);

    service.saveWidgetState(false);
    expect(service.isWidgetEnabled).toBe(false);
  });

  it('_getCompetitionData', () => {
    const params: any = {};
    expect(service['_getCompetitionData'](params, '')).toEqual(jasmine.any(Observable));
    expect(inPlayDataService.loadData).toHaveBeenCalledWith('competition', params);
  });

  it('_addLiveUpdatesHandler', () => {
    service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((a, b, cb) => {
      cb(123, 'test');
    });
    service['_handleLiveUpdate'] = jasmine.createSpy();
    service['_addLiveUpdatesHandler']();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'inplayLiveUpdate', 'WS_EVENT_LIVE_UPDATE', jasmine.any(Function)
    );
    expect(service['_handleLiveUpdate']).toHaveBeenCalledWith(123 as any, 'test' as any);
  });

  describe('_getRibbon', () => {
    let result;
    let ribbonData;

    beforeEach(() => {
      ribbonData = { items: [{ id: '1' }, { id: '0', targetUriCopy: 'allsports' }] };
      inPlayDataService.loadData.and.returnValue(observableOf(ribbonData).pipe(delay(0)));
    });

    it(`should Not create new instance if ribbonLoaded$ is defined`, () => {
      const subject$ = new Subject() as any;
      service['ribbonLoaded$'] = subject$;

      service['_getRibbon']();

      expect(service['ribbonLoaded$']).toEqual(subject$);
      subject$.complete();
    });

    it(`should create new instance if ribbonLoaded$ is not defined`, () => {
      inPlayStorageService.isOutdatedRibbon.and.returnValue(true);
      service['ribbonLoaded$'] = undefined;

      service['_getRibbon']();

      expect(inPlayStorageService.cacheRibbon).not.toHaveBeenCalled();
    });

    it(`should create new instance if ribbonLoaded$ isStopped`, () => {
      inPlayStorageService.isOutdatedRibbon.and.returnValue(true);
      service['ribbonLoaded$'] = {
        isStopped: true
      } as any;

      service['_getRibbon']();

      expect(inPlayStorageService.cacheRibbon).not.toHaveBeenCalled();
    });

    describe('should load data from server when isOutdatedRibbon', () => {
      beforeEach(() => {
        inPlayStorageService.isOutdatedRibbon.and.returnValue(true);
      });

      it('the first time if loadDataSubscription is Not defined', fakeAsync(() => {
        service['loadDataSubscription'] = undefined;
      }));

      it('the second time if loadDataSubscription is closed', fakeAsync(() => {
        service['loadDataSubscription'] = { closed: true } as any;
      }));

      afterEach(fakeAsync(() => {
        result = service['_getRibbon']();
        tick();

        expect(service['ribbonLoaded$']).toBeDefined();
        expect(inPlayDataService.loadData).toHaveBeenCalledWith('ribbon', null);
        expect(inPlayStorageService.cacheRibbon).toHaveBeenCalledWith(ribbonData);
        expect(result.constructor.name).toEqual('Observable');
      }));
    });

    describe('should try to load data from server when isOutdatedRibbon', () => {
      beforeEach(() => {
        inPlayStorageService.isOutdatedRibbon.and.returnValue(true);
        inPlayDataService.loadData.and.returnValue(throwError({}));
      });

      it('should load ribbon data from cash when loadData returns error', fakeAsync(() => {
        service['_getRibbon']();
        tick();

        expect(service['ribbonLoaded$']).toBeDefined();
        expect(inPlayDataService.loadData).toHaveBeenCalledWith('ribbon', null);
        expect(inPlayStorageService.cacheRibbon).not.toHaveBeenCalledWith(ribbonData);
        expect(result.constructor.name).toEqual('Observable');
      }));
    });
  });

  it('should call _handleLiveUpdate when event found in storage', () => {
    inPlayStorageService.allEvents = { 1: { id: 1, categoryId: 'CID1' }};
    service['_handleLiveUpdate']('1', {} as any);
    expect(pubSubService.publish).toHaveBeenCalledWith(
      'WS_EVENT_UPDATE', {
      events: [{ id: 1, categoryId: 'CID1' }],
      update: {}
    });
  });

  it('should call _handleLiveUpdate when event not found in storage', () => {
    inPlayStorageService.allEvents = {};
    service['_handleLiveUpdate']('1', {} as any);
    expect(pubSubService.publish).toHaveBeenCalledWith(
      'WS_EVENT_UPDATE', {
      events: [],
      update: {}
    });
  });

  describe('_getStructure', () => {
    it('should call inPlayDataService.loadData', () => {
      service['_getStructure']();
      expect(inPlayDataService.loadData).toHaveBeenCalledWith('structure', null);
    });
    it('should call _addExpandProperties', () => {
      const dataMock = {
        someData: 'someData'
      };
      service['_addExpandProperties'] = jasmine.createSpy();
      inPlayDataService.loadData.and.returnValue(observableOf(dataMock));
      service['_getStructure'](false).subscribe();
      expect(service['_addExpandProperties']).toHaveBeenCalledWith(dataMock as any, undefined, false);
    });
  });

  it('getLiveStreamStructure', () => {
    service['inPlayDataService'].loadData = jasmine.createSpy().and.returnValue(observableOf({
      liveStream: {
        eventCount: 1
      },
      upcomingLiveStream: {
        eventCount: 2
      }
    }));
    service['filterLiveStreamInPlay'] = jasmine.createSpy();
    service['addExpandLiveStream'] = jasmine.createSpy();
    service['getLiveStreamStructure']().subscribe();

    expect(inPlayDataService.loadData).toHaveBeenCalledWith('ls_structure', null);
    expect(service['filterLiveStreamInPlay']).toHaveBeenCalled();
    expect(service['addExpandLiveStream']).toHaveBeenCalled();
  });

  it('_filterShowInPlay', () => {
    const data: any = {
      livenow: {
        eventsBySports: [
          { showInPlay: false },
          { showInPlay: true }
        ]
      },
      upcoming: {
        eventsBySports: [
          { showInPlay: false },
          { showInPlay: true }
        ]
      }
    };

    expect(service['_filterShowInPlay'](data)).toBe(data);
    expect(data.livenow.eventsBySports.length).toBe(1);
    expect(data.upcoming.eventsBySports.length).toBe(1);
  });

  it('filterLiveStreamInPlay', () => {
    const structureData = {
      creationTime: 1,
      generation: 1,
      liveStream: {
        eventCount: 2,
        eventsBySports: [
          { showInPlay: true },
          { showInPlay: false }
        ],
        eventsIds: [1, 2]
      }
    } as IInplayAllSports;
    const expectedResult = {
      creationTime: 1,
      generation: 1,
      liveStream: {
        eventCount: 2,
        eventsBySports: [
          { showInPlay: true }
        ],
        eventsIds: [1, 2]
      }
    } as IInplayAllSports;
    const actualResult = service['filterLiveStreamInPlay'](structureData);

    expect(actualResult).toEqual(expectedResult);
  });

  it('filterLiveStreamInPlay with error', () => {
    const structureData = {
      error: true,
      creationTime: 1,
      generation: 1,
      liveStream: {
        eventCount: 2,
        eventsBySports: [
          { showInPlay: true },
          { showInPlay: false }
        ],
        eventsIds: [1, 2]
      }
    } as any;
    const expectedResult = {
      error: true,
      creationTime: 1,
      generation: 1,
      liveStream: {
        eventCount: 2,
        eventsBySports: [
          { showInPlay: true },
          { showInPlay: false }
        ],
        eventsIds: [1, 2]
      }
    } as any;
    const actualResult = service['filterLiveStreamInPlay'](structureData);

    expect(actualResult).toEqual(expectedResult);
  });

  it('_getSport', fakeAsync(() => {
    service.getExpandedLeaguesCount = jasmine.createSpy().and.returnValue(observableOf({}));
    service['_getSport']({}).subscribe();
    expect(service.getExpandedLeaguesCount).toHaveBeenCalled();
    expect(inPlayDataService.loadData).toHaveBeenCalled();
  }));

  describe('_addExpandProperties', () => {
    it('should expand first accordion for inplay and upcoming', () => {
      const inplayData: any = {
        livenow: {
          eventsBySports: [{}]
        },
        upcoming: {
          eventsBySports: [{}]
        }
      };
      expect(service['_addExpandProperties'](inplayData, undefined, true)).toBe(inplayData);
      expect(inplayData.livenow.eventsBySports[0].isExpanded).toBeTruthy();
      expect(inplayData.upcoming.eventsBySports[0].isExpanded).toBeTruthy();
    });

    it('should expand first accordion for only inplay', () => {
      const inplayData: any = {
        livenow: {
          eventsBySports: [{}]
        },
        upcoming: {
          eventsBySports: [{}]
        }
      };
      expect(service['_addExpandProperties'](inplayData)).toBe(inplayData);
      expect(inplayData.livenow.eventsBySports[0].isExpanded).toBeTruthy();
      expect(inplayData.upcoming.eventsBySports[0].isExpanded).toBeFalsy();
    });

    it('should expand proper leagues count for sports sections', () => {
      const sportsData: any = {
        eventsByTypeName: [{}]
      };
      service.expandedLeaguesCount = 1;
      expect(service['_addExpandProperties'](null, sportsData)).toBe(sportsData);
      expect(sportsData.eventsByTypeName[0].isExpanded).toBeTruthy();
    });

  });

  it('addExpandLiveStream', () => {
    const inplaySructureData = {
      creationTime: 1,
      generation: 1,
      liveStream: {
        eventCount: 2,
        eventsBySports: [
          { showInPlay: true }
        ],
        eventsIds: [1, 2]
      }
    } as IInplayAllSports;
    const expectedResult = {
      creationTime: 1,
      generation: 1,
      liveStream: {
        eventCount: 2,
        eventsBySports: [
          { showInPlay: true, isExpanded: true }
        ],
        eventsIds: [1, 2]
      }
    } as IInplayAllSports;
    const actualResult = service['addExpandLiveStream'](inplaySructureData);

    expect(actualResult).toEqual(expectedResult);
  });

  it('updateCommentsDataFormat', () => {
    commentsService.footballMSInitParse = jasmine.createSpy();
    const events: any[] = [
      { comments: [] },
      { comments: null },
      { comments: [] }
    ];

    expect(service['updateCommentsDataFormat']('football', events)).toBe(events);
    expect(commentsService.footballMSInitParse).toHaveBeenCalledTimes(2);
  });

  it('_addClockData create new clock', () => {
    const events: any[] = [
      { initClock: true },
      { initClock: false },
    ];
    service['_addClockData'](events);
    expect(liveEventClockProviderService.create).toHaveBeenCalledTimes(1);
  });

  it('_deleteEntity', () => {
    const group: any = {
      prop: [1, 2, 3],
      eventsIds: [10, 20, 30]
    };
    service['_deleteEntity'](group, 'prop', 1, 20);
    expect(group.prop).toEqual([1, 3]);
    expect(group.eventsIds).toEqual([10, 30]);
    expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).not.toHaveBeenCalled();
  });

  it('_deleteEntity, unsubscribe from event updates when undisplayed', () => {
    const group: any = {
      events: [{
        id: 20
      }],
      eventsIds: [10, 20, 30]
    };
    const eventIdMock = 20;

    service['_deleteEntity'](group, 'events', 1, eventIdMock);

    expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalledWith([eventIdMock]);
  });

  it('_isEventsInViewAvailable', () => {
    const data: any = {
      'F1': { eventsIds: [] },
      'F2': { eventsIds: [1] }
    };
    expect(service['_isEventsInViewAvailable'](data, 'F1')).toBeFalsy();
    expect(service['_isEventsInViewAvailable'](data, 'F2')).toBeTruthy();
  });

  describe('_getEventsCounter', () => {
    it('football counters', () => {
      const data: any[] = [
        {
          targetUriCopy: 'football',
          liveEventCount: 5,
          upcomingEventCount: 7,
          liveStreamEventCount: 2,
          upcommingLiveStreamEventCount: 3
        }
      ];

      expect(service['_getEventsCounter'](data)).toEqual({
        livenow: '(5)',
        upcoming: '(7)',
        liveStream: '(2)',
        upcomingLiveStream: '(3)'
      });
    });

    it('inplay counters', () => {
      routingStateService.getPathName.and.returnValue('in-play');
      const data: any = [{
        targetUriCopy: 'allsports',
        liveEventCount: 1,
        upcomingEventCount: 2,
        liveStreamEventCount: 3,
        upcommingLiveStreamEventCount: 4
      }];
      expect(service['_getEventsCounter'](data)).toEqual({
        livenow: '(1)',
        upcoming: '(2)',
        liveStream: '(3)',
        upcomingLiveStream: '(4)'
      });
    });

    it('live stream counters', () => {
      routingStateService.getPathName.and.returnValue('live-stream');
      const data: any = [{
        targetUriCopy: 'watchlive',
        liveEventCount: 1,
        upcomingEventCount: 2,
        liveStreamEventCount: 3,
        upcommingLiveStreamEventCount: 4
      }];
      expect(service['_getEventsCounter'](data)).toEqual({
        livenow: '(1)',
        upcoming: '(2)',
        liveStream: '(3)',
        upcomingLiveStream: '(4)'
      });
    });
  });

  describe('handleAddRemoveCompetition', () => {
    const topLevelType = EVENT_TYPES.LIVE_EVENT;
    let websocketData: any;

    beforeEach(() => {
      websocketData = {
        removed: [],
        added: {},
        changed: []
      };
      spyOn(service as any, 'getAndUpdateCompetitionData');
      spyOn(service as any, 'callSpecificAndCommonCallbacks');
    });
    const sportId = '34';

    it('removedCompetitionIds', () => {
      websocketData.removed = ['ID1', 'ID2'];
      spyOn(service as any, 'unsubscribeAndRemoveCompetition');

      const result = service['handleAddRemoveCompetition'](sportId, topLevelType);

      expect(result).toEqual(jasmine.any(Function));

      result(websocketData);

      websocketData.removed.forEach(id => {
        expect(service['unsubscribeAndRemoveCompetition']).toHaveBeenCalledWith(
          topLevelType, sportId, id
        );
      });
    });
    describe('added', () => {
      it(`should add Competition if data has added events`, () => {
        websocketData.added = { 1: { categoryCode: 'TENNIS' }, 2: { categoryCode: 'FOOTBALL' } };

        service['handleAddRemoveCompetition'](sportId, topLevelType)(websocketData);

        Object.keys(websocketData.added).forEach((id: string) => {
          const competitionObject = websocketData.added[id];
          expect(service['getAndUpdateCompetitionData']).toHaveBeenCalledWith(
            false, sportId, topLevelType, id, competitionObject, undefined
          );
        });
      });

      it(`should Not add Competition if data has Not  added/changed events`, () => {
        service['handleAddRemoveCompetition'](sportId, topLevelType)(websocketData);

        expect(service['getAndUpdateCompetitionData']).not.toHaveBeenCalled();
      });
    });

    describe('changed', () => {
      beforeEach(() => {
        websocketData.changed = [1, 2];
      });

      it(`should changed Competition if data has changed events`, () => {
        const competitionObject = { isExpanded: true };
        inPlayStorageService.getSportCompetition.and.returnValue(competitionObject);

        service['handleAddRemoveCompetition'](sportId, topLevelType)(websocketData);

        websocketData.changed.forEach((id: string) => {
          expect(inPlayStorageService.getSportCompetition).toHaveBeenCalledWith(topLevelType, sportId, id);
          expect(service['getAndUpdateCompetitionData']).toHaveBeenCalledWith(
            true, sportId, topLevelType, id, competitionObject as any, undefined
          );
        });
      });

      it(`should Not changed Competition if data has Not changed events`, () => {
        const competitionObject = { isExpanded: false };
        inPlayStorageService.getSportCompetition.and.returnValue(competitionObject);

        service['handleAddRemoveCompetition'](sportId, topLevelType)(websocketData);

        websocketData.changed.forEach(() => {
          expect(service['getAndUpdateCompetitionData']).not.toHaveBeenCalled();
          expect(service['callSpecificAndCommonCallbacks'])
            .toHaveBeenCalledWith('INPLAY_COMPETITION_UPDATED', undefined, sportId, topLevelType);
        });
      });
      it(`should Not changed Competition if data has Not changed events and competitionObject as null`, () => {
        const competitionObject = null;
        inPlayStorageService.getSportCompetition.and.returnValue(competitionObject);

        service['handleAddRemoveCompetition'](sportId, topLevelType)(websocketData);

        websocketData.changed.forEach(() => {
          expect(service['callSpecificAndCommonCallbacks']).toHaveBeenCalledWith('INPLAY_COMPETITION_UPDATED', undefined, sportId, topLevelType);
        });
      });
    });
  });

  describe('getAndUpdateCompetitionData', () => {
    let competitionObject: any;
    const competitionEvents = [{ id: 22 }, { id: 23 }];
    const competitionEventsIds = [22, 23];
    const sportId = '16';
    const typeId = '13';
    let topLevelType: string;

    it('should getAndUpdateCompetitionData when marketselector present with modifyMainMarkets', () => {
      topLevelType = EVENT_TYPES.LIVE_EVENT;
      competitionObject = { categoryCode: 'TENNIS', events: [{ id: 21 }, { id: 22 }], eventsIds: [21, 22] };

      const requestParamsToCompare = {
        categoryId: sportId,
        isLiveNowType: true,
        topLevelType,
        typeId,
        marketSelector: 'marketSelector',
        modifyMainMarkets: true
      };

      service['getAndUpdateCompetitionData'](
        false, sportId, topLevelType, typeId, competitionObject, 'marketSelector', true
      );

      expect(service['_getCompetitionData']).toHaveBeenCalledWith(requestParamsToCompare, competitionObject.categoryCode);
    });

    it('should getAndUpdateCompetitionData when marketselector present', () => {
      topLevelType = EVENT_TYPES.LIVE_EVENT;
      competitionObject = { categoryCode: 'TENNIS', events: [{ id: 21 }, { id: 22 }], eventsIds: [21, 22] };

      const requestParamsToCompare = {
        categoryId: sportId,
        isLiveNowType: true,
        topLevelType,
        typeId,
        marketSelector: 'marketSelector',
        modifyMainMarkets: false
      };

      service['getAndUpdateCompetitionData'](
        false, sportId, topLevelType, typeId, competitionObject, 'marketSelector', false
      );

      expect(service['_getCompetitionData']).toHaveBeenCalledWith(requestParamsToCompare, competitionObject.categoryCode);
    });

    beforeEach(() => {
      spyOn(service as any, 'subscribeForUpdates');
      spyOn(service as any, 'callSpecificAndCommonCallbacks');
      spyOn(service as any, '_getCompetitionData').and.returnValue(observableOf(competitionEvents));
    });

    describe('added', () => {
      beforeEach(() => {
        topLevelType = EVENT_TYPES.LIVE_EVENT;
        competitionObject = { categoryCode: 'TENNIS', events: [{ id: 21 }, { id: 22 }], eventsIds: [21, 22] };
        const isAggregated: boolean = true;

        service['getAndUpdateCompetitionData'](false, sportId, topLevelType, typeId, competitionObject);
      });

      it(`should get Competition Data`, () => {
        const requestParams = {
          categoryId: sportId,
          isLiveNowType: true,
          topLevelType,
          typeId,
          modifyMainMarkets: true
        };

        expect(service['_getCompetitionData']).toHaveBeenCalledWith(requestParams, competitionObject.categoryCode);
      });

      it(`should update events and eventsIds`, () => {
        expect(competitionObject.events).toEqual(competitionEvents);
        expect(competitionObject.eventsIds).toEqual(competitionEventsIds);
      });

      it(`should add Competition to storage`, () => {
        expect(inPlayStorageService.addCompetition).toHaveBeenCalledWith(topLevelType, sportId, competitionObject, undefined);
      });

      it(`should emit INPLAY_COMPETITION_ADDED`, () => {
        expect(service['callSpecificAndCommonCallbacks'])
          .toHaveBeenCalledWith('INPLAY_COMPETITION_ADDED', competitionObject, sportId, topLevelType);
      });

      it(`should Not subscribe/unsubscribe of updates`, () => {
        expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).not.toHaveBeenCalled();
        expect(service['subscribeForUpdates']).not.toHaveBeenCalled();
      });
    });


    describe('changed', () => {
      beforeEach(() => {
        topLevelType = EVENT_TYPES.UPCOMING_EVENT;
        competitionObject = { categoryCode: 'TENNIS', events: [{ id: 21 }, { id: 22 }], eventsIds: [21, 22] };

        service['getAndUpdateCompetitionData'](true, sportId, topLevelType, typeId, competitionObject);
      });

      it(`should get Competition Data`, () => {
        const requestParams = {
          categoryId: sportId,
          isLiveNowType: false,
          topLevelType,
          typeId,
          modifyMainMarkets: true
        };

        expect(service['_getCompetitionData']).toHaveBeenCalledWith(requestParams, competitionObject.categoryCode);
      });

      it(`should unsubscribe For Live Updates of removed events`, () => {
        expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalledWith([21]);
      });

      it(`should subscribe For Live Updates of added events`, () => {
        expect(service['subscribeForUpdates']).toHaveBeenCalledWith([{ id: 23 }] as any);
      });

      it(`should emit INPLAY_COMPETITION_UPDATED`, () => {
        expect(service['callSpecificAndCommonCallbacks'])
          .toHaveBeenCalledWith('INPLAY_COMPETITION_UPDATED', undefined, sportId, topLevelType);
      });
    });

    it(`should Not subscribe/unsubscribe of updates if No removedEvents or addedEvents`, () => {
      competitionObject = { categoryCode: 'TENNIS', events: [{ id: 23 }, { id: 22 }], eventsIds: [23, 22] };

      service['getAndUpdateCompetitionData'](true, sportId, topLevelType, typeId, competitionObject);

      expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).not.toHaveBeenCalled();
      expect(service['subscribeForUpdates']).not.toHaveBeenCalled();
    });
  });

  it('unsubscribeAndRemoveCompetition', () => {
    const topLevelType = 'TLT';
    const sportId = 'SID';
    const competitionId = 'CID';
    const competition = { eventsIds: ['Q', 'W'] };
    spyOn(service as any, 'callSpecificAndCommonCallbacks');

    inPlayStorageService.getSportCompetition = jasmine.createSpy()
      .and.returnValue(competition);

    service['unsubscribeAndRemoveCompetition'](topLevelType, sportId, competitionId);

    expect(inPlayStorageService.getSportCompetition).toHaveBeenCalledWith(
      topLevelType, sportId, competitionId
    );
    expect(inPlaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalledWith(
      competition.eventsIds
    );
    expect(inPlayStorageService.removeCompetition).toHaveBeenCalledWith(
      topLevelType, sportId, competitionId
    );

    expect(service['callSpecificAndCommonCallbacks'])
      .toHaveBeenCalledWith('INPLAY_COMPETITION_REMOVED', competition, sportId, topLevelType);
    expect(pubSubService.publish).toHaveBeenCalledWith('INPLAY_DATA_RELOADED');
  });

  it('unsubscribeAndRemoveCompetition not called', () => {
    const topLevelType = 'TLT';
    const sportId = 'SID';
    const competitionId = 'CID';
    spyOn(service as any, 'callSpecificAndCommonCallbacks');

    inPlayStorageService.getSportCompetition = jasmine.createSpy()
      .and.returnValue(null);

    service['unsubscribeAndRemoveCompetition'](topLevelType, sportId, competitionId);

    expect(service['callSpecificAndCommonCallbacks']).not.toHaveBeenCalled();
  });

  it('getUnformattedEventsCounter', () => {
    service['_getEventsCounter'] = jasmine.createSpy();
    service['getUnformattedEventsCounter']([], 123);
    expect(service['_getEventsCounter']).toHaveBeenCalled();
  });

  describe('updateEventsCounter', () => {
    it('updateEventsCounter should update count', () => {
      const structure = {
        'someFilter': {
          eventCount: 1
        }
      };
      service['_getEventsCounter'] = jasmine.createSpy();
      service['updateEachSportCounter'] = jasmine.createSpy('updateEachSportCounter');
      service['updateEventsCounter'](structure, ['someFilter'], {
        'someFilter': 123
      } as any, {} as any, false, 'SINGLE');

      expect(structure).toEqual({
        'someFilter': {
          eventCount: 123
        }
      });
      expect(service['updateEachSportCounter']).toHaveBeenCalledWith(structure as any, 'someFilter', {}, false);
      expect(
        pubSubService.publish
      ).toHaveBeenCalledWith(`${pubSubApi.EVENT_BY_SPORTS_CHANNEL}_SINGLE`, { someFilter: { eventCount: 123 } });
    });

    it('updateEventsCounter should not update count', () => {
      const structure = {
        'someFilter': {
          eventCount: 1
        }
      };
      service['_getEventsCounter'] = jasmine.createSpy();
      service['updateEachSportCounter'] = jasmine.createSpy('updateEachSportCounter');
      service['updateEventsCounter'](structure, ['not existFilter'], {
        'someFilter': 123
      } as any, {} as any);

      expect(structure).toEqual({
        'someFilter': {
          eventCount: 1
        }
      });

      expect(service['updateEachSportCounter']).not.toHaveBeenCalled();
    });

    it('updateEventsCounter should not update count', () => {
      const structure = {
        'someFilter': {
          eventCount: 1
        }
      };
      service['_getEventsCounter'] = jasmine.createSpy();
      service['updateEachSportCounter'] = jasmine.createSpy('updateEachSportCounter');
      service['updateEventsCounter'](structure, ['someFilter'], {} as any, {} as any);

      expect(structure).toEqual({
        'someFilter': {
          eventCount: 1
        }
      });

      expect(service['updateEachSportCounter']).not.toHaveBeenCalled();
    });
  });

  describe('updateEachSportCounter', () => {
    let structure, countersByCategory;
    beforeEach(() => {
      structure = {
        'livenow': {
          eventCount: 4,
          eventsBySports: [
            {
              categoryId: 5,
              eventCount: 159
            }
          ]
        },
        'upcoming': {
          eventCount: 4,
          eventsBySports: [
            {
              categoryId: 5,
              eventCount: 268
            }
          ]
        }
      };
      countersByCategory = {
        5: {
          livenow: '1',
          upcoming: '2',
          liveStream: '3',
          upcomingLiveStream: undefined
        }
      };
    });
    it('should update counters for livenow non livestream case', () => {
      service.updateEachSportCounter(structure as any, 'livenow', countersByCategory as any, false);
      expect(structure['livenow'].eventsBySports[0].eventCount).toEqual(1);
    });
    it('should update counters for livenow livestream case', () => {
      service.updateEachSportCounter(structure as any, 'livenow', countersByCategory as any, true);
      expect(structure['livenow'].eventsBySports[0].eventCount).toEqual(3);
    });
    it('should update counters for upcoming non livestream case', () => {
      service.updateEachSportCounter(structure as any, 'upcoming', countersByCategory as any, false);
      expect(structure['upcoming'].eventsBySports[0].eventCount).toEqual(2);
    });
    it('should update counters for upcoming livestream case', () => {
      service.updateEachSportCounter(structure as any, 'upcoming', countersByCategory as any, true);
      expect(structure['upcoming'].eventsBySports[0].eventCount).toEqual(0);
    });
    it('should not fail in default case', () => {
      const defaultStructure = {
        'livenow': {}
      };
      service.updateEachSportCounter(defaultStructure as any, 'livenow', {} as any, true);
    });
  });

  describe('getSportName', () => {
    it('should remove dashes from category path if it exist', () => {
      expect(service['getSportName']({
        categoryPath: 'horse-racing'
      } as any)).toEqual('horseracing');
    });

    it('should work correct for edge case', () => {
      expect(service['getSportName']({} as any)).toEqual('');
    });
  });

  describe('extendSectionWithSportInstance', () => {
    it('should set proper isTierOneSport to true for tier one', () => {
      const sportSection = {},
        sportInstance = {
          config: {
            tier: 1
          }
        };
      service['extendSectionWithSportInstance'](sportSection as any, sportInstance as any);
      expect((sportSection as any).tier).toEqual(1);
      expect((sportSection as any).isTierOneSport).toEqual(true);
    });

    it('should set proper isTierOneSport to false for tier two', () => {
      const sportSection = {},
        sportInstance = {
          config: {
            tier: 2
          }
        };
      service['extendSectionWithSportInstance'](sportSection as any, sportInstance as any);
      expect((sportSection as any).tier).toEqual(2);
      expect((sportSection as any).isTierOneSport).toEqual(false);
    });

    it('should set proper isTierOneSport to false for tier three', () => {
      const sportSection = {},
        sportInstance = {
          config: {
            tier: 3
          }
        };
      service['extendSectionWithSportInstance'](sportSection as any, sportInstance as any);
      expect((sportSection as any).tier).toEqual(3);
      expect((sportSection as any).isTierOneSport).toEqual(false);
    });
    it('should set proper isTierOneSport to false for sportInstance is null', () => {
      const sportSection = {},
      sportInstance = null
      service['extendSectionWithSportInstance'](sportSection as any, sportInstance as any);
      expect((sportSection as any).isTierOneSport).toEqual(false);
    });
    it('should set proper isTierOneSport to false for sportInstance.config is null', () => {
      const sportSection = {},
      sportInstance = {
        config: { }
      };
      service['extendSectionWithSportInstance'](sportSection as any, sportInstance as any);
      expect((sportSection as any).isTierOneSport).toEqual(false);
    });
  });

  describe('getSportConfigSafe', () => {
    it('should return config if it exist', fakeAsync(() => {
      let result;
      getSportError = false;
      service.getSportConfigSafe('football').subscribe((data) => {
        result = data;
      });
      tick();
      expect(result).toEqual({
        config: {
          tier: 1
        }
      });
    }));
    it('should return {} if config not exist', fakeAsync(() => {
      let result;
      getSportError = true;
      service.getSportConfigSafe('football').subscribe((data) => {
        result = data;
      });
      tick();
      expect(result).toEqual({});
    }));
  });

  describe('filterAllSportsRibbonItems', () => {
    let ribbonData;

    beforeEach(() => {
      ribbonData = [
        { categoryId: 0, targetUriCopy: 'allsports' },
        { categoryId: 1, targetUriCopy: 'football' },
        { categoryId: 2, targetUriCopy: 'tennis' },
      ];
      service.isWatchLiveEnabled = true;
    });

    it(`should return Not filter data if 'isWatchLiveEnabled' is equal false`, () => {
      service.isWatchLiveEnabled = false;

      expect(service['filterAllSportsRibbonItems'](ribbonData).map(item => item.categoryId)).toEqual([0, 1, 2]);
    });

    it(`should Not prepend 'watchLiveItem' if 'isWatchLiveEnabled' is equal False`, () => {
      service.isWatchLiveEnabled = false;

      expect(service['filterAllSportsRibbonItems'](ribbonData)[0].categoryId).not.toEqual(watchLiveItem.categoryId);
    });

    it(`should prepend 'watchLiveItem' if 'isWatchLiveEnabled' is equal true`, () => {
      expect(service['filterAllSportsRibbonItems'](ribbonData)[0].categoryId).toEqual(watchLiveItem.categoryId);
    });

    it(`should return empty array if no ribbonData is empty`, () => {
      ribbonData = [];
      expect(service['filterAllSportsRibbonItems'](ribbonData)).toEqual([]);
    });

    it(`should return same ribbonData if watchlive item already exist`, () => {
      ribbonData = [{ categoryId: 999999, targetUriCopy: 'watchlive' }];
      expect(service['filterAllSportsRibbonItems'](ribbonData)[0].categoryId).toEqual(watchLiveItem.categoryId);
    });

    it(`should remove all sports item 'removeAllSportsItem' is equal true`, () => {
      service['removeAllSportsItem'] = true;

      expect(service['filterAllSportsRibbonItems'](ribbonData).find(item => item.targetUriCopy === 'allsports')).toBeFalsy();
    });

    it(`should Not remove all sports item 'removeAllSportsItem' is equal false`, () => {
      expect(service['filterAllSportsRibbonItems'](ribbonData, false).find(item => item.targetUriCopy === 'allsports')).toBeTruthy();
    });
  });

  describe('#callSpecificAndCommonCallbacks', () => {
    const sportId = '34';
    const topLevelType = EVENT_TYPES.LIVE_EVENT;
    const args = [1, 2, 3];
    it(`pubSubService.publish should NOT be called`, () => {
      const method = 'INPLAY_COMPETITION_ADDED';
      service['callSpecificAndCommonCallbacks'](method, args, sportId, topLevelType);

      expect(pubSubService.publish).toHaveBeenCalledWith('INPLAY_COMPETITION_ADDED', args);
      expect(pubSubService.publish).toHaveBeenCalledWith('INPLAY_COMPETITION_ADDED:34:LIVE_EVENT', args);
    });
    it(`pubSubService.publish should be called`, () => {
      const method = 'INPLAY_COMPETITION_REMOVED';
      service['callSpecificAndCommonCallbacks'](method, args, sportId, topLevelType);

      expect(pubSubService.publish).toHaveBeenCalledWith('INPLAY_COMPETITION_REMOVED', args);
      expect(pubSubService.publish).toHaveBeenCalledWith('INPLAY_COMPETITION_REMOVED:34:LIVE_EVENT', args);
    });
  });

  describe('#getFirstSport', () => {
    it('should return first sport and skip allsports', () => {
      const result = service.getFirstSport(ribbonCacheData);

      expect(result).toEqual(ribbonCacheData.data[1]);
    });

    it('should return first sport and skip watchlive', () => {
      ribbonCacheData.data.pop([{ categoryId: 999999, targetUriCopy: 'watchlive' }]);
      const result = service.getFirstSport(ribbonCacheData);

      expect(result).toEqual(ribbonCacheData.data[1]);
    });
  });

  describe('getSingleEventCounter', () => {
    it('should return not formatted event counters object', () => {
      const ribbonItem = {
        liveEventCount: 1,
        upcomingEventCount: 2,
        liveStreamEventCount: 3,
        upcommingLiveStreamEventCount: 4
      } as any;
      expect(service['getSingleEventCounter'](ribbonItem, false )).toEqual({
        livenow: '1',
        upcoming: '2',
        liveStream: '3',
        upcomingLiveStream: '4'
      });
    });
    it('should return formatted event counters object', () => {
      const ribbonItem = {
        liveEventCount: 1,
        upcomingEventCount: 2,
        liveStreamEventCount: 3,
        upcommingLiveStreamEventCount: 4
      } as any;
      expect(service['getSingleEventCounter'](ribbonItem)).toEqual({
        livenow: '(1)',
        upcoming: '(2)',
        liveStream: '(3)',
        upcomingLiveStream: '(4)'
      });
    });
    it('should return object with empty value in default case', () => {
      expect(service['getSingleEventCounter']({} as any)).toEqual({
        livenow: undefined,
        upcoming: undefined,
        liveStream: undefined,
        upcomingLiveStream: undefined
      });
    });
    it('should return object with empty value in default case', () => {
      expect(service['getSingleEventCounter']({} as any, false)).toEqual({
        livenow: undefined,
        upcoming: undefined,
        liveStream: undefined,
        upcomingLiveStream: undefined
      });
    });
  });
  describe('getEventCountersByCategory', () => {
    it('should create event counters by category map', () => {
      const data = [
        {
          categoryId: 1
        },
        {
          categoryId: 2
        }
      ];
      service['getSingleEventCounter'] = jasmine.createSpy('getSingleEventCounter').and.returnValue({});
      expect(service.getEventCountersByCategory(data as any)).toEqual({
        1: {},
        2: {}
      } as any);
    });
  });

  it('should call checkAggregateMarkets', () => {
    const requestParams = {
      marketSelector: "Match Result,Total Points"
    };
    const eventsData: any[] = [{ id: 1, markets: [{name: 'Match Result'}] }, { id: 2, 
      markets: [{name: 'Total Points'}] }];
    const competition = { eventsIds: [1, 2]} as any;
    // const competitionEvents = { eventsIds: [1,2,3], events: eventsData} as any;
    const resp = service.checkAggregateMarkets(requestParams, competition, eventsData);
    expect(resp.length).toEqual(2);
  });

  describe('getVirtualData', () => {
    it('getVirtualsData', fakeAsync(() => {
      service['_getVirtuals'] = () => observableOf(['1','2'])
      const retVal = service.getVirtualsData()
      retVal.subscribe(data => 'data')
      tick()
    }))
  })

  describe('_getVirtuals', () => {
    it('should call inPlayDataService.loadData', () => {
      const retVal = service['_getVirtuals']();
      retVal.subscribe(data => 'data')
      expect(inPlayDataService.loadData).toHaveBeenCalledWith('virtuals', null);
    });
  });
});
