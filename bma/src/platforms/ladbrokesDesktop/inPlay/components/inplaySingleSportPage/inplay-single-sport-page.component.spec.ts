import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import {
  InplaySingleSportPageComponent
} from '@ladbrokesDesktop/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';

describe('LDInplaySingleSportPageComponent', () => {
  let component: InplaySingleSportPageComponent;
  let cmsService;
  let inplaySubscriptionManagerService;
  let router;
  let inplayConnectionService;
  let pubSubService;
  let route;
  let inplayMainService;
  let awsService;
  let changeDetectorRef;
  let sportsConfigService;

  const ribbonItems = [
    {
      targetUriCopy: 'watchlive',
      targetUri: '/in-play/watchlive'
    },
    {
      targetUriCopy: 'allsports',
      targetUri: '/in-play/allsports'
    },
    {
      targetUriCopy: 'football',
      targetUri: '/in-play/football',
      categoryId: '16'
    },
    {
      targetUriCopy: 'tennis',
      targetUri: '/in-play/tennis',
    }
  ];
  const systemConfig = {
    InPlayCompetitionsExpanded: {
      competitionsCount: 2
    }
  };

  beforeEach(fakeAsync(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    route = {
      params: observableOf([{
        InPlayCompetitionsExpanded: {
          competitionsCount: '3'
        },
        sport: 'football'
      }]),
      snapshot: { params: {} }
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(systemConfig)),
      getMarketSwitcherFlagValue: jasmine.createSpy('getMarketSwitcherFlagValue').and.returnValue(observableOf(true))
    };

    inplaySubscriptionManagerService = {
      unsubscribeForSportCompetitionChanges: jasmine.createSpy('unsubscribeForSportCompetitionChanges'),
      unsubscribeForLiveUpdates: jasmine.createSpy('unsubscribeForLiveUpdates')
    };

    inplayConnectionService = {
      status: jasmine.createSpy(),
      setConnectionErrorState: jasmine.createSpy('setConnectionErrorState')
    };

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    inplayMainService = {
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf([{}])),
      generateSwitchers: jasmine.createSpy(),
      addRibbonURLHandler: jasmine.createSpy('addRibbonURLHandler'),
      getFirstSport: jasmine.createSpy('getFirstSport').and.returnValue({ targetUriCopy: 'football', targetUri: '/in-play/football' }),
      getSportId: jasmine.createSpy('getSportId').and.returnValue(observableOf('16')),
      getSportData: jasmine.createSpy().and.returnValue(observableOf(null)),
      getTopLevelTypeParameter: jasmine.createSpy(),
      isNewUserFromOtherCountry: () => false,
      clearDeletedEventFromType: jasmine.createSpy('clearDeletedEventFromType')
    };

    pubSubService = {
      subscribe: jasmine.createSpy(),
      API: pubSubApi,
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy('publish')
    };

    awsService = {
      addAction: jasmine.createSpy()
    };

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf({
        sportConfig: {
          config: {
            request: {
              categoryId: '16'
            }
          }
        }
      }))
    };
    component = new InplaySingleSportPageComponent(
      inplayMainService,
      inplaySubscriptionManagerService,
      pubSubService,
      inplayConnectionService,
      route,
      cmsService,
      router,
      awsService,
      changeDetectorRef,
      sportsConfigService
    );
  }));

  describe('@ngOnInit', () => {
    it('should init component', fakeAsync(() => {
      component.ngOnInit();
      tick(200);

      expect(component.filter).toEqual('livenow');
      expect(inplayConnectionService.setConnectionErrorState).toHaveBeenCalledWith(false);
    }));

    it('should init component when no sportId', fakeAsync(() => {
      spyOn(component, 'applyData');
      inplayMainService.getSportId.and.returnValue(observableOf(null));
      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);

      expect(inplayMainService.addRibbonURLHandler).toHaveBeenCalled();
      expect(inplayMainService.getSportData).not.toHaveBeenCalled();
      expect(component['applyData']).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();

    }));

    it('should init component when no CmsConfig', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(observableOf(null));
      spyOn(component, 'applyData');

      component['showContent'] = jasmine.createSpy('showContent');
      component.ngOnInit();
      tick(200);

      expect(component['applyData']).not.toHaveBeenCalled();
    }));
  });

  describe('applyData', () => {
    it('should not goToFilter if ssError be truthy', fakeAsync(() => {
      spyOn(component, 'goToFilter');
      spyOn<any>(component, 'trackErrorMessage');
      component.firstLoad = true;
      component.applyData({} as ISportSegment);
      tick(200);
      expect(component.goToFilter).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component['trackErrorMessage']).toHaveBeenCalled();
    }));
  });

  describe('#showContent', () => {
    it('should redirect to first sport after undisplay last event from current sport', fakeAsync(() => {
      component['sportUri'] = 'tennis';
      pubSubService.subscribe.and.callFake((subscriberName: string, channel: string, channelFunction: Function) => {
        if (channel === pubSubService.API.EVENT_COUNT_UPDATE) {
          channelFunction(ribbonItems);
        }
      });
      component['reloadComponent'] = jasmine.createSpy('reloadComponent');
      component['getSwitchers'] = jasmine.createSpy('getSwitchers');
      component['showContent']();
      tick(200);
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.cSyncName,
        pubSubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
      expect(component['getSwitchers']).toHaveBeenCalledWith(ribbonItems as any);
      expect(router.navigateByUrl).not.toHaveBeenCalledWith('/in-play/football');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('should redirect to first sport after undisplay last event from current sport', fakeAsync(() => {
      component['sportUri'] = 'basketball';
      pubSubService.subscribe.and.callFake((subscriberName: string, channel: string, channelFunction: Function) => {
        channelFunction(ribbonItems);
      });
      component['reloadComponent'] = jasmine.createSpy('reloadComponent');
      component['showContent']();
      tick(200);
      expect(router.navigateByUrl).toHaveBeenCalledWith('/in-play/football');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));
  });

  describe('trackErrorMessage', () => {
    it('should track Site Serve error', () => {
      component['ssError'] = true;
      spyOn<any>(component, 'showNoEventsSection').and.returnValue(false);
      component['trackErrorMessage']();

      expect(awsService.addAction).toHaveBeenCalledWith('inplay=>UI_Message=>Unavailable=>ssError');
    });

    it('should not track error if no ssError', () => {
      component['ssError'] = false;
      spyOn<any>(component, 'showNoEventsSection').and.returnValue(false);
      component['trackErrorMessage']();

      expect(awsService.addAction).not.toHaveBeenCalled();
    });

    it('should not track error if ssError but not events to show', () => {
      component['ssError'] = true;
      spyOn<any>(component, 'showNoEventsSection').and.returnValue(true);
      component['trackErrorMessage']();

      expect(awsService.addAction).not.toHaveBeenCalled();
    });
  });

  it('should reinit unsubscribe Subject when reloadComponent triggered by RELOAD_IN_PLAY event', fakeAsync(() => {
    component.ngOnInit();
    tick(200);

    expect(component['unsubscribe'].isStopped).toEqual(false);

    component['reloadComponent']();
    tick(200);

    expect(component['unsubscribe'].isStopped).toEqual(false);
  }));

  it(`should unsubscribe from 'getRibbonData' stream`, () => {
    // @ts-ignore
    component.routeListener = { unsubscribe: jasmine.createSpy() };

    component.ngOnDestroy();

    expect(component.routeListener.unsubscribe).toHaveBeenCalledTimes(1);
  });

  it('#reloadComponent', () => {
    spyOn(component, 'ngOnDestroy');
    spyOn(component, 'showSpinner');
    spyOn(component, 'ngOnInit');

    component.reloadComponent();

    expect(inplayConnectionService.setConnectionErrorState).toHaveBeenCalledWith(false);
    expect(component.ngOnDestroy).toHaveBeenCalled();
    expect(component.showSpinner).toHaveBeenCalled();
    expect(component.ngOnInit).toHaveBeenCalled();
  });

  it('should subscribe to reload components', () => {
    pubSubService.subscribe.and.callFake((namespace: string, eventName: string[] | string, callback: Function) => {
      if (eventName === 'RELOAD_IN_PLAY') {
        spyOn(component, 'ngOnInit');
        spyOn(component, 'ngOnDestroy');
        spyOn(component, 'reloadComponent').and.callThrough();

        callback();

        expect(component.reloadComponent).toHaveBeenCalled();
      }
    });

    component['showContent']();
  });

  it('should use OnPush strategy', () => {
    expect(InplaySingleSportPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });
  describe('updateSportData', () => {
    it('should update sport data', fakeAsync(() => {
      component.firstLoad = true;
      inplayMainService.getSportData = jasmine.createSpy().and.returnValue(observableOf({}));
      component.filter = 'livenow';
      inplayMainService.getTopLevelTypeParameter= jasmine.createSpy().and.returnValue('LIVE_EVENT');
      component.updateSportData({
        useCache: false,
        additionalParams: {
          marketSelector: 'Match Beting'
        }
      });
      tick(200);

      expect(inplayMainService.getTopLevelTypeParameter).toHaveBeenCalledWith('livenow');
      expect(inplayMainService.getSportData).toHaveBeenCalledWith({
        categoryId: '16',
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
        marketSelector: 'Match Beting'
      }, false, true, true, false,undefined);
    }));
  });
});
