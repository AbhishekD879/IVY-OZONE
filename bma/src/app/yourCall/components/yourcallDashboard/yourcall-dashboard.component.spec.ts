import { YourcallDashboardComponent } from './yourcall-dashboard.component';
import { of, Subject } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

describe('YourcallDashboardComponent', () => {
  let component: YourcallDashboardComponent;
  let windowRefService;
  let userService;
  let accountUpgradeLinkService;
  let rendererService;
  let elementRef;
  let pubSubService;
  let domToolsService;
  let commandService;
  let localeService;
  let yourcallMarketsService;
  let deviceService;
  let yourcallDashboardService;
  let bybSelectedSelectionsService;

  const title = 'YOUR_CALL';
  const dashboardItemsUpdate$ = new Subject<void>();

  beforeEach(() => {
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen')
      }
    } as any;

    elementRef = {
      nativeElement: {
        querySelector: (section) => {
          return section;
        }
      }
    } as any;

    pubSubService = {
      API: {
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        YC_DASHBOARD_DISPLAYING_CHANGED: 'YC_DASHBOARD_DISPLAYING_CHANGED',
        YC_MARKET_TOGGLED: 'YC_MARKET_TOGGLED',
        YC_NOTIFICATION_TOGGLED: 'YC_NOTIFICATION_TOGGLED',
        OPEN_LOGIN_DIALOG: 'OPEN_LOGIN_DIALOG',
        QUICK_SWITCHER_ACTIVE: 'QUICK_SWITCHER_ACTIVE'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg1, arg2, cb) => cb && cb({})),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy()
    } as any;

    domToolsService = {
      getHeight: jasmine.createSpy().and.returnValue(1000),
      getOffset: jasmine.createSpy().and.returnValue({top: 20}),
      getWidth: jasmine.createSpy().and.returnValue('100%'),
      css: jasmine.createSpy('css'),
      scrollTop: jasmine.createSpy('scrollTop'),
      getScrollTop: jasmine.createSpy('getScrollTop').and.returnValue(200)
    } as any;

    commandService = {
      API: {
        TOGGLE_FOOTER_MENU: 'TOGGLE_FOOTER_MENU'
      },
      executeAsync: jasmine.createSpy('executeAsync')
    } as any;

    localeService = {
      getString: jasmine.createSpy('localeService').and.returnValue('yourCall.dashboardAlert')
    } as any;

    yourcallMarketsService = {
      markets: [],
      removeSelection: jasmine.createSpy('removeSelection'),
      trackMarketEditingSelection: jasmine.createSpy('trackMarketEditingSelection'),
      updatedPlayersubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      updatedStatsubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      updatedStatValsubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      playerBetRemovalsubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      showBetRemovalsubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      betRemovalsubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      oldNewplayerStatIdsubject$: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      goalscorerSubject$: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      selectedSelectionsSet: new Set()
    } as any;

    deviceService = {
      isMobileOrigin: false,
      isTablet: false,
      isDesktop: true
    } as any;

    yourcallDashboardService = {
      items: [
        {
          id: '1212',
          getTitle: () => 'title1',
          getMarketTitle: () => 'marketTitle1',
          getSelectionTitle: () => 'selectionTitle1'
        },
        {
          id: '3521',
          getTitle: () => 'title2',
          getMarketTitle: () => 'marketTitle2',
          getSelectionTitle: () => 'selectionTitle2'
        }
      ],
      odds: '1/2',
      canPlaceBet: jasmine.createSpy('canPlaceBet'),
      validSelectionCount: jasmine.createSpy('validSelectionCount').and.returnValue(false),
      trackAddToQuickBetSlip: jasmine.createSpy('trackAddToQuickBetSlip'),
      trackBoardRemovingSelection: jasmine.createSpy('trackBoardRemovingSelection'),
      isErrorMsg: false,
      isButtonAvailable: true,
      error: true,
      errorMessage: 'errorMessage',
      valid: true,
      loading: true,
      isBetslipLoading: true,
      dashboardItemsUpdate$,
      dashboardItems$: dashboardItemsUpdate$.asObservable()
    } as any;

    userService = {
      username: 'testUser',
      isInShopUser: () => false
    } as any;

    windowRefService = {
      nativeWindow: {
        innerHeight: 10,
        pageYOffset: 20,
        location: {
          href: ''
        }
      }
    };

    accountUpgradeLinkService = {
      inShopToMultiChannelLink: () => false
    };

    bybSelectedSelectionsService = {
      callGTM: jasmine.createSpy('callGTM').and.callFake(({}, {})=> false),
      duplicateIdd: new Set()
  };

    component = new YourcallDashboardComponent(
      windowRefService,
      elementRef,
      rendererService,
      deviceService,
      pubSubService,
      commandService,
      domToolsService,
      yourcallDashboardService,
      yourcallMarketsService,
      localeService,
      userService,
      accountUpgradeLinkService,
      bybSelectedSelectionsService
    );

    component['element'] = {
      querySelector: jasmine.createSpy().and.returnValue({}),
      getBoundingClientRect: jasmine.createSpy().and.returnValue({
        left: 20
      })
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#relocate', () => {
    it('should should call relocate method when element is sticky', () => {
      component.relocate();
      expect(domToolsService.css).toHaveBeenCalledWith({}, {
        position: 'fixed',
        left: 20,
        bottom: 0,
        width: '100%'
      });
    });

    it('should should call relocate method when element is not sticky', () => {
      component['windowRefService'].nativeWindow.pageYOffset = 2000;
      component.relocate();

      expect(domToolsService.css).toHaveBeenCalledWith({}, {
        position: 'relative',
        left: 'auto',
        bottom: 'auto',
        width: '100%'
      });
    });
  });

  describe('#checkAlertMessage', () => {
    it('Should clears alert notification state', () => {
      component.alert = true;
      component['checkAlertMessage'](true);

      expect(component.alert).toEqual(false);
    });

    it('Should perform validity check of selected bets ', () => {
      component.expanded = true;
      component['checkAlertMessage'](false);

      expect(component.alert).toEqual(true);
    });
  });

  describe('#placeBet', () => {
    it('@placeBet should NOT be called for already logged-in in-shop users', () => {
      Object.defineProperty(component['userService'], 'status', { get: () => null , configurable: true});
      Object.defineProperty(component['accountUpgradeLinkService'], 'inShopToMultiChannelLink', { get: () => 'http://ffs.com' });
      component['userService'].isInShopUser = () => true;

      const disableDoneButtonSpy = spyOnProperty(component, 'disableDoneButton', 'get').and.returnValue(false);
      const userServiceStatusSpy = spyOnProperty(component['userService'], 'status', 'get').and.returnValue(false);

      component.placeBet();

      expect(component['windowRefService'].nativeWindow.location.href).toEqual('http://ffs.com');
      expect(disableDoneButtonSpy).not.toHaveBeenCalled();
      expect(userServiceStatusSpy).not.toHaveBeenCalled();
      expect(component['yourcallDashboardService'].trackAddToQuickBetSlip).not.toHaveBeenCalled();
    });

    it('@placeBet should NOT be called when disableDoneButton is true and user is NOT logged-in and NOT in-shop user', () => {
      Object.defineProperty(component['userService'], 'status', { get: () => null,configurable: true });

      const disableDoneButtonSpy = spyOnProperty(component, 'disableDoneButton', 'get').and.returnValue(true);
      const userServiceStatusSpy = spyOnProperty(component['userService'], 'status', 'get').and.returnValue(true);

      component.placeBet();
      expect(disableDoneButtonSpy).toHaveBeenCalled();
      expect(userServiceStatusSpy).not.toHaveBeenCalled();
    });

    it(`@placeBet should NOT be called when disableDoneButton is false and user is NOT logged-in and NOT in-shop user`, () => {
      Object.defineProperty(component['userService'], 'status', { get: () => null,configurable: true });

      const disableDoneButtonSpy = spyOnProperty(component, 'disableDoneButton', 'get').and.returnValue(false);
      const userServiceStatusSpy = spyOnProperty(component['userService'], 'status', 'get').and.returnValue(false);

      component.placeBet();
      expect(disableDoneButtonSpy).toHaveBeenCalled();
      expect(userServiceStatusSpy).toHaveBeenCalled();
      expect(component['yourcallDashboardService'].trackAddToQuickBetSlip).toHaveBeenCalledWith('click odds', false);
      expect(component['pubsubService'].publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'header' });
    });

    it('@placeBet should be called when disableDoneButton is false and user is logged-in and NOT in-shop user', () => {
      Object.defineProperty(component['userService'], 'status', { get: () => null,configurable: true });

      const disableDoneButtonSpy = spyOnProperty(component, 'disableDoneButton', 'get').and.returnValue(false);
      const userServiceStatusSpy = spyOnProperty(component['userService'], 'status', 'get').and.returnValue(true);

      component.placeBet();
      expect(disableDoneButtonSpy).toHaveBeenCalled();
      expect(userServiceStatusSpy).toHaveBeenCalled();
      // expect(component['yourcallDashboardService'].trackAddToQuickBetSlip).toHaveBeenCalled();
      expect(component['pubsubService'].publish).toHaveBeenCalled();
    });

    it('@placeBet event.stopPropagation', () => {
      Object.defineProperty(component['userService'], 'status', { get: () => null,configurable: true });

      const disableDoneButtonSpy = spyOnProperty(component, 'disableDoneButton', 'get').and.returnValue(false);
      const userServiceStatusSpy = spyOnProperty(component['userService'], 'status', 'get').and.returnValue(true);

      component.placeBet({
        stopPropagation: () => {}
      } as any);
      expect(disableDoneButtonSpy).toHaveBeenCalled();
      expect(userServiceStatusSpy).toHaveBeenCalled();
      // expect(component['yourcallDashboardService'].trackAddToQuickBetSlip).toHaveBeenCalled();
      expect(component['pubsubService'].publish).toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    beforeEach(() => {
      component['unsubscribe$'] = {
        next: jasmine.createSpy('next'),
        complete: jasmine.createSpy('complete')
      } as any;
    });

    it('ngOnDestroy', () => {
      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(1);
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(title);
      expect(component['unsubscribe$']['next']).toHaveBeenCalled();
      expect(component['unsubscribe$']['complete']).toHaveBeenCalled();
    });

    it('ngOnDestroy remove listeners', () => {
      component.windowScrollListener = () => {};
      component.windowResizeListener = () => {};
      component.elementClickListener = () => {};

      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(title);
      expect(component['unsubscribe$']['next']).toHaveBeenCalled();
      expect(component['unsubscribe$']['complete']).toHaveBeenCalled();
    });
  });


  describe('#ngOnInit', () => {
    it('ngOnInit', () => {
      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledTimes(5);
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.SUCCESSFUL_LOGIN, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.QUICK_SWITCHER_ACTIVE, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.YC_DASHBOARD_DISPLAYING_CHANGED, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.YC_MARKET_TOGGLED, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.YC_NOTIFICATION_TOGGLED, jasmine.any(Function));
    });

    it('ngOnInit for rendererService listeners', () => {
      component['unauthorizedFail'] = true;
      component.document = {
        body: 'body'
      };
      rendererService.renderer.listen.and.callFake((a, b, cd) => {
        cd && cd({
          target: {
            nodeName: 'select'
          }
        });
      });
      deviceService.isIos = true;

      component.ngOnInit();

      expect(rendererService.renderer.listen).toHaveBeenCalledTimes(3);
      expect(domToolsService.scrollTop).toHaveBeenCalledWith('body', 200);
      expect(domToolsService.getScrollTop).toHaveBeenCalledWith('body');
      expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.TOGGLE_FOOTER_MENU, [false], []);
    });

    it('ngOnInit should handle dashboard items update', () => {
      component['handleDashboardItemsUpdate'] = jasmine.createSpy();
      component.ngOnInit();
      component['yourcallDashboardService']['dashboardItemsUpdate$'].next();
      expect(component['handleDashboardItemsUpdate']).toHaveBeenCalled();
    });

    it('playerId without value', fakeAsync(() => {
      yourcallMarketsService.updatedPlayersubject$ = new Subject<any>();
      component.ngOnInit();
      yourcallMarketsService.updatedPlayersubject$.next({ updatedPlayerId: {} });
      tick();
      expect(component.newPlayer).toEqual(undefined);
    }));

    it('statId without value', fakeAsync(() => {
      yourcallMarketsService.updatedPlayersubject$ = new Subject<any>();
      component.ngOnInit();
      yourcallMarketsService.updatedPlayersubject$.next({ updatedStatId: {} });
      tick();
      expect(component.newStat).toEqual(undefined);
    }));

    it('statId without value', fakeAsync(() => {
      yourcallMarketsService.updatedPlayersubject$ = new Subject<any>();
      component.ngOnInit();
      yourcallMarketsService.updatedPlayersubject$.next({ selection: {} });
      tick();
      expect(component.newStatVal).toEqual(undefined);
    }));

    it('playerId with value', fakeAsync(() => {
      yourcallMarketsService.updatedPlayersubject$ = new Subject<any>();
      component.ngOnInit();
      yourcallMarketsService.updatedPlayersubject$.next({ updatedPlayerId: { id: 1 } });
      tick();
      expect(component.newPlayer).toEqual(1);
    }));
    it('statId with value', fakeAsync(() => {
      yourcallMarketsService.updatedPlayersubject$ = new Subject<any>();
      component.ngOnInit();
      yourcallMarketsService.updatedPlayersubject$.next({ updatedStatId: { id: 8 } });
      tick();
      expect(component.newStat).toEqual(8);
    }));
    it('sataValId with value', fakeAsync(() => {
      yourcallMarketsService.updatedPlayersubject$ = new Subject<any>();
      component.ngOnInit();
      yourcallMarketsService.updatedPlayersubject$.next({ updatedStatValId: 2 });
      tick();
      expect(component.newStatVal).toEqual(2);
    }));

    it('sataValId with no selection', fakeAsync(() => {
      yourcallMarketsService.updatedPlayersubject$ = new Subject<any>();
      component.ngOnInit();
      yourcallMarketsService.updatedPlayersubject$.next();
      tick();
      expect(component.newStatVal).toBeUndefined();
    }));
    it('should call setFooterVisibility with true when state is false', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((QUICK_SWITCHER_ACTIVE, listeners, handler) => {
        if (listeners == 'QUICK_SWITCHER_ACTIVE') {
          handler();
        }
      });
      component['setFooterVisibility'] = jasmine.createSpy('setFooterVisibility');
      component.ngOnInit();
      tick();
      expect(component['setFooterVisibility']).toHaveBeenCalledWith(false);
    }));
  });

  describe('#trackByDashboard', () => {
    it('should call trackByDashboard method', () => {
     const result = component.trackByDashboard(1, {
       market: { id: '7879' },
       selection: { id: '8732' }
     } as any);

     expect(result).toEqual('7879_8732');
   });
  });

  describe('#disableDoneButton', () => {
    it('should get disableDoneButton property', () => {
      expect(component.disableDoneButton).toEqual(true);
    });
  });

  describe('#toggle', () => {
    it('should call toggle method', () => {
      expect(component.expanded).toEqual(true);

      component.toggle();

      expect(component.expanded).toEqual(false);
    });

    it('should call toggle method with true', () => {
      expect(component.expanded).toEqual(true);
      component.expanded = false;
      component.toggle();
      expect(component.expanded).toEqual(true);
    });
  });

  describe('#markets', () => {
    it('should get markets', () => {
      expect(component.markets).toEqual([]);
    });
  });

  describe('#isEnabled', () => {
    it('should get enabled', () => {
      yourcallDashboardService.items = [];

      expect(component['isDashboardEnabled']()).toBeFalsy();
    });
  });

  describe('#counter', () => {
    it('getCounter', () => {
      yourcallDashboardService.items = [
        { id: '1212', getTitle: () => 'title1' },
        { id: '3521', getTitle: () => 'title2' }
      ];

      expect(component['getCounter']()).toEqual(2);
    });
  });

  describe('#errorMessage', () => {
    it('should get errorMessage', () => {
      expect(component.errorMessage).toEqual('errorMessage');

      yourcallDashboardService.error = false;
      component.alert = true;

      expect(component.errorMessage).toEqual('yourCall.dashboardAlert');

      yourcallDashboardService.error = false;
      component.alert = false;

      expect(component.errorMessage).toEqual('');
    });
  });

  describe('#isValid', () => {
    it('isDashboardValid', () => {
      expect(component['isDashboardValid']()).toEqual(true);
    });
  });

  describe('#hasErrors', () => {
    it('should call hasErrors method alert = true', () => {
      component.alert = true;
      const result = component.hasErrors();

      expect(result).toEqual(true);
    });

    it('should call hasErrors method yourcallDashboardService.error = true', () => {
      component.alert = false;
      yourcallDashboardService.error = true;
      const result = component.hasErrors();

      expect(result).toEqual(true);
    });

    it('should call hasErrors method all properties = false', () => {
      component.alert = false;
      yourcallDashboardService.valid = false;
      yourcallDashboardService.error = false;
      const result = component.hasErrors();

      expect(result).toEqual(true);
    });
  });

  describe('#hideFooter', () => {
    it('should call hideFooter method with callback', () => {
      component.hideFooter(true, () => {});

      expect(component.animate).toEqual(false);
      expect(component.showDashboard).toEqual(false);
    });

    it('should call hideFooter method without callback', () => {
      component.hideFooter(true);

      expect(component.animate).toEqual(false);
      expect(component.showDashboard).toEqual(false);
    });
  });

  describe('#canDisplayOdds', () => {
    it('should get canDisplayOdds', () => {
      yourcallDashboardService.canPlaceBet.and.returnValue(false);
      expect(component.canDisplayOdds).toEqual(false);
      expect(yourcallDashboardService.canPlaceBet).toHaveBeenCalled();

      yourcallDashboardService.canPlaceBet.and.returnValue(true);
      yourcallDashboardService.valid = false;
      expect(component.canDisplayOdds).toEqual(false);

      yourcallDashboardService.canPlaceBet.and.returnValue(true);
      yourcallDashboardService.valid = true;
      yourcallDashboardService.error = true;
      expect(component.canDisplayOdds).toEqual(false);
    });
  });

  describe('#odds', () => {
    it('should get odds', () => {
      yourcallDashboardService.odds = '1/2';
      expect(component.odds).toEqual('1/2');
    });
  });

  describe('#oddsLoading', () => {
    it('should get oddsLoading', () => {
      expect(component.oddsLoading).toEqual(true);

      yourcallDashboardService.loading = false;
      expect(component.oddsLoading).toEqual(true);
    });
  });

  describe('#listHeight', () => {
    it('should get listHeight', () => {
      expect(component['getListHeight']()).toEqual({
        'height': '0px',
        'max-height': '180px'
      });
    });
  });

  describe('#brief', () => {
    it('should get brief', () => {
      expect(component['getBriefDescriptionText']()).toEqual('title1, title2');
    });
  });

  describe('#getMarketTitle', () => {
    it('should call getMarketTitle method', () => {
      const result = component['getMarketTitle']({ getMarketTitle: () => 'MarketTitle'} as any);

      expect(result).toEqual('MarketTitle');
    });
  });

  describe('#getSelectionTitle', () => {
    it('should call getSelectionTitle method', () => {
      const result = component['getSelectionTitle']({ getSelectionTitle: () => 'SelectionTitle' } as any);

      expect(result).toEqual('SelectionTitle');
    });
  });

  describe('#removeSelection', () => {
    it('should call removeSelection method with _counter = 0', () => {
      component.expanded = true;
      spyOn(component, 'callGTM');
      component.removeSelection({
        selection: {},
        market: {
          title: 'title'
        }
      } as any);
      expect(yourcallMarketsService.removeSelection).toHaveBeenCalledWith({
        title: 'title'
      }, {});
      // expect(yourcallDashboardService.trackBoardRemovingSelection).toHaveBeenCalledWith('title');
      expect(component.expanded).toEqual(false);
    });

    it('should call removeSelection method with _counter = 2', () => {
      expect(component['getCounter']()).toEqual(2);
      spyOn(component, 'callGTM');
      component.removeSelection({
        selection: {},
        market: {
          title: 'title'
        }
      } as any);

      expect(yourcallMarketsService.removeSelection).toHaveBeenCalledWith({
        title: 'title'
      }, {});
      // expect(yourcallDashboardService.trackBoardRemovingSelection).toHaveBeenCalledWith('title');
    });

    it('should get playerstat id for removeSelected', () => {
     const selected={
      selection:{
        marketType:'playerBets',
        playerId:1,
        statisticId:8,
        value:2
      },
      market:{
        key:'playerBets'
      }
     }
     const obj={
      playerId:1
     }
    spyOn(component,'callGTM');
     component.removeSelection(selected as any);
     expect(yourcallMarketsService.lastRemovedMarket).toBe('1-8-2');
     expect(obj.playerId).toBe(1);
    });

    it('should get playerstat id if idd with value', () => {
     const selected={
      selection:{
        marketType:'playerBets',
        idd:'1-6-2',
        playerId:1,
        statisticId:6,
        value:2
      },
      market:{
        key:'playerBets'
      }
     }
    spyOn(component,'callGTM');
      component.removeSelection(selected as any)
     expect(yourcallMarketsService.lastRemovedMarket).toBe('1-6-2');
    });

    it('should get playerstat id if idd with value', () => {
     const selected={
      selection:{
        marketType:'',
        idd:'1 - 6',
        id:1,
        playerId:1,
        statisticId:6,
        value:2
      },
      market:{
        key:''
      }
     }
    spyOn(component,'callGTM');
      component.removeSelection(selected as any)
     expect(yourcallMarketsService.lastRemovedMarket).toBe(1);
    });

    it('should call removeSelection undefined', () => {
      component.expanded = true;

      spyOn(component, 'callGTM');
      component.removeSelection({
        market: {
          title: 'title'
        }
      } as any);

      expect(component.expanded).toBeTruthy();
    });

    it('should call removeSelection goalscorermarket', () => {
      component.expanded = true;
      const selected={
        selection:{
          marketType:'',
          idd:'1 - 6',
          id:1,
          playerId:1,
          statisticId:6,
          value:2
        },
        market:{
          key:'ANYTIME GOALSCORER'
        }
       }
      spyOn(component, 'callGTM');
      component.removeSelection(selected as any);

      expect(component.expanded).toBeFalsy();
    });
 
  });

  describe('#editSelection', () => {
    it('should call editSelection method', () => {
      const item = {
        selection: {
          edit: false
        }
      };
      component.editSelection(item as any);

      expect(item.selection.edit).toEqual(true);
      // expect(yourcallMarketsService.trackMarketEditingSelection).toHaveBeenCalled();
    });
  });

  describe('#saveEditSelection', () => {
    it('should call saveEditSelection method', () => {
      const item = {
        selection: {
          edit: true
        }
      };
      component.saveEditSelection(item as any);

      expect(item.selection.edit).toEqual(false);
    });

    it('should call oldID false', () => {
      const item = {
        selection: {
          edit: true
        }
      };
      component.saveEditSelection(item as any);
      expect(item.selection.edit).toEqual(false);
    });

    it('should call oldID true', () => {
      const item = {
        selection: {
          edit: true
        }
      };
      component.oldID = 1;
      bybSelectedSelectionsService.duplicateIdd.add(1);
      component.saveEditSelection(item as any);
      expect(bybSelectedSelectionsService.duplicateIdd.size).toBe(0);
    });

    it('should get old player stats ids', () => {
      const item = {
        selection: {
          edit: true
        }
      };
    component.newPlayer=undefined;
    component.newStat=undefined;
    component.newStatVal=undefined;
    component.oldPlyerId=1;
    component.oldStatId=8;
    component.oldStatVal=2;
    component['saveEditSelection'](item as any);
    expect(component.newPlrId).toEqual(1);
    expect(component.newStatId).toEqual(8);
    expect(component.newStatValId).toEqual(2);
      });

    it('should get old player stats ids when null', () => {
      const item = {
        selection: {
          edit: true
        }
      };
    component.newPlayer=null;
    component.newStat=null;
    component.newStatVal=0;
    component.oldPlyerId=1;
    component.oldStatId=8;
    component.oldStatVal=2;
    component['saveEditSelection'](item as any);
    expect(component.newPlrId).toEqual(1);
    expect(component.newStatId).toEqual(8);
    expect(component.newStatValId).toEqual(2);
      });

    it('should get old player stats ids ', () => {
      const item = {
        selection: {
          edit: true
        }
      };
    component.newPlayer=1;
    component.newStat=8;
    component.newStatVal=2;
    component['saveEditSelection'](item as any);
    expect(component.newPlrId).toEqual(1);
    expect(component.newStatId).toEqual(8);
    expect(component.newStatValId).toEqual(2);
      });

  });

  describe('#getCssClass', () => {
    it('should call getCssClass method selection error true', () => {
      const result = component.getCssClass({
        selection: {
          error: true
        },
        market: {
          key: 'key'
        }
      } as any);

      expect(result).toEqual('key error');
    });

    it('should call getCssClass method selection error false', () => {
      const result = component.getCssClass({
        selection: {
          error: false
        },
        market: {
          key: 'key'
        }
      } as any);

      expect(result).toEqual('key');
    });
  });

  describe('#removeErrorDisplay', () => {
    it('should call removeErrorDisplay method', () => {
      component['removeErrorDisplay']();

      expect(yourcallDashboardService.showOdds).toEqual(true);
      expect(yourcallDashboardService.isErrorMsg).toEqual(false);
      expect(yourcallDashboardService.odds).toEqual(0);
    });
  });

  describe('#setFooterVisibility', () => {
    it('should call setFooterVisibility method', () => {
      component['setFooterVisibility'](true);

      expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.TOGGLE_FOOTER_MENU, [true], []);
    });
  });

  describe('#isFunction', () => {
    it('should return true', () => {
      const param = () => {};
      const result = component['isFunction'](param);
      expect(result).toBeTruthy();
    });

    it('should return false', () => {
      const param = {};
      const result = component['isFunction'](param);
      expect(result).toBeFalsy();
    });
  });

  describe('#updateVisibility', () => {
    beforeEach(() => {
      component['relocate'] = jasmine.createSpy('relocate');
      component['hideFooter'] = jasmine.createSpy('hideFooter');
    });

    it('visible false, isMobile false', () => {
      deviceService.isMobile = false;
      component.updateVisibility(false, false);
      expect(component['relocate']).toHaveBeenCalled();
      expect(component.visible).toBeFalsy();
      expect(component['hideFooter']).toHaveBeenCalledWith(false, undefined);
    });

    it('visible false, isMobile true', () => {
      deviceService.isMobile = true;
      component.updateVisibility(false, false);
      expect(component['relocate']).toHaveBeenCalled();
      expect(component.visible).toBeFalsy();
    });

    it('visible true, callback is not a function', () => {
      component['isFunction'] = jasmine.createSpy('isFunction').and.returnValue(false);
      component.updateVisibility(true, false);
      expect(component['relocate']).toHaveBeenCalled();
      expect(component.visible).toBeTruthy();
      expect(component['isFunction']).toHaveBeenCalledWith(undefined);
    });

    it('visible true, callback is a function', () => {
      const callback = jasmine.createSpy('callback');
      component['isFunction'] = jasmine.createSpy('isFunction').and.returnValue(true);
      component.updateVisibility(true, false, callback);
      expect(component['relocate']).toHaveBeenCalled();
      expect(component.visible).toBeTruthy();
      expect(component['isFunction']).toHaveBeenCalledWith(callback);
      expect(callback).toHaveBeenCalled();
    });
  });

  describe('#callGTM', () => {
    it('should call callGTM', () => {
      const selection = {
          id: '1212',
          getTitle: () => 'title1',
          getMarketTitle: () => 'marketTitle1',
          getSelectionTitle: () => 'selectionTitle1',
        };
      component.callGTM(selection as any);
      expect(bybSelectedSelectionsService.callGTM).toHaveBeenCalled();
    });
  });

  describe('#setVisibility', () => {
    it('should call pubsubService with true', () => {
      component['setFooterVisibility'] = jasmine.createSpy('setFooterVisibility');
      component['setVisibility'](true, false, () => { });
      expect(component['pubsubService'].publish).toHaveBeenCalledWith('NETWORK_INDICATOR_BOTTOM_INDEX', true);
    });
    it('should call pubsubService with false', () => {
      component['setFooterVisibility'] = jasmine.createSpy('setFooterVisibility');
      deviceService.isMobile = true;
      component['setVisibility'](false, false, () => { });
      expect(component['pubsubService'].publish).toHaveBeenCalledWith('NETWORK_INDICATOR_BOTTOM_INDEX', false);
    });
  });
});
