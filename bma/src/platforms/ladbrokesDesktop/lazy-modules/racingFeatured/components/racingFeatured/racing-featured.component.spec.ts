import { RacingFeaturedComponent } from './racing-featured.component';

describe('LDRacingFeaturedComponent', () => {
  let component;
  let locale;
  let filtersService;
  let windowRef;
  let pubsub;
  let featuredModuleService;
  let templateService;
  let commentsService;
  let wsUpdateEventService;
  let sportEventHelper;
  let cmsService;
  let promotionsService;
  let changeDetectorRef;
  let router;
  let gtmService;
  let routingHelperService;
  let awsService;
  let user;
  let eventService;
  let virtualSharedService;
  let racingGaService;
  let storage;
  let horseRacingService;
  let greyhoundService;
  let routingState;
  let buildUtilityService;
  let timeService;
  let deviceService;
  let bonusSuppressionService;
  let vEPService;

  beforeEach(() => {
    locale = {};
    filtersService = {};
    windowRef = {
      nativeWindow: {
        setInterval:  jasmine.createSpy('setInterval').and.callFake(cb => cb())
      }
    };
    pubsub = {};
    featuredModuleService = {};
    templateService = {};
    commentsService = {};
    wsUpdateEventService = {};
    sportEventHelper = {};
    cmsService = {};
    router = {};
    gtmService = {};
    routingHelperService = {};
    promotionsService = {};
    changeDetectorRef = {
      detach: jasmine.createSpy('cdr.detach'),
      detectChanges: jasmine.createSpy('cdr.detectChanges')
    };
    awsService = {};
    user = {};
    eventService = {};
    virtualSharedService = {};
    racingGaService = {};
    storage = {};
    horseRacingService = {};
    greyhoundService = {};
    routingState = {};
    buildUtilityService = {};
    timeService = {};
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    };
    vEPService = {}

    component = new RacingFeaturedComponent(
      locale,
      filtersService,
      windowRef,
      pubsub,
      featuredModuleService,
      templateService,
      commentsService,
      wsUpdateEventService,
      sportEventHelper,
      cmsService,
      promotionsService,
      changeDetectorRef,
      routingHelperService,
      router,
      gtmService,
      awsService,
      user,
      eventService,
      virtualSharedService,
      racingGaService,
      storage,
      horseRacingService,
      greyhoundService,
      routingState,
      buildUtilityService,
      timeService,
      deviceService,
      bonusSuppressionService,
      vEPService
    );
  });

  it('emitFetchCardId', () => {
    component.fetchCardId.emit = jasmine.createSpy('emitFetchCardId.emit');
    component.emitFetchCardId('123');
    expect(component.fetchCardId.emit).toHaveBeenCalledWith('123');
  });
});
