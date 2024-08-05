import { forkJoin as observableForkJoin, of as observableOf, throwError, BehaviorSubject } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { InplayWatchLivePageComponent } from '@app/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('InplayWatchLivePageComponent', () => {
  let component,
    pubsubService, inplayMainService, cms, router,
    changeDetectorRef, deleteFn;

  const inplayConnectionService = {
    setConnectionErrorState: jasmine.createSpy('setConnectionErrorState'),
    connectComponent: jasmine.createSpy('connectComponent').and.returnValue(observableOf({})),
    disconnectComponent: jasmine.createSpy()
  } as any;
  const inPlayWatchLive = {
    InPlayWatchLive: {
      enabled: true
    },
    InPlayCompetitionsExpanded: {
      competitionsCount: '3'
    }
  };

  const inPlayWatchLiveDisabled = {
    InPlayWatchLive: {
      enabled: false
    },
    InPlayCompetitionsExpanded: {
      competitionsCount: '3'
    }
  };
  const liveStreamStructureData = {
    liveStream: {
      eventCount: 10,
      eventsBySports: [],
      eventsIds: []
    },
    livenow: {
      eventCount: 10,
      eventsBySports: [],
      eventsIds: []
    },
    upcoming: {
      eventCount: 10,
      eventsBySports: [],
      eventsIds: []
    },
    upcomingLiveStream: {
      eventCount: 10,
      eventsBySports: [],
      eventsIds: []
    }
  };
  const ribbonItems = {
    data: [{ targetUriCopy: 'football' }, { targetUriCopy: 'tennis' }]
  } as any;
  const inplaySubscriptionManagerService = {
    subscribe4RibbonUpdates: jasmine.createSpy('subscribe4RibbonUpdates'),
    unsubscribe4RibbonUpdates: jasmine.createSpy('unsubscribe4RibbonUpdates')
  } as any;
  const inplayStorageService = {
    destroySportsCache: jasmine.createSpy('destroySportsCache')
  } as any;

  beforeEach(fakeAsync(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    pubsubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a: string, b: string[] | string, fn: Function) => {
        if (b === 'EVENT_COUNT_UPDATE') {
          fn(ribbonItems);
        } else if (b === 'RELOAD_IN_PLAY') {
          spyOn(component, 'ngOnInit');
          spyOn(component, 'ngOnDestroy');
          fn();
        } else if (b === 'DELETE_EVENT_FROM_CACHE') {
          deleteFn = fn;
        }
      }),
      API: pubSubApi,
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    inplayMainService = {
      getFirstSport: jasmine.createSpy('getFirstSport').and.returnValue({ targetUriCopy: 'UriCopy' }),
      getSportUri: jasmine.createSpy('getSportUri'),
      getLsStructureData: jasmine.createSpy('getLsStructureData'),
      clearDeletedEventFromSport: jasmine.createSpy('clearDeletedEventFromSport'),
      getRibbonData: jasmine.createSpy('getRibbonData').and.returnValue(observableOf(ribbonItems)),
      updateEventsCounter: jasmine.createSpy('updateEventsCounter'),
      getUnformattedEventsCounter: jasmine.createSpy('getUnformattedEventsCounter'),
      initSportsCache: jasmine.createSpy('initSportsCache'),
      unsubscribeForUpdates: jasmine.createSpy('unsubscribeForUpdates'),
      getLiveStreamStructureData: jasmine.createSpy('getLiveStreamStructureData').and.returnValue(observableOf({
        liveStream: {
          eventCount: 10,
          eventsBySports: [],
          eventsIds: []
        },
        livenow: {
          eventCount: 10,
          eventsBySports: [],
          eventsIds: []
        },
        upcoming: {
          eventCount: 10,
          eventsBySports: [],
          eventsIds: []
        },
        upcomingLiveStream: {
          eventCount: 10,
          eventsBySports: [],
          eventsIds: []
        }
      })),
      getEventCountersByCategory: jasmine.createSpy('getEventCountersByCategory').and.returnValue({} as any)
    };
    cms = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(inPlayWatchLive))
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    component = new InplayWatchLivePageComponent(pubsubService, inplayMainService,
      inplayConnectionService, cms, router, inplaySubscriptionManagerService, inplayStorageService, changeDetectorRef);
    component.cSyncName = 'inplayWatchLivePage';
  }));

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayWatchLivePageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('#addEventListeners', () => {
    beforeEach(() => {
      component['reloadComponent'] = jasmine.createSpy();
    });
    it('for delete event from cache event', fakeAsync(() => {
      component.addEventListeners();
      deleteFn();
      expect(pubsubService.subscribe).toHaveBeenCalledWith(
        'inplayWatchLivePage',
        pubsubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
      expect(inplayMainService.clearDeletedEventFromSport).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));
  });

  describe('#ngOnInit', () => {
    it('should not redirect', () => {
      cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLive));
      component.ngOnInit();
      expect(inplayConnectionService.connectComponent).toHaveBeenCalled();
      expect(inplayMainService.initSportsCache).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      observableForkJoin([
        cms.getSystemConfig(),
        inplayMainService.getLiveStreamStructureData()
      ]).subscribe((data: any[]) => {
        expect(data[0]).toEqual(inPlayWatchLive);
        expect(data[1]).toEqual(liveStreamStructureData);
        expect(component['data']).toEqual(liveStreamStructureData);
        expect(component.ssError).toBeFalsy();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayWatchLivePage', 'RELOAD_IN_PLAY', jasmine.any(Function));
      expect(cms.getSystemConfig).toHaveBeenCalled();
    });

    it('should make initial requests and initialise component data', () => {
      component.ngOnInit();

      expect(cms.getSystemConfig).toHaveBeenCalled();
      expect(inplayMainService.getLiveStreamStructureData).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalledWith(
        'inplayWatchLivePage',
        pubsubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayWatchLivePage', 'RELOAD_IN_PLAY', jasmine.any(Function));
      expect(component['data']).toEqual(liveStreamStructureData);
      expect(component.ssError).toBeFalsy();
      expect(component.expandedLeaguesCount).toEqual(inPlayWatchLive.InPlayCompetitionsExpanded.competitionsCount);
    });

    it('should make initial requests and initialise component data for Live Stream Tab', () => {
      component.isLiveStreamPage = true;
      const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
      const stream$ = new BehaviorSubject(ribbonData);
      inplayMainService.getRibbonData.and.returnValue(observableOf(stream$ as any));
      cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));

      component.ngOnInit();

      stream$.next(ribbonData);

      expect(cms.getSystemConfig).toHaveBeenCalledWith();
      expect(inplayMainService.getLiveStreamStructureData).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalledWith(
        'inplayWatchLivePage',
        pubsubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayWatchLivePage', 'RELOAD_IN_PLAY', jasmine.any(Function));
      expect(component['data']).toEqual(liveStreamStructureData);
      expect(component.ssError).toBeFalsy();
      expect(component.expandedLeaguesCount).toEqual(inPlayWatchLive.InPlayCompetitionsExpanded.competitionsCount);
      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });

    it('should make initial requests and initialise component data not for Live stream Tab', () => {
      component.isLiveStreamPage = false;
      const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
      const stream$ = new BehaviorSubject(ribbonData);
      inplayMainService.getRibbonData.and.returnValue(observableOf(stream$ as any));
      cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));

      component.ngOnInit();

      stream$.next(ribbonData);

      expect(cms.getSystemConfig).toHaveBeenCalledWith();
      expect(inplayMainService.getLiveStreamStructureData).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalledWith(
        'inplayWatchLivePage',
        pubsubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayWatchLivePage', 'RELOAD_IN_PLAY', jasmine.any(Function));
      expect(component['data']).toEqual(liveStreamStructureData);
      expect(component.ssError).toBeFalsy();
      expect(component.expandedLeaguesCount).toEqual(inPlayWatchLive.InPlayCompetitionsExpanded.competitionsCount);
      expect(router.navigateByUrl).toHaveBeenCalledWith('/in-play/UriCopy');
    });

    it('shoud handle Error during initial requests', fakeAsync(() => {
      component['inplayMainService'].getLiveStreamStructureData = jasmine.createSpy().and.returnValue(throwError('error'));

      component.ngOnInit();

      tick();
      expect(component.ssError).toEqual(true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should reinitComponent', () => {
      spyOn(component, 'ngOnDestroy');
      spyOn(component, 'showSpinner');
      spyOn(component, 'ngOnInit');

      component['reloadComponent']();

      expect(component.ngOnDestroy).toHaveBeenCalled();
      expect(component.showSpinner).toHaveBeenCalled();
      expect(component.ngOnInit).toHaveBeenCalled();
      expect(inplayConnectionService.setConnectionErrorState).toHaveBeenCalledWith(false);
    });

    it('should subscribe on EVENT_COUNT_UPDATE', () => {
      component.ngOnInit();
      expect(pubsubService.subscribe)
        .toHaveBeenCalledWith(component.cSyncName, pubsubService.API.EVENT_COUNT_UPDATE, jasmine.any(Function));
      expect(inplayMainService.updateEventsCounter).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  it('ngOnDestroy', () => {
    spyOn<any>(component, 'unsubscribeFromMs');
    component.ngOnDestroy();

    expect(component['unsubscribeFromMs']).toHaveBeenCalled();
  });

  it('unsubscribeFromMs', () => {
    component['unsubscribeFromMs']();

    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayWatchLivePage');
    expect(inplaySubscriptionManagerService.unsubscribe4RibbonUpdates).toHaveBeenCalled();
    expect(inplayStorageService.destroySportsCache).not.toHaveBeenCalled();
    expect(inplayMainService.unsubscribeForUpdates).toHaveBeenCalled();
    expect(inplayConnectionService.disconnectComponent).not.toHaveBeenCalled();
  });

  it('unsubscribeFromMs on livestream page', () => {
    component.isLiveStreamPage = true;
    component['unsubscribeFromMs']();

    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayWatchLivePage');
    expect(inplaySubscriptionManagerService.unsubscribe4RibbonUpdates).toHaveBeenCalled();
    expect(inplayStorageService.destroySportsCache).toHaveBeenCalled();
    expect(inplayMainService.unsubscribeForUpdates).toHaveBeenCalled();
    expect(inplayConnectionService.disconnectComponent).toHaveBeenCalled();
  });

  it(`should unsubscribe from 'getRibbonData' stream`,  fakeAsync(() => {
    pubsubService.subscribe = jasmine.createSpy('subscribe');
    const secondData = { data: [{ targetUriCopy: 'SubjectUriCopy' }] } as any;
    const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
    const stream$ = new BehaviorSubject(ribbonData);
    inplayMainService.getRibbonData.and.returnValue(observableOf(stream$ as any));
    cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));

    component.ngOnInit();
    tick();

    expect(component['router'].navigateByUrl).toHaveBeenCalledWith('/in-play/UriCopy');

    component.ngOnDestroy();
    stream$.next(secondData);

    expect(component['router'].navigateByUrl).toHaveBeenCalledTimes(1);
    expect(component['unsubscribe'].isStopped).toBeTruthy();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  }));
});
