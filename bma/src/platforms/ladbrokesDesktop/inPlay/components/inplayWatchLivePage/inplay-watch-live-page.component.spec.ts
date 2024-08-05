import { forkJoin as observableForkJoin, of as observableOf, BehaviorSubject } from 'rxjs';

import { InplayWatchLivePageComponent } from '@ladbrokesDesktop/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('InplayWatchLivePageComponent', () => {
  let component: InplayWatchLivePageComponent;
  let pubsubService;
  let inplayMainService;
  let cms;
  let router;
  let changeDetectorRef;
  let inplayConnectionService;
  let inplayStorageService;

  const inPlayWatchLive = {
    InPlayWatchLive: {
      enabled: true
    },
    InPlayCompetitionsExpanded: {
      competitionsCount: '3'
    }
  } as any;

  const inPlayWatchLiveDisabled = {
    InPlayWatchLive: {
      enabled: false
    },
    InPlayCompetitionsExpanded: {
      competitionsCount: '3'
    }
  } as any;
  const liveStreamStructureData = {
    liveStream: {
      eventCount: 10,
      eventsBySports: [],
      eventsIds: []
    },
    livenow:  {
      eventCount: 10,
      eventsBySports: [],
      eventsIds: []
    },
    upcoming:  {
      eventCount: 10,
      eventsBySports: [],
      eventsIds: []
    }
  } as any;
  const ribbonItems = {
    data: [{targetUriCopy: 'football'}, {targetUriCopy: 'tennis'}]
  } as any;

  beforeEach(() => {
    inplayConnectionService = {
      disconnectComponent: jasmine.createSpy('disconnectComponent')
    };

    inplayStorageService = {
      destroySportsCache: jasmine.createSpy('destroySportsCache')
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    pubsubService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    inplayMainService = {
      unsubscribeForUpdates: jasmine.createSpy('unsubscribeForUpdates'),
      getFirstSport: jasmine.createSpy('getFirstSport').and.returnValue({ targetUriCopy: 'UriCopy' }),
      getSportUri: jasmine.createSpy(),
      getLsStructureData: jasmine.createSpy(),
      clearDeletedEventFromSport: jasmine.createSpy(),
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf(ribbonItems)),
      getLiveStreamStructureData: jasmine.createSpy().and.returnValue(observableOf({
        liveStream: {
          eventCount: 10,
          eventsBySports: [],
          eventsIds: []
        },
        livenow:  {
          eventCount: 10,
          eventsBySports: [],
          eventsIds: []
        },
        upcoming:  {
          eventCount: 10,
          eventsBySports: [],
          eventsIds: []
        }
      }))
    };
    cms = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(inPlayWatchLive))
    };
    router = {
      navigateByUrl: jasmine.createSpy()
    };

    component = new InplayWatchLivePageComponent(
      pubsubService,
      inplayMainService,
      cms,
      router,
      inplayConnectionService,
      inplayStorageService,
      changeDetectorRef
    );
    component.cSyncName = 'inplayWatchLivePage';
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayWatchLivePageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('#ngOnInit', () => {
    it('should not redirect', () => {
      cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLive));
      component.ngOnInit();

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

      expect(pubsubService.subscribe).toHaveBeenCalledWith(
        'inplayWatchLivePage',
        pubsubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
      expect(pubsubService.subscribe).toHaveBeenCalledWith(
        'inplayWatchLivePage',
        pubsubService.API.SESSION_LOGIN,
        jasmine.any(Function)
      );
      expect(cms.getSystemConfig).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should not redirect on Live stream tab', () => {
      component.isLiveStreamPage = true;
      cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));
      const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
      const stream$ = new BehaviorSubject(ribbonData);
      inplayMainService.getRibbonData.and.returnValue(stream$ as any);

      component.ngOnInit();

      expect(component['router'].navigateByUrl).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should redirect', () => {
      component.isLiveStreamPage = false;
      cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));
      const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
      const stream$ = new BehaviorSubject(ribbonData);
      inplayMainService.getRibbonData.and.returnValue(stream$ as any);

      component.ngOnInit();

      expect(component['router'].navigateByUrl).toHaveBeenCalledWith('/in-play/UriCopy');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayWatchLivePage');
    expect(inplayStorageService.destroySportsCache).not.toHaveBeenCalled();
    expect(inplayConnectionService.disconnectComponent).not.toHaveBeenCalled();
  });

  it('ngOnDestroy', () => {
    component.isLiveStreamPage = true;
    component.ngOnDestroy();

    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayWatchLivePage');
    expect(inplayStorageService.destroySportsCache).toHaveBeenCalled();
    expect(inplayConnectionService.disconnectComponent).toHaveBeenCalled();
  });

  it(`should unsubscribe from 'getRibbonData' stream`, () => {
    const secondData = { data: [{ targetUriCopy: 'SubjectUriCopy' }] }as any;
    const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
    const stream$ = new BehaviorSubject(ribbonData);
    inplayMainService.getRibbonData.and.returnValue(stream$ as any);
    cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));

    component.ngOnInit();

    expect(component['router'].navigateByUrl).toHaveBeenCalledWith('/in-play/UriCopy');

    component.ngOnDestroy();
    stream$.next(secondData);

    expect(component['router'].navigateByUrl).toHaveBeenCalledTimes(1);
    expect(component['unsubscribe'].isStopped).toBeTruthy();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });
});
