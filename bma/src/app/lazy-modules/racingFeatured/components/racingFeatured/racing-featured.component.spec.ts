import { of as observableOf } from 'rxjs';

import { FeaturedModuleComponent } from '@app/featured/components/featured-module/featured-module.component';
import { RacingFeaturedComponent } from './racing-featured.component';

import { ISystemConfig } from '@core/services/cms/models/system-config';
import environment from '@environment/oxygenEnvConfig';


import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

const racingMock = {
  events: [],
  classesTypeNames: {},
  groupedRacing: [
    {
      flag: 'UK',
      data: [{id: '1'}]
    },
    {
      flag: 'INT',
      data: []
    },
    {
      flag: 'FR',
      data: []
    },
    {
      flag: 'VR',
      data: []
    }
  ],
  selectedTab: 'horseracing',
  modules: {}
};

const featuredModulesMock = {
  modules: [
    {
      '@type': 'RacingEventsModule',
      data: [
        {
          '@type': 'RacingEventsModule'
        }
      ]
    },
    {
      '@type': 'VirtualRaceModule',
      data: [
        {
          '@type': 'test'
        }
      ]
    }
  ]
};

describe('AppRacingFeaturedComponent', () => {
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
  
  const sysConfig: ISystemConfig = {
    InternationalTotePool: {
      Enable_International_Totepools: true
    },
    NextRacesToggle: {
      nextRacesComponentEnabled: true,
      nextRacesTabEnabled: true
    },
    VirtualSports: {
      'virtual-horse-racing': true
    },
    defaultAntepostTab: {
    }
  };


  beforeEach(() => {
    locale = {};
    filtersService = {};
    windowRef = {
      nativeWindow: {
        setInterval:  jasmine.createSpy('setInterval').and.callFake(cb => cb()),
        setTimeout: jasmine.createSpy().and.callFake(cb => cb && cb()),
        view: 'Mobile'
      }
    };
    pubsub = {
      publish:jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    featuredModuleService = {
      cacheEvents: jasmine.createSpy('cacheEvents'),
    };
    templateService = {};
    commentsService = {};
    wsUpdateEventService = {};
    sportEventHelper = {};
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(sysConfig))
    };
    router = {
      url : jasmine.createSpy('url').and.returnValue('/horse-racing/featured')
    };
    gtmService = {};
    routingHelperService = {
      getPreviousSegment: jasmine.createSpy().and.returnValue(''),
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('/horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/')
    };
    promotionsService = {};
    changeDetectorRef = {
      detach: jasmine.createSpy('cdr.detach'),
      detectChanges: jasmine.createSpy('cdr.detectChanges'),
      markForCheck: jasmine.createSpy('cdr.markForCheck')
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    user = {};
    eventService = {
      addAvailability: jasmine.createSpy('addAvailability')
    };
    virtualSharedService = {};
    racingGaService = {
      trackModule: jasmine.createSpy(),
      reset: jasmine.createSpy(),
      todayEventsByClasses: jasmine.createSpy('todayEventsByClasses')
    };

    storage = {
      set: jasmine.createSpy('storage.set')
    };

    horseRacingService = {
      todayEventsByClasses: jasmine.createSpy('todayEventsByClasses').and.returnValue(Promise.resolve(racingMock)),
      getConfig: jasmine.createSpy('getConfig').and.returnValue({
        request: {
          date: 'today'
        }
      }),
      config: {
        request: {
          categoryId: '21',
        }
      },
      addLpAvailableProp: jasmine.createSpy('addLpAvailableProp'),
      addPersistentInCacheProp: jasmine.createSpy('addPersistentInCacheProp'),
      groupByFlagCodesAndClassesTypeNames: jasmine.createSpy('groupByFlagCodesAndClassesTypeNames').and.returnValue(racingMock),
      sortRaceGroup: jasmine.createSpy('sortRaceGroup')
    };
    greyhoundService = {};
    routingState = {
      getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.returnValue('horseracing')
    };
    buildUtilityService = {
      msEventBuilder: jasmine.createSpy('msEventBuilder')
    };
    timeService = {
      getDayI18nValue: jasmine.createSpy(' timeService.getDayI18nValue').and.returnValue('sb.today')
    };
    deviceService = {
      isRobot: jasmine.createSpy('isRobot').and.returnValue(false)
    };
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled'),
    };
    vEPService = {
      targetTab: {subscribe : (cb) => cb()},
      lastBannerEnabled: {subscribe : (cb) => cb()},
      accorditionNumber: {subscribe : (cb) => cb()},
    };
    component = new RacingFeaturedComponent(
      locale, filtersService, windowRef, pubsub, featuredModuleService, templateService, commentsService,
      wsUpdateEventService, sportEventHelper, cmsService, promotionsService, changeDetectorRef, routingHelperService,
      router, gtmService, awsService, user, eventService, virtualSharedService, racingGaService, storage,
      horseRacingService, greyhoundService, routingState, buildUtilityService, timeService,deviceService, bonusSuppressionService,
      vEPService
    );
  });

  it('ngOnInit', () => {
    spyOn(FeaturedModuleComponent.prototype, 'ngOnInit');
    spyOn(FeaturedModuleComponent.prototype, 'init');
    component.featuredModuleData = {
      modules: []
    };
    spyOn(component,'schemaForHRGHEvents');
    component.sportId = Number(environment.CATEGORIES_DATA.racing.horseracing.id);
    component.racing = racingMock;
    component.setIntTotePool = jasmine.createSpy('setIntTotePool').and.returnValue(true);
    component.ngOnInit();
    component.init();
    expect(component.setIntTotePool).toHaveBeenCalledWith(sysConfig);
    expect(component.isTotePoolsAvailable).toEqual(true);
    expect(component.isHorseracingVirtualsEnabled).toBeTruthy();
    component.sportId = Number(environment.CATEGORIES_DATA.racing.greyhound.id);
    component.ngOnInit();
    component.init();
    expect(component.isTotePoolsAvailable).toEqual(false);
    expect(component.inspiredVirtualsDataReady).toEqual(false);
  });

  describe('', () => {
    beforeEach(() => {
      spyOn(FeaturedModuleComponent.prototype, 'ngOnInit');
      spyOn(FeaturedModuleComponent.prototype, 'init');
      component.featuredModuleData = Object.assign({}, featuredModulesMock);
      component.racing = racingMock;
      component.setIntTotePool = jasmine.createSpy('setIntTotePool').and.returnValue(true);
    });

    it('init', () => {
      spyOn(component,'schemaForHRGHEvents');
      component.reload = true;
      component.ngOnInit();
      component.init();
      expect(component.featuredModuleData.modules[1]['@type']).toEqual('VirtualRaceModule');
    });

    it('init isDesktop true', () => {
      component.isDesktop = true;
      spyOn(component,'schemaForHRGHEvents');
      component.racing= racingMock;
      component.ngOnInit();
      component.init();
      expect(component.featuredModuleData.modules[1]['@type']).toEqual('VirtualRaceModule');
    });

    it('init with racingEventsModules', fakeAsync(() => {
      component.featuredModuleData.modules.push({
        '@type': 'RacingEventsModule',
        data: [
          {
            '@type': 'RacingEventsModule'
          }
        ]
      });
      spyOn(component,'schemaForHRGHEvents');
      buildUtilityService.msEventBuilder.and.returnValue({ '@type': 'RacingEventsModule', id: '1', correctedDay: 'sb.tooday'});
      tick(500);
      component.ngOnInit();
      component.init();
      expect(racingGaService.todayEventsByClasses).not.toHaveBeenCalled();
    }));
    it('init without racingEventsModules + ' +
      'viruals shoud be received via call to SS inside inspired virtuals component', fakeAsync(() => {
      component.featuredModuleData.modules = [];
      spyOn(component,'schemaForHRGHEvents');
      horseRacingService.todayEventsByClasses.and.returnValue(Promise.resolve(racingMock));

      component.init();
      tick();

      const lastModule = component.featuredModuleData.modules[component.featuredModuleData.modules.length - 1];

      expect(lastModule).toEqual({
        '@type': 'VirtualRaceModule',
        title: 'Virtual Race Carousel',
        data: [
          {
            '@type': 'VirtualRaceModuleData',
            name: 'VRC'
          }
        ]
      });
      expect(component.inspiredVirtualsDataReady).toEqual(true);
    }));

    it('init with racingEventsModules 333', fakeAsync(() => {
      const virtualsDataFromFeaturedMS = {
        '@type': 'VirtualRaceModule',
        title: 'Virtual Racing',
        data: [
          {
            '@type': 'VirtualRaceModuleData',
            id: '15945635'
          }
        ]
      };
      spyOn(component,'schemaForHRGHEvents');
      component.featuredModuleData.modules = [virtualsDataFromFeaturedMS];

      horseRacingService.todayEventsByClasses.and.returnValue(Promise.resolve(racingMock));

      component.init();
      tick();

      const lastModule = component.featuredModuleData.modules[component.featuredModuleData.modules.length - 1];

      expect(lastModule).toEqual(virtualsDataFromFeaturedMS);
      expect(component.inspiredVirtualsDataReady).toEqual(true);
    }));
  });

  it('ngOnDestroy', () => {
    spyOn(FeaturedModuleComponent.prototype, 'ngOnDestroy');
    spyOn(component,'removeSchemaForHRGHEvents');
    component.sysConfigSubscription = { unsubscribe: jasmine.createSpy('sysConfigSubsciption.unsubsctibe') };
    component.ngOnDestroy();

    expect(racingGaService.reset).toHaveBeenCalled();
    expect(component.sysConfigSubscription.unsubscribe).toHaveBeenCalled();
    expect(component.removeSchemaForHRGHEvents).toHaveBeenCalled();
  });

  describe('init', () => {
    it('init', fakeAsync(() => {
      component.featuredLoaded = {
        emit: jasmine.createSpy('featuredLoaded.emit')
      };
      component.racing = racingMock;
      component.featuredModuleData = {
        modules: [
          {
            '@type': 'RacingModule',
            data: [{ name: 'UIR'}]
          },
          {
            '@type': 'RacingModule',
            data: [{ name: 'LVR'}]
          },
          {
            '@type': 'RacingEventsModule',
            data: [{ name: 'IR'}]
          }
        ]
      };
      spyOn(component,'schemaForHRGHEvents');
      spyOn(FeaturedModuleComponent.prototype, 'init');
      component.display = 'today';
      component.sportName = 'greyhound';
      component.filter = 'by-time';
      buildUtilityService.msEventBuilder.and.returnValue({ id: '1', correctedDay: 'sb.tooday'});
      component.init();
      tick();
      expect(component.featuredLoaded.emit).toHaveBeenCalled();
      expect(buildUtilityService.msEventBuilder).toHaveBeenCalled();
    }));
  });


  it('setIntTotePool: check whether result returns value from CMS config', () => {
    const result = component.setIntTotePool(sysConfig);
    const resultFalse = component.setIntTotePool({});
    expect(result).toEqual(true);
    expect(resultFalse).toEqual(false);
  });

  it('setHorseracingVirtualSportsSwitcher: check whether result returns value from CMS config', () => {
    const result = component.setHorseracingVirtualSportsSwitcher(sysConfig);
    const resultFalse = component.setHorseracingVirtualSportsSwitcher({});
    expect(result).toEqual(true);
    expect(resultFalse).toEqual(false);
  });

  it('trackModule', () => {
    component.trackModule('horseracing', 'sb.UKRacing');
    expect(racingGaService.trackModule).toHaveBeenCalledWith('horseracing', 'sb.UKRacing');
  });

  it('handleErrorOnFirstLoad', () => {
    component.loadDefaultModules = jasmine.createSpy();
    component.handleErrorOnFirstLoad();
    expect(component.loadDefaultModules).toHaveBeenCalled();
  });

  it('reloadComponent', () => {
    component.ngOnInit = jasmine.createSpy('ngOnInit');
    component.ngOnDestroy = jasmine.createSpy('ngOnDestroy');
    component.reloadComponent();

    expect(component.ngOnInit).toHaveBeenCalled();
    expect(component.ngOnDestroy).toHaveBeenCalled();
  });

  describe('loadDefaultModules', () => {
    beforeEach(() => {
      component.featuredModuleData = {
        modules: []
      };
      component['groupEvents'] = jasmine.createSpy();
    });

    it('with data', fakeAsync(() => {
      spyOn(component,'schemaForHRGHEvents');
      component['loadDefaultModules']();
      tick();
      expect(component.featuredModuleData.modules.find(m => m._id === '1').data).toEqual([{id: '1'}]);
      expect(buildUtilityService.msEventBuilder).not.toHaveBeenCalled();
    }));

    it('withoout data', fakeAsync(() => {
      spyOn(component,'schemaForHRGHEvents');
      const mock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [],
        selectedTab: 'horseracing',
        modules: {}
      };
      horseRacingService.todayEventsByClasses.and.returnValue(Promise.resolve(mock));
      component['loadDefaultModules']();
      tick();
      expect(component.featuredModuleData.modules.find(m => m._id === '1').data).toEqual([]);
    }));
  });

  describe('ngOnChanges', () => {
    it('ngOnChanges (groupEvents)', () => {
      const changes = <any>{
        display: {}
      };
      spyOn(component, 'groupEvents');
      spyOn(component,'schemaForHRGHEvents');
      spyOn(component,'removeSchemaForHRGHEvents');
      component.ngOnChanges(changes);
      expect(component['groupEvents']).toHaveBeenCalled();
      expect(component.removeSchemaForHRGHEvents).toHaveBeenCalled();
    });

    it('ngOnChanges (!groupEvents)', () => {
      const changes = <any>{
        display: { firstChange: true }
      };

      spyOn(component, 'groupEvents');
      component.ngOnChanges(changes);
      expect(component['groupEvents']).not.toHaveBeenCalled();
    });
  });

  it('inspiredVirtualsDataReady', () => {
    component.racing = {} as any;
    spyOn(component, 'schemaForHRGHEvents');
    component.featuredLoaded = {
      emit: jasmine.createSpy('featuredLoaded.emit')
    };
    component.featuredModuleData = {
      modules: [{
        '@type': 'TestModule'
      }, {
        '@type': 'VirtualRaceModule'
      }]
    } as any;
    component['groupEvents']();
    expect(component.inspiredVirtualsDataReady).toBeTruthy();
  });
  it('should call schemaForHRGHEvents if deviceservice.isRobot is true', () => {
    spyOn(component, 'schemaForHRGHEvents');
    deviceService.isRobot.and.returnValue(true);
    const data = {
      '@type': 'RacingEventsModule',
      _id: 'dsge322',
      data: [
        {
          '@type': 'RacingEventsModule'
        }
      ]
    } as any;

    component.featuredModuleData = {
      modules: featuredModulesMock.modules
    } as any;
    component.racing = {
      events: []
    } as any;
    component.badges = {
      'dsge322': {}
    } as any;
    component['HORSE_RACING_CATEGORY_ID'] = '21';
    component.allEvents = [{
      id: '1',
      "@type": "RacingEventsModuleData",
      name: "Catterick",
      categoryId: "21",
      categoryName: "Horse Racing",
      classId: 223,
      className: "Horse Racing - Live",
      typeName: "Catterick",
      correctedDayValue: "racing.today",
    }];
    component['groupEvents']();
    expect(component.schemaForHRGHEvents).toHaveBeenCalledWith(component.allEvents);
  });

  describe('#onModuleUpdate', () => {
    const data = {
      '@type': 'RacingEventsModule',
      _id: 'dsge322',
      data: [
        {
          '@type': 'RacingEventsModule'
        }
      ]
    } as any;
    beforeEach(() => {
      component.featuredModuleData = {
        modules: featuredModulesMock.modules
      } as any;
      component.racing = {
        events: []
      } as any;
      component.badges = {
        'dsge322': {}
      } as any;
      component['HORSE_RACING_CATEGORY_ID'] = '21';
    });

    it('should sort races if category is horse racing', () => {
      spyOn(component,'schemaForHRGHEvents');
      component.onModuleUpdate(data);
      expect(featuredModuleService.cacheEvents).toHaveBeenCalled();
      expect(buildUtilityService.msEventBuilder).toHaveBeenCalled();
      expect(storage.set).toHaveBeenCalled();
      expect(horseRacingService.sortRaceGroup).toHaveBeenCalled();
    });
    it('should not sort races if category is horse racing', () => {
      spyOn(component,'schemaForHRGHEvents');
      horseRacingService.config.request.categoryId = '19';
      component.onModuleUpdate(data);
      expect(featuredModuleService.cacheEvents).toHaveBeenCalled();
      expect(buildUtilityService.msEventBuilder).toHaveBeenCalled();
      expect(storage.set).toHaveBeenCalled();
      expect(horseRacingService.sortRaceGroup).not.toHaveBeenCalled();
    });
  });

  describe('isSimpleModule', () => {
    it('not simple module', () => {
      const module = {
        '@type': 'lorem'
      } as any;
      expect(component.isSimpleModule(module)).toBe(false);
    });

    it('not racing module true', () => {
      const module = {
        '@type': 'RecentlyPlayedGameModule'
      } as any;
      expect(component.isSimpleModule(module)).toBe(true);
    });

    it('RacingEventsModule module true', () => {
      const module = {
        '@type': 'RacingEventsModule'
      } as any;
      expect(component.isSimpleModule(module)).toBe(true);
    });

    it('InternationalToteRaceModule module true', () => {
      const module = {
        '@type': 'InternationalToteRaceModule'
      } as any;
      expect(component.isSimpleModule(module)).toBe(true);
    });

    it('VirtualRaceModule module true', () => {
      const module = {
        '@type': 'VirtualRaceModule'
      } as any;
      expect(component.isSimpleModule(module)).toBe(true);
    });
  });
  describe('#schemaForHRGHEvents', () => {
    it('should call pubsub.publish with events for HR today', fakeAsync(() => {
      component.sportName = 'horseracing';
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['today']
        }
      }));
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDayValue: "racing.today",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'horseracing',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/horse-racing/featured'
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/horse-racing/featured']);
    }));
    it('should call pubsub.publish with events for HR both', fakeAsync(() => {
      component.sportName = 'horseracing';
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['today', 'tomorrow']
        }
      }));
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDayValue: "racing.today",
      },
        {
          id: '2',
          "@type": "RacingEventsModuleData",
          name: "Catterick",
          categoryId: "21",
          categoryName: "Horse Racing",
          classId: 223,
          className: "Horse Racing - Live",
          typeName: "Catterick",
          correctedDayValue: "racing.tomorrow",
        }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: races
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'horseracing',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/horse-racing/featured'
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/horse-racing/featured']);
    }));
    it('should call pubsub.publish with events for HR tomorrow', fakeAsync(() => {
      component.sportName = 'horseracing';
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['tomorrow']
        }
      }));
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDayValue: "racing.tomorrow",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'horseracing',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/horse-racing/featured'
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/horse-racing/featured']);
    }));
    it('should call pubsub.publish with events for GH today', fakeAsync(() => {
      component.sportName = 'greyhound';
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['today']
        }
      }));
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "sb.today",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/greyhound-racing/today';
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/greyhound-racing/today']);
    }));
    it('should call pubsub.publish with events for GH tommorow', fakeAsync(() => {
      component.sportName = 'greyhound';
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['tomorrow']
        }
      }));
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "sb.tomorrow",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/greyhound-racing/tomorrow';
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/greyhound-racing/tomorrow']);
    }));
    it('should call pubsub.publish with events for GH both', fakeAsync(() => {
      component.sportName = 'greyhound';
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: {
          schemaConfig: ['today', 'tomorrow']
        }
      }));
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "sb.tomorrow",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/greyhound-racing/tomorrow';
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/greyhound-racing/tomorrow']);
    }));
    it('should not call pubsub.publish with events for GH if cms config sysConfig is null', fakeAsync(() => {
      component.sportName = 'greyhound';
      cmsService.getSystemConfig.and.returnValue(observableOf(null));
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "sb.tomorrow",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/greyhound-racing/tomorrow';
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/greyhound-racing/tomorrow']);
    }));
    it('should not call pubsub.publish with events for GH  if cms config sysConfig.SeoSchemaConfig is null', fakeAsync(() => {
      component.sportName = 'greyhound';
      cmsService.getSystemConfig.and.returnValue(observableOf({
        SeoSchemaConfig: null
      }));
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "sb.tomorrow",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/greyhound-racing/tomorrow';
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, '/greyhound-racing/tomorrow']);
    }));
    it('should not call pubsub.publish with events for GH if router.url is null', fakeAsync(() => {
      component.sportName = 'greyhound';
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "sb.today",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = null;
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, 'greyhound-racing/today']);
    }));
    it('should not call pubsub.publish with events for GH router is null', fakeAsync(() => {
      component.sportName = 'greyhound';
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "s.today",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: [races[0]]
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      component.router = null;
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, 'greyhound-racing/today']);
    }));
    it('should not call pubsub.publish with events for GH with groupedRacing.data', fakeAsync(() => {
      component.sportName = 'greyhound';
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "s.today",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: [
          {
            flag: 'UK',
            data: null
          },
          {
            flag: 'INT',
            data: []
          },
          {
            flag: 'FR',
            data: []
          },
          {
            flag: 'VR',
            data: []
          }
        ],
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      component.router = null;
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, 'greyhound-racing/today']);
    }));
    it('should not call pubsub.publish with events for GH if racing is null', fakeAsync(() => {
      component.sportName = 'greyhound';
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "s.today",
      }];
      const racingMock = null;
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = '/greyhound-racing/today';
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, 'greyhound-racing/today']);
    }));
    it('should not call pubsub.publish with events for GH groupedRacing is null', fakeAsync(() => {
      component.sportName = 'greyhound';
      const races = [{
        id: '1',
        "@type": "RacingEventsModuleData",
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        classId: 223,
        className: "Horse Racing - Live",
        typeName: "Catterick",
        correctedDay: "s.today",
      }];
      const racingMock = {
        events: [],
        classesTypeNames: {},
        groupedRacing: null,
        selectedTab: 'greyhound',
        modules: {}
      };
      horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(racingMock);
      router.url = 'greyhound-racing/today';
      tick(500);
      component.schemaForHRGHEvents(races);
      expect(pubsub.publish).not.toHaveBeenCalledWith('SCHEMA_DATA_UPDATED', [races, 'greyhound-racing/today']);
    }));
  });
  describe('removeSchemaForHRGHEvents', () => {
    it('should publish schema_removed with url', () => {
      deviceService.isRobot.and.returnValue(true);
      component.schemaUrl = 'horse-racing/featured';
      component.removeSchemaForHRGHEvents();
      expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.SCHEMA_DATA_REMOVED, 'horse-racing/featured');
    });
  });
});
