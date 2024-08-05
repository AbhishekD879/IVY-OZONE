import { fakeAsync, tick } from '@angular/core/testing';
import { NavigationEnd, NavigationStart } from '@angular/router';
import { BehaviorSubject, Subscription, throwError, of } from 'rxjs';

import { SportEventPageComponent } from '@edp/components/sportEventPage/sport-event-page.component';
import { IMarket, IMarketTemplate } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';

describe('SportEventPageComponent', () => {
  let component;
  let activatedRoute;
  let sportEventPageProviderService;
  let templateService;
  let router;
  let footballExtensionService;
  let tennisExtensionService;
  let pubSubService;
  let routingHelperService;
  let sportConfigService;
  let changeDetectorRef;
  let windowRefService;
  let deleteMarketHandler;
  let cmsService;
  let deviceService;
  let routingState;
  let marketsOptaLinksService;
  let localeService;
  let seoDataService;
  let isPropertyAvailableService; 
  let cashOutLabelService;
  let sportEventPageService;

  beforeEach(() => {

    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get').and.callFake(str => str)
        }
      }
    } as any;

    sportEventPageProviderService = {
      sportData: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(new Subscription()),
        unsubscribe: jasmine.createSpy('unsubscribe')
      }
    } as any;

    templateService = {
      sortOutcomesByPriceAndDisplayOrder: jasmine.createSpy('sortOutcomesByPriceAndDisplayOrder').and.returnValue([{
        prices: [{
          priceDec: 0.34
        }],
      }, {
        prices: [{
          priceDec: 2.4
        }]
      }])
    };

    footballExtensionService = {
      eventMarkets: jasmine.createSpy('eventMarkets')
    };

    tennisExtensionService = {
      eventMarkets: jasmine.createSpy('eventMarkets')
    };

    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(new Subscription()),
        unsubscribe: jasmine.createSpy('unsubscribe')
      },
      navigateByUrl: jasmine.createSpy(),
      navigate: jasmine.createSpy()
    };

    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, handler) => {
        if (method === 'DELETE_MARKET_FROM_CACHE') {
          deleteMarketHandler = handler;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };

    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl'),
    };
    
    routingState = {
      getPreviousUrl: jasmine.createSpy('getPreviousUrl'),
      getHistory: () => {
        return ['all-markdata', 'main-markets', 'other-markets']
      },
      setHistory: (data) => {
        return data;
      }
    };

    marketsOptaLinksService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({})),
      getMarketLinks: jasmine.createSpy('getMarketLinks').and.returnValue(of({} as any)),
    };

    sportConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({}))
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('changeDetectorRef')
    };

    windowRefService = {
      document: {
        body: {
          scrollTop: 100
        },
        documentElement: {
          scrollTop: 100
        },
        querySelector: jasmine.createSpy('querySelector')
      }
    };

    cmsService = {
      getFeatureConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({})),
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        StatisticalContentInformation: {
        enabled: true
      }
    }))
  } as any;

    localeService = {  
      getString: jasmine.createSpy().and.returnValue('Match Result')
    };
    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    isPropertyAvailableService = {
      isPropertyAvailable: () => {
        return () => {};
      }
    } as any;

    cashOutLabelService = {
      checkCondition: jasmine.createSpy()
    } as any;

    sportEventPageService = {
      transformMarkets: jasmine.createSpy('transformMarkets')
    }

    component = new SportEventPageComponent(
      router,
      activatedRoute,
      sportEventPageProviderService,
      templateService,
      footballExtensionService,
      tennisExtensionService,
      routingHelperService,
      pubSubService,
      sportConfigService,
      changeDetectorRef,
      windowRefService,
      cmsService,
      routingState,
      marketsOptaLinksService,
      localeService,
      seoDataService,
      isPropertyAvailableService,
      cashOutLabelService,
      sportEventPageService
    );
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('showLimit', () => {
    it('should not define market showLimit', () => {
      const marketEntity = {
        isAllShown: true,
        showLimit: 1
      };

      const result = component.showLimit(marketEntity as any);
      expect(result).toBeUndefined();
    });

    it('shloud return showLimit', () => {
      const marketEntity = {
        isAllShown: false,
        showLimit: 1
      };

      const result = component.showLimit(marketEntity as any);
      expect(result).toBe(marketEntity.showLimit);
    });
  });

  describe('showYourCallMarket', () => {
    let market;

    beforeEach(() => {
      market = {
        localeName: 'yourCall'
      };
    });

    it('should not show YourCall markets for unavailable CallMarket option', () => {
      component['yourCallMarketAvailable'] = false;

      const result = component.showYourCallMarket(market as any);
      expect(result).toBeFalsy();
    });

    it('should not show YourCall markets for non YourCallMarket', () => {
      market.localeName = 'NotYourCallMarket';
      component['yourCallMarketAvailable'] = true;

      const result = component.showYourCallMarket(market as any);
      expect(result).toBeFalsy();
    });

    it('should show YourCall markets', () => {
      component['yourCallMarketAvailable'] = true;

      const result = component.showYourCallMarket(market as any);
      expect(result).toBeTruthy();
    });
  });

  describe('hasScorecastMarket', () => {
    let market;
    let marketName;

    beforeEach(() => {
      market = {
        name: 'Correct Score'
      };
      marketName = 'Active Scorecast Market';

      component['isFootball'] = true;
      component['eventEntity'] = {
        isStarted: false
      } as any;
      component['isScorecastMarketsAvailable'] = true;
      component['scorecastInTabs'] = [marketName];
      component['activeTab'] = {
        marketName: marketName
      };
    });

    it('should successfully check the existence of Scorecast Market', () => {
      const result = component.hasScorecastMarket(market);
      expect(result).toBeTruthy();
    });

    it('should successfully check the existence of Scorecast Market', () => {
      const result = component.hasScorecastMarket(<any>{ name: 'correct score' });
      expect(result).toBeTruthy();
    });

    it('should check the  of Scorecast Market for started event', () => {
      component['eventEntity']['isStarted'] = true;

      const result = component.hasScorecastMarket(market);
      expect(result).toBeFalsy();
    });

    it('should check the absence of Scorecast Market for not football event', () => {
      component['isFootball'] = false;

      const result = component.hasScorecastMarket(market);
      expect(result).toBeFalsy();
    });

    it('should check the absence of Scorecast Market for unavailable ScorecastMarket option', () => {
      component['isScorecastMarketsAvailable'] = false;

      const result = component.hasScorecastMarket(market);
      expect(result).toBeFalsy();
    });

    it('should check the absence of Scorecast Market if not Market in tabs', () => {
      component['scorecastInTabs'] = ['Any', 'others', 'tabs'];

      const result = component.hasScorecastMarket(market);
      expect(result).toBeFalsy();
    });

    it('should check the presence of Scorecast Market with the help of pills', () => {
      component.isMobileOnly = true;
      component.showPills = true;
      component.activePill = 'All Markets';
      const tabs1 = [
        {id: 'tab-all-markets', marketName: 'all-markets', pills: [{
          marketName: "Active Scorecast Market", label: "All Markets"
        },
        {
          marketName: "main-markets", label: "Main"
        }]},
        {id: 'tab-main-markets', marketName: 'main-markets'}
      ] as any;
      component['eventTabs'] = tabs1;
      const result = component.hasScorecastMarket(market);
      expect(result).toBeTruthy();
    });

    it('should check the presence of Scorecast Market with the help of pills', () => {
      component.isMobileOnly = true;
      component.showPills = true;
      component.activePill = 'All Markets';
      const tabs1 = [
        {id: 'tab-all-markets', marketName: 'all-markets', pills: [{
          marketName: "all-markets", label: "Markets"
        },
        {
          marketName: "main-markets", label: "Main"
        }]},
        {id: 'tab-main-markets', marketName: 'main-markets'}
      ] as any;
      component['eventTabs'] = tabs1;
      const result = component.hasScorecastMarket(market);
      expect(result).toBeFalsy();
    });
  });

  it('toggleShowYourCallMarket should toggle market isAllShown', () => {
    const isAllShown = false;
    const market = {
      isAllShown: isAllShown
    };

    component.toggleShowYourCallMarket(market as any);
    expect(market.isAllShown).toBe(!isAllShown);
  });
  describe('goToSeo', () => {
    it('should create seo ', () => {
      routingHelperService.formEdpUrl.and.returnValue('url');
      component.goToSeo(({id: '1'} as any));
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith({ id: '1' },'url');
    });
  });
  describe('isHeaderHidden', () => {
    let market;

    beforeEach(() => {
      market = {
        marketsGroup: false,
        viewType: 'Any view type'
      };
    });

    it('should check false', () => {
      const result = component.isHeaderHidden(market);
      expect(result).toBeFalsy();
    });

    it('should check true for markets group', () => {
      market.marketsGroup = true;
      const result = component.isHeaderHidden(market);
      expect(result).toBeTruthy();
    });

    it('should check true for correctScore viewType', () => {
      market.marketsGroup = false;
      market.viewType = 'Correct Score';
      const result = component.isHeaderHidden(market);
      expect(result).toBeTruthy();
    });
    it('should check true for Scorer viewType', () => {
      market.marketsGroup = false;
      market.viewType = 'Scorer';
      const result = component.isHeaderHidden(market);
      expect(result).toBeTruthy();
    });
  });

  describe('isExpanded', () => {
    beforeEach(() => {
      component['openedMarketTabsMap'] = {'123456': true, '980907': false};
      component.isMTASport = false;
    });

    it('should be falsy for missing market', () => {
      const result = component.isExpanded('547856');
      expect(result).toBeFalsy();
    });

    it('should be falsy for falsy openMarketTab and not market', () => {
      const market = {};
      spyOn<any>(component, 'isHeaderHidden').and.returnValue(false);

      const result = component.isExpanded('', market as IMarket);
      expect(result).toBeFalsy();
    });

    it('should be truthy for truthy openMarketTab', () => {
      const result = component.isExpanded('123456');
      expect(result).toBeTruthy();
    });
    
    it('should be truthy for falsy openMarketTab and market', () => {
      const market = {};
      spyOn<any>(component, 'isHeaderHidden').and.returnValue(true);

      const result = component.isExpanded('', market as IMarket);
      expect(result).toBeTruthy();
    });

    it('should be truthy for falsy isSCAvailable in market', () => {
      const market = {isSCAvailable: true};
      const result = component.isExpanded('', market as IMarket);
      expect(result).toBeTruthy();
    });

    it('should be truthy for truthy when for MTA sport', ()=>{
      component['openedMarketTabsMap'] = {'total goals': true};
      component.isMTASport = true;
      const result = component.isExpanded('', {name: 'total goals'} as IMarket);
      expect(result).toBeTruthy();
    });
  });

  describe('changeAccordionState', ()=>{
    it('should test changeAccordionState state changings', () => {
      component.changeAccordionState({id: '565894'} as IMarket, true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();

      const result = component.isExpanded('565894');
      expect(result).toBeTruthy();
    });
    it('should test changeAccordionState state changings for MTA sport', () => {
      component.changeAccordionState({name: 'total goals'} as IMarket, true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();

      const result = component.isExpanded('', {name: 'total goals'} as IMarket);
      expect(result).toBeTruthy();
    });
  });

  describe('getTrackByValue', () => {
    it('should track by market.id', () => {
      const market = {
        id: 111
      };
      const index = 5;
      component['isFootball'] = false;
      component['activeTab'] = null;

      const result = component.getTrackByValue(index, market as any);
      expect(result).toBe(`${market.id}-`);
    });

    it('should track by index', () => {
      const market = {
        id: 111
      };
      const index = 5;
      component['isFootball'] = true;
      component['activeTab'] = {
        id: 0
      };

      const result = component.getTrackByValue(index, market as any);
      expect(result).toBe(`${index}-`);
    });

    it('should track by market.id and by activeTab id', () => {
      const market = {
        id: 111
      };
      const index = 5;
      component['isFootball'] = false;
      component['activeTab'] = {
        id: 5
      };

      const result = component.getTrackByValue(index, market as any);
      expect(result).toBe(`${market.id}-${component['activeTab']['id']}`);
    });

    it('should track by index and by activeTab id', () => {
      const market = {
        id: 111
      };
      const index = 5;
      component['isFootball'] = true;
      component['activeTab'] = {
        id: 5
      };

      const result = component.getTrackByValue(index, market as any);
      expect(result).toBe(`${index}-${component['activeTab']['id']}`);
    });
  });

  it('getTrackById should track by entity.id', () => {
    const entity = {
      id: 111
    };

    const result = component.getTrackById(0, entity);
    expect(result).toBe('111_0');
  });

  describe('isEnabledOnCms', () => {
    it('should be falsy for missing yourCallPlayerStatsName', () => {
      component['sysConfig'] = {};

      const result = component.isEnabledOnCms();
      expect(result).toEqual(false);
    });

    it('should be falsy for disabled option', () => {
      component['sysConfig'] = {
        yourCallPlayerStatsName: {
          enabled: false
        }
      };
      const result = component.isEnabledOnCms();
      expect(result).toEqual(false);
    });

    it('should be truthy for enabled option', () => {
      component['sysConfig'] = {
        yourCallPlayerStatsName: {
          enabled: true
        }
      };
      const result = component.isEnabledOnCms();
      expect(result).toEqual(true);
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe listeners', () => {
      component['yourCallTabContentComponent'] = {} as any;
      component['sportDataSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['routeChangeListener'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['sportsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;

      component.ngOnDestroy();

      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('sportEventPageCtrl');
      expect(component['sportDataSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['routeChangeListener'].unsubscribe).toHaveBeenCalled();
    });

    it('should not throw error', () => {
      component.sportDataSubscription = component.routeChangeListener = null;
      expect(() => component.ngOnDestroy()).not.toThrowError();
    });
  });

  describe('ngOnInit', () => {

    it('should subscribe sportData and router events', () => {
      spyOn(component, 'init');
      spyOn(component, 'extendMarketsWithOptaLinks');
      const links = [{}, {}];
      marketsOptaLinksService.getMarketLinks.and.returnValue(of(links));
      component.ngOnInit();

      expect(sportEventPageProviderService.sportData.subscribe)
        .toHaveBeenCalledWith(component['sportDataHandler'], jasmine.any(Function));
      expect(router.events.subscribe).toHaveBeenCalledWith(jasmine.any(Function));
      component.replaySubj.subscribe( (data) => {
        expect(data).toEqual(links);
      });
    });

    it('should properly set default tab in case if tab was renamed', () => {
      const tabs1 = [
        {id: 'tab-all-markets'},
        {id: 'tab-main-markets'}
      ] as any;
      const tabs2 = [
        {id: 'tab-all-markets'},
        {id: 'tab-main'}
      ] as any;
      component.filteredMarketGroup = [{ outcomes: [{ name: '' }], name:'2Upmarket' }] as IMarket[];
      component.marketGroup = [{ name: '2Upmarket', outcomes: [{ name: '' }] }] as IMarket[];
      component['sport'].isMarketTabCorrect = () => true;
      component['eventTabs'] = tabs1;
      component['marketName'] = 'main-markets';
      component.eventEntity = {} as ISportEvent;
      component['marketsByCollection'] = [];
      component['generateYourCallMarkets'] = () => {};
      component.init();
      expect(component['activeTab'].id).toEqual('tab-main-markets');
      component['eventTabs'] = tabs2;
      component.init();
      expect(component['activeTab'].id).toEqual('tab-main');
    });

    it('should properly set redirect tab', () => {
      const tabs1 = [
        {id: 'tab-all-markets'},
        {id: 'tab-main-markets'},
        {id: 'tab-default'}
      ] as any;
      
      component['eventTabs'] = tabs1;
      component['sport'].isMarketTabCorrect = () => false;
      routingHelperService.formEdpUrl.and.returnValue('baseURL');
      component['marketName'] = 'fakeName';
      component['defaultMarketName'] = 'default';
      component.eventEntity = {} as ISportEvent;
      component['marketsByCollection'] = [];
      component['generateYourCallMarkets'] = () => {};
      component.init();
      expect(router.navigateByUrl).toHaveBeenCalledWith('baseURL/default');
    });

    it('should trigger init for NavigationEnd event', fakeAsync(() => {
      const eventEnd = new NavigationEnd(0, '', '');
      router.events.subscribe.and.callFake((fn) => fn(eventEnd));
      spyOn(component, 'init');
      component.ngOnInit();
      tick();

      expect(activatedRoute.snapshot.paramMap.get).toHaveBeenCalledWith('market');
      expect(component['marketName']).toEqual('market');
      expect(component.init).toHaveBeenCalled();
    }));

    it('should not trigger init for non NavigationEnd event', fakeAsync(() => {
      const eventStart = new NavigationStart(0, '');
      router.events.subscribe.and.callFake((fn) => fn(eventStart));
      spyOn(component, 'init');
      component.ngOnInit();
      tick();

      expect(component.init).not.toHaveBeenCalled();
    }));

    it('should trigger NavigationStart event with popstate', fakeAsync(() => {
      component.eventTabs = [];
      const eventStart = new NavigationStart(0, '', 'popstate');
      router.events.subscribe.and.callFake((fn) => fn(eventStart));
      spyOn(component, 'init');
      spyOn(routingState, 'getHistory').and.returnValue(['all-markdata', 'main-markets', 'other-markets']);
      component.ngOnInit();
      tick();

      expect(routingState.getHistory).toHaveBeenCalled();
    }));
    it('should trigger NavigationStart event with popstate and url', fakeAsync(() => {
      component.eventTabs = [{marketName:'main-markets'}];
      const eventStart = new NavigationStart(0, 'main-markets', 'popstate');
      router.events.subscribe.and.callFake((fn) => fn(eventStart));
      spyOn(component, 'init');
      spyOn(routingState, 'getHistory').and.returnValue(['all-markdata', 'main-markets', 'other-markets']);
      component.ngOnInit();
      tick();

      expect(routingState.getHistory).toHaveBeenCalled();
    }));

    it('should trigger NavigationStart event without popstate', fakeAsync(() => {
      component.eventTabs = [];
      const eventStart = new NavigationStart(0, '');
      router.events.subscribe.and.callFake((fn) => fn(eventStart));
      spyOn(component, 'init');
      spyOn(routingState, 'getHistory');
      component.ngOnInit();
      tick();

      expect(routingState.getHistory).not.toHaveBeenCalled();
    }));

    it('should trigger NavigationStart event with popstate and history length 0', fakeAsync(() => {
      component.eventTabs = [];
      const eventStart = new NavigationStart(0, '', 'popstate');
      router.events.subscribe.and.callFake((fn) => fn(eventStart));
      spyOn(component, 'init');
      spyOn(routingState, 'getHistory').and.returnValue([]);
      component.ngOnInit();
      tick();

      expect(routingState.getHistory()).toEqual([]);
    }));

    it ('should call error handler', () => {
      sportEventPageProviderService.sportData = new BehaviorSubject<any>(null);
      sportEventPageProviderService.sportData.error(throwError('err'));
      component.ngOnInit();

      expect(component.state.loading).toBe(false);
      expect(component.state.error).toBe(true);
    });
  });

  describe('init', () => {
    beforeEach(() => {
      component.sport = { isMarketTabCorrect: jasmine.createSpy('isMarketTabCorrect') };
      component.eventEntity = {};
      environment.brand = 'ladbrokes';
      component.marketsByCollection = [];
      component.sysConfig = { YourCallMarket: {} };
      deviceService = {
        isMobileOnly: true,
      };
    });
    
    it('show pills for all markets', ()=> {
      const tabs1 = [
        {id: 'tab-all-markets', marketName: 'all-markets', pills: [{
          marketName: "all-markets", label: "All Markets"
        },
        {
          marketName: "main-markets", label: "Main"
        }]},
        {id: 'tab-main-markets', marketName: 'main-markets'}
      ] as any;
      routingState.getPreviousUrl.and.returnValue('/betbuilder');
      component['eventTabs'] = tabs1;
      deviceService.isMobileOnly = true;
      component.marketName = "all-markets";
      component.isMobileOnly = deviceService.isMobileOnly;
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of(false));
      component.init();
      expect(component.showPills).toBeTrue();
    })

    it('hide pills for all markets', ()=> {

      const tabs1 = [
        {id: 'tab-all-markets'},
        {id: 'tab-main-markets'}
      ] as any;
      component['eventTabs'] = tabs1;
      deviceService.isMobileOnly = false;
      component.marketName = "all-markets";
      component.isMobileOnly = deviceService.isMobileOnly;
      component.init();
      expect(component.showPills).toBeFalse();
    })

    it('if active pill is null', () => {
      component.eventTabs = [ {
        label: "Market",
        active: true,
        id: 'tab-all-markets',
        index: 12,
        marketName: "all-markets",
        pills: [{label: 'Market', marketName: "all-markets"},{label: 'Main', marketName: "main-markets"}]
      }]
      routingState.getPreviousUrl.and.returnValue('/betbuilder');
      component.isMobileOnly = true;
      component.marketName = "all-markets";
      component.init();
      expect(component.activePill).toBe('Main');
    });
 
    it('if active pill is available', () => {
      component.marketName = 'main-markets';
      component.isMobileOnly = true;
      component.activePill = "Market";
      component.activeTab = null;
      component.eventTabs = [ {
          label: "Market",
          active: true,
          id: 'tab-all-markets',
          index: 12,
          marketName: "all-markets",
          pills: [{label: 'Market', marketName: "all-markets"}]
        }]
      routingState.getPreviousUrl.and.returnValue('/buildyourbet');
      spyOn(component, 'checkBybTabs');
      component.init();
      expect(component.activePill).toBe('Market');
    });
    
    it('main tab should be selected by default in coral', () => {
      component.marketName = 'all-markets';
      component.isMobileOnly = true;
      component.showPills = true;
      component.eventTabs = [{
        label: "Market",
        active: true,
        id: 'tab-all-markets',
        index: 12,
        marketName: "all-markets",
        pills: [{label: 'Market', marketName: "all-markets"},{label: 'Main', marketName: "main-markets"}]
      }]
      routingState.getPreviousUrl.and.returnValue('/betbuilder');
      spyOn(component, 'checkBybTabs');
      environment.brand = 'bma'
      component.init();
    });

    it('should not change the pill when checkBybUrl is false and active pill is available', () => {
      spyOn(component as any, 'filterAndSortMarkets');
      component.marketName = 'all-markets';
      component.isMobileOnly = true;
      component.showPills = true;
      component.activePill = 'Market';
      component.eventTabs = [{
        label: "Market",
        active: true,
        id: 'tab-all-markets',
        index: 12,
        marketName: "all-markets",
        pills: [{label: 'Market', marketName: "all-markets"},{label: 'Main', marketName: "main-markets"}]
      }, { id: 'tab-build-your-bet', label: 'builbet', index: 13 }]
      routingState.getPreviousUrl.and.returnValue('/betbuilders');
      spyOn(component, 'checkBybTabs');
      environment.brand = 'bma'
      component.init();
      expect(component['filterAndSortMarkets']).toHaveBeenCalledWith('Market');
    });

    it('should not change the pill when checkBybUrl is false and active pill is not available', () => {
      spyOn(component as any, 'filterAndSortMarkets');
      component.marketName = 'all-markets';
      component.isMobileOnly = true;
      component.showPills = true;
      component.activePill = '';
      component.eventTabs = [{
        label: "Market",
        active: true,
        id: 'tab-all-markets',
        index: 12,
        marketName: "all-markets",
        pills: [{label: 'Market', marketName: "all-markets"},{label: 'Main', marketName: "main-markets"}]
      }, { id: 'tab-build-your-bet', label: 'builbet', index: 13 }]
      routingState.getPreviousUrl.and.returnValue('/betbuilders');
      spyOn(component, 'checkBybTabs');
      environment.brand = 'bma'
      component.init();
      expect(component['filterAndSortMarkets']).toHaveBeenCalledWith('Main');
    });

    it('should not change the pill when checkBybUrl is false and active pill is not available and is active', () => {
      spyOn(component as any, 'filterAndSortMarkets');
      component.marketName = 'all-markets';
      component.isMobileOnly = true;
      component.showPills = true;
      component.activePill = '';
      component.eventTabs = [{
        label: "Market",
        active: true,
        id: 'tab-all-markets',
        index: 12,
        marketName: "all-markets",
        pills: [{label: 'Market', marketName: "all-markets"},{label: 'Main', marketName: "main-markets",active: true},{ marketName: "main-markets",active: true}]
      }, { id: 'tab-build-your-bet', label: 'builbet', index: 13 }]
      routingState.getPreviousUrl.and.returnValue('/betbuilders');
      spyOn(component, 'checkBybTabs');
      environment.brand = 'bma'
      component.init();
      expect(component['filterAndSortMarkets']).toHaveBeenCalledWith('Main');
    });

    it('Active tab is null when checkBybUrl is false and active pill is un available', () => {
      spyOn(component as any, 'filterAndSortMarkets');
      component.marketName = 'bet-builder';
      component.isMobileOnly = true;
      component.showPills = false;
      component.activePill = 'Market';
      component.eventTabs = [{ id: "tab-bet-builder",
      marketName: "bet-builder",
      label: "Bet Builder",
      url: "/event/football/bet-builder",
      index: 1
      },{
        label: "Market",
        id: 'tab-all-markets',
        index: 14,
        marketName: "all-markets",
        pills: [{label: 'Market', marketName: "all1-markets"},{label: 'Main', marketName: "main1-markets"}]
      }]
      routingState.getPreviousUrl.and.returnValue('/betbuilders');
      spyOn(component, 'checkBybTabs');
      environment.brand = 'bma'
      component.init();
      expect(component['filterAndSortMarkets']).toHaveBeenCalledWith(undefined);
    });

    it('should not change the pill when checkBybUrl is false and active pill is not available', () => {
      spyOn(component as any, 'filterAndSortMarkets');
      component.marketName = 'all-markets';
      component.isMobileOnly = true;
      component.showPills = true;
      component.activePill = '';
      component.eventTabs = [{
        label: "Market",
        active: true,
        id: 'tab-all-markets',
        index: 12,
        marketName: "all-markets",
        pills: [{label: 'Market', marketName: "all-markets"}]
      }, { id: 'tab-build-your-bet', label: 'builbet', index: 13 }]
      routingState.getPreviousUrl.and.returnValue('/betbuilders');
      spyOn(component, 'checkBybTabs');
      environment.brand = 'bma'
      component.init();
      expect(component['filterAndSortMarkets']).toHaveBeenCalledWith('Market');
    });

    it('should not init component', () => {
      component.eventEntity = null;
      component.init();
      environment.brand = 'ladbrokes';
      expect(component.sport.isMarketTabCorrect).not.toHaveBeenCalled();
      expect(component.showSurfaceBets).toBe(false);
    });

    it('market name same as default market name', () => {
      component.marketName = component.defaultMarketName = 'mkt';
     
      const tabs1 = [
        {id: 'tab-all-markets'},
        {id: 'tab-main-markets'}
      ] as any;
      component['eventTabs'] = tabs1;
      component.init();
      environment.brand = 'ladbrokes';
    });

    it('should set selected market group', () => {
      component.sport.isMarketTabCorrect.and.returnValue(true);
      component.eventTabs = [{ id: 'tab-mkt', label: 'mkt' }];
      environment.brand = 'ladbrokes';
      component.marketName = 'mkt';
      component.marketsByCollection = [{ markets: [], name: 'mkt' }];
      component.init();
      expect(component.marketGroup).toEqual(component.marketsByCollection[0].markets);
    });

    it('should create player stats market group', () => {
      spyOn(component, 'createPlayerStatsMarketsGroup');
      component.sport.isMarketTabCorrect.and.returnValue(true);
      environment.brand = 'ladbrokes';
      component.eventTabs = [{ id: 'tab-mkt', label: 'mkt' }];
      component.marketName = 'mkt';
      component.marketsByCollection = [{
        name: 'mkt', markets: [{ templateMarketName: 'Player_Stats_' , name: '' }]
      }];
      component.init();
      expect(component.createPlayerStatsMarketsGroup).toHaveBeenCalledTimes(1);
    });

    it('init opened markets tabs', () => {
      component.isMTASport = true;
      component.sport.isMarketTabCorrect.and.returnValue(true);
      component.eventTabs = [{ id: 'tab-mkt', label: 'mkt' }];
      component.marketName = 'mkt';
      environment.brand = 'bma';
      component.marketsByCollection = [{
        name: 'mkt', markets: [
          { name: 'over', outcomes: [{}] },
          { name: 'under', outcomes: [{}] },
          { name: 'tie', outcomes: [{}] }
        ]
      }];
      component.aggregatedMarketsGroup = [{name: 'over'}]
      component.init();
      expect(component['openedMarketTabsMap']).toEqual({'over': true, 'under': false, 'tie': true});
    });

    it('should insert collapsed state', () => {
      component.isMTASport = false;
      spyOn(component, 'insertCollapsedState');
      component.sport.isMarketTabCorrect.and.returnValue(true);
      component.eventTabs = [{ id: 'tab-mkt', label: 'mkt' }];
      component.marketName = 'mkt';
      environment.brand = 'bma';
      component.marketsByCollection = [{ name: 'mkt', markets: [{name: '1', isDisplayed: true}] }];
      component['openedMarketTabsMap'] = {'343445': false, '1': true};
      component.init();
      expect(component['insertCollapsedState']).toHaveBeenCalledTimes(1);
    });

    it('should call extendMarketsWithOptaLinks', fakeAsync(() => {
      spyOn(component, 'insertCollapsedState');
      const tabs1 = [
        {id: 'tab-all-markets'},
        {id: 'tab-main-markets'}
      ] as any;
      component['eventTabs'] = tabs1;
      const links = [{}];
      component['extendMarketsWithOptaLinks'] = jasmine.createSpy('extendMarketsWithOptaLinks');
      component.marketConfig = [];
      component.replaySubj.next(links);
      component.init();
      expect(component['extendMarketsWithOptaLinks']).toHaveBeenCalledWith([], [], links);
    }));

    it('should not show SurfaceBets on BYB and 5-A-Side tabs', () => {
      component.eventTabs = [{ id: 'tab-mkt' },
                        { id: 'tab-build-your-bet' },
                        { id: 'tab-bet-builder' },
                        { id: 'tab-5-a-side' }];
      component.eventEntity = {} as any;
      component.defaultMarketName = 'mkt';
      environment.brand = 'bma';
      component.init();
      expect(component.showSurfaceBets).toBe(false);

      component.eventEntity = { id: 12 } as any;
      component.init();
      expect(component.showSurfaceBets).toBe(true);

      component.defaultMarketName = 'build-your-bet';
      component.init();
      expect(component.showSurfaceBets).toBe(false);

      component.defaultMarketName = 'bet-builder';
      component.init();
      expect(component.showSurfaceBets).toBe(false);

      component.defaultMarketName = '5-a-side';
      component.init();
      expect(component.showSurfaceBets).toBe(false);
    });

    describe('#formAggregatedMarkets', ()=>{
      beforeEach(()=>{
        environment.CATEGORIES_DATA.sortCodesForMTA = ['HL', 'MH', 'WH'];
        component.isMTASport = true;
        component.eventTabs = [{id:'tab-all-markets', label: 'all-markets'}, {id: 'tab-main-markets', label: 'main'}];
        component.marketName = 'all-markets'
      });
      it('should form aggreatedMarkets #1', ()=>{
        component.eventEntity = {id: 1, name: 'Boston v Atlanta'} as any;
        component.marketsByCollection = [{ 
            name: 'main',
            markets: [
              {id: 1, name: 'Over/Under', templateMarketName: 'Total Points', templateMarketId: 1, displayOrder: 3, marketMeaningMinorCode: 'HL', cashoutAvail: 'Y', isDisplayed: true}, 
              {id: 2, name: 'Spread 1.5', templateMarketName: 'Spread', templateMarketId: 2, displayOrder: 1, marketMeaningMinorCode: 'WH', rawHandicapValue: '1.5', isDisplayed: true},
              {id: 6, name: 'Spread 2.5', templateMarketName: 'Spread', templateMarketId: 2, displayOrder: 1, marketMeaningMinorCode: 'WH', rawHandicapValue: '2.5', drilldownTagNames: 'EVE_DF', isDisplayed: true},
              {id: 3, name: 'Match Betting', templateMarketName: 'Match Betting', templateMarketId: 3, displayOrder: 0, marketMeaningMinorCode: 'MR', cashoutAvail: 'N', isDisplayed: true},
              {id: 4, name: 'Boston Total Points -1.5', templateMarketName: 'Home Team Total Points', templateMarketId: 4, displayOrder: 2,  marketMeaningMinorCode: 'HL', rawHandicapValue: '-1.5', isDisplayed: true},
              {id: 4, name: 'Boston Total Points 2.5', templateMarketName: 'Home Team Total Points', templateMarketId: 4, displayOrder: 2,  marketMeaningMinorCode: 'HL', rawHandicapValue: '2.5', isDisplayed: true},
              {id: 5, name: 'Atlanta Total Points +1.5', templateMarketName: 'Away Team Total Points', templateMarketId: 5, displayOrder: 5,  marketMeaningMinorCode: 'HL', rawHandicapValue: '+1.5', isDisplayed: true}] 
          }];
        component.init();
  
        expect(component.aggregatedMarketsGroup.length).toEqual(5);
        expect(component.aggregatedMarketsGroup[1].drilldownTagNames).toEqual('EVE_DF');
        expect(component.aggregatedMarketsGroup[2].name).toEqual('Boston Total Points');
        expect(component.aggregatedMarketsGroup[4].name).toEqual('Atlanta Total Points +1.5');
      });
      it('should form aggreatedMarkets #2', ()=>{
        isPropertyAvailableService.isPropertyAvailable = () => {
            return () => {return true};
          }
        component.eventEntity = {id: 1, name: 'Boston vs Atlanta'} as any;
        component['openedMarketTabsMap'] = {'Spread': true};
        component.marketsByCollection = [{ 
            name: 'main',
            markets: [
              {id: 2, name: 'Spread 1.5', templateMarketName: 'Spread', templateMarketId: 2, displayOrder: 1, marketMeaningMinorCode: 'WH', cashoutAvail: 'N', isDisplayed: true},
              {id: 6, name: 'Spread 2.5', templateMarketName: 'Spread', templateMarketId: 2, displayOrder: 1, marketMeaningMinorCode: 'WH', cashoutAvail: 'Y', isDisplayed: true},
              {id: 5, name: 'Boston Total Points', templateMarketName: 'Home Team Total Points', templateMarketId: 3, displayOrder: 3,  marketMeaningMinorCode: 'HL', isDisplayed: true},
              {id: 4, name: 'Atlanta Total Points', templateMarketName: 'Away Team Total Points', templateMarketId: 4, displayOrder: 2,  marketMeaningMinorCode: 'HL', isDisplayed: true}] 
          }];
        component.init();
  
        expect(component.aggregatedMarketsGroup.length).toEqual(3);
        expect(component.aggregatedMarketsGroup[2].name).toEqual('Boston Total Points');
        expect(component.aggregatedMarketsGroup[1].name).toEqual('Atlanta Total Points');
        expect(component.aggregatedMarketsGroup[0].cashoutAvail).toEqual('Y');
      });
      it('should filter empty markets after the outcomes are fetched', ()=>{
        component.eventEntity = {id: 1} as any;
        component.marketsByCollection = [{ 
          name: 'main',
          markets: [
            {id: 2, name: 'Spread 1.5', templateMarketName: 'Spread', templateMarketId: 2, displayOrder: 1, marketMeaningMinorCode: 'WH', cashoutAvail: 'N', isOutcomesFetched: true, outcomes: [{id:1}]},
            {id: 4, name: 'Total Points', templateMarketName: 'Total Points', templateMarketId: 3, displayOrder: 3, marketMeaningMinorCode: 'MH', cashoutAvail: 'Y', isOutcomesFetched: true, outcomes: []},
            {id: 6, name: 'Handicap 3Way', templateMarketName: 'Handicap', templateMarketId: 4, displayOrder: 7, marketMeaningMinorCode: 'MH', cashoutAvail: 'Y', isOutcomesFetched: true}
          ]}];
        component.init();
      });
    });
  });

  describe('#generateYourCallMarkets', () => {
    const marketGroup_01 = [{
      id: '1',
      displayOrder: 2,
      templateMarketName: 'Over/Under Second Half Home Team Total Goals',
      name: '2.5',
      outcomes: [{
        prices: [{
          priceDec: 0.34
        }]
      }, {
        prices: [{
          priceDec: 2.4
        }]
      }]
    }, {
      id: '2',
      displayOrder: 1,
      templateMarketName: 'YourCall InPlay and Cashout',
      name: '#YourCall - River Plate'
    }] as any;

    const marketGroup_02 = [{
      id: '1',
      displayOrder: 1,
      templateMarketName: 'YourCall InPlay Market',
      name: '#YourCall - Palestino'
    }] as any;

    const marketGroup_03 = [{
      id: '2',
      displayOrder: 2,
      templateMarketName: 'Match Betting',
      name: 'Match Result'
    }] as any;

    const marketGroup_04 = [{
      id: '1',
      displayOrder: 2,
      templateMarketName: 'Over/Under Second Half Home Team Total Goals',
      name: '2.5',
      outcomes: [{
        prices: [{
          priceDec: 2.4
        }]
      }, {
        prices: [{
          priceDec: 0.34
        }]
      }]
    }, {
      id: '2',
      displayOrder: 1,
      templateMarketName: 'YourCall InPlay and Cashout',
      name: '#YourCall - River Plate',
      outcomes: [{
        prices: [{
          priceDec: 2.4
        }]
      }, {
        prices: [{
          priceDec: 0.34
        }]
      }]
    }] as any;

    const marketGroup_05 = [{
      id: '1',
      displayOrder: 2,
      templateMarketName: 'Over/Under Second Half Home Team Total Goals',
      name: '2.5'
    }, {
      id: '2',
      displayOrder: 1,
      templateMarketName: 'YourCall InPlay and Cashout',
      name: '#YourCall - River Plate'
    }] as any;

    const eventEntity_01 = {
      id: 12558682,
      name: 'Palestino v River Plate',
      markets: marketGroup_01
    } as any;

    const eventEntity_02 = {
      id: 23432423,
      name: 'Palestino v River Plate',
      markets: marketGroup_02
    } as any;

    const eventEntity_03 = {
      id: 24234223,
      name: 'Palestino v River Plate',
      markets: marketGroup_03
    } as any;

    const eventEntity_04 = {
      id: 12558682,
      name: 'Palestino v River Plate',
      markets: marketGroup_04
    } as any;

    const eventEntity_05 = {
      id: 12558682,
      name: 'Palestino v River Plate',
      markets: marketGroup_05
    } as any;

    const result_01 = [{
      id: '1',
      displayOrder: 2,
      templateMarketName: 'Over/Under Second Half Home Team Total Goals',
      name: '2.5',
      outcomes: [{
        prices: [{
          priceDec: 0.34
        }],
      }, {
        prices: [{
          priceDec: 2.4
        }]
      }]
    }, {
      id: '2',
      displayOrder: 1,
      isAllShown: false,
      showLimit: 6,
      templateMarketName: 'YourCall InPlay and Cashout',
      name: '#YourCall - River Plate'
    }] as any;

    const result_02 = [{
      id: '1',
      isAllShown: false,
      showLimit: 6,
      displayOrder: 1,
      templateMarketName: 'YourCall InPlay Market',
      name: '#YourCall - Palestino'
    }] as any;

    const result_03 = [{
      id: '1',
      displayOrder: 2,
      templateMarketName: 'Over/Under Second Half Home Team Total Goals',
      name: '2.5',
      outcomes: [{
        prices: [{
          priceDec: 2.4
        }]
      }, {
        prices: [{
          priceDec: 0.34
        }]
      }]
    }, {
      id: '2',
      displayOrder: 1,
      isAllShown: false,
      showLimit: 6,
      templateMarketName: 'YourCall InPlay and Cashout',
      name: '#YourCall - River Plate',
      outcomes: [{
        prices: [{
          priceDec: 0.34
        }]
      }, {
        prices: [{
          priceDec: 2.4
        }]
      }]
    }] as any;

    const result_05 = [{
      id: '1',
      displayOrder: 2,
      templateMarketName: 'Over/Under Second Half Home Team Total Goals',
      name: '2.5'
    }, {
      id: '2',
      displayOrder: 1,
      isAllShown: false,
      showLimit: 6,
      templateMarketName: 'YourCall InPlay and Cashout',
      name: '#YourCall - River Plate'
    }] as any;

    it('it should generate YourCall markets it is exist', () => {
      component['sysConfig'] = {
        YourCallMarket: {
          football: '#YourCall',
          basketball: '#YourCall'
        }
      };
      component.marketGroup = marketGroup_01;
      component.eventEntity = eventEntity_01;
      component['sportName'] = 'football';

      component['generateYourCallMarkets']();
      expect(component.marketGroup).toEqual(result_01);
    });

    it('it should generate YourCall markets it is exist and should sort outcomes', () => {
      component['sysConfig'] = {
        YourCallMarket: {
          football: '#YourCall',
          basketball: '#YourCall'
        }
      };
      component.marketGroup = marketGroup_04;
      component.eventEntity = eventEntity_04;
      component['sportName'] = 'football';

      component['generateYourCallMarkets']();
      expect(templateService.sortOutcomesByPriceAndDisplayOrder).toHaveBeenCalled();
      expect(component.marketGroup).toEqual(result_03);
    });

    it('it should generate YourCall markets it is exist but should NOT sort outcomes', () => {
      component['sysConfig'] = {
        YourCallMarket: {
          football: '#YourCall',
          basketball: '#YourCall'
        }
      };
      component.marketGroup = marketGroup_05;
      component.eventEntity = eventEntity_05;
      component['sportName'] = 'football';

      component['generateYourCallMarkets']();
      expect(templateService.sortOutcomesByPriceAndDisplayOrder).not.toHaveBeenCalled();
      expect(component.marketGroup).toEqual(result_05);
    });

    it('it should NOT generate YourCall markets it is already exist', () => {
      component['sysConfig'] = {
        YourCallMarket: {}
      };
      component.marketGroup = marketGroup_01;
      component.eventEntity = eventEntity_01;
      component['sportName'] = 'football';

      expect(component.marketGroup).toEqual(result_01);
      component['generateYourCallMarkets']();
      expect(component.marketGroup).toEqual(result_01);
    });

    it('it should generate YourCall markets it is exist and set default market name', () => {
      component['sysConfig'] = {
        YourCallMarket: {}
      };
      component.marketGroup = marketGroup_02;
      component.eventEntity = eventEntity_02;
      component['sportName'] = 'tennis';

      component['generateYourCallMarkets']();
      expect(component.marketGroup).toEqual(result_02);
    });

    it('it should NOT generate YourCall markets it is not exist', () => {
      component['sysConfig'] = {
        YourCallMarket: {}
      };
      component.marketGroup = marketGroup_03;
      component.eventEntity = eventEntity_03;
      component['sportName'] = 'basketball';

      component['generateYourCallMarkets']();
      expect(component.marketGroup).toEqual(marketGroup_03);
    });
  });

  describe('onFIlterSelect', () => { 
    it('selected market is same as new market', () => {
      const pill = {
        label: "mrkt"
      }
      spyOn(component as any, 'filterAndSortMarkets');
      component.activePill = "mrkt"
      expect(component.onFilterSelect(pill)).toBe(undefined);
      expect(component['filterAndSortMarkets']).not.toHaveBeenCalled();
    });

    it('selected market is diff as new market', () => {
      const pill = {
        label: "market",
        marketName: "main-market"
      }
      component.marketsByCollection = [{ name: 'mkt', markets: [{id: '1', isDisplayed: true}] }];
      component.activeTab = { marketName: 'all-markets',
       pills: [{label: 'main market', active: false, marketName: "main-market"}]
      }
      component.activePill = "mrkt"
      component['openedMarketTabsMap'] = {'1': true}
      component.onFilterSelect(pill);
      expect(component.activePill).toEqual(pill.label)
    });

    it('filteringPills',() => {
      const pill = {
        label: "market",
        marketName: "main-market"
      }
      spyOn(component as any, 'validateMarketTab');
      component.filteredMarketGroup = [{ outcomes: [{ name: '' }] }] as IMarket[];
      component.initialized = true;
      component.marketsByCollection = [{ name: 'mkt', markets: [] }];
      component.activeTab = { marketName: 'all-markets',
       pills: [{label: 'main market', active: false, marketName: "main-market"}]
      }
      spyOn(component as any, 'filterAndSortMarkets');
      component.activePill = "mrkt";
      component['openedMarketTabsMap'] = {'1': true}
      component.onFilterSelect(pill);
      expect(component.activePill).toEqual(pill.label);
      expect(component.activeTab.pills[0].active).toBeTrue();
      expect(component['filterAndSortMarkets']).toHaveBeenCalled();
    });

    it('notfilteringPills',() => {
      spyOn(component as any, 'validateMarketTab');
      component.filteredMarketGroup = [{ outcomes: [{ name: '' }] }] as IMarket[];
      component.initialized = true;
      const pill = {
        label: "market",
        marketName: "main"
      }
      component.marketsByCollection = [{ name: 'mkt', markets: [] }];
      component.activeTab = { marketName: 'all-markets',
       pills: [{label: 'main-market', active: true, marketName: "main-market"}]
      }
      component['openedMarketTabsMap'] = {'1': true}
      spyOn(component as any, 'filterAndSortMarkets');
      component.onFilterSelect(pill);
      expect(component.activePill).toEqual(pill.label);
      expect(component.activeTab.pills[0].active).toBeFalse();
      expect(component['filterAndSortMarkets']).toHaveBeenCalled();
    });
  });

  describe('recalculateExpandedMarkets', () => {
    it('should be recalculate openMarketTabs', () => {
      spyOn(component as any, 'validateMarketTab');
      component['openedMarketTabsMap'] = {};
      component['openedMarketTabsCountByDefault'] = 1;
      component.filteredMarketGroup = [{ id: '1', outcomes: [{ name: '' }] }, { id: '2', outcomes: [] }] as IMarket[];
      component.isMTASport = false;
      component.recalculateExpandedMarkets(null);
      expect(component['openedMarketTabsMap']).toEqual({'1': true, '2': false});
    });

    it('should be check openMarketTabs length', () => {
      const filterMarkets = {'1': true, '2': true};
      spyOn(component as any, 'validateMarketTab');
      component['openedMarketTabsMap'] = {};
      component['openedMarketTabsCountByDefault'] = 2;
      component.filteredMarketGroup = [{id: '1', outcomes: [{ name: '' }] }, {id: '2'}] as IMarket[];
      component.isMTASport = false;
      component.recalculateExpandedMarkets(null);
      expect(component['openedMarketTabsMap']).toEqual(filterMarkets);
    });

    it('should be recalculate openMarketTabs for MTA', () => {
      spyOn(component as any, 'validateMarketTab');
      component['openedMarketTabsMap'] = {};
      component['openedMarketTabsCountByDefault'] = 1;
      component.aggregatedMarketsGroup = [{ name: 'over'}, { name: 'under'}] as IMarketTemplate[];
      component.isMTASport = true;
      component.recalculateExpandedMarkets(null);
      expect(component['openedMarketTabsMap']).toEqual({'over': true, 'under': false});
    });

    it('should be check openMarketTabs length for MTA', () => {
      const filterMarkets = {'over': true, 'under': true};
      spyOn(component as any, 'validateMarketTab');
      component['openedMarketTabsMap'] = {};
      component['openedMarketTabsCountByDefault'] = 2;
      component.aggregatedMarketsGroup = [{name: 'over'}, {name: 'under'}] as IMarketTemplate[];
      component.isMTASport = true;
      component.recalculateExpandedMarkets(null);
      expect(component['openedMarketTabsMap']).toEqual(filterMarkets);
    });

    it('should`t reset initialized prop if resetInit param is false', () => {
      spyOn(component as any, 'validateMarketTab');
      component.filteredMarketGroup = [{ outcomes: [{ name: '' }] }] as IMarket[];
      component.initialized = true;
      component.recalculateExpandedMarkets(null,false);
      expect(component.initialized).toBeTruthy();
    });
    it('should reset initialized prop if resetInit param is true', () => {
      spyOn(component as any, 'validateMarketTab');
      component.filteredMarketGroup = [{ outcomes: [{ name: '' }] }] as IMarket[];
      component.initialized = true;
      component.recalculateExpandedMarkets(null);
      expect(component.initialized).toBeFalsy();
    });
  });

  describe('invokeSportExtension', () => {
    it('football', () => {
      component['isFootball'] = true;
      component['invokeSportExtension']();
      expect(footballExtensionService.eventMarkets).toHaveBeenCalledTimes(1);
    });

    it('tennis', fakeAsync(() => {
      component['sportName'] = 'tennis';
      component['invokeSportExtension']();
      tick();
      expect(sportConfigService.getSport).toHaveBeenCalledWith('tennis');
      expect(tennisExtensionService.eventMarkets).toHaveBeenCalledTimes(1);
    }));
  });

  describe('DELETE_MARKET_FROM_CACHE', () => {
    it('should init after DELETE_MARKET_FROM_CACHE', () => {
      spyOn(component, 'init');
      component['marketsByCollection'] = <any>[{ markets: [{id: 1}] }];
      deleteMarketHandler(1);
      expect(component.init).toHaveBeenCalledTimes(1);
    });

    it('should not init after DELETE_MARKET_FROM_CACHE', () => {
      spyOn(component, 'init');
      component['marketsByCollection'] = <any>[{ markets: [{id: 1}] }];
      deleteMarketHandler(2);
      expect(component.init).not.toHaveBeenCalled();
    });
  });

  it('childComponentLoaded should set initialized to true', () => {
    component.childComponentLoaded();
    expect(component.initialized).toBeTruthy();
  });

  describe('sportDataHandler', () => {
    beforeEach(() => {
      spyOn(component, 'init');
    });

    it('data present', () => {
      component.sportDataHandler({ eventData: { event: [{}] } });
      expect(component.init).toHaveBeenCalledTimes(1);
    });

    it('no data', () => {
      component.sportDataHandler(null);
      expect(component.init).not.toHaveBeenCalled();
    });
  });

  describe('extendMarketsWithOptaLinks', () => {
    it('extendMarketsWithOptaLinks fot NOT YourCall markets', () => {
      const markets = [{name: 'match result'}] as any;
      const marketConfig = [{name: 'correct score'}];
      const links = [{marketName: 'match result', tabKey: 'assists' }];
      component['extendMarketsWithOptaLinks'](markets, marketConfig, links);
      expect(markets[0].marketOptaLink).toEqual(links[0]);
    });
    it('extendMarketsWithOptaLinks fot YourCall markets', () => {
      const markets = [{name: 'match result', templateMarketName: 'YourCall templateMarketName'}] as any;
      const marketConfig = [{name: 'correct score'}];
      const links = [{marketName: 'YourCall templateMarketName', tabKey: 'assists' }];
      component['extendMarketsWithOptaLinks'](markets, marketConfig, links);
      expect(markets[0].marketOptaLink).toEqual(links[0]);
    });
  });

  describe('createPlayerStatsMarketsGroup', () => {
    beforeEach(() => {
      component.sysConfig = { yourCallPlayerStatsName: { name: 'player' } };
      component.eventEntity = {
        markets: [{ templateMarketName: 'Player_Stats_' }, {}]
      };
      component.marketGroup = [];
    });

    it('should add market group', () => {
      component.createPlayerStatsMarketsGroup();
      expect(component.marketGroup.length).toBe(1);
    });

    it('should not add market group', () => {
      component.sysConfig.yourCallPlayerStatsName = null;
      component.marketGroup = [{ localeName: 'playerStats' }];
      component.createPlayerStatsMarketsGroup();
      expect(component.marketGroup.length).toBe(1);
    });
  });
  describe('insertCollapsedState', ()=>{
    it('insertCollapsedState non-MTA', () => {
      component.openedMarketTabsMap = { '1': {} };
      component.insertCollapsedState({id: '2'} as any, 1);
      expect(component.openedMarketTabsMap['2']).toBeDefined();
    });
    it('insertCollapsedState-MTA', () => {
      component.isMTASport = true;
      component.openedMarketTabsMap = { '1': {} };
      component.insertCollapsedState({name: '2'} as any, 1);
      expect(component.openedMarketTabsMap['2']).toBeDefined();
    });
  })
  

  describe('subscribeToEvents', () => {
    it('should detect changes (OUTCOME_UPDATED)', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'OUTCOME_UPDATED' && cb());
      component['subscribeToEvents']();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should check byb tabs (MOVE_EVENT_TO_INPLAY)', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'MOVE_EVENT_TO_INPLAY' && cb({ id: 1 }));
      spyOn(component, 'checkBybTabs');
      component.eventEntity = { id: 1 };
      component['subscribeToEvents']();
      expect(component.checkBybTabs).toHaveBeenCalled();
    });

    it('should not check byb tabs (MOVE_EVENT_TO_INPLAY)', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'MOVE_EVENT_TO_INPLAY' && cb({ id: 2 }));
      spyOn(component, 'checkBybTabs');
      component.eventEntity = { id: 1 };
      component['subscribeToEvents']();
      expect(component.checkBybTabs).not.toHaveBeenCalled();
    });

    it('should remove byb tabs (REMOVE_EDP_BYB_TABS)', () => {
      pubSubService.subscribe.and.callFake((name, channel, cb) => channel === 'REMOVE_EDP_BYB_TABS' && cb());
      spyOn(component, 'removeBybTabs');
      component['subscribeToEvents']();
      expect(component.removeBybTabs).toHaveBeenCalled();
    });
  });

  describe('checkBybTabs', () => {
    beforeEach(() => {
      component.eventEntity = { id: 1,  eventIsLive: false };
      component.eventTabs = [{ id: 'tab-all-markets', url: 'all-market-url' }, { id: 'tab-build-your-bet' }];
      spyOn(component, 'removeBybTabs').and.callThrough();
    });

    it('should not remove byb tabs', () => {
      component.checkBybTabs();
      expect(component.removeBybTabs).not.toHaveBeenCalled();
    });

    it('should remove byb tabs', () => {
      component.eventEntity.eventIsLive = true;
      component.checkBybTabs();
      expect(component.removeBybTabs).toHaveBeenCalled();
      expect(component.eventTabs).toEqual([{ id: 'tab-all-markets', url: 'all-market-url' }]);
    });

    it('should remove byb tabs and redirect to all markets', () => {
      component.eventEntity.eventIsLive = true;
      component.activeTab = { id: 'tab-build-your-bet' };
      component.checkBybTabs();
      expect(component.removeBybTabs).toHaveBeenCalled();
      expect(component.eventTabs).toEqual([{ id: 'tab-all-markets', url: 'all-market-url' }]);
      expect(router.navigateByUrl).toHaveBeenCalledWith('all-market-url');
      expect(pubSubService.publish).toHaveBeenCalledWith('REMOVE_BYB_STORED_EVENT', component.eventEntity.id);
    });
  });

  describe('#validateMarketTab', () => {
    it('should not set five a side launcher, if it is not all markets tab', () => {
      cmsService.getFeatureConfig.and.returnValue(of({enabled: false}));
      environment.brand = 'ladbrokes';
      spyOn(component as any, 'setFiveASideLauncher');
      component['validateMarketTab']({id: 2, tab: {id: 'no-market'} as any});
      expect(component['setFiveASideLauncher']).not.toHaveBeenCalled();
    });
    it('should call cms servic, if it is all markets tab', () => {
      cmsService.getFeatureConfig.and.returnValue(of({enabled: false}));
      environment.brand = 'ladbrokes';
      spyOn(component as any, 'setFiveASideLauncher');
      component['validateMarketTab']({id: 2, tab: {id: 'tab-all-markets'} as any});
      expect(component['setFiveASideLauncher']).toHaveBeenCalled();
    });
    it('should not set five a side launcher, if cms service does not return any config', () => {
      cmsService.getFeatureConfig.and.returnValue(of({}));
      environment.brand = 'ladbrokes';
      component['validateMarketTab']({id: 2, tab: {id: 'tab-all-markets'} as any});
      expect(component.showBanner).toBe(false);
    });
    it('should not set five a side launcher, if cms config is disabled', () => {
      cmsService.getFeatureConfig.and.returnValue(of({enabled: false}));
      environment.brand = 'ladbrokes';
      component['validateMarketTab']({id: 2, tab: {id: 'tab-all-markets'} as any});
      expect(component.showBanner).toBe(false);
    });
    it('should not set five a side launcher, if cms config is enabled but no five a side tab', () => {
      cmsService.getFeatureConfig.and.returnValue(of({enabled: true,
      header: 'header', description: 'description', position: 2}));
      component.eventTabs = [{id: 'tab-main-markets'}, {id: 'tab-all-markets'}] as any;
      component.filteredMarketGroup = [{ id: 1 }] as any;
      component['validateMarketTab']({id: 2, tab: {id: 'tab-all-markets'} as any});
      expect(component.showBanner).toBe(false);
    });
    it('should set five a side launcher, if cms config is enabled and has five a side tab', () => {
      cmsService.getFeatureConfig.and.returnValue(of({enabled: true,
      header: 'header', description: 'description', position: 2}));
      component.eventTabs = [{id: 'tab-main-markets'}, {id: 'tab-all-markets'},
      { id: 'tab-5-a-side'}] as any;
      component.filteredMarketGroup = [{ id: 1 }, {id: 2}] as any;
      component['validateMarketTab']({id: 2, tab: {id: 'tab-all-markets'} as any});
      expect(component.showBanner).toBe(true);
    });
    it('should not set five a side launcher, if event is not triggered from mobile', () => {
      component.showBanner = false;
      component['validateMarketTab'](null);
      expect(component.showBanner).toBe(false);
    });
  });

  it('should not set five a side launcher, if cms config is enabled and has five a side tab but not all markets', () => {
    cmsService.getFeatureConfig.and.returnValue(of({enabled: true,
    header: 'header', description: 'description', position: 2}));
    component.eventTabs = [{id: 'tab-main-markets'}, {id: 'tab-all-markets'},
    { id: 'tab-5-a-side'}] as any;
    component.filteredMarketGroup = [{ id: 1 }, {id: 2}] as any;
    component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
    expect(component.showBanner).toBe(false);
  });
  describe('#FiveASideLauncher', () => {
    it('should not set five-a-side content length, if both conditions does not satisfy', () => {
      const config = {};
      cmsService.getFeatureConfig.and.returnValue(of(config));
      component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
      expect(component['fiveASideContent']).toBe(undefined);
    });
    it('should not set five-a-side content , if only one condition satisfy', () => {
      const config = {
          enabled: false
      };
      cmsService.getFeatureConfig.and.returnValue(of(config));
      component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
      expect(component['fiveASideContent']).toBe(undefined);
    });
    it('should set five-a-side content, if both condition satisfy(length < 112)', () => {
      const config = {enabled: true,
        header: 'header', description: 'description', position: 2};
      component.eventTabs = [{id: 'tab-main-markets'}, {id: 'tab-all-markets'},
      { id: 'tab-5-a-side'}] as any;
      component.filteredMarketGroup = [{ id: 1 }, {id: 2}] as any;
      cmsService.getFeatureConfig.and.returnValue(of(config));
      component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
      expect(component['fiveASideContent']).toBe(`description`);
    });
    it('should set five-a-side content, if both condition satisfy(length > 112)', () => {
      const config = {enabled: true,
        header: 'header',
        description: 'Pick between 2-5 players from selected matches to complete markets in 90 minutes and back them to be successful!come',
        position: 2};
      cmsService.getFeatureConfig.and.returnValue(of(config));
      component.eventTabs = [{id: 'tab-main-markets'}, {id: 'tab-all-markets'},
      { id: 'tab-5-a-side'}] as any;
      component.filteredMarketGroup = [{ id: 1 }, {id: 2}] as any;
      component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
      expect(component['fiveASideContent']).toBe(`${config.description.substring(0, 112)}...`);
    });

    describe('#FiveASideLauncher', () => {
      it('should not set five-a-side content length, if both conditions does not satisfy', () => {
        const config = {};
        cmsService.getFeatureConfig.and.returnValue(of(config));
        component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
        expect(component['fiveASideTitle']).toBe(undefined);
      });
      it('should not set five-a-side content , if only one condition satisfy', () => {
        const config = {
            enabled: false
        };
        cmsService.getFeatureConfig.and.returnValue(of(config));
        component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
        expect(component['fiveASideTitle']).toBe(undefined);
      });
      it('should set five-a-side content, if both condition satisfy(length < 20)', () => {
        const config = {enabled: true,
          header: 'header', description: 'description', position: 2};
        component.eventTabs = [{id: 'tab-main-markets'}, {id: 'tab-all-markets'},
        { id: 'tab-5-a-side'}] as any;
        component.filteredMarketGroup = [{ id: 1 }, {id: 2}] as any;
        cmsService.getFeatureConfig.and.returnValue(of(config));
        component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
        expect(component['fiveASideTitle']).toBe(`header`);
      });
      it('should set five-a-side content, if both condition satisfy(length > 20)', () => {
        const config = {enabled: true,
          header: 'My 5-a-side team .......',
          description: 'description',
          position: 2};
        cmsService.getFeatureConfig.and.returnValue(of(config));
        component.eventTabs = [{id: 'tab-main-markets'}, {id: 'tab-all-markets'},
        { id: 'tab-5-a-side'}] as any;
        component.filteredMarketGroup = [{ id: 1 }, {id: 2}] as any;
        component['setFiveASideLauncher']({id: 'tab-main-markets'} as any);
        expect(component['fiveASideTitle']).toBe(`${config.header.substring(0, 23)}...`);
      });
    });
  });

  describe('#drilldownTagNames', () => {
    it('should return market name with drilldowntagnames',() => {
      component.eventEntity = {categoryId: '16'};
      const result = component.appendDrillDownTagNames({name: 'Match Result', drilldownTagNames:'MKTFLAG_PB,'});
      expect(result).toEqual('MKTFLAG_PB,Match Result,');
    });

    it('should return market name with out drilldowntagnames',() => {
      component.eventEntity = {categoryId: '16'};
      const result = component.appendDrillDownTagNames({name: 'Match Result', drilldownTagNames:''});
      expect(result).toEqual('Match Result,');
    });

    it('should return drilldownTagNames without market name',() => {
      component.eventEntity = {categoryId: '21'};
      const result = component.appendDrillDownTagNames({name: 'Both Teams to Score', drilldownTagNames:'MKTFLAG_PB,'});
      expect(result).toEqual('MKTFLAG_PB,');
    });

    it('should return drilldownTagNames without market names for HR categoryId',() => {
      component.eventEntity = {categoryId: '21'};
      const result = component.appendDrillDownTagNames({name: 'Match Result', drilldownTagNames:''});
      expect(result).toEqual('');
    });
  })

  describe('#handleStatisticalEvents',()=>{
    it('should close the handleStatisticalEvents screen on close emitter', () => {
      const event: any = { output: 'marketStatistical', value: {isSCAvailable:true, id:'1234'} }
      const cMarket = null;
      component.filteredMarketGroup = [{isSCAvailable:true, id:'1234'}] as IMarket[];
      component.handleStatisticalEvents(event);
      expect(component.filteredMarketGroup[0].id).toEqual(event.value.id);
  });

    it('should close the handleStatisticalEvents screen on close emitter', () => {
      const event: any = { output: 'marketStatistical', value: {isSCAvailable:true, id:'1234'} }
      const cMarket = null;
      component.filteredMarketGroup = [{isSCAvailable:true, id:'12345'}] as IMarket[];
      component.handleStatisticalEvents(event);
      expect(component.filteredMarketGroup[0].id).not.toEqual(event.value.id);
    });
    it('should close the handleStatisticalEvents screen on close emitter2', () => {
      const event: any = { output: 'marketStatistical', value: {isSCAvailable:true, marketIds:['12345']} }
      const cMarket = null;
      component.filteredMarketGroup = [{isSCAvailable:true, id:'12345'}] as IMarket[];
      component.handleStatisticalEvents(event);
      expect(component.filteredMarketGroup[0].id).not.toEqual(event.value.id);
    });
  });

  it('isSingleMarketViewType', ()=>{
    expect(component.isSingleMarketViewType('WW')).toBeTruthy();
    expect(component.isSingleMarketViewType('WDW')).toBeTruthy();
    expect(component.isSingleMarketViewType('Handicap WW')).toBeTruthy();
    expect(component.isSingleMarketViewType('Handicap WDW')).toBeTruthy();
    expect(component.isSingleMarketViewType('List')).toBeTruthy();
    expect(component.isSingleMarketViewType('Scorer')).toBeFalsy();
    expect(component.isSingleMarketViewType('Correct Score')).toBeFalsy();
  });

  it('should call formatTemplateMarketName', () => {
    let market: any = {
      rawHandicapValue: '0.5',
      name: '+0.5Football',
      templateMarketName: 'handicap'
    };
    expect(component.formatTemplateMarketName(market)).toEqual('Football');
    market = {
      rawHandicapValue: '0.5',
      name: '0.5Football',
      templateMarketName: 'handicap'
    };
    expect(component.formatTemplateMarketName(market)).toEqual('Football');
  });
});
