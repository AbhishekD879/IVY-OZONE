import { of as observableOf } from 'rxjs';
import { FeaturedModuleComponent } from '@featured/components/featured-module/featured-module.component';
import {
  featuredDataMock,
  surfaceBetModuleWithHREvent
} from '@featured/components/featured-module/featured-module.component.mock';
import { LadbrokesFeaturedModuleComponent } from '@ladbrokesMobile/featured/components/featured-module/featured-module.component';
import { FANZONECONFIG } from '@ladbrokesMobile/featured/components/featured-module/mockdata/featured-module.component.mock';

describe('LadbrokesFeaturedModuleComponent', () => {
  let component: LadbrokesFeaturedModuleComponent;

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
  let germanSupportFeaturedService;
  let router;
  let routingHelperService;
  let gtmService;
  let awsService;
  let userService;
  let eventService;
  let virtualSharedService;
  let vanillaApiService;
  let location;
  let freeRideHelperService;
  let bonusSuppressionService;
  let deviceService;
  let storage;

  const sitecorePromotion = [{
    type: 'segmentDefault',
    teasers: [{
      title: 'Test',
      subTitle: 'QA',
      itemId: '{32ACDBCF-D0CD-4194-91EA-A49182D0473D}',
      backgroundImage: {src: 'abc'}
    }]
  }];
  const fanzoneConfig = FANZONECONFIG

  const teamColors = [{
    primaryColour: '#CCC',
    secondaryColour: '#DDD',
    teamName: 'Man United',
  }];

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy().and.returnValue('tranlation')
    };
    filtersService = {
      orderBy: jasmine.createSpy().and.callFake((args) => args)
    };
    windowRef = {
      nativeWindow: {
        view: { mobile: true },
        setInterval: (callback: Function, time: number) => {
          setTimeout(() => {
            callback();
          }, time);
        },
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearInterval: jasmine.createSpy(),
        location:{href: 'football'}
      }
    };
    pubsub = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: {
        NAMESPACE_ERROR: 'NAMESPACE_ERROR',
        SESSION_LOGIN: 'SESSION_LOGIN'
      }
    };
    featuredModuleService = {
      addEventListener: jasmine.createSpy(),
      reconnect: jasmine.createSpy(),
      startConnection: jasmine.createSpy(),
      onError: jasmine.createSpy(),
      clearSubscribedFeaturedTabModules: jasmine.createSpy(),
      disconnect: jasmine.createSpy(),
      cacheEvents: jasmine.createSpy(),
      addModuleToSubscribedFeaturedTabModules: jasmine.createSpy(),
      tabModuleStates: new Map(),
      emit: jasmine.createSpy(),
      addClock: jasmine.createSpy().and.callFake((args) => args),
      getSubscribedFeaturedTabModules: jasmine.createSpy(),
      removeAllListeners: jasmine.createSpy(),
      removeEventListener: jasmine.createSpy()
    };
    templateService = {
      setCorrectPriceType: jasmine.createSpy()
    };
    commentsService = {
      badmintonMSInitParse: jasmine.createSpy()
    };
    wsUpdateEventService = {
      subscribe: jasmine.createSpy()
    };
    sportEventHelper = {
      isSpecialEvent: jasmine.createSpy().and.returnValue(true)
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        YourCallIconsAndTabs: {
          enableIcon: true
        },
        'Highlight Carousel': {
          enabled: true
        },
        Fanzone: {
          enabled: true
        }
      })),
      getFanzone: jasmine.createSpy('getFanzone').and.returnValue(observableOf(fanzoneConfig)),
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(observableOf(teamColors)),
    };
    promotionsService = {
      openPromotionDialog: jasmine.createSpy()
    };

    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    germanSupportFeaturedService = {
      getInitialData: jasmine.createSpy().and.returnValue(featuredDataMock),
      getActualData: jasmine.createSpy(),
      moduleFilterHandler:  jasmine.createSpy(),
      isGermanUser: jasmine.createSpy().and.returnValue(true)
    };

    router = { navigateByUrl: jasmine.createSpy() };
    gtmService = { push: jasmine.createSpy() };
    routingHelperService = { formSportUrl: jasmine.createSpy().and.returnValue('/horse-racing') };
    userService = {username: 'abc'};
    eventService = {};
    vanillaApiService = {
      get: jasmine.createSpy('get').and.returnValue(observableOf(sitecorePromotion))
    };

    awsService = {
      addAction: jasmine.createSpy()
    };
    virtualSharedService = { isVirtual: () => false };
    location = {
      href: '/football'
    };
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled'),
    };

    component = new LadbrokesFeaturedModuleComponent(
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
      germanSupportFeaturedService,
      routingHelperService,
      router,
      gtmService,
      awsService,
      userService,
      eventService,
      virtualSharedService,
      vanillaApiService,
      location,
      freeRideHelperService,
      bonusSuppressionService,
      deviceService,
      storage
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('onSocketUpdate', () => {
    component.badges = {};
    component.featuredModuleData = {
      modules: []
    } as any;

    FeaturedModuleComponent.prototype['featureTabOnSocketUpdate'] = jasmine.createSpy('featuredTabOnSocketUpdate');
    component['onSocketUpdate'](surfaceBetModuleWithHREvent);

    germanSupportFeaturedService.isGermanUser.and.returnValue(false);
    component['onSocketUpdate'](surfaceBetModuleWithHREvent);

    expect(pubsub.subscribe).toHaveBeenCalledWith('LadbrokesFeaturedModuleComponent', 'SESSION_LOGIN', jasmine.any(Function));
    expect(FeaturedModuleComponent.prototype['featureTabOnSocketUpdate']).toHaveBeenCalledTimes(2);
  });

  it('should call needed methods on init', () => {
    spyOn(FeaturedModuleComponent.prototype, 'init');
    component.init(<any>featuredDataMock);
    expect(FeaturedModuleComponent.prototype.init).toHaveBeenCalledWith(featuredDataMock as any);
    expect(component['germanSupportFeaturedService'].getInitialData).toHaveBeenCalledWith(featuredDataMock as any);
  });

  it('should call needed methods on ngOnDestroy', () => {
    spyOn(FeaturedModuleComponent.prototype, 'ngOnDestroy');
    component.ngOnDestroy();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('LadbrokesFeaturedModuleComponent');
    expect(FeaturedModuleComponent.prototype.ngOnDestroy).toHaveBeenCalled();
  });

  it('should use OnPush strategy', () => {
    expect(LadbrokesFeaturedModuleComponent['__annotations__'][0].changeDetection).toBe(0);
  });
});
