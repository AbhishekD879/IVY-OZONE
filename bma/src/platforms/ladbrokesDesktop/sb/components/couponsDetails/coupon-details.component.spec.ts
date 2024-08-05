import { Observable, of } from 'rxjs';
import { CouponsDetailsComponent } from './coupons-details.component';
import { NavigationEnd } from '@angular/router';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('CouponsDetailsComponentLadbrokesDesktop', () => {
  let component: CouponsDetailsComponent;
  let couponsDetailsService;
  let pubSubService;
  let deviceService;
  let marketSortService;
  let couponsListService;
  let updateEventService;
  let routingHelperService;
  let footballService;
  let domToolsService;
  let router;
  let activatedRoute;
  let windowRefService;
  let changeDetectorRef;
  let cacheEventsService;
  let elementParamsMap;
  let elementRef;
  let getSportInstanceService;
  let routingState;
  let cmsService;
  let optaScoreboardLoaderService;
  let optaScoreboardOverlayService;
  let gtmService;
  let userService;
  let storageService;
  let rendererService;
  let timeService;

  beforeEach(() => {
    couponsDetailsService = {
      setOddsHeader: jasmine.createSpy('setOddsHeader'),
      isBetFilterEnable: jasmine.createSpy('isBetFilterEnable'),
      getCouponEvents: jasmine.createSpy('getCouponEvents'),
      groupCouponEvents: jasmine.createSpy('groupCouponEvents'),
      initMarketSelector: jasmine.createSpy('initMarketSelector'),
      isQuickBetBlocked: jasmine.createSpy('isQuickBetBlocked'),
      isCustomCoupon: false
    };

    updateEventService = {};

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      API: pubSubApi
    };

    deviceService = {
      isTablet: true
    };

    cacheEventsService = {
      store: jasmine.createSpy('store'),
      clearByName: jasmine.createSpy('clearByName')
    };

    marketSortService = {
      setMarketFilterForMultipleSections : jasmine.createSpy(),
    };

    footballService = {
      unSubscribeCouponsForUpdates : jasmine.createSpy('unSubscribeCouponsForUpdates'),
      coupons: jasmine.createSpy('coupons'),
      extendRequestConfig: jasmine.createSpy('extendRequestConfig'),
      subscribeCouponsForUpdates: jasmine.createSpy('subscribeCouponsForUpdates')
    };
    elementRef = { nativeElement: { tagName: 'parent' } };
    elementParamsMap = {
      header: { bottom: 50 },
      parent: { top: 40 },
      topBar: { bottom: 70 }
    };

    domToolsService = {
      HeaderEl: { tagName: 'header' },
      getElementTopPosition: jasmine.createSpy('getElementTopPosition').and.callFake(
        el => elementParamsMap[el.tagName] ? elementParamsMap[el.tagName].top : 0
      ),
      getElementBottomPosition: jasmine.createSpy('getElementBottomPosition').and.callFake(
        el => elementParamsMap[el.tagName] ? elementParamsMap[el.tagName].bottom : 0
      ),
      getWidth: jasmine.createSpy().and.returnValue(50),
      css: jasmine.createSpy(),
      getOffset: jasmine.createSpy('getOffset').and.returnValue({ top: 120 }),
      getHeight: jasmine.createSpy('getHeight').and.returnValue(150)
    };

    router = {
      events: Observable.create((observer) => {
        const event = new NavigationEnd(559, 'coupons/football/coupon-1809-weekend/', 'coupons/football/coupon-1809-weekend/');
        setTimeout(() => {
          observer.next(event);
        }, 50);
      }),
      navigateByUrl : jasmine.createSpy()
    };

    activatedRoute = {
      snapshot: {
        data: {
          segment: 'couponsDetails'
        },
        paramMap: {
          get: jasmine.createSpy().and.callFake((() => {
            let i = 0;
            return () => `test${i++}`;
          })())
        }
      }
    };

    windowRefService = {
      nativeWindow: {
        clearInterval: jasmine.createSpy('clearInterval'),
        setInterval: jasmine.createSpy('setInterval').and.callFake((cb) => {
          cb();
          return 2;
        }),
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((cb) => {
          cb();
        }),
        scrollTo: jasmine.createSpy('scrollTo')
      },
      document: {
        getElementById: jasmine.createSpy().and.returnValue({ clientHeight: 0 }),
        body: {
          scrollTop: 1
        },
        documentElement: {
          scrollTop: 1
        },
        querySelector: jasmine.createSpy('querySelector')
      }
    };

    elementRef = {
      nativeElement : {
        querySelector: jasmine.createSpy().and.returnValue({ clientHeight: 0, scrollTop: 1 })
      }
    };

    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    getSportInstanceService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of(footballService))
    };

    routingState = {
      getPreviousSegment: jasmine.createSpy('getPreviousSegment').and.returnValue(''),
      getPreviousUrl: jasmine.createSpy('getPreviousUrl').and.returnValue('')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({})),
      getCouponLeagueLinks: jasmine.createSpy('getCouponLeagueLinks').and.returnValue(of([]))
    };
    optaScoreboardLoaderService = {
      loadBundle: jasmine.createSpy('loadBundle').and.returnValue(of('bundle'))
    };
    optaScoreboardOverlayService = {
      showOverlay: jasmine.createSpy('showOverlay'),
      setOverlayData: jasmine.createSpy('setOverlayData'),
      destroyOverlay: jasmine.createSpy('destroyOverlay'),
      initOverlay: jasmine.createSpy('initOverlay').and.returnValue(of(Symbol('HTMLElement')))
    };

    component = new CouponsDetailsComponent(
      activatedRoute,
      getSportInstanceService,
      deviceService,
      pubSubService,
      marketSortService,
      elementRef,
      router,
      domToolsService,
      windowRefService,
      changeDetectorRef,
      couponsDetailsService,
      cacheEventsService,
      routingState,
      cmsService,
      optaScoreboardLoaderService,
      optaScoreboardOverlayService,
      couponsListService,
      routingHelperService,
      updateEventService,
      gtmService,
      userService,
      storageService,
      rendererService,
      timeService
    );

    component['footballService'] = footballService;
  });

  it('should create a component', () => {
    expect(component).toBeTruthy();
  });

  describe('getStickyElementsHeight', () => {
    it('should return 0 if no element found', () => {
      expect(component['getStickyElementsHeight']()).toEqual(0);
    });
    it('should return sticky elements height', () => {
      windowRefService.document.querySelector = jasmine.createSpy('querySelector').and.returnValue({});
      expect(component['getStickyElementsHeight']()).toEqual(150);
    });
  });
});
