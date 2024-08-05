import { DesktopSportEventPageComponent } from '@ladbrokesDesktop/edp/components/sportEventPage/sport-event-page.component';
import { of as observableOf } from 'rxjs';

describe('LadbrokesDesktopSportEventPageComponent', () => {
  let component: DesktopSportEventPageComponent;
  let activatedRoute;
  let sportEventPageProviderService;
  let templateService;
  let router;
  let pubSubService;
  let storageService;
  let footballExtensionService;
  let tennisExtantionService;
  let routingHelperService;
  let sportsConfigService;
  let changeDetectorRef;
  let windowRefService;
  let cmsService;
  let routingState;
  let marketsOptaLinksService;
  let localeService;
  let seoDataService;
  let isPropertyAvailableService; 
  let cashOutLabelService;
  let sportEventPageService;

  const fakeObservable = {
    unsubscribe: jasmine.createSpy()
  };

  beforeEach(() => {

    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy()
        }
      }
    };

    sportEventPageProviderService = {
      sportData: {
        subscribe: jasmine.createSpy().and.returnValue(fakeObservable),
        unsubscribe: jasmine.createSpy()
      }
    };

    templateService = {
      sortOutcomesByPrice: jasmine.createSpy('sortOutcomesByPrice')
    };

    router = {
      events: {
        subscribe: jasmine.createSpy().and.returnValue(fakeObservable),
        unsubscribe: jasmine.createSpy()
      }
    };

    pubSubService = {
      API: {
        DELETE_MARKET_FROM_CACHE: 'DELETE_MARKET_FROM_CACHE'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl'),
    };

    storageService = {
      remove: jasmine.createSpy('remove')
    };
    tennisExtantionService = {};
    footballExtensionService = {};
    sportsConfigService = {};
    cmsService = {
      getFeatureConfig: jasmine.createSpy('getSystemConfig')
    };
    
    routingState = {
      getPreviousUrl: jasmine.createSpy('getPreviousUrl')
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    marketsOptaLinksService = {
      getMarketLinks: jasmine.createSpy('getMarketLinks').and.returnValue(observableOf())
    };

    windowRefService = {
      document: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };

    localeService = {
      getString: jasmine.createSpy().and.returnValue('Match Result')
    };

    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    isPropertyAvailableService = {
      isPropertyAvailable: jasmine.createSpy('isPropertyAvailable')
    };
    cashOutLabelService = {
      isAnyCashoutAvailable: jasmine.createSpy('isAnyCashoutAvailable')
    }
    sportEventPageService = {
      transformMarkets: jasmine.createSpy('transformMarkets')
    }
    component = new DesktopSportEventPageComponent(
      router,
      activatedRoute,
      sportEventPageProviderService,
      templateService,
      footballExtensionService,
      tennisExtantionService,
      routingHelperService,
      pubSubService,
      storageService,
      sportsConfigService,
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
    const links = [{}, {}];
    marketsOptaLinksService.getMarketLinks.and.returnValue(observableOf(links));
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('should check default component properties', () => {
    const links = [{}, {}] as any;
    marketsOptaLinksService.getMarketLinks.and.returnValue(observableOf(links));
    component.ngOnInit();
    expect(component.openedMarketTabsCountByDefault).toEqual(4);

    component.replaySubj.subscribe( (data) => {
      expect(data).toEqual(links);
    });
  });
  describe('goToSeo', () => {
    it('should create seo ', () => {
      routingHelperService.formEdpUrl.and.returnValue('url');
      component.goToSeo(({id: '1'} as any));
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith({ id: '1' },'url');
    });
  });
  describe('isSameEvent', () => {
    it('should return false if event is not available', () => {
      component.eventEntity = null;

      expect(component['isSameEvent']()).toBeFalsy();
    });

    it('should return false if there are different ids in stored event and url', () => {
      activatedRoute.snapshot.paramMap.get.and.returnValue('2');
      component.eventEntity = { id: 1 } as any;

      expect(component['isSameEvent']()).toBeFalsy();
    });

    it('should return true if there are same ids in stored event and url', () => {
      const id = '2';

      activatedRoute.snapshot.paramMap.get.and.returnValue(id);
      component.eventEntity = { id: +id } as any;

      expect(component['isSameEvent']()).toBeTruthy();
    });
  });
});
