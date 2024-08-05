import { Subscription, Observable, of, throwError } from 'rxjs';
import { fakeAsync, tick, flush } from '@angular/core/testing';
import { CouponsDetailsComponent } from './coupons-details.component';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { NavigationEnd } from '@angular/router';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ICouponSegment } from '../couponsList/coupons-list.model';
import { COUPONS_WIDGET, GA_COUPON_STATS_WIDGET } from './coupons-details.constant';

describe('CouponsDetailsComponent', () => {
  let component: CouponsDetailsComponent;
  let couponsDetailsService;
  let pubSubService;
  let deviceService;
  let marketSortService;
  let updateEventService;
  let footballService;
  let domToolsService;
  let router;
  let activatedRoute;
  let windowRefService;
  let changeDetectorRef;
  let cacheEventsService;
  let couponsList;
  let elementParamsMap;
  let elementRef;
  let getSportInstanceService;
  let cmsService;
  let optaScoreboardLoaderService;
  let optaScoreboardOverlayService;
  let routingState;
  let couponsListService;
  let routingHelperService;
  let gtmService;
  let userService;
  let storageService;
  let rendererService;
  let timeService;

  const marketOptions = [
    {
      title: 'Match Result',
      templateMarketName: 'Match Betting',
      header: ['Home', 'Draw', 'Away'],
    },
    {
      title: 'Both Teams to Score',
      templateMarketName: 'Both Teams to Score',
      header: ['Yes', 'No'],
    }
  ];

  const couponSegments: ICouponSegment[] = [
    {
      title: "Featured Accas",
      couponKeys: ["334"],
      dayOfWeek:
        "WEDNESDAY",
      from: null,
      to: null,
      coupons: [
        {
          id: "333",
          cashoutAvail: true,
          name: "Weekend Matches",
          couponSortCode: "MR",
          displayOrder: -10000,
          siteChannels: "C,D,e,f,G,I,J,j,k,l,M,m,n,o,P,Q,q,r,T,U,W,y,z,",
          categoryId: "16",
          categoryCode: "FOOTBALL",
          categoryName: "|Football|",
          categoryDisplayOrder: "-11010",
          hasOpenEvent: "true",
          hasLiveNowOrFutureEvent: "true",
          responseCreationTime: "2022-04-27T11:14:51.804Z"
        }
      ]
    },
    {
      title: "Popular Coupons",
      couponKeys: [
        "346"
      ],
      coupons: [
        {
          id: "346",
          cashoutAvail: true,
          name: "Tomorrows Matches",
          couponSortCode: "MR",
          displayOrder: -10006,
          siteChannels: "C,D,e,f,G,I,J,j,k,l,M,m,P,Q,T,U,W,y,z,",
          categoryId: "16",
          categoryCode: "FOOTBALL",
          categoryName: "|Football|",
          categoryDisplayOrder: "-11010",
          hasOpenEvent: "true",
          responseCreationTime: "2022-04-27T11:14:51.804Z",
          hasLiveNowOrFutureEvent: ''
        },
        {
          id: "334",
          cashoutAvail: true,
          name: "Todays Matches",
          couponSortCode: "MR",
          displayOrder: -10001,
          siteChannels: "C,D,e,f,G,I,J,j,k,l,M,m,n,o,P,Q,q,r,T,U,W,y,z,",
          categoryId: "16",
          categoryCode: "FOOTBALL",
          categoryName: "|Football|",
          categoryDisplayOrder: "-11010",
          hasOpenEvent: "true",
          hasLiveNowOrFutureEvent: "true",
          responseCreationTime: "2022-04-27T11:14:51.804Z"
        }
      ]
    }
  ]
  const couponSegment = [{ title: 'Coupons', couponKeys: '23, 56, 76' }];
  const couponEvents = [{
    typeId: 971,
    events: [{
      id: 5112681,
      typeId: 971
    }, {
      id: 3567838,
      typeId: 971
    }],
    groupedByDate: [{
      events: [{
        id: 5112681
      }, {
        id: 3567838
      }]
    }]
  }];

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

    routingHelperService = {
      encodeUrlPart: jasmine.createSpy('encodeUrlPart').and.callFake(v => {
        return v.replace(/([^a-zA-Z0-9])+/g, '-').toLowerCase();
      })
    };
    updateEventService = {};

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      API: pubSubApi
    };

    deviceService = {
      isTablet: true,
      requestPlatform : 'mobile',
      isWrapper: false
    };

    userService = {
      username: 'username'
    };

    cacheEventsService = {
      store: jasmine.createSpy('store'),
      clearByName: jasmine.createSpy('clearByName')
    };

    marketSortService = {
      setMarketFilterForMultipleSections : jasmine.createSpy(),
    };

    footballService = {
      isFootball: false,
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
      getOffset: jasmine.createSpy('getOffset').and.returnValue({ top: 120 })
    };

    router = {
      events: Observable.create((observer) => {
        const event = new NavigationEnd(559, 'coupons/football/coupon-1809-weekend/', 'coupons/football/coupon-1809-weekend/');
        setTimeout(() => {
          observer.next(event);
        }, 50);
      }),
      navigateByUrl : jasmine.createSpy(),
      navigate: jasmine.createSpy('navigate')
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
        scrollTo: jasmine.createSpy('scrollTo'),
        scroll: jasmine.createSpy('scroll')
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
      getCouponLeagueLinks: jasmine.createSpy('getCouponLeagueLinks').and.returnValue(of([])),
      getOnboardingOverlay: jasmine.createSpy('getOnboardingOverlay').and.returnValue(of({
        isEnable: true
      }))
    };

    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };

    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass')
      }
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

    couponsListService = {
      getCouponSegment: jasmine.createSpy().and.returnValue(of(couponSegment)),
      groupCouponBySegment: jasmine.createSpy().and.returnValue(couponSegments)
    };

    gtmService={
      push: jasmine.createSpy('push')
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
      couponsListService,
      routingHelperService,
      cmsService,
      optaScoreboardLoaderService,
      optaScoreboardOverlayService,
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
    expect(component.leagueLinksMap).toEqual({});
  });

  describe('@ngOnInit', () => {
    beforeEach(() => {
      component['deleteEvent'] = jasmine.createSpy();
      component['setCouponsData'] = jasmine.createSpy();
      component['setTabletTopTitleWidth'] = jasmine.createSpy();
      component['getShowStatsIncludedLeagues'] = jasmine.createSpy();
      couponsDetailsService.isQuickBetBlocked.and.returnValue(of(true));
    });

    it('should init component', fakeAsync(() => {
      component.marketFilter = '';
      component.couponFilter = '';
      component.eventIdFromEDP = 189;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, method, callback) => {
        if (method === pubSubService.API.BETSLIP_LOADED || method === pubSubService.API.SHOW_HIDE_WIDGETS) {
          callback();
        } else if (method === pubSubService.API.DELETE_EVENT_FROM_CACHE) {
          callback('123');
        }
      });
      component.ngOnInit();

      tick(100);

      expect(footballService.extendRequestConfig).toHaveBeenCalledWith('coupons');
      expect(couponsDetailsService.isQuickBetBlocked).toHaveBeenCalled();
      expect(component.marketFilter).toEqual('');
      expect(component.couponFilter).toEqual('');
      expect(component['setTabletTopTitleWidth']).toHaveBeenCalledTimes(2);
      expect(component['deleteEvent']).toHaveBeenCalledWith('123' as any);
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.BLOCK_QUICK_BET, true);
      expect(pubSubService.subscribe.calls.allArgs()[2]).toEqual(
        ['CouponsDetailsCtrl', pubSubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function)]
      );
      tick();
      expect(getSportInstanceService.getSport).toHaveBeenCalledWith('football');
    }));

    it('should block quick-bet', fakeAsync(() => {
      couponsDetailsService.isQuickBetBlocked.and.returnValue(of(false));
      component.eventIdFromEDP = 189;
      component.ngOnInit();
      tick(100);
      expect(pubSubService.subscribe).not.toHaveBeenCalledWith('CouponsDetailsCtrl', pubSubService.API.BETSLIP_LOADED);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('CouponsDetailsCtrl', pubSubService.API.BLOCK_QUICK_BET, true);
    }));

    it('should block quick-bet', fakeAsync(() => {
      component.eventIdFromEDP = 189;
      component.ngOnInit();
      tick(100);
      expect(pubSubService.subscribe).not.toHaveBeenCalledWith('CouponsDetailsCtrl', pubSubService.API.BETSLIP_LOADED);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('CouponsDetailsCtrl', pubSubService.API.BLOCK_QUICK_BET, true);
    }));

    it('should not setTabletTopTitleWidth if device is not a tablet', () => {
      deviceService.isTablet = false;
      deviceService.isTabletLandscape = false;
      component.eventIdFromEDP = 189;
      component.ngOnInit();

      expect(component['setTabletTopTitleWidth']).not.toHaveBeenCalledTimes(2);
      expect(pubSubService.subscribe)
        .not.toHaveBeenCalledWith('CouponsDetailsCtrl', pubSubService.API.SHOW_HIDE_WIDGETS, jasmine.any(Function));
    });

    it('should subscribe for router events', fakeAsync(() => {
      component.ngOnInit();

      tick(100);

      expect(activatedRoute.snapshot.paramMap.get).toHaveBeenCalledTimes(4);
      expect(activatedRoute.snapshot.paramMap.get).toHaveBeenCalledWith('couponId');
      expect(activatedRoute.snapshot.paramMap.get).toHaveBeenCalledWith('couponName');
      expect(component.marketFilter).toEqual('');
	  	expect(component.couponFilter).toEqual('')
      expect(component.applyingParams).toBeTruthy();
      expect(component['setCouponsData']).toHaveBeenCalledTimes(2);
      expect(component['setCouponsData']).toHaveBeenCalledWith('test0');
      expect(component['setCouponsData']).toHaveBeenCalledWith('test3');
    }));

    it('should no set setCouponsData on router events', fakeAsync(() => {
      activatedRoute.snapshot.data['segment'] = undefined;
      component.ngOnInit();

      tick(100);

      expect(component['setCouponsData']).toHaveBeenCalledTimes(1);
      expect(component['setCouponsData']).toHaveBeenCalledWith('test0');
    }));

    it('should not proceed if router event is not of NavigationEnd type', fakeAsync(() => {
      router.events.subscribe = jasmine.createSpy('router.events.subscribe').and.returnValue(of({}));
      component.ngOnInit();

      tick(100);

      expect(activatedRoute.snapshot.paramMap.get).toHaveBeenCalledTimes(2);
      expect(component['setCouponsData']).toHaveBeenCalledTimes(1);
      expect(component['setCouponsData']).toHaveBeenCalledWith('test0');
    }));
  });

  describe('ngAfterViewInit', () => {
    it(`should detectChanges`, () => {
      component.ngAfterViewInit();

      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('@ngOnDestroy', () => {
    it('base flow', () => {
      optaScoreboardOverlayService.destroyOverlay= jasmine.createSpy('destroyOverlay');
      const subscriptions = [
        'routeChangeSuccessHandler', 'couponsDetailsSubscription', 'couponsListSubscription', 'sportsConfigSubscription'
      ].map((subscription: string) => {
        component[subscription] = new Subscription();
        component[subscription].unsubscribe = jasmine.createSpy(`${ subscription }.unsubscribe`);

        return component[subscription];
      });

      component.ngOnDestroy();
      expect(cacheEventsService.clearByName).toHaveBeenCalledWith('coupons');
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
      expect(footballService.unSubscribeCouponsForUpdates).toHaveBeenCalledWith('football-coupons');
      subscriptions.forEach((subscription: Subscription) => expect(subscription.unsubscribe).toHaveBeenCalled());
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('CouponsDetailsCtrl');
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.BLOCK_QUICK_BET, false);
    });

    it('should remove class from body if is homeBody', () => {
      const homeBody = {
        tagName: 'BODY'
      } as any;

      component.homeBody = homeBody;
      component.ngOnDestroy();

      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(homeBody, 'coupon-content-overlay');
    });

    it('should destroy OptaScoreboardOverlay', () => {
      component.ngOnDestroy();
      expect(optaScoreboardOverlayService.destroyOverlay).toHaveBeenCalled();
    });
    it('if subscription is not defined', () => {
      component['routeChangeSuccessHandler'] = null;
      component['couponsDetailsSubscription'] = null;
      component['couponsListSubscription'] = null;
      component['sportsConfigSubscription'] = null;
      expect(() => component.ngOnDestroy()).not.toThrow();
    });
  });

  describe('@trackById', () => {
    it('trackById should return a string', () => {
      const mockLeg = {
        id: 1
      } as ISportEvent;
      const result = component.trackById(1, mockLeg);

      expect(result).toBe('11');
    });

    it('trackByIndex should return a string', () => {
      const result = component.trackById(1, {} as any);

      expect(result).toBe('1');
    });
  });

  describe('trackByTypeId', () => {
    it('trackByTypeId should track by typeId', () => {
      const type = {
        typeId: '1',
        deactivated: true
      } as ITypeSegment;
      const result = component.trackByTypeId(1, type);

      expect(result).toBe('11true');
    });
  });

  it('@changeAccordionState', () => {
    component.changeAccordionState(1, false);

    expect(component.isExpanded).toEqual([true, false, true]);
  });

  it('@filterEvents', () => {
    component.couponEvents = couponEvents.slice();
    component.marketOptions = marketOptions;
    component.filterEvents('Match Betting');

    expect(component.marketFilter).toEqual('Match Betting');
    expect(marketSortService.setMarketFilterForMultipleSections).toHaveBeenCalledWith(component.couponEvents, 'Match Betting');
    expect(component.isEventsUnavailable).toBe(false);
    expect(couponsDetailsService.setOddsHeader).toHaveBeenCalledWith(component.marketOptions, 'Match Betting');
  });

  it('@filterCoupons', () => {
    component.couponSegments = couponSegments;
    component.filterCoupons(['Todays Matches']);
    expect(routingHelperService.encodeUrlPart).toHaveBeenCalledWith('Todays Matches');
    expect(router.navigate).toHaveBeenCalledWith(['/coupons/football/todays-matches/334']);
  });

  describe('@showCouponsList', () => {
    it('showCouponsList if it is CLOSED', () => {
      component.showCoupons = true;
      component.showCouponsList();

      expect(component.showCoupons).toBe(false);
      expect(windowRefService.document.body.scrollTop).toBe(1);
      expect(windowRefService.document.documentElement.scrollTop).toBe(1);
    });

    it('showCouponsList if it is OPENED', () => {
      component.showCoupons = false;
      component.showCouponsList();

      expect(component.showCoupons).toBe(true);
      expect(windowRefService.document.body.scrollTop).toBe(0);
      expect(windowRefService.document.documentElement.scrollTop).toBe(0);
    });
  });

  describe('goTopPage', () => {
    it('should return a promise with true', () => {
      router.navigateByUrl.and.returnValue(Promise.resolve(true));

      const result = component.goToPage('test_path');

      (result as Promise<boolean>).then((response: boolean) => {
        expect(response).toBeTruthy();
      });
      expect(router.navigateByUrl).toHaveBeenCalledWith('test_path');
    });

    it('should return false', () => {
      expect(component.goToPage('')).toBeFalsy();
      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });
  });

  describe('filteredEvents', () => {
    it('it should filter coupons events', () => {
      component.savedCouponEvents = [
        { typeName: 'type 1', deactivated: false },
        { typeName: 'type 2', deactivated: true }
      ] as ITypeSegment[];
      const result = component.filteredEvents();

      expect(result).toEqual([{ typeName: 'type 1', deactivated: false }] as ITypeSegment[]);
    });
  });

  describe('@setCouponsData', () => {
    beforeEach(() => {
      spyOn(component as any, 'getCouponsData').and.callThrough();
      spyOn(component as any, 'getCouponsListData').and.callThrough();
      spyOn(component as any, 'initCouponLeagueLinks').and.callThrough();
      couponsDetailsService.getCouponEvents.and.returnValue(of({ coupons: [{}], options: marketOptions }));
      footballService.coupons.and.returnValue(of([]));
      couponsDetailsService.groupCouponEvents.and.returnValue([]);
    });

    it('it should set coupon data for Goalscorer coupon', () => {
      component.couponId = '10';
      (component as any).setCouponsData('Goalscorer-Coupon');

      expect(component.marketOptions).toEqual([]);
      expect(couponsDetailsService.isGoalscorerCoupon).toBe(true);
      expect(footballService.unSubscribeCouponsForUpdates).toHaveBeenCalledWith('football-coupons');
      expect((component as any).getCouponsData).toHaveBeenCalledWith('Goalscorer Coupon');
      expect((component as any).getCouponsListData).toHaveBeenCalledWith();
    });

    it('it should set coupon data for Over/Under Coupon', () => {
      component.couponId = '10';
      (component as any).setCouponsData('Over / Under Total Goals');

      expect(couponsDetailsService.isGoalscorerCoupon).toBe(false);
    });

    it('it should set coupon data for UK Coupon', () => {
      component.couponId = '10';
      (component as any).setCouponsData('UK Coupon');

      expect(couponsDetailsService.isGoalscorerCoupon).toBe(false);
    });
  });

  describe('@getEventsIsUnavailable', () => {
    it('eventsIdsUnavailable should return true -> isEmptyEvents ', () => {
      component.isEmptyEvents = true;
      expect(component['getEventsIsUnavailable']).toBe(true);
    });

    it('eventsIdsUnavailable should return false -> isCustomCoupon', () => {
      couponsDetailsService.isCustomCoupon = true;
      expect(component['getEventsIsUnavailable']).toBe(false);
    });

    it('eventsIdsUnavailable should return true', () => {
      component.couponEvents = [
        {
          groupedByDate: [
            { deactivated : true },
            { deactivated : true }
          ]
        }
      ];
      expect(component['getEventsIsUnavailable']).toBe(true);
    });

    it('eventsIdsUnavailable should return false', () => {
      component.couponEvents = [
        { groupedByDate: [
            { deactivated : true },
            { deactivated : false }
          ]
        }
      ];
      expect(component['getEventsIsUnavailable']).toBe(false);
    });
  });

  describe('@setTabletTopTitleWidth', () => {
    it('setTabletTopTitleWidth', () => {
      component['setTabletTopTitleWidth']();

      expect(elementRef.nativeElement.querySelector).toHaveBeenCalled();
      expect(windowRefService.document.getElementById).toHaveBeenCalled();
      expect(domToolsService.getWidth).toHaveBeenCalled();
      expect(domToolsService.css).toHaveBeenCalledTimes(2);
    });

    it(`should return if Not couponsTopTitle`, () => {
      elementRef.nativeElement.querySelector.and.returnValue(null);

      component['setTabletTopTitleWidth']();

      expect(domToolsService.css).not.toHaveBeenCalled();
    });
  });

  describe('deleteEvent: should delete proper event', () => {
    it('deleteEvent: should delete event by id', () => {
      component.savedCouponEvents = couponEvents;
      component['deleteEvent'](5112681);
      expect(component.savedCouponEvents).toEqual([{
        typeId: 971,
        events: [{
          id: 3567838,
          typeId: 971,
        }],
        groupedByDate: [{
          events: [{
            id: 3567838
          }]
        }]
      }]);
    });

    it('deleteEvent: should delete full section', () => {
      component.savedCouponEvents = [{
        typeId: 971,
        events: [{
          id: 3567838
        }],
        groupedByDate: [{
          events: [{
            id: 3567838
          }]
        }]
      }];
      component['deleteEvent'](3567838);
      expect(component.savedCouponEvents).toEqual([{
        typeId: 971,
        events: [],
        groupedByDate: [{
          events: []
        }]
      }]);
    });

    it('deleteEvent: should not delete is section is empty', () => {
      component.couponEvents = [undefined];
      component['deleteEvent'](3567838);
      expect(component.couponEvents).toEqual([undefined]);
    });

    it('deleteEvent: should not delete is event is not exist', () => {
      component.couponEvents = [{
        typeId: 971,
        events: [{
          id: 3567838
        }],
        groupedByDate: [{
          events: [{
            id: 3567838
          }]
        }]
      }];
      component['deleteEvent'](2564839);
      expect(component.couponEvents).toEqual(component.couponEvents);
    });
  });

  describe('@getCouponName', () => {
    it('should get coupon name', () => {
      const result = component['getCouponName']('Test Coupon');

      expect(result).toBe('Test Coupon');
    });
  });

  describe('@getCouponsListData', () => {
    beforeEach(() => {
      couponsList = [
        { id: '1', couponSortCode: 'MR', name: 'UK coupon' } as any,
        { id: '2', couponSortCode: 'HH', name: 'Test-coupon' } as any
      ];
      footballService.coupons.and.returnValue(of(couponsList));
    });
    it('should get coupon list and check if BetFilter is enable', fakeAsync(() => {
      couponsDetailsService.isBetFilterEnable.and.returnValue(of(true));
      component.couponId = '2';
      (component as any).getCouponsListData();
      tick();
      expect(component.applyingList).toBeFalsy();
      expect(component.couponName).toEqual('Test coupon');
      expect(component.isBetFilterEnable).toBeTruthy();
      expect(component.couponsList).toEqual(couponsList);
    }));

    it('should get coupon list and check if BetFilter is disable', fakeAsync(() => {
      component.couponId = '1';
      couponsDetailsService.isBetFilterEnable.and.returnValue(of(false));
      (component as any).getCouponsListData();
      tick();
      expect(component.applyingList).toBeFalsy();
      expect(component.isBetFilterEnable).toBeFalsy();
      expect(component.couponsList).toEqual(couponsList);
    }));

    it('should get coupon list if error', fakeAsync(() => {
      footballService.coupons.and.returnValue(throwError(null));
      couponsDetailsService.isBetFilterEnable.and.returnValue(of(false));
      component.couponId = '1';
      (component as any).getCouponsListData();
      tick();
      expect(component.applyingList).toBeFalsy();
      expect(component.isBetFilterEnable).toBeFalsy();
      expect(component.couponsList).toEqual([]);
    }));

    it('should get coupon list if error', fakeAsync(() => {
      footballService.coupons.and.returnValue(throwError(null));
      couponsDetailsService.isBetFilterEnable.and.returnValue(of(false));
      component.couponId = '1';
      (component as any).getCouponsListData();
      tick();
      expect(component.applyingList).toBeFalsy();
      expect(component.isBetFilterEnable).toBeFalsy();
      expect(component.couponsList).toEqual([]);
    }));
  });

  describe('@getCouponsData', () => {
    beforeEach(() => {
      cmsService.getSystemConfig.and.returnValue(of({ }));
      component['initCouponLeagueLinks'] = jasmine.createSpy('initCouponLeagueLinks');
      component['loadCouponEvents'] = jasmine.createSpy('loadCouponEvents');

      couponsDetailsService.groupCouponEvents.and.returnValue([]);
    });
    it('should get coupon data if it is exist', fakeAsync(() => {
      const coupons =[{}] as any;
      const leagueLinks = [] as any;
      cmsService.getSystemConfig.and.returnValue(of({ }));
	    component['loadCouponEvents'] = jasmine.createSpy('loadCouponEvents');
      couponsDetailsService.getCouponEvents.and.returnValue(of([{ coupons, options: []}, leagueLinks]));
      component.couponId = '1';
	    component['getCouponsData']('test');
      tick();
      expect(couponsDetailsService.getCouponEvents).toHaveBeenCalledWith('1', 'test', footballService);
      expect((component as any).initCouponLeagueLinks).toHaveBeenCalledWith('1');
    }));

    it('should get coupon data if ERROR', fakeAsync(() => {
      const coupons = [{}] as any;
      component['loadCouponEvents'] = jasmine.createSpy('loadCouponEvents');
      couponsDetailsService.getCouponEvents.and.returnValue(throwError({ coupons, options: []}));
      component.couponId = '1';
      (component as any).getCouponsData('test');
      tick();
      expect(couponsDetailsService.getCouponEvents).toHaveBeenCalledWith('1', 'test', footballService);
    }));

    it('should call showError message in case of connection error', fakeAsync(() => {
      couponsDetailsService.getCouponEvents.and.returnValue(throwError({
        name: 'HttpErrorResponse'
      } as any));
      component.couponId = '1';
      spyOn(component, 'showError').and.callThrough();
      (component as any).getCouponsData('test');
      tick();
      expect(component.showError).toHaveBeenCalled();
    }));
  });

  describe('initCouponLeagueLinks', () => {
    let nextSpy, error;
    beforeEach(() => {
      error = '';
      nextSpy = jasmine.createSpy('nextSpy');
      spyOn(component as any, 'initScoreboardOverlay').and.callThrough();
      spyOn(console, 'warn');
      cmsService.getSystemConfig.and.returnValue(of({ StatisticsLinks: { leagues: true } }));
      cmsService.getCouponLeagueLinks.and.returnValue(of([
        { couponId: '1', obLeagueId: '11', dhLeagueId: '12', linkName: 'l1'}
      ]));
    });

    it('should return league links array if CMS Settings are valid and ScoreBoard overlay is initialized', () => {
      (component as any).initCouponLeagueLinks('123').subscribe(nextSpy);
      expect(cmsService.getCouponLeagueLinks).toHaveBeenCalledWith('123');
      expect((component as any).initScoreboardOverlay).toHaveBeenCalled();
      expect(nextSpy).toHaveBeenCalledWith([{ couponId: '1', obLeagueId: '11', dhLeagueId: '12', linkName: 'l1'}]);
      expect(console.warn).not.toHaveBeenCalled();
    });

    describe('should return empty array', () => {
      describe('if CMS SystemConfig', () => {
        beforeEach(() => {
          error = 'Coupon League Links are disabled in CMS';
        });
        it('has StaticsticsLinks disabled for leagues', () => {
          cmsService.getSystemConfig.and.returnValue(of({ StatisticsLinks: { leagues: false } }));
        });
        it('does not have StaticsticsLinks property', () => {
          cmsService.getSystemConfig.and.returnValue(of({ }));
        });
        it('is missing', () => {
          cmsService.getSystemConfig.and.returnValue(of(null));
        });
        it('request failed', () => {
          error = 'SystemConfig request failed';
          cmsService.getSystemConfig.and.returnValue(throwError(error));
        });
        afterEach(() => {
          (component as any).initCouponLeagueLinks('123').subscribe(nextSpy);
          expect(cmsService.getCouponLeagueLinks).not.toHaveBeenCalled();
          expect((component as any).initScoreboardOverlay).not.toHaveBeenCalled();
        });
      });
      describe('if CMS getCouponLeagueLinks request', () => {
        beforeEach(() => {
          error = `Coupon League Links are not available in CMS for the '123' couponId`;
        });
        it('is resolved as empty array', () => {
          cmsService.getCouponLeagueLinks.and.returnValue(of([]));
        });
        it('is resolved as falsy value', () => {
          cmsService.getCouponLeagueLinks.and.returnValue(of(null));
        });
        it('has failed', () => {
          error = 'CouponLeagueLinks request failed';
          cmsService.getCouponLeagueLinks.and.returnValue(throwError(error));
        });
        afterEach(() => {
          (component as any).initCouponLeagueLinks('123').subscribe(nextSpy);
          cmsService.getSystemConfig.and.returnValue(of({ }));
          expect(cmsService.getCouponLeagueLinks).toHaveBeenCalledWith('123');
          expect((component as any).initScoreboardOverlay).toHaveBeenCalled();
        });
      });

      describe('if ScoreBoard bundle', () => {
        beforeEach(() => {
          error = 'Could not initialize Scoreboard Overlay';
        });
        it('failed loading', () => {
          error = 'Scoreboard bundle request failed';
          optaScoreboardLoaderService.loadBundle.and.returnValue(throwError(error));
        });
        it('is loaded but ScoreboardOverlay element is not created', () => {
          optaScoreboardOverlayService.initOverlay.and.returnValue(null);
        });
        afterEach(() => {
          (component as any).initCouponLeagueLinks('123').subscribe(nextSpy);
          expect(cmsService.getCouponLeagueLinks).toHaveBeenCalledWith('123');
          expect((component as any).initScoreboardOverlay).toHaveBeenCalled();
        });
      });
      afterEach(() => {
        expect(nextSpy).toHaveBeenCalledWith([]);
        expect(console.warn).toHaveBeenCalledWith(error);
      });
    });
  });

  describe('@loadCouponEvents', () => {
    let leagueLinks;
    beforeEach(() => {
      spyOn(component as any, 'buildLeagueLinksMap').and.callThrough();
      spyOn(component as any, 'checkIsShowStatsEnabled').and.callThrough();
      leagueLinks = [
        { couponId: '1', obLeagueId: '11', dhLeagueId: '12', linkName: 'l1'},
        { couponId: '1', obLeagueId: '21', dhLeagueId: '22', linkName: 'l2'}
      ];
    });
    it('should get coupon data if it is exist and init MarketSelector', fakeAsync(() => {
      const events = [{  markets: [] }] as any;
      storageService.get.and.returnValue({ 'user': 'username1', 'segment': true, widget: 'couponAndMarketSwitcherWidget1'});
      couponsDetailsService.groupCouponEvents.and.returnValue(couponEvents);
      (component as any).loadCouponEvents(events, marketOptions, leagueLinks);
      tick();
      expect(component.couponEvents).toEqual(couponEvents);
      expect(component.isEmptyEvents).toBeFalsy();
      expect(component.isEventsUnavailable).toBeFalsy();
      expect(component.applyingParams).toBeFalsy();
      expect(component.hideCoupons).toBeTruthy();
      expect(couponsDetailsService.isCustomCoupon).toBeFalsy();
      expect(component.marketOptions).toEqual(marketOptions);
      expect((component as any).leagueLinksMap).toEqual({
        11: { leagueId: '12', leagueName: 'l1' },
        21: { leagueId: '22', leagueName: 'l2' }
      });
      expect(couponsDetailsService.groupCouponEvents).toHaveBeenCalledWith(events, footballService);
      expect(footballService.subscribeCouponsForUpdates).toHaveBeenCalledWith(events, 'football-coupons');
      expect((component as any).buildLeagueLinksMap).toHaveBeenCalledWith(leagueLinks);
      expect((component as any).checkIsShowStatsEnabled).toHaveBeenCalled();
    }));
    it('should get coupon data if it is exist and init MarketSelector when user same', fakeAsync(() => {
      const events = [{  markets: [] }] as any;
      storageService.get.and.returnValue({ 'user': 'username', 'segment': true, widget: 'couponAndMarketSwitcherWidget'});
      couponsDetailsService.groupCouponEvents.and.returnValue(couponEvents);
      (component as any).loadCouponEvents(events, marketOptions, leagueLinks);
      tick();
      expect(component.couponEvents).toEqual(couponEvents);
      
    }));

    it('should get coupon data if it is exist and init MarketSelector when user same with coupon-stats-widget', fakeAsync(() => {
      const events = [{  markets: [] }] as any;
      storageService.get.and.returnValue({ 'user': 'username', 'segment': true, widget: 'coupon-stats-widget'});
      couponsDetailsService.groupCouponEvents.and.returnValue(couponEvents);
      (component as any).loadCouponEvents(events, marketOptions, leagueLinks);
      tick();
      expect(component.couponEvents).toEqual(couponEvents);
      
    }));


    it('should get coupon data if it is exist and init MarketSelector when empty object', fakeAsync(() => {
      const events = [{  markets: [] }] as any;
      storageService.get.and.returnValue(null);
      couponsDetailsService.groupCouponEvents.and.returnValue(couponEvents);
      (component as any).loadCouponEvents(events, marketOptions, leagueLinks);
      tick();
      expect(component.couponEvents).toEqual(couponEvents);
      
    }));

    it('should get coupon data if it is NOT exist', fakeAsync(() => {
      const events = [] as any;
      couponsDetailsService.groupCouponEvents.and.returnValue([]);
      (component as any).loadCouponEvents(events, marketOptions, []);
      tick();
      expect(component.couponEvents).toEqual([]);
      expect(component.isEmptyEvents).toBeTruthy();
      expect(component.isEventsUnavailable).toBeTruthy();
      expect(component.applyingParams).toBeFalsy();
      expect(component.marketOptions).toEqual([]);
      expect((component as any).leagueLinksMap).toEqual({});
      expect(couponsDetailsService.groupCouponEvents).toHaveBeenCalledWith(events, footballService);
      expect(footballService.subscribeCouponsForUpdates).not.toHaveBeenCalled();
    }));
  });
  describe('getStickyElementsHeight', () => {
    it('should return 0 if no element found', () => {
      expect((component as any).getStickyElementsHeight()).toEqual(0);
    });
    it('should return sticky elements height', () => {
      windowRefService.document.querySelector = jasmine.createSpy('querySelector').and.returnValue({});
      expect((component as any).getStickyElementsHeight()).toEqual(120);
    });
  });
  describe('scrollToPreviousState', () => {
    it('should not call scrollTo in case if no element found', fakeAsync(() => {
      component.eventIdFromEDP = 189;
      (component as any).scrollToPreviousState();
      flush();
      expect(windowRefService.nativeWindow.scroll).not.toHaveBeenCalled();
    }));
    it('should scrollTo with previous state position', fakeAsync(() => {
      component.eventIdFromEDP = 189;
      windowRefService.document.querySelector = jasmine.createSpy('querySelector').and.returnValue({});
      (component as any).scrollToPreviousState();
      flush();
      expect(windowRefService.nativeWindow.scroll).toHaveBeenCalledWith(0, 0);
    }));
  });
  describe('updatePreviousStateInfo', () => {
    beforeEach(() => {
      component.couponEvents = couponEvents;
      component.isExpanded[0] = false;
    });
    it('should set eventIdFromEDP if previous URL is EDP', () => {
      const edpUrl = '/event/football/football-england/championship/event-v-test/3567838/all-markets';
      routingState.getPreviousSegment = jasmine.createSpy('getPreviousSegment').and.returnValue('eventMain');
      routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue(edpUrl);
      (component as any).updatePreviousStateInfo();
      expect(component.eventIdFromEDP).toEqual(3567838);
      expect(component.isExpanded[0]).toBeTruthy();
    });
    it('should no set eventIdFromEDP if event not found', () => {
      const edpUrl = '/event/football/football-england/championship/event-v-test/134213/all-markets';
      routingState.getPreviousSegment = jasmine.createSpy('getPreviousSegment').and.returnValue('eventMain');
      routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue(edpUrl);
      (component as any).updatePreviousStateInfo();
      expect(component.eventIdFromEDP).not.toBeDefined();
      expect(component.isExpanded[0]).toBeFalsy();
    });
    it('should no set eventIdFromEDP if link is wrong', () => {
      const edpUrl = '/event/football/football-england/championship/event-v-test/';
      routingState.getPreviousSegment = jasmine.createSpy('getPreviousSegment').and.returnValue('eventMain');
      routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue(edpUrl);
      (component as any).updatePreviousStateInfo();
      expect(component.eventIdFromEDP).not.toBeDefined();
      expect(component.isExpanded[0]).toBeFalsy();
    });
    it('should no set eventIdFromEDP if page not EDP', () => {
      const edpUrl = '/event/football/football-england/championship/event-v-test/';
      routingState.getPreviousSegment = jasmine.createSpy('getPreviousSegment').and.returnValue('HR_LP');
      routingState.getPreviousUrl = jasmine.createSpy('getPreviousUrl').and.returnValue(edpUrl);
      (component as any).updatePreviousStateInfo();
      expect(component.eventIdFromEDP).not.toBeDefined();
      expect(component.isExpanded[0]).toBeFalsy();
    });
  });

  describe('handleMatchesMarketSelectorEvent', () => {
    beforeEach(() => {
      spyOn(component, 'filterEvents').and.callThrough();
    });

    it('should filter events', () => {
      component.handleMatchesMarketSelectorEvent({ output: 'filterChange', value: {} });
      expect(component.filterEvents).toHaveBeenCalled();
    });

    it('should not filter events', () => {
      component.handleMatchesMarketSelectorEvent({ output: 'test', value: {} });
      expect(component.filterEvents).not.toHaveBeenCalled();
    });
  });

  describe('openLeagueTable', () => {
    beforeEach(() => {
      (component as any).leagueLinksMap = {
        438: { leagueId: '456', leagueName: 'league' }
      };
      const events = {
        typeId: '438',
        events: [{
          typeName: 'FA Cup',
          categoryId: '16',
          typeId: 438
        }]
      };
      // @ts-ignore
      component.openLeagueTable(events);
    });
    it('should set Scoreboard Overlay data', () => {
      expect(optaScoreboardOverlayService.setOverlayData).toHaveBeenCalledWith({
        overlayKey: 'leagueTable', data: { leagueId: '456', leagueName: 'league' }
      });
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'in-line stats',
        eventAction: 'league table',
        eventLabel: 'FA Cup',
        categoryID: '16',
        typeID: '438'
      }]);
      expect(optaScoreboardOverlayService.showOverlay).toHaveBeenCalled();
    });
  });

  describe('@onexpand ', () => {
    beforeEach(()=>
    {
     component.availableIds=['sdm-scoreboard3','sdm-scoreboard4','sdm-scoreboard5']
    });
    const event1 = {
      isCouponScoreboardOpened: false,
      cashoutAvail: '',
      categoryCode: '',
      categoryId: '',
      categoryName: '',
      displayOrder: 0,
      eventSortCode: '',
      eventStatusCode: '',
      id: 0,
      liveServChannels: '',
      liveServChildrenChannels: '',
      typeId: '',
      typeName: '',
      name: '',
      startTime: '',
      couponStatId: 'sdm-scoreboard1'
    };
    const event2 = Object.assign({}, event1);
    const event3 = Object.assign({}, event1);
    const event4 = Object.assign({}, event1);
    const event5 = Object.assign({}, event1);
    const event6 = Object.assign({}, event1);
    event1.isCouponScoreboardOpened = true;
    event2.isCouponScoreboardOpened = true;
    event2.id = 2;
    event3.isCouponScoreboardOpened = true;
    event3.id = 3;
    event4.isCouponScoreboardOpened = true;
    event4.id = 4;
    event5.isCouponScoreboardOpened = true;
    event5.id = 5;
    event6.isCouponScoreboardOpened = false;
    event6.id = 6;
    const dummyPreviousTag = document.createElement('div');
    dummyPreviousTag.id = event1.couponStatId;
    document.getElementById = jasmine.createSpy('html element').and.returnValue(dummyPreviousTag);
    it('isCouponScoreboardOpened should become true', () => {

      event1.isCouponScoreboardOpened = false;
      component.onExpand(event1);
      expect(component.couponStatOpenedEvents.length).toEqual(1);
      expect(event1.isCouponScoreboardOpened).toBe(true);
    });
    it('should  remove the passed event from couponstatOpenedEvents', () => {
      component.couponStatOpenedEvents = [event1, event2, event4, event5];
      component.onExpand(event4);
      expect(component.couponStatOpenedEvents).toEqual([event1, event2, event5]);

    });

    it('should remove first event in couponStatOpenedEvents if morethan 5 events', () => {
      component.couponStatOpenedEvents = [event1, event2, event3, event4, event5];
      component.onExpand(event6);
      expect(component.couponStatOpenedEvents).toEqual([event2, event3, event4, event5, event6]);
    });


    it('should  call closeFirstOpenedBoard and sendGTMData methods', () => {
      spyOn(component as any, 'closeFirstOpenedBoard');
      event1.isCouponScoreboardOpened = true;
      event2.isCouponScoreboardOpened = true;
      event3.isCouponScoreboardOpened = true;
      event4.isCouponScoreboardOpened = true;
      event5.isCouponScoreboardOpened = true;
      event6.isCouponScoreboardOpened = false;
      component.couponStatOpenedEvents = [event1, event2, event3, event4, event5];
      component.onExpand(event6);
      expect(component.closeFirstOpenedBoard).toHaveBeenCalled();
    });

    it('return true if same username', () => {
      storageService.get.and.returnValue({ 'user': 'username', 'segment': true});
      component.onExpand(event1);
      expect(storageService.get).not.toHaveBeenCalledWith('OnBoardingCSW');
    });
    
    it('return false if same username', () => {
      storageService.get.and.returnValue({ 'user': 'username1', 'segment': true});
      component.onExpand(event1);
      expect(storageService.get).toHaveBeenCalledWith('OnBoardingCSW');
    });

    it('should call initElements', () => {
      spyOn(component as any, 'initElements');
      windowRefService.nativeWindow.setTimeout.and.callFake(cb => {
        cb(); // call setTimeout callback
      });
      component.onExpand(event1);
      expect(component.homeBody).toBeDefined;
    });
    it('should  call closeFirstOpenedBoard', () => {
      component.availableIds = [];
      component.couponStatOpenedEvents = [
        {couponStatId: 1, isCouponScoreboardOpened: 2},
        {couponStatId: 1, isCouponScoreboardOpened: 2}
      ];
      component.closeFirstOpenedBoard();
      expect(component.availableIds.length).toBe(1);

    });
    it('isCouponScoreboardOpened should become true and username same', () => {

      event1.isCouponScoreboardOpened = false;
      storageService.get.and.returnValue({ 'user': 'username', 'segment': true, widget: 'couponAndMarketSwitcherWidget'});
      component.onExpand(event1);
      expect(component.couponStatOpenedEvents.length).toEqual(1);
      expect(event1.isCouponScoreboardOpened).toBe(true);
    });
  });
  describe('sendGtm', () => {
    const event = {
      isCouponScoreboardOpened: false,
      cashoutAvail: '',
      categoryCode: '',
      categoryId: '',
      categoryName: '',
      displayOrder: 0,
      eventSortCode: '',
      eventStatusCode: '',
      id: 0,
      liveServChannels: '',
      liveServChildrenChannels: '',
      typeId: '',
      typeName: '',
      name: '',
      startTime: '',
      couponStatId: 'sdm-scoreboard1'
    };
    it("Should  send gtm data  when more than 5 is false", () => {
      const gtmData = {
        event: 'trackEvent',
        eventAction: 'click',
        eventCategory: 'coupon stats widget',
        eventLabel: 'hide stats',
        categoryID: '16',
        typeID: '25230',
        eventID: 1
      };
      event.categoryId = '16';
      event.id = 1;
      event.typeId = '25230';
      event.isCouponScoreboardOpened = true;
      component.sendGTMData(event);
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    })
  });

  describe('@getShowStatsIncludedLeagues', () => {
    beforeEach(() => {
      cmsService.getSystemConfig.and.returnValue(of({ CouponStatsWidget:{"402":true,"971" :true}}));
    });
    it('it should get the leaugeids from cms ', () => {
      component['getShowStatsIncludedLeagues']();
      expect(component.includedLeagues).toEqual(['402','971']);
    });
  });

  describe('check is showstats enabled', () => {

    it('isShowStatsEnabled of events to be true', () => {
      component.couponEvents = [{
        typeId: 971,
        events: [{
          id: 5112681,
          typeId: 971,
          isShowStatsEnabled: false,
          startTime:'1666204200000',
          markets: [{
            title: 'Match Result',
            templateMarketName: 'Match Betting',
            header: ['Home', 'Draw', 'Away'],
            hidden:false,
            outcomes: [{
              "id": "1785252862",
              "marketId": "558972199"
            }]
          }]
        }]
      }];
      spyOn(component as any, 'getdaysToEventStart').and.returnValue(6);
      footballService.isFootball=true;
      component.includedLeagues=['402','971'];
      component['checkIsShowStatsEnabled']();
      expect(component.couponEvents[0].events[0].isShowStatsEnabled).toBeTrue();
    });
  });

  describe('initElements', () => {
    it('if isWrapper returns true', () => {
      deviceService.isWrapper = true;
      (component as any).initElements();
      component.homeBody = {} as any;
      windowRefService.document.querySelector.and.returnValue({});
      expect(deviceService.isWrapper).toBeTruthy;
      expect(windowRefService.document.querySelector).toHaveBeenCalledTimes(1);
    })
  })

  describe('isDisplay', () => {
   it('returns true', () => {
    (component as any).isDisplay();
    component.isDisplay();
    expect(component.isDisplayed).toBeTruthy;
   })
  })
  
  describe('imageclose', () => {
    const onboardingOverlay = {
      imageLabel: 'string',
      buttonText: 'string',
      imageUrl: 'string',
      isEnable: true,
      directFileUrl: 'string',
      useDirectFileUrl: true
    }

    it('when imageclose is called', () => {
      component.onboardingCoupon = onboardingOverlay;
      const location = 'CTA';
      component.widgetType = COUPONS_WIDGET;
      (component as any).imageclose(location);
      expect(component.isShowDiv).toBeTruthy;
      expect(component.showOnboardingOverlay).toBeFalsy;
      (component as any).setGtmData
      expect(rendererService.renderer.removeClass).toHaveBeenCalledTimes(0);
      component.widgetType = GA_COUPON_STATS_WIDGET;
      (component as any).imageclose(location);
      expect(component.isShowDiv).toBeTruthy;
      expect(component.showOnboardingOverlay).toBeFalsy;
    })

    it('when location equal to close', () => {
      const location = 'close';
      component.widgetType = COUPONS_WIDGET;
      (component as any).imageclose(location);
      (component as any).setGtmData
      expect(component.isShowDiv).toBeTruthy;
    })
  });

  describe('getOnboardingOverlayCMS', () => {
    const onboardingOverlay = 
      {
        isEnable: true
      }

    it('showOnBoardingOverlay returns true', () => {
      component.showOnboardingOverlay = true;
      (component['getOnboardingOverlayCMS'] as any)();
      expect(cmsService.getOnboardingOverlay).toHaveBeenCalled();
      expect(storageService.set).toHaveBeenCalledTimes(1);
    })

    it('ShowOnBoardingOvelay returns false', () => {
      component.showOnboardingOverlay = false;
        cmsService.getOnboardingOverlay = jasmine.createSpy('getOnboardingOverlay').and.returnValue(throwError({ status: 404 }));
        (component['getOnboardingOverlayCMS'] as any)();
        expect(storageService.set).not.toHaveBeenCalled();
        
    });
  });

  describe('@getdaysToEventStart',()=>
  {
    timeService = {
      daysDifference: jasmine.createSpy('daysDifference').and.returnValue(-6)
    };
   const  e={
      startTime:'1666204200000'
    } as any;
    it('should return 6 ',()=>
    {
     expect(component['getdaysToEventStart'](e)).toBe(6);
    })
  })
  describe('@removeAllWidgetsFromDom',()=>
  {
    beforeEach(()=>
    {
     component.availableIds=['sdm-scoreboard3','sdm-scoreboard4','sdm-scoreboard5']
    });
    const event1 = {
      isCouponScoreboardOpened: false,
      cashoutAvail: '',
      categoryCode: '',
      categoryId: '',
      categoryName: '',
      displayOrder: 0,
      eventSortCode: '',
      eventStatusCode: '',
      id: 0,
      liveServChannels: '',
      liveServChildrenChannels: '',
      typeId: '',
      typeName: '',
      name: '',
      startTime: '',
      couponStatId: 'sdm-scoreboard1'
    };
    event1.isCouponScoreboardOpened = true;
    const dummyPreviousTag = document.createElement('div');
    dummyPreviousTag.id = event1.couponStatId;
    document.getElementById = jasmine.createSpy('html element').and.returnValue(dummyPreviousTag);
   
    it('should become empty ', () => {
      component.couponStatOpenedEvents = [event1];
      component.removeAllWidgetsFromDom();
      expect(component.couponStatOpenedEvents).toEqual([]);
    });
  })
  
  describe('@removeTagFromDom',()=>
  {
    beforeEach(()=>
    {
     component.availableIds=['sdm-scoreboard3','sdm-scoreboard4','sdm-scoreboard5']
    });
    const event1 = {
      id: 987654,
      couponStatId: 'sdm-scoreboard1'
    } as any;
    const dummyPreviousTag = document.createElement('div');
    dummyPreviousTag.id = 'spin987654';
    document.getElementById = jasmine.createSpy('html element').and.returnValue(dummyPreviousTag);
   
    it('should remove  spinner div ', () => {
      component['removeTagFromDom'](event1);
      expect(dummyPreviousTag.id).toBe('spin987654');
    });
  })
});
