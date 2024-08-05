import { InplayTabComponent } from './inplay-tab.component';
import { BehaviorSubject, of as observableOf, of } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('LDInplayTabComponent', () => {
  let component,
    inPlayConnectionService,
    inplayMainService,
    cmsService,
    inplayStorageService,
    inplaySubscriptionManagerService,
    pubsubService,
    awsService,
    changeDetectorRef,
    activatedRoute;

  beforeEach(() => {
    inPlayConnectionService = {
      connectComponent: jasmine.createSpy().and.returnValue(observableOf(true)),
      disconnectComponent: jasmine.createSpy(),
      status: {
        reconnectFailed: true
      }
    };
    inplayMainService = {
      getEventsCounter: jasmine.createSpy(),
      initSportsCache: jasmine.createSpy(),
      unsubscribeForUpdates: jasmine.createSpy(),
      getStructureData: jasmine.createSpy().and.returnValue(observableOf({})),
      getTopLevelTypeParameter: jasmine.createSpy(),
      getSportData: jasmine.createSpy().and.returnValue(observableOf({})),
      clearDeletedEventFromType: jasmine.createSpy(),
      clearDeletedEventFromSport: jasmine.createSpy(),
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf({})),
      getUnformattedEventsCounter: jasmine.createSpy(),
      updateEventsCounter: jasmine.createSpy()
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        InPlayCompetitionsExpanded: {
          competitionsCount: 10
        }
      }))
    };
    inplayStorageService = {
      destroySportsCache: jasmine.createSpy()
    };
    inplaySubscriptionManagerService = {
      unsubscribeForSportCompetitionChanges: jasmine.createSpy(),
      unsubscribeForLiveUpdates: jasmine.createSpy(),
      subscribe4RibbonUpdates: jasmine.createSpy()
    };
    pubsubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((fileName: string, method: string | string[], callback: Function) => {
        callback();
      }),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy('publish')
    };

    awsService = {
      addAction: jasmine.createSpy()
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    activatedRoute = {
      snapshot: {
          paramMap: {
              get: jasmine.createSpy('paramMap.get').and.returnValue('golf')
          }
      },
      params: of({
          sport: 'golf',
          id: '18'
      })
  };

    component = new InplayTabComponent(
      inPlayConnectionService,
      inplayMainService,
      cmsService,
      inplayStorageService,
      inplaySubscriptionManagerService,
      pubsubService,
      awsService,
      changeDetectorRef,
      activatedRoute
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayTabComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('should get switchers LiveNow and Upcoming', () => {
    const secondData = { data: [{ targetUriCopy: 'SubjectUriCopy' }] }as any;
    const ribbonData = { data: [{ targetUriCopy: 'UriCopy' }] } as any;
    const stream$ = new BehaviorSubject(ribbonData);
    inplayMainService.getRibbonData.and.returnValue(stream$ as any);
    spyOn(component as any, 'getSwitchers');
    spyOn(component as any, 'addEventListeners');

    component.ngOnInit();

    expect(component['getSwitchers']).toHaveBeenCalledWith(ribbonData.data);

    component.ngOnDestroy();
    stream$.next(secondData);

    expect(component['getSwitchers']).toHaveBeenCalledTimes(1);
    expect(component['unsubscribe'].isStopped).toBeTruthy();
  });

  it('reload handler should subscribe to sport data updating', () => {
    spyOn(component, 'updateSportData').and.returnValue(observableOf({}));
    const options = {useCache: true} as any;
    component.onDataReload(options);

    expect(component.updateSportData).toHaveBeenCalledWith(options);
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('should addEventListeners for singlesport', () => {
    spyOn(component as any, 'getSwitchers');
    component.pubsubService.subscribe = jasmine.createSpy('subscribe');
    component.singleSport = true;
    component.id = 16;

    component.addEventListeners();

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay', pubsubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function));
    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay', pubsubService.API.EVENT_COUNT_UPDATE, jasmine.any(Function));
  });

  it('should addEventListeners for not singlesport', () => {
    spyOn(component as any, 'getSwitchers');
    component.pubsubService.subscribe = jasmine.createSpy('subscribe');
    component.singleSport = false;

    component.addEventListeners();

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay', pubsubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function));
  });
  describe('#updateSingleSportData', () => {
    beforeEach(() => {
      component['applySingleSportData'] = jasmine.createSpy();
      component.data = {};
    });
    it('when segment is present', () => {
      component.data = {
        eventsIds: [],
        categoryId: [],
        topLevelType: 'someType',
        marketSelector: 'someSelector'
      } as any;
      component['updateSingleSportData'](false, {} as any).subscribe();
      expect(inplaySubscriptionManagerService.unsubscribeForSportCompetitionChanges).toHaveBeenCalled();
      expect(inplaySubscriptionManagerService.unsubscribeForLiveUpdates).toHaveBeenCalled();
      expect(inplayMainService.getSportData).toHaveBeenCalled();
      expect(component['applySingleSportData']).toHaveBeenCalled();
      expect(pubsubService.publish).toHaveBeenCalledWith('INPLAY_DATA_RELOADED');
    });
  });
});
