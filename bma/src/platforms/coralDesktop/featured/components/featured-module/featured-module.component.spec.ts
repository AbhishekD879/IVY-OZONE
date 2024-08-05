import { of as observableOf } from 'rxjs';
import { DesktopFeaturedModuleComponent } from './featured-module.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import {
  featuredInplayModuleMock
} from '@featured/components/featured-module/featured-module.component.mock';

describe('DesktopFeaturedModuleComponent', () => {
  let component: DesktopFeaturedModuleComponent;

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
  let userService;
  let eventService;
  let virtualSharedService;
  let bonusSuppressionService;
  let deviceService;
  let storage;

  const featuredModulesMock = {
    modules: [
      {
        '@type': 'SurfaceBetModule',
        data: [
          {
            '@type': 'SurfaceBetModuleData'
          }
        ]
      },
      {
        '@type': 'EventsModule',
        data: [
          {
            '@type': 'EventsModuleData'
          }
        ]
      }
    ]
  };
  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy().and.returnValue('tranlation')
    };
    filtersService = {
      orderBy: jasmine.createSpy().and.callFake((args) => args)
    };
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    };
    windowRef = {
      nativeWindow: {
        view: {mobile: true},
        setInterval: (callback: Function, time: number) => {
          setTimeout(() => {
            callback();
          }, time);
        },
        setTimeout: jasmine.createSpy('setTimeout'),
        clearInterval: jasmine.createSpy(),
        location:{href:'abc'}
      }
    };
    pubsub = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      API: pubSubApi
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
      getSubscribedFeaturedTabModules: jasmine.createSpy().and.returnValue(['1', '2', '3']),
      removeAllListeners: jasmine.createSpy(),
      removeEventListener: jasmine.createSpy(),
      trackDataReceived: jasmine.createSpy('trackDataReceived')
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
        'Inplay Module': {
          enabled: true
        },
        'Sport Quick Links': {enabled: true}
      }))
    };

    router = {navigateByUrl: jasmine.createSpy()};
    gtmService = {push: jasmine.createSpy()};
    routingHelperService = {formSportUrl: jasmine.createSpy().and.returnValue('/horse-racing')};
    promotionsService = {
      openPromotionDialog: jasmine.createSpy()
    };

    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    awsService = {
      addAction: jasmine.createSpy()
    };
    userService = {};
    eventService = {};
    virtualSharedService = { isVirtual: () => false };

    component = new DesktopFeaturedModuleComponent(
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
      userService,
      eventService,
      virtualSharedService,
      bonusSuppressionService,
      deviceService,
      storage
    );
});

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#filterModules', () => {
    it('should filter modules for desktop', () => {
      const eventsModule = {
        hasNoLiveEvents: true,
        '@type': 'EventsModule'
      } as any;
      const surfaceBetModule = {
        '@type': 'SurfaceBetModule',
        data: [{
          eventIsLive: false,
          displayOnDesktop: true
        }]
      } as any;
      const highlightsCarouselModule = {
        '@type': 'HighlightCarouselModule',
        displayOnDesktop: true
      } as any;
      const modules = [
        eventsModule,
        featuredInplayModuleMock,
        surfaceBetModule,
        highlightsCarouselModule
      ] as any;
      const filteredModules = component['filterModules'](modules);
      expect(filteredModules).toEqual([eventsModule, surfaceBetModule, highlightsCarouselModule]);
    });
  });

  describe('#isEventsModule', () => {
    it('when is eventsModule', () => {
      const eventsModule = {
        hasNoLiveEvents: true,
        '@type': 'EventsModule'
      } as any;
      expect(component['isEventsModule'](eventsModule as any)).toBeTruthy();
    });

    it('when is not eventsModule', () => {
      expect(component['isEventsModule'](featuredInplayModuleMock as any)).toBeFalsy();
    });
  });

  describe('#onModuleUpdate', () => {
    beforeEach(() => {
      component.badges = {
        '5f17e543c9e77c0001f2c90c': {}
      } as any;
      component.featuredModuleData = {
        modules: featuredModulesMock.modules
      } as any;
    });
    it('should call filterDesktopSurfaceBets', () => {
      const data = {
        "@type": "SurfaceBetModule",
        _id: "5f17e543c9e77c0001f2c90c",
        isSpecial: true,
        isEnhanced: false,
        data: [
          {
            '@type': 'SurfaceBetModuleData'
          }
        ]
      } as any;
      component.onModuleUpdate(data);
    });
    it('should call removeInPlayEvents', () => {
      const data = {
        "@type": "EventsModule",
        _id: "5f17e543c9e77c0001f2c90c",
        isSpecial: true,
        isEnhanced: false,
        data: [
          {
            '@type': 'EventsModuleData'
          }
        ]
      } as any;
      component.onModuleUpdate(data);
    });
  });

  describe('isSurfaceBetModule', () => {
    it('#isSurfaceBetModule with data as undefined', () => {
      const data = {
        "@type": "SurfaceBetModule"
      } as any;
      component['isSurfaceBetModule'](data);
    })
  });
  
  describe('init', () => {
    beforeEach(() => {
      component.featuredModuleData = {
        directiveName: null,
        modules: [],
        showTabOn: null,
        title: null,
        visible: null
      } as any;
    });

    it('isModuleAvailable with no modules - hide featured', () => {
      const featured = {
        modules: []
      } as any;
      component.init(featured);
      expect(component.isModuleAvailable).toBe(false);
    });

    it('isModuleAvailable with modules - show featured', () => {
      const featured = {
        modules: [{
          '@type': 'EventsModule',
          hasNoLiveEvents: true,
          dataSelection: {
            selectionType: 'Lorem'
          },
          publishedDevices: [],
          data:[{
            eventIsLive: false
          }]
        }]
      } as any;
      component.init(featured);
      expect(component.isModuleAvailable).toBe(true);
    });
    it('isModuleAvailable with surface bet modules - show featured#1', () => {
      const featured = {
        modules: [{
          '@type': 'SurfaceBetModule',
          publishedDevices: [],
          data: [
            {
              '@type': 'SurfaceBetModuleData',
              displayOnDesktop: true
            }
          ]
        }]
      } as any;
      component.isFeaturedModuleAvailable = true;
      component.init(featured);
      expect(component.isModuleAvailable).toBe(true);
    });
  });

  it('should use OnPush strategy', () => {
    expect(DesktopFeaturedModuleComponent['__annotations__'][0].changeDetection).toBe(0);
  });
});
