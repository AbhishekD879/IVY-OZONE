import { StreamBetOverlayProviderComponent } from './stream-bet-overlay-provider.component';
import {
  Subject, of, Subscription
} from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ISportEvent } from '@core/models/sport-event.model';

describe('StreamBetOverlayProviderComponent', () => {
    let component;
    let activatedRoute;
    let sportEventPageProviderService;
    let templateService;
    let router;
    let footballExtensionService;
    let tennisExtensionService;
    let pubSubService;
    let filtersService;
    let routingHelperService;
    let smartBoostsService;
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
    let quickbetService;
    let userService;
    let eventVideoStreamProviderService;
    let streamBetService;
    let isPropertyAvailableService;
    let cashOutLabelService;
    let sportEventPageService;
    let storageService;
    let gtmService;

    const eventEntity = {
        siteChannels: 'M, S, ',
        liveStreamAvailable: true,
        markets: [
        {
            marketStatusCode: 'A',
            id: '27',
            siteChannels: "P,Q,C,I,M,",
            isMarketBetInRun: 'true',
            isDisplayed: 'true'
        },
        {
            marketStatusCode: 'A',
            id: '28',
            siteChannels: "P,Q,C,I,M,",
            isMarketBetInRun: 'true',
            isDisplayed: 'true'
        }
        ]
    } as any;
  const testStr = 'TestString';
  const wasPriceStub = 'TestWasPrice';
  const marketTemplateType = 'price-odd-button';

  const marketsByCollection: ISportEvent[] = [
    { name: 'All Markets', markets: [] }] as ISportEvent[];

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

    filtersService = {
      groupBy: jasmine.createSpy(),
      filterAlphabetsOnly: jasmine.createSpy('filterAlphabetsOnly').and.returnValue('filterAlphabetsOnly'),
      filterNumbersOnly: jasmine.createSpy('filterNumbersOnly').and.returnValue('filterNumbersOnly')
    };

    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
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

    quickbetService = {
      quickBetOnOverlayCloseSubj: new Subject<string>()
    };
    userService = {
        sportBalanceWithSymbol: 10,
        sportBalance: '10'
    };
    eventVideoStreamProviderService = {
      isStreamAndBet: true
    };
    streamBetService = {
      lastTemplateLoadedSubj: new Subject<void>(),
      multiOddMarketCounter: 0,
      totalMultiOddMarketElemsCount: 0,
      getMarketTemplate: jasmine.createSpy().and.returnValue(marketTemplateType)
    }
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };

    component = new StreamBetOverlayProviderComponent(
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
      seoDataService, isPropertyAvailableService, cashOutLabelService, sportEventPageService,
      quickbetService, userService, eventVideoStreamProviderService, streamBetService,
      storageService, gtmService
    );
    component.marketsByCollection = marketsByCollection;
    component.eventEntity = eventEntity;
    component.currMktContainerScrollLeft = 10;
  });

  it('StreamBetOverlayProviderComponent: should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('StreamBetOverlayProviderComponent: ngOnInit with quickbet close scenario', () => {
    component.marketsByCollection = [{
      name: 'All Markets', markets: [
        {
          marketStatusCode: 'A',
          id: '27',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Match result'
        },
        {
          marketStatusCode: 'A',
          id: '28',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Both Teams To Score'
        }
      ]
    }];
    component.ngOnInit();
    expect(component.showQuickBet).toEqual(false);
    expect(component.showReceipt).toEqual(false);
    expect(component.allMarkets).toEqual(component.marketsByCollection[0].markets);
  });

  it('splitMarkets - special-market', () => {
    component.marketsByCollection = [{
      name: 'All Markets', markets: [
        {
          marketStatusCode: 'A',
          id: '27',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Match result'
        },
        {
          marketStatusCode: 'A',
          id: '28',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Both Teams To Score'
        }
      ]
    }];
    component.streamBetService.getMarketTemplate = (market, eventEntity) => {
        return 'special-market';
      };
      component.ngOnInit();
      component.streamBetService.lastTemplateLoadedSubj.next();
    expect(component.showQuickBet).toEqual(false);
    expect(component.showReceipt).toEqual(false);
    expect(component.allMarkets).toEqual(component.marketsByCollection[0].markets);
  });

  it('splitMarkets - single-drop-double-odd', () => {
    component.marketsByCollection = [{
      name: 'All Markets', markets: [
        {
          marketStatusCode: 'A',
          id: '27',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Match result'
        },
        {
          marketStatusCode: 'A',
          id: '28',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Both Teams To Score'
        }
      ]
    }];
    component.streamBetService.getMarketTemplate = (market, eventEntity) => {
        return 'single-drop-double-odd';
      };
      component.ngOnInit();
    expect(component.showQuickBet).toEqual(false);
    expect(component.showReceipt).toEqual(false);
  });

  it('splitMarkets - special', () => {
    component.marketsByCollection = [{
      name: 'All Markets', markets: [
        {
          marketStatusCode: 'A',
          id: '27',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Match result'
        },
        {
          marketStatusCode: 'A',
          id: '28',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Both Teams To Score'
        }
      ]
    }];
    component.streamBetService.getMarketTemplate = (market, eventEntity) => {
        return 'special';
      };
      component.ngOnInit();
    expect(component.showQuickBet).toEqual(false);
    expect(component.showReceipt).toEqual(false);
  });

  it('StreamBetOverlayProviderComponent: ngOnInit with quickbet receipt scenario', () => {
    component.marketsByCollection = [{
      name: 'All Markets', markets: [
        {
          marketStatusCode: 'A',
          id: '27',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Match result'
        },
        {
          marketStatusCode: 'A',
          id: '28',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Both Teams To Score'
        }
      ]
    }];
    component.ngOnInit();
    component['quickbetService'].quickBetOnOverlayCloseSubj.next('qb receipt');
    expect(component.showQuickBet).toEqual(true);
    expect(component.showReceipt).toEqual(true);
    expect(component.allMarkets).toEqual(component.marketsByCollection[0].markets);
  });

  it('StreamBetOverlayProviderComponent: ngOnInit with close qb panel scenario', () => {
    component.marketsByCollection = [{
      name: 'All Markets', markets: [
        {
          marketStatusCode: 'A',
          id: '27',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Match result'
        },
        {
          marketStatusCode: 'A',
          id: '28',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Both Teams To Score'
        }
      ]
    }];
    component.ngOnInit();
    component['quickbetService'].quickBetOnOverlayCloseSubj.next('close qb panel');
    expect(component.showQuickBet).toEqual(false);
    expect(component.showReceipt).toEqual(false);
  });

  it('StreamBetOverlayProviderComponent: showHideClick with qb show', () => {
    component.showMarkets = true;
    component.showHideText = 'HIDE';
    component.showHideClick();
    expect(component.showHideText).toEqual('SHOW');
    expect(component.showMarkets).toEqual(false);
  });

  it('StreamBetOverlayProviderComponent: showHideClick with qb hide', () => {
    component.showMarkets = true;
    component.showHideText = 'SHOW';
    component.showHideClick();
    expect(component.showHideText).toEqual('HIDE');
    expect(component.showMarkets).toEqual(false);
  });

  describe('#splitMarkets', () => {
    it('should split markets null', () => {
      component.allMarkets = null;
      component.splitMarkets();
        expect(component.allMarkets).toBe(null);
    });

    it('should split markets undefined', () => {
      component.allMarkets = undefined;
      component.splitMarkets();
      expect(component.allMarkets).toBe(undefined);
  });

    it('should split markets correctly', () => {
      const allMarkets = [
        {
          name: 'Market 1',
          outcomes: [{}, {}],
          templateMarketName: 'Template Market 1'
        },
        {
          name: 'Market 2',
          outcomes: [{}, {}],
          templateMarketName: 'Template Market 2'
        }
      ];

      component.allMarkets = allMarkets;
      component.streamBetService.getMarketTemplate = (market, eventEntity) => {
          return 'price-odd-button';
      };
      component.templateService = {
        sortOutcomesByPriceAndDisplayOrder: (outcomes) => {
          return outcomes;
        }
      };
      component.eventEntity = {};
      component.splitMarkets();
      expect(component.templateMarketTypes).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 1']).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 1'].markets.length).toBe(1);
      expect(component.templateMarketTypes['template-market-type']['Template Market 2']).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 2'].markets.length).toBe(1);
    });

    it('should split markets correctly', () => {
      const allMarkets = [
        {
          name: 'Market 1',
          outcomes: [{}, {}],
          templateMarketName: 'Template Market 1'
        },
        {
          name: 'Market 2',
          outcomes: [{}, {}],
          templateMarketName: 'Template Market 2'
        }
      ];

      component.allMarkets = allMarkets;
      component.streamBetService.getMarketTemplate = (market, eventEntity) => {
          return 'special-market';
      };
      component.templateService = {
        sortOutcomesByPriceAndDisplayOrder: (outcomes) => {
          return outcomes;
        }
      };
      component.eventEntity = {};

      component.splitMarkets();

      expect(component.templateMarketTypes).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 1']).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 1'].markets.length).toBe(1);
      expect(component.templateMarketTypes['template-market-type']['Template Market 2']).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 2'].markets.length).toBe(1);
    });

    it('should split markets correctly', () => {
      const allMarkets = [
        {
          name: 'Market 1',
          outcomes: [{}, {}],
          templateMarketName: 'Template Market 1'
        },
        {
          name: 'Market 2',
          outcomes: [{}, {}],
          templateMarketName: 'Template Market 2'
        }
      ];

      component.allMarkets = allMarkets;
      component.streamBetService.getMarketTemplate = (market, eventEntity) => {
          return 'single-drop-double-odd';
      };
      component.templateService = {
        sortOutcomesByPriceAndDisplayOrder: (outcomes) => {
          return outcomes;
        }
      };
      component.eventEntity = {};
      component.splitMarkets();
      expect(component.templateMarketTypes).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 1']).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 1'].markets.length).toBe(1);
      expect(component.templateMarketTypes['template-market-type']['Template Market 2']).toBeDefined();
      expect(component.templateMarketTypes['template-market-type']['Template Market 2'].markets.length).toBe(1);
    });
  });


  describe('#ngAfterViewInit', () => {
    it('call ngAfterViewInit', () => {
      component.sbOverlayLoaded.emit = jasmine.createSpy();
      component['ngAfterViewInit']();
      expect(component.sbOverlayLoaded.emit).toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    it('call ngOnDestroy', () => {
      const service = new StreamBetOverlayProviderComponent(
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
        seoDataService, isPropertyAvailableService, cashOutLabelService, sportEventPageService,
        quickbetService, userService, eventVideoStreamProviderService, streamBetService,
        storageService, gtmService
      );
      component.ngOnDestroy();
      expect(service['eventVideoStreamProviderService'].isStreamAndBet).toEqual(false);
    });
  });

  describe('sportBalance', () => {
    it('should return sportBalance', () => {
      component.sportBalance = 10;
      expect(component.sportBalance).toEqual(10);
    });
    it('should return sportBalance with null value', () => {
      component['userService'].sportBalance = 'undefined';
      component['userService'].sportBalanceWithSymbol = null;
      expect(component.sportBalance).toEqual(null);
    });
    it('should refresh sportBalance and return userService', () => {
      userService.sportBalance = 'undefined';
      const result = component.sportBalance;
      expect(component.balanceRefreshed).toBe(true);
      expect(result).toBe(component.sportBalance);
    });
  });

  describe('handleSelectionClick', () => {
    it('should call handleSelectionClick', () => {
      spyOn(document, 'querySelector').and.returnValue({scrollLeft: 100} as Element);
      component['handleSelectionClick'](eventEntity.markets[0], 0);
      expect(component.selectedMarket).toBe(eventEntity.markets[0]);
    });
  });

  it('StreamBetOverlayProviderComponent: ngOnInit with siteChannels null', () => {
    component.marketsByCollection = [{
      name: 'All Markets', markets: [
        {
          marketStatusCode: 'A',
          id: '27',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Match result'
        },
        {
          marketStatusCode: 'A',
          id: '28',
          siteChannels: "P,Q,C,I,M,",
          isMarketBetInRun: 'true',
          isDisplayed: 'true',
          viewType: 'test',
          templateMarketName: 'test',
          name: 'Both Teams To Score'
        }
      ]
    }];
    component.eventEntity.siteChannels = null;
    component.ngOnInit();
    expect(component.showQuickBet).toEqual(false);
    expect(component.showReceipt).toEqual(false);
  })

});
