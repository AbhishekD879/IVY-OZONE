import { BehaviorSubject, forkJoin as observableForkJoin, of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { InplayWatchLivePageComponent } from '@coralDesktop/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('InplayWatchLivePageComponent', () => {
  let component: InplayWatchLivePageComponent;
  let pubsubService, inplayMainService, inPlayConnectionService, cms, router, inplayStorageService, changeDetectorRef;
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
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    pubsubService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    inplayMainService = {
      getFirstSport: jasmine.createSpy('getFirstSport').and.returnValue({ targetUriCopy: 'UriCopy' }),
      getSportUri: jasmine.createSpy(),
      getLsStructureData: jasmine.createSpy(),
      clearDeletedEventFromSport: jasmine.createSpy(),
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf(ribbonItems)),
      initSportsCache: jasmine.createSpy('initSportsCache'),
      unsubscribeForUpdates: jasmine.createSpy('unsubscribeForUpdates'),
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
    inPlayConnectionService = {
      connectComponent: jasmine.createSpy('connectComponent').and.returnValue(observableOf({})),
      disconnectComponent: jasmine.createSpy()
    };
    cms = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(inPlayWatchLive))
    };
    router = {
      navigateByUrl: jasmine.createSpy()
    };
    inplayStorageService = {
      destroySportsCache: jasmine.createSpy('destroySportsCache')
    };
    component = new InplayWatchLivePageComponent(
      pubsubService,
      inplayMainService,
      cms,
      router,
      inPlayConnectionService,
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
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayWatchLivePage', 'RELOAD_IN_PLAY', jasmine.any(Function));
      expect(cms.getSystemConfig).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should not redirect on Live Stream Tab', () => {
      component.isLiveStreamPage = true;
      cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));
      router.navigateByUrl = jasmine.createSpy();

      component.ngOnInit();

      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should redirect', () => {
      component.isLiveStreamPage = false;
      cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));
      router.navigateByUrl = jasmine.createSpy();

      component.ngOnInit();

      expect(router.navigateByUrl).toHaveBeenCalledWith('/in-play/UriCopy');
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
    expect(inplayStorageService.destroySportsCache).not.toHaveBeenCalled();
    expect(inplayMainService.unsubscribeForUpdates).toHaveBeenCalled();
    expect(inPlayConnectionService.disconnectComponent).not.toHaveBeenCalled();
  });

  it('unsubscribeFromMs', () => {
    component.isLiveStreamPage = true;
    component['unsubscribeFromMs']();

    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayWatchLivePage');
    expect(inplayStorageService.destroySportsCache).toHaveBeenCalled();
    expect(inplayMainService.unsubscribeForUpdates).toHaveBeenCalled();
    expect(inPlayConnectionService.disconnectComponent).toHaveBeenCalled();
  });

  it(`should unsubscribe from 'getRibbonData' stream`,  fakeAsync(() => {
    const secondData = { data: [{ targetUriCopy: 'SubjectUriCopy' }] }as any;
    const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
    const stream$ = new BehaviorSubject(ribbonData);
    inplayMainService.getRibbonData = jasmine.createSpy().and.returnValue(observableOf(stream$ as any));
    cms.getSystemConfig.and.returnValue(observableOf(inPlayWatchLiveDisabled));
    component.ngOnInit();
    tick();

    expect(component['router'].navigateByUrl).toHaveBeenCalledWith('/in-play/UriCopy');
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    component.ngOnDestroy();
    stream$.next(secondData);

    expect(component['router'].navigateByUrl).toHaveBeenCalledTimes(1);
    expect(component['unsubscribe'].isStopped).toBeTruthy();
  }));
});
