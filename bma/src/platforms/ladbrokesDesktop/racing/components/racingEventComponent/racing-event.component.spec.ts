import { DesktopRacingEventComponent } from './racing-event.component';

import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { eventMock } from '@racing/components/racingEventComponent/racing-event.component.mock';

describe('DesktopRacingEventComponent', () => {
  let component: DesktopRacingEventComponent;
  let windowRef,
  timeService,
  pubSubService,
  nativeBridgeService,
  ukToteService,
  lpAvailabilityService,
  deviceService,
  gtmService,
  streamTrackingService,
  dialogService,
  filterService,
  localeService,
  horseracing,
  routingHelperService,
  cmsService,
  tools,
  sbFilters,
  router,
  location,
  changeDetectorRef,
  sortByOptionsService,
  route,
  watchRulesService,
  seoDataService,
  elementRef,
  racingGaService

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        document: {} as HTMLDocument,
        open: jasmine.createSpy('window.open')
      } as any
    };
    timeService = seoDataService = {};
    pubSubService = {
      API: {
        CLOSE_SORT_BY: 'CLOSE_SORT_BY',
        SORT_BY_OPTION: 'SORT_BY_OPTION'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        channelFunction('price');
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };
    nativeBridgeService = {};
    ukToteService = {};
    lpAvailabilityService = {};
    deviceService = {};
    gtmService = {
      push: jasmine.createSpy('push')
    };
    streamTrackingService = {};
    dialogService = {};
    filterService = {};
    localeService = {};
    horseracing = {
      showHideToolTip: jasmine.createSpy('showHideToolTip').and.returnValue(true)
    };
    routingHelperService = {};
    cmsService =  {};
    tools = {};
    sbFilters = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.returnValue(eventMock.markets[0].outcomes)};
    router = {};
    location = {};
    changeDetectorRef = {};
    sortByOptionsService = {};
    route = {};

    watchRulesService = {
      shouldShowCSBIframe: jasmine.createSpy('shouldShowCSBIframe')
    };

    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy().and.returnValue({ clientWidth: 22 })
      }
    } as any;

    racingGaService = {
      trackEvent: jasmine.createSpy('trckEvent')
    };

    component = new DesktopRacingEventComponent(
      windowRef,
      timeService,
      pubSubService,
      nativeBridgeService,
      ukToteService,
      lpAvailabilityService,
      deviceService,
      gtmService,
      streamTrackingService,
      dialogService,
      filterService,
      localeService,
      horseracing,
      routingHelperService,
      cmsService,
      tools,
      sbFilters,
      router,
      location,
      changeDetectorRef,
      sortByOptionsService,
      route,
      watchRulesService,
      seoDataService,
      elementRef,
      racingGaService
    );
  });

  it('#openLiveCommentary without CMS config', () => {
    component.defaultLiveCommentaryUrl = 'https://test-live-commentary.com';
    component.sportName = 'horseracing';
    component.openLiveCommentary();

    component.sportName = 'greyhound';
    component.openLiveCommentary();

    component.liveCommentary = {
      horseracing: 'https://horseracing-live-commentary.com',
      greyhound: 'https://greyhound-live-commentary.com',
    };

    component.openLiveCommentary();

    expect(windowRef.nativeWindow.open).toHaveBeenCalledTimes(3);
  });

  describe('#ngOnInit', () => {
    it('if have eventEntity should set racingPostVerdictData', () => {
      RacingEventComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      component.expandedSummary = [];
      component.eventEntity = Object.assign({}, eventMock);
      component.ngOnInit();

      expect(component.racingPostVerdictData).toEqual({} as any);
    });

    it('if have not eventEntity racingPostVerdictData should not to be defined', () => {
      RacingEventComponent.prototype.ngOnInit = jasmine.createSpy('super.ngOnInit');
      component.expandedSummary = [];
      component.eventEntity = null;
      component.ngOnInit();

      expect(component.racingPostVerdictData).not.toBeDefined();
    });
  });
});
