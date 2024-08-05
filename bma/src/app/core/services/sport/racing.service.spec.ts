import { of, throwError } from 'rxjs';
import { ISportEvent } from '@core/models/sport-event.model';

import { RacingService } from './racing.service';
import { IInitialSportTab } from '@core/services/sport/config/initial-sport-config.model';
import { IMarket } from '@core/models/market.model';
import { fakeAsync, tick } from '@angular/core/testing';
import { nextRacesModule } from '@core/services/sport/racingService.mock';
describe('RacingService', () => {
  let service: RacingService;

  let timeformService;
  let ukToteService;
  let dailyRacingService;
  let eventFactory;
  let templateService;
  let timeService;
  let filtersService;
  let liveUpdatesWSService;
  let channelService;
  let lpAvailabilityService;
  let commandService;
  let localeService;
  let racingYourcallService;
  let pubSubService;
  let cmsService;
  let racingPostService;
  let routingHelperservice;

  const tabsSpecialsMock: IInitialSportTab = {
    id: 'tab-specials',
    label: '',
    url: ''
  };
  const tabsRacesMock: IInitialSportTab = {
    id: 'tab-races',
    label: '',
    url: ''
  };
  const tabsFeaturedMock: IInitialSportTab = {
    id: 'tab-featured',
    label: '',
    url: ''
  };

  const tabsMock = [tabsSpecialsMock, tabsRacesMock, tabsFeaturedMock];

  const systemConfig = {
    raceInfo: {
      timeFormEnabled: true
    },
    RacingDataHub: {
      isEnabledForGreyhound: true,
      isEnabledForHorseRacing: true,
    },
    HorseRacingBIR: {
      marketsEnabled:['winOnly'] }
  };

  const testUKEvent = {
    typeFlagCodes: 'GVA,UK,NE,AVA,RVA,'
  };

  const testIEEvent = {
    typeFlagCodes: 'GVA,IE,NE,AVA,RVA,'
  };

  const testUSEvent = {
    typeFlagCodes: 'GVA,US,NE,AVA,RVA,'
  };
 const eventsDataMock = [
    {
      id: 8793203,
      name: 'Wolverhampton',
      typeName: 'Wolverhampton',
      typeDisplayOrder: 0,
      typeFlagCodes: 'GVA,IN,AVA,RVA,'
    },
    {
      id: 8793694,
      name: 'Club Hipico',
      typeName: 'Club Hipico',
      typeDisplayOrder: 0,
      typeFlagCodes: 'GVA,UK,AVA,IE,'
    },
    {
      id: 8795859,
      name: 'Portman Park',
      typeName: 'Portman Park',
      typeDisplayOrder: 0,
      typeFlagCodes: 'GVA,AVA,RVA,US,'
    },
    {
      id: 8795839,
      name: 'Charles Town',
      typeName: 'Charles Town',
      typeDisplayOrder: 0,
      typeFlagCodes: 'GVA,UK,AVA,RVA,'
    },
    {

      id: 8795859,
      name: 'NewCastle',
      typeName: 'NewCastle',
      typeDisplayOrder: 0,
      typeFlagCodes: 'GVA,AVA,RVA,US,'
    },
    {
      id: 8795779,
      name: 'Manchester',
      typeName: 'Manchester',
      typeDisplayOrder: 0,
      typeFlagCodes: 'SP,GB,'
    },
    {
      id: 8791234,
      name: 'Without typeFlagCodes',
      typeName: 'typeName',
      typeDisplayOrder: 0
    }
  ];

  const groupedDataMock = [
    {
      flag: 'UK',
      data: [
        {
          id: 8793694,
          name: 'Club Hipico',
          typeName: 'Club Hipico',
          typeDisplayOrder: 0,
          typeFlagCodes: 'GVA,UK,AVA,IE,'
        },
        {
          id: 8795839,
          name: 'Charles Town',
          typeName: 'Charles Town',
          typeDisplayOrder: 0,
          typeFlagCodes: 'GVA,UK,AVA,RVA,'
        }
      ]
    },
    {
      flag: 'IN',
      data: [
        {
          id: 8793203,
          name: 'Wolverhampton',
          typeName: 'Wolverhampton',
          typeDisplayOrder: 0,
          typeFlagCodes: 'GVA,IN,AVA,RVA,'
        }
      ]
    },
    {
      flag: 'US',
      data: [
        {
          id: 8795859,
          name: 'Portman Park',
          typeName: 'Portman Park',
          typeDisplayOrder: 0,
          typeFlagCodes: 'GVA,AVA,RVA,US,'
        },
        {

          id: 8795859,
          name: 'NewCastle',
          typeName: 'NewCastle',
          typeDisplayOrder: 0,
          typeFlagCodes: 'GVA,AVA,RVA,US,'
        }
      ]
    },
    {
      flag: "INT",
      data: [
        {
          id: 8795859,
          name: "Portman Park",
          typeName: "Portman Park",
          typeDisplayOrder: 0,
          typeFlagCodes: "GVA,AVA,RVA,US,",
        },

        {
          id: 8795859,
          name: "Club Hipico",
          typeDisplayOrder: -27760,
          cashoutAvail: false,
          liveStreamAvailable: true,
        },
        {
          id: 8795859,
          name: "Delaware Park",
          typeDisplayOrder: -29430,
          cashoutAvail: false,
          liveStreamAvailable: true,
        },
        {
          id: 8795859,
          name: "Pornichet-La Baule",
          typeDisplayOrder: -30450,
          cashoutAvail: false,
          liveStreamAvailable: true,
        },
        {
          id: 8795859,
          name: "Laurel Park",
          typeDisplayOrder: -29080,
          cashoutAvail: false,
          liveStreamAvailable: true,
        },
        {
          id: 8795859,
          name: "Gulfstream",
          typeDisplayOrder: -29500,
          cashoutAvail: false,
          liveStreamAvailable: true,
        },
      ],
    },
  ];

  const groupedEventsByMeetings = {
    'Steepledowns': [
      { classFlagCodes: 'UF,LI,',
        classId: 223,
        eventStatusCode: 'A',
        name: 'Steepledowns',
        typeFlagCodes: 'UK,NE,AVA,RVA,',
        typeName: 'Steepledowns',
        startTime: 1548787980000
      },
      { classFlagCodes: 'UF,LI,',
        classId: 223,
        eventStatusCode: 'S',
        name: 'Steepledowns',
        typeFlagCodes: 'UK,NE,AVA,RVA,',
        typeName: 'Steepledowns',
        startTime: 1548758100000
      }],

    'Turf Paradise': [
      { classFlagCodes: 'UF,LI,', classId: 223, name: 'Turf Paradise', typeFlagCodes: 'GVA,AVA,US,', typeName: 'Turf Paradise' }],
    'Racing Specials' : [
      { classFlagCodes: 'UF,LI,', classId: 224, name: 'Special Event', typeFlagCodes: 'UK,SP', typeName: 'Special Event' }
    ]
  };

  const iInitialSportConfig = {
    config: {
      categoryType: 'categoryType',
      eventMethods: {
        name: 'test',
        typeName: 'typeName',
        typeDisplayOrder: 1,
        path: 'url/test',
        tier: 12,
        request: 'request',
        sportModule: 'sportModule',
        tabs: {},
        eventRequest: 'test',
        inConnectApp: true,
        scoreboardConfig: () => {
          return ['service.getConfig'];
          },
      },
    filters: {
      LIVE_VIEW_BY_FILTERS: ['LIVE_VIEW_BY_FILTERS'],
      VIEW_BY_FILTERS: ['VIEW_BY_FILTERS'],
      RACING_FILTERS: ['RACING_FILTERS'],
      RESULTS_FILTERS: ['RESULTS_FILTERS']
    },
    order: {
      BY_LEAGUE_ORDER: ['BY_LEAGUE_ORDER'],
      BY_LEAGUE_EVENTS_: ['BY_LEAGUE_EVENTS_'],
      BY_TIME_ORDER: ['BY_TIME_ORDER'],
      EVENTS_ORDER: ['EVENTS_ORDER'],
  }
  }
  };

  const sortOrderArray = ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'];

  const requestParams = {
    request: {
      categoryId: '21',
      isRacing: true,
      typeFlagCodes: 'UK,IE,FR,AE,ZA,IN,US,AU,CL,INT,VR',
      siteChannels: 'M',
      racingFormOutcome: true,
      racingFormEvent: true,
      isResulted: true,
      resultedMarketName: '|Win or Each Way|',
      resultedMarketPriceTypeCodesIntersects: 'SP',
      resultedPriceTypeCodeToDisplay: 'SP',
      resultedOutcomeResultCodeNotEquals: 'V',
      resultedOutcomesExcludeUnnamedFavourites: true,
      resultedIncludeUndisplayed: true,
      groupByFlagCodesSortOrder: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
      breadcrumbsNavMenuFlags: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
      date: null,
      priceHistory: true,
      externalKeysEvent: true,
      modules: {
        dailyRacing: {
          classIds: [],
          typeNames: ['Enhanced Multiples', 'Mobile Exclusive', 'Price Bomb', 'Winning Distances'],
          collapsedSections: 'Winning Distances'
        }
      }
    }
  };

  beforeEach(() => {
    timeformService = {
      getGreyhoundRaceById: jasmine.createSpy().and.returnValue(of({ raceTitle: 'greyhound' })),
      mergeGreyhoundRaceData: jasmine.createSpy().and.returnValue([{ name: 'updated event' }])
    };
    ukToteService = {
      addAvailablePoolTypes: arg => arg
    };
    eventFactory = {
      isAnyCashoutAvailable: jasmine.createSpy(),
      isAnyLiveStreamAvailable: jasmine.createSpy(),
      eventsByClasses: jasmine.createSpy().and.returnValue(Promise.resolve([])),
      getEvent: jasmine.createSpy('getEvent').and.returnValue(Promise.resolve({ name: 'event' })),
      eventsByTypeIds: jasmine.createSpy('eventsByTypeIds').and.returnValue(Promise.resolve({ name: 'event' })),
      isSpecialsAvailable: jasmine.createSpy('isSpecialsAvailable').and.returnValue(Promise.resolve(true))
    };
    dailyRacingService = {};
    templateService = {
      groupEventsByTypeName: jasmine.createSpy().and.returnValue(groupedEventsByMeetings),
      filterEventsWithoutMarketsAndOutcomes: arg => arg
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('2020-09-30')
    };
    filtersService = {
      orderBy: jasmine.createSpy().and.returnValue([groupedEventsByMeetings['Steepledowns'][0]])
    };
    liveUpdatesWSService = {};
    channelService = {};
    lpAvailabilityService = {
      check: arg => false
    };
    commandService = {};
    localeService = {
      getString: jasmine.createSpy().and.returnValue('Win or Each Way')
    };
    racingYourcallService = {};
    pubSubService = {};
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of(systemConfig))
    };
    racingPostService = {
      getHorseRacingPostById: jasmine.createSpy('getHorseRacingPostById').and.returnValue(
        of({ Error: 'false', document: { 1: { raceType: 'horseracing' } } })),
      mergeHorseRaceData: jasmine.createSpy('mergeHorseRaceData').and.returnValue([{ name: 'updated event' }]),
      getGreyhoundRacingPostById: jasmine.createSpy('getGreyhoundRacingPostById').and.returnValue(
        of({ Error: 'false', document: { 1: { raceType: 'greyhound' } } })),
      mergeGreyhoundRaceData: jasmine.createSpy('mergeGreyhoundRaceData').and.returnValue([{ name: 'updated event' }])
    };
    routingHelperservice = {
      encodeUrlPart: jasmine.createSpy('encodeUrlPart').and.callFake(v => {
        return v.replace(/([^a-zA-Z0-9])+/g, '-').toLowerCase();
      })
    };

    service = new RacingService(
      timeformService,
      ukToteService,
      dailyRacingService,
      eventFactory,
      templateService,
      timeService,
      filtersService,
      liveUpdatesWSService,
      channelService,
      lpAvailabilityService,
      commandService,
      localeService,
      racingYourcallService,
      pubSubService,
      cmsService,
      racingPostService,
      routingHelperservice
    );
    service.setConfig(<any>{
      config: {
        request: {
          modules: {
            dailyRacing: {}
          },
          breadcrumbsNavMenuFlags: [],
          priceHistory: true,
          racingFormOutcome: true,
          racingFormEvent: true
        },
        sportModule: 'horseracing'
      }
    });
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['pubSubService']).toBeTruthy();
  });

  it('to finish market config', () => {
    expect(service['racingConfig'].TO_FINISH_MARKET.SUB_MARKETS[3]).toEqual('To Finish 2nd');
    expect(service['racingConfig'].TO_FINISH_MARKET.SUB_MARKETS[4]).toEqual('To Finish 3rd');
  });

  describe('racing service: getRacingEventTypeFlagCodeKey', () => {
    it('getRacingEventTypeFlagCodeKey: UK event', () => {
      const country = service.getRacingEventTypeFlagCodeKey(testUKEvent);
      expect(country).toEqual('UK');
    });

    it('getRacingEventTypeFlagCodeKey: IE event', () => {
      const country = service.getRacingEventTypeFlagCodeKey(testIEEvent);
      expect(country).toEqual('UK');
    });

    it('getRacingEventTypeFlagCodeKey: US event', () => {
      const country = service.getRacingEventTypeFlagCodeKey(testUSEvent);
      expect(country).toEqual('US');
    });

    it('getRacingEventTypeFlagCodeKey: event without flagCodes', () => {
      const country = service.getRacingEventTypeFlagCodeKey({});
      expect(country).toEqual(null);
    });
  });

  describe('racing service: groupByFlagCodes', () => {
    it('groupByFlagCodes: sortOrder is array ', () => {
      const groupedEvents = service.groupByFlagCodes(eventsDataMock, sortOrderArray);
     });

    it('groupByFlagCodes: spy on getRacingEventTypeFlagCodeKey', () => {
      spyOn(service, 'getRacingEventTypeFlagCodeKey');
      service.groupByFlagCodes(eventsDataMock, sortOrderArray);
      expect(service.getRacingEventTypeFlagCodeKey).toHaveBeenCalled();
    });
  });

  describe('getGeneralConfig', () => {
    it('it should return configs ', () => {
      service['generalConfig'] = iInitialSportConfig as any;
      const result = service.getGeneralConfig();
      expect(result).toEqual(iInitialSportConfig as any);
    });

  });

  describe('getEvents', () => {
    beforeEach(() => {
      service['newFunction'] = jasmine.createSpy().and.returnValue(Promise.resolve([{config: {}}]));
      dailyRacingService['addEvents'] = jasmine.createSpy().and.returnValue(Promise.resolve([{config: {}}]));
    });
    it('it should promise resolve configs ', () => {
      service.getConfig = jasmine.createSpy().and.returnValue(
        {
          eventMethods: {
            scoreboardConfig: 'newFunction'
          },
          inConnectApp: true,
          name: 'horseracing'
        }
      );
      const result = service.getEvents('scoreboardConfig', false);
      result.then(res => {
        expect(res).toEqual([{config: {}}] as any);
      });
    });

    it('it should promise resolve configs ', () => {
      service.getConfig = jasmine.createSpy().and.returnValue(
        {
          eventMethods: {
            scoreboardConfig: 'newFunction'
          },
          inConnectApp: true,
          name: 'tests'
        }
      );
      dailyRacingService['addEvents'] = jasmine.createSpy().and.returnValue(Promise.resolve([{config: {}}]));
      const result = service.getEvents('scoreboardConfig', false);
      result.then(res => {
        expect(res).toEqual([{config: {}}] as any);
      });
    });

    it('it should promise resolve configs ', () => {
      service.getConfig = jasmine.createSpy().and.returnValue(
        {
          eventMethods: {
            scoreboardConfig: 'newFunction'
          },
          inConnectApp: false,
          name: 'horseracing',
          request: {
            modules: 'modules'
          }
        }
      );
      service['newFunction'] = jasmine.createSpy().and.returnValue(Promise.resolve({config: {}}));
      dailyRacingService['addEvents'] = jasmine.createSpy().and.returnValue([{config: {}}]);
      const result = service.getEvents('scoreboardConfig', false);
      result.then(res => {
        expect(res).toEqual({
          config: {},
          modules: 'modules',
          selectedTab: 'scoreboardConfig'
        } as any);
      });
    });

    it('it should group events by tab - featured (case: grouped/true)', () => {
      service.getConfig = jasmine.createSpy().and.returnValue(
        {
          eventMethods: {
            ms: 'newFunction'
          },
          inConnectApp: false,
          name: 'horseracing',
          request: {
            modules: 'modules'
          }
        }
      );
      service['newFunction'] = jasmine.createSpy().and.returnValue(Promise.resolve({config: {}}));
      dailyRacingService['addEvents'] = jasmine.createSpy().and.returnValue([{config: {}}]);
      const result = service.getEvents('featured', true);
      result.then(res => {
        expect(res).toEqual({
          groupedRacing: [],
          classesTypeNames: [],
          config: {},
          modules: 'modules',
          selectedTab: 'featured'
        } as any);
      });
    });

    it('it should group events by tab - featured (case: grouped false)', () => {
      service.getConfig = jasmine.createSpy().and.returnValue(
        {
          eventMethods: {
            featured: 'newFunction'
          },
          inConnectApp: false,
          name: 'horseracing',
          request: {
            modules: 'modules'
          }
        }
      );
      service['newFunction'] = jasmine.createSpy().and.returnValue(Promise.resolve({config: {}}));
      dailyRacingService['addEvents'] = jasmine.createSpy().and.returnValue([{config: {}}]);
      const result = service.getEvents('featured', false);
      result.then(res => {
        expect(res).toEqual({
          config: {},
          modules: 'modules',
          selectedTab: 'featured'
        } as any);
      });
    });

    it('it should group events by tab - today', () => {
      service.getConfig = jasmine.createSpy().and.returnValue(
        {
          eventMethods: {
            ms: 'newFunction'
          },
          inConnectApp: false,
          name: 'horseracing',
          request: {
            modules: 'modules'
          }
        }
      );
      service['newFunction'] = jasmine.createSpy().and.returnValue(Promise.resolve({config: {}}));
      dailyRacingService['addEvents'] = jasmine.createSpy().and.returnValue([{config: {}}]);
      const result = service.getEvents('today', true);
      result.then(res => {
        expect(res).toEqual({
          groupedRacing: [],
          classesTypeNames: [],
          config: {},
          modules: 'modules',
          selectedTab: 'today'
        } as any);
      });
    });
  });

  describe('getByTab', () => {
    it('it should return promise ', () => {
      service.getRequestConfigByTab = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      service.getEvents = jasmine.createSpy().and.returnValue(Promise.resolve({}));
      const result = service.getByTab('scoreboardConfig', true);
      result.then(cb => {
        expect(cb).toEqual({} as any);
      });
    });
  });

  describe('prepareEventsObj', () => {
    it('it should return data obj ', () => {
      const result = service.prepareEventsObj(['test']);
      expect(result).toEqual({
        events: ['test'],
        eventsByTypeName: groupedEventsByMeetings,
        typeNamesArray: ['Steepledowns', 'Turf Paradise', 'Racing Specials']
      } as any);
      expect(templateService.groupEventsByTypeName).toHaveBeenCalledWith(['test']);
    });
  });

  describe('getYourCallSpecials', () => {
    it('it should return promise ', () => {
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue(123456789);

      const result = service.getYourCallSpecials();

      result.then(cb => {
        expect(cb).toEqual({ name: 'event' } as any);
      });
      expect(timeService.getSuspendAtTime).toHaveBeenCalled();
      expect(eventFactory.eventsByTypeIds).toHaveBeenCalledWith({
        typeId: service['BYBConfig'].HR_YC_EVENT_TYPE_ID,
        suspendAtTime: 123456789
      });
    });
  });

  describe('getEventsGroupingByTabs', () => {
    it('it should return function ', () => {
      const result = service.getEventsGroupingByTabs('specials');

      expect(result).toEqual(jasmine.any(Function));
    });
  });

  describe('getClassesTypeNames', () => {
    it('it should return order 1 ', () => {
      iInitialSportConfig.config.eventMethods.name = 'typeName';
      const p2 = {
        name: 'test2',
        typeName: 'test2',
        typeDisplayOrder: 2
      };
      const res = [
        {name: 'typeName', typeDisplayOrder: 1},
        {name: 'test2', typeDisplayOrder: 2}
      ];
      const result = service.getClassesTypeNames([iInitialSportConfig.config.eventMethods, p2]);
      expect(result).toEqual({
        classesTypeNames: {
          default: res
        }
      });
    });

    it('it should not find name  in events array  ', () => {
      iInitialSportConfig.config.eventMethods.name = 'test';
      const p2 = {
        name: 'test',
        typeName: 'typeName',
        typeDisplayOrder: 2
      };
      const res = [
        {name: 'typeName', typeDisplayOrder: 1}
      ];
      const result = service.getClassesTypeNames([iInitialSportConfig.config.eventMethods, p2]);
      expect(result).toEqual({
        classesTypeNames: {
          default: res
        }
      });
    });

    it('it should return order -1 ', () => {
      iInitialSportConfig.config.eventMethods.name = 'typeName';
      const p2 = {
        name: 'test2',
        typeName: 'test2',
        typeDisplayOrder: 0
      };
      const res = [
        {name: 'test2', typeDisplayOrder: 0},
        {name: 'typeName', typeDisplayOrder: 1}
      ];
      const result = service.getClassesTypeNames([iInitialSportConfig.config.eventMethods, p2]);
      expect(result).toEqual({
        classesTypeNames: {
          default: res
        }
      });
    });

    it('it should return order name 1 ', () => {
      iInitialSportConfig.config.eventMethods.name = 'typeName';
      const p2 = {
        name: 'veryLongTestName',
        typeName: 'veryLongTestName',
        typeDisplayOrder: 1
      };
      const res = [
        {name: 'typeName', typeDisplayOrder: 1},
        {name: 'veryLongTestName', typeDisplayOrder: 1}

      ];
      const result = service.getClassesTypeNames([iInitialSportConfig.config.eventMethods, p2]);
      expect(result).toEqual({
        classesTypeNames: {
          default: res
        }
      });
    });

    it('it should return order name  - 1', () => {
      iInitialSportConfig.config.eventMethods.name = 'typeName';
      const p2 = {
        name: 'test2',
        typeName: 'test2',
        typeDisplayOrder: 1
      };
      const res = [
        {name: 'test2', typeDisplayOrder: 1},
        {name: 'typeName', typeDisplayOrder: 1}
      ];
      const result = service.getClassesTypeNames([iInitialSportConfig.config.eventMethods, p2]);
      expect(result).toEqual({
        classesTypeNames: {
          default: res
        }
      });
    });

    it('it should return static order  ', () => {
      iInitialSportConfig.config.eventMethods.name = '1';
      iInitialSportConfig.config.eventMethods.typeName = '1';
      const p2 = {
        name: 1,
        typeName: 1,
        typeDisplayOrder: 1
      };
      const res = [
        {name: '1', typeDisplayOrder: 1},
        {name: 1, typeDisplayOrder: 1}

      ];
      const result = service.getClassesTypeNames([iInitialSportConfig.config.eventMethods, p2]);
      expect(result).toEqual({
        classesTypeNames: {
          default: res
        }
      });
    });
  });

  describe('results', () => {
    it('it should return promise ', () => {
      service.results().then(cb => {
        expect(cb).toEqual([]);
      });
    });
  });

  describe('arrangeEvents', () => {
    it('it should return promise ', fakeAsync(() => {
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      const func = () => {};
      const result = service.arrangeEvents({}, 'selectedTab', func);
      result.then(cb => {
        expect(cb).toEqual({ events: {}} as any);
      });
    }));

    it('it should return promise reject ', fakeAsync(() => {
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      const func = () => {};
      const result = service.arrangeEvents([], '', func);
      result.catch(cb => {
        expect(cb).toEqual('Error in params');
      }).catch(cb => {
        expect(cb).toEqual('Error in params');
      });
    }));
  });

  describe('isSpecialsAvailable', () => {
    it('it should return eventFactory ', fakeAsync(() => {
      service['readonlyRequestConfig'] = iInitialSportConfig.config as any;
      service.config.name = 'horseracing';
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      routingHelperservice.getLastUriSegment = jasmine.createSpy().and.returnValue('future');
      const url = 'racing/future';

      service.getConfig = jasmine.createSpy().and.returnValue({
        tabs: {
          specials: ''
        }
      });
      service.isSpecialsAvailable(url).subscribe(result => {
        // expect(result).toBe(true);
      });
    }));

    it('it should return true if it is Specials tab', fakeAsync(() => {
      service['readonlyRequestConfig'] = iInitialSportConfig.config as any;
      service.config.request.categoryId = '21';
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      routingHelperservice.getLastUriSegment = jasmine.createSpy().and.returnValue('specials');
      const url = 'racing/specials';

      service.getConfig = jasmine.createSpy().and.returnValue({
        tabs: {
          specials: ''
        }
      });
      service.isSpecialsAvailable(url).subscribe(result => {
        expect(result).toBe(true);
      });
    }));

    it('it should return false if it is Coral greyhounds racing', fakeAsync(() => {
      service['readonlyRequestConfig'] = iInitialSportConfig.config as any;
      service.config.request.categoryId = '19';
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      service.isSpecialsAvailable('test', true).subscribe(result => {
        expect(result).toBe(false);
      });
    }));

    it('it should return false if it is Coral horseracing', fakeAsync(() => {
      service['readonlyRequestConfig'] = iInitialSportConfig.config as any;
      service.config.request.categoryId = '21';
      service.getConfig = jasmine.createSpy().and.returnValue({
        tabs: {
          specials: ''
        }
      });
      routingHelperservice.getLastUriSegment = jasmine.createSpy().and.returnValue('specials');
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      service.isSpecialsAvailable('test', true).subscribe(result => {
        expect(result).toBe(true);
      });
    }));
  });

  describe('getAntepostEvents', () => {
    it('it should return eventFactory ', () => {
      service.getConfig = jasmine.createSpy().and.returnValue({
        tabs: {
          specials: ''
        },
        request: 'request'
      });
      const result = service.getAntepostEvents();
      result.then(cb => {
        expect(cb).toEqual({ events: [] });
      });
      expect(eventFactory.eventsByClasses).toHaveBeenCalledWith('request');
      expect(service.getConfig).toHaveBeenCalled();
    });
  });

  describe('getClassesTypeNamesByFlagCodes', () => {
    it('it should return eventFactory ', () => {
      const classesTypeNames = {
        IN: [{name: 'Wolverhampton'}],
        INT: [],
        UK: [
          {name: 'Club Hipico'},
          {name: 'Charles Town'}
        ],
        US: [
          {name: 'Portman Park'},
          {name: 'NewCastle'}
          ]
      };
      const secondParams = [
        {
          data: [ {
            id: 8793694,
            name: 'Club Hipico',
            typeName: 'Club Hipico',
            typeDisplayOrder: 0,
            typeFlagCodes: 'GVA,UK,AVA,IE,'
          },
            {
              id: 8795839,
              name: 'Charles Town',
              typeName: 'Charles Town',
              typeDisplayOrder: 0,
              typeFlagCodes: 'GVA,UK,AVA,RVA,'
            }
          ],
        flag: 'UK'
        },
        {
          data: [{
              id: 8793203,
              name: 'Wolverhampton',
              typeName: 'Wolverhampton',
              typeDisplayOrder: 0,
              typeFlagCodes: 'GVA,IN,AVA,RVA,'
            }],
          flag: 'IN'
        },
        {
          data: [{
              id: 8795859,
              name: 'Portman Park',
              typeName: 'Portman Park',
              typeDisplayOrder: 0,
              typeFlagCodes: 'GVA,AVA,RVA,US,'
            },
            {
              id: 8795859,
              name: 'NewCastle',
              typeName: 'NewCastle',
              typeDisplayOrder: 0,
              typeFlagCodes: 'GVA,AVA,RVA,US,'
            }
          ],
          flag: 'US'
        },
        {
          data: [],
          flag: 'INT'
        }
      ];
      service['getCashoutAvailGroups'] = jasmine.createSpy();

      service.getClassesTypeNamesByFlagCodes(eventsDataMock, groupedDataMock);

     });

    it('it should retur smth ', () => {
      const newGroupedDataMock =  JSON.parse(JSON.stringify((groupedDataMock)));

      newGroupedDataMock[0].data[1].name = 'Club Hipico';
      newGroupedDataMock[0].data[1].typeName = 'Club Hipico';
      service['getCashoutAvailGroups'] = jasmine.createSpy();

      service.getClassesTypeNamesByFlagCodes(eventsDataMock, newGroupedDataMock);
      expect(service['getCashoutAvailGroups']).toHaveBeenCalled();
    });
  });

  describe('prepareYourCallSpecialsForFeaturedTab', () => {
    it('it should return eventFactory ', () => {
     const yourCallSpecials: any = {
        cashoutAvail: 'cashoutAvail',
        categoryCode: 'categoryCode',
        categoryId: 'categoryId',
        categoryName: 'categoryName',
        displayOrder: 11,
        drilldownTagNames: 'drilldownTagNames',
        eventIsLive: true,
        eventSortCode: 'eventSortCode',
        eventStatusCode: 'eventStatusCode',
        eventTerms: 'eventTerms',
        id: 11,
        name: 'Featured'
     };
      racingYourcallService.prepareData = jasmine.createSpy().and.callFake(p1 => [p1]);

      expect(service.prepareYourCallSpecialsForFeaturedTab(yourCallSpecials)).toEqual([]);
      expect(racingYourcallService.prepareData).toHaveBeenCalledWith([], yourCallSpecials);
    });
  });

  describe('addEventsFromModules', () => {
    it('it should return promise ', () => {
      commandService.executeAsync = jasmine.createSpy().and.callFake(p1 => {
        return [p1];
      });
      const result = service.addEventsFromModules(groupedDataMock);
      const data = {
        events: 'events'
      };
      result(data).then((response) => {
        expect(response).toBeTruthy();
      });
    });
    it('it should return empty array ', () => {
      commandService.executeAsync = jasmine.createSpy().and.callFake(p1 => {
        return [p1];
      });
      service.addEventsFromModules('').then((res) => {
        expect(res).toEqual([]);
      });
    });
  });

  describe('addFirstActiveEventProp', () => {
    it('it should have been called ', () => {

      const racingEvents = {
        groupedRacing: [
          {
            data: {
              name: 'test1',
              isResulted: true,
              startTime: '19:55'
            },

          } ,
          {
            data: [{
              name: 'data1',
              isResulted: true,
              startTime: '12:55',
              isOpenEvent: true
            },
              {
                name: 'data1',
                isResulted: true,
                startTime: '12:55',
                isOpenEvent: true
              },
              {
                name: 'data1',
                isResulted: true,
                startTime: '12:55',
                isOpenEvent: true
              }],

          },
          {
            data: [{
              name: 'data1',
              isResulted: true,
              startTime: '12:55'
            }, {
              isResulted: true,
              startTime: '12:55'
            },
              {
                name: 'test1',
                isResulted: true,
                startTime: '19:55',
                isOpenEvent: true
              }]

          },
          {
            data: {
              name: 'test3',
              isResulted: true,
              startTime: '1e:55'
            },
          }
          ]
      };
      service.addFirstActiveEventProp(racingEvents);
      expect(service.addFirstActiveEventProp).toBeTruthy();
    });
  });

  describe('arrangeOutcomesWithResults', () => {
    it('it should return eventFactory ', () => {
      const eventId = '12135493';
      const markets = {
        markets: [{
          templateMarketName: 'Win/Win',
          name: 'Seven Emirates v Three Coins',
          outcomes: [{
            priceDEc: 100
          }, {
            priceDEc: 200
          }],
          eventId
        }, {
          templateMarketName: 'Trap Market',
          name: 'Trap Market',
          outcomes: [{
            priceDEc: 100
          }, {
            priceDEc: 200
          }],
          eventId
        }]
      };
      const reqData = [markets, markets];
      templateService.genEachWayPlaces = jasmine.createSpy().and.callFake(p1 => {
        return 'test';
      });
      service.addFavouriteLabelToOutcomesWithResults = jasmine.createSpy().and.callFake(p1 => {
        return [
          {
            results: {
              outcomeResultCode: 'outcomeResultCode',
              outcomePosition: 'outcomePosition'
            }
          },
          {
            results: {
              outcomeResultCode: 'L',
              outcomePosition: 'outcomePosition'
            }
          }
        ];
      });
      const result = service.arrangeOutcomesWithResults(reqData);
      result.then(res => {
        expect(res[0].atLeastOneWinnerIsPresent).toEqual(true);
      });
    });

    it('it should check else path ', () => {
      const eventId = '12135493';
      const markets = {
        atLeastOneWinnerIsPresent: false,
        markets: [{
          templateMarketName: 'Win/Win',
          name: 'Seven Emirates v Three Coins',
          outcomes: [],
          eventId
        }, {
          templateMarketName: 'Trap Market',
          name: 'Trap Market',
          outcomes: [],
          eventId
        }]
      };
      const reqData = [markets, markets];
      templateService.genEachWayPlaces = jasmine.createSpy().and.callFake(p1 => {
        return 'test';
      });
      service.addFavouriteLabelToOutcomesWithResults = jasmine.createSpy().and.callFake(p1 => {
        return [
          {
            results: {
              outcomeResultCode: 'outcomeResultCode',
              outcomePosition: 'outcomePosition'
            }
          }
        ];
      });
      const result = service.arrangeOutcomesWithResults(reqData);
      result.then(res => {
        expect(res).toEqual([]);
      });
    });

  });

  describe('updateOucomesArray', () => {
    it('should return outcomes', () => {
      const outcomesArray = [
        {
          results: {
            outcomeResultCode: 'outcomeResultCode',
            outcomePosition: 'outcomePosition',
            priceDec: 100
          }
        },
        ''
      ];

      const outcomes = [
        {
          flag: 'UK',
          favourite: '',
          data: [
            {
              id: 8793694,
              name: 'Club Hipico',
              typeName: 'Club Hipico',
              typeDisplayOrder: 0,
              typeFlagCodes: 'GVA,UK,AVA,IE,'
            },
            {
              id: 8795839,
              name: 'Charles Town',
              typeName: 'Charles Town',
              typeDisplayOrder: 0,
              typeFlagCodes: 'GVA,UK,AVA,RVA,'
            }
          ]
        }
      ];

      const result = service.updateOucomesArray(outcomesArray, outcomes);
      expect(result[0].flag).toEqual('UK');
      expect(result[0].favourite).toEqual(outcomesArray[0]);
    });
  });

  describe('groupedPricesArray', () => {
    it('should return groupedArray', () => {
      const outcomesArray = [
        {
          results: {
            outcomeResultCode: 'outcomeResultCode',
            outcomePosition: 'outcomePosition',
            priceDec: 100
          }
        },
        {
          results: {
            outcomeResultCode: 'L',
            outcomePosition: 'outcomePosition',
            priceDec: 250
          }
        }
      ];

      const result = service.groupedPricesArray(outcomesArray);
      expect(result).toEqual([[100], [250]]);
    });
  });

  describe('sortOutcomesByLowestPrice', () => {
    it('should return sorted outcomes', () => {
      const outcomesArray = [
        {
          results: {
            outcomeResultCode: 'outcomeResultCode',
            outcomePosition: 'outcomePosition',
            priceDec: 100
          }
        },
        {
          results: {
            outcomeResultCode: 'L',
            outcomePosition: 'outcomePosition',
            priceDec: 250
          }
        }
      ];

      const result = service.sortOutcomesByLowestPrice(outcomesArray);
      expect(result[0].results.priceDec).toEqual(100);
    });
  });

  describe('addFavouriteLabelToOutcomesWithResults', () => {
    it('should update outcomes', () => {
      const outcomesArray = [
        {
          results: {
            outcomeResultCode: 'outcomeResultCode',
            outcomePosition: 'outcomePosition',
            priceDec: 100
          }
        },
        {
          results: {
            outcomeResultCode: 'L',
            outcomePosition: 'outcomePosition',
            priceDec: 250
          }
        }
      ];

      spyOn(service, 'updateOucomesArray').and.callThrough();

      const result = service.addFavouriteLabelToOutcomesWithResults(outcomesArray);
      const resultValue = {
        favourite: 'F',
        results: {
          outcomePosition: 'outcomePosition',
          outcomeResultCode: 'outcomeResultCode',
          priceDec: 100
        }
      };
      expect(result[0]).toEqual(resultValue);
      expect(service.updateOucomesArray).toHaveBeenCalledWith(['F', '2F'], outcomesArray);
    });

    it('should update outcomes', () => {
      const outcomesArray = [
        {
          results: {
            outcomeResultCode: 'outcomeResultCode',
            outcomePosition: 'outcomePosition'
          }
        },
        {
          results: {
            outcomeResultCode: 'L',
            outcomePosition: 'outcomePosition'
          }
        }
      ];

      spyOn(service, 'groupedPricesArray').and.returnValue([]);
      spyOn(service, 'updateOucomesArray').and.returnValue([]);

      const result = service.addFavouriteLabelToOutcomesWithResults(outcomesArray);
      expect(result).toEqual([]);
      expect(service.groupedPricesArray).toHaveBeenCalledWith(outcomesArray);
      expect(service.updateOucomesArray).toHaveBeenCalledWith(undefined, outcomesArray);
    });
  });

  describe('sortMarketsName', () => {
    it('should set uiClass', () => {
      const yourCallSpecials: any = {
        cashoutAvail: 'cashoutAvail',
        categoryCode: 'categoryCode',
        categoryId: 'categoryId',
        categoryName: 'categoryName',
        displayOrder: 11,
        drilldownTagNames: 'drilldownTagNames',
        eventIsLive: true,
        eventSortCode: 'eventSortCode',
        eventStatusCode: 'eventStatusCode',
        eventTerms: 'eventTerms',
        id: 11,
        name: 'Featured',
        markets: [{
          templateMarketName: 'Win/Win',
          name: 'Seven Emirates v Three Coins',
          displayOrder: 111,
          outcomes: [{
            priceDEc: 200
          }, {
            priceDEc: 400
          }]
        }, {
          templateMarketName: 'Trap Market',
          name: 'Trap Market',
          displayOrder: 222,
          outcomes: [{
            priceDEc: 111
          }, {
            priceDEc: 444
          }]
        }]
      };

      const sortedArray = ['testName', 'Seven Emirates v Three Coins'];
      templateService.genTerms = jasmine.createSpy().and.callFake(p1 => {
        return 'genTerms';
      });
      templateService.genClass = jasmine.createSpy().and.callFake(p1 => {
        return 'genClass';
      });

      const result = service.sortMarketsName(yourCallSpecials, sortedArray);
      expect(result.uiClass).toEqual('genClass');
    });

    it('should return promise', () => {
      const yourCallSpecials: any = {
        cashoutAvail: 'cashoutAvail',
        categoryCode: 'categoryCode',
        categoryId: 'categoryId',
        categoryName: 'categoryName',
        displayOrder: 11
      };

      const result = service.sortMarketsName(yourCallSpecials,  false);
      expect(result).toEqual(yourCallSpecials);
    });
  });

  xdescribe('getTypeNamesEvents', () => {
    it('should return promise', () => {
      const requestParams = { request: { breadcrumbsNavMenuFlags: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'] } };
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue('12/05/2020');
      service.getRequestConfigByTab = jasmine.createSpy().and.returnValue(requestParams);
      spyOn(service, 'getConfig').and.returnValue(requestParams);
      service.getEvents = jasmine.createSpy().and.returnValue(Promise.resolve({
        events: [{
          startTime: '19:00'
        }]
      }));
      const outputparams = { groupedByMeetings: groupedEventsByMeetings, groupedByFlagAndData: [] };
      spyOn(service, 'navMenuGroupEventsByCountryCodes').and.returnValue(outputparams as any);
      service.addEventsFromModules = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      timeService.determineCurrentAndNextDayRange = jasmine.createSpy().and.returnValue({
        timeStampFrom: '16:00',
        timeStampTo: '20;00'
      });

      const result = service.getTypeNamesEvents({ selectedTab: 'tabs', filterByDate: '12/05/2020', additionalEventsFromModules: 'click' }); 
      result.then(res => {
        expect(res).toEqual(outputparams);
      });
    });

    xit('should return data ', () => {
      service.getConfig = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue('12/05/2020');
      service.getRequestConfigByTab = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      service.getEvents = jasmine.createSpy().and.returnValue(Promise.resolve({
        events: [{
          startTime: '19:00'
        }]
      }));
      spyOn(service, 'navMenuGroupEventsByCountryCodes').and.returnValue(Promise.resolve([]) as any);
      service.addEventsFromModules = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      timeService.determineCurrentAndNextDayRange = jasmine.createSpy().and.returnValue({
        timeStampFrom: '16:00',
        timeStampTo: '20;00'
      });

      const result = service.getTypeNamesEvents({selectedTab: 'tabs',filterByDate:  '', additionalEventsFromModules: 'click'});
      result.then(res => {
        expect(res).toEqual([]);
      });
    });

    it('should return promise reject', () => {
      service.getConfig = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue('12/05/2020');
      service.getRequestConfigByTab = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      service.getEvents = jasmine.createSpy().and.returnValue(Promise.reject('error'
      ));
      spyOn(service, 'navMenuGroupEventsByCountryCodes').and.returnValue(Promise.resolve([]) as any);
      service.addEventsFromModules = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);
      timeService.determineCurrentAndNextDayRange = jasmine.createSpy().and.returnValue(iInitialSportConfig.config);

      const result = service.getTypeNamesEvents({selectedTab: 'tabs',filterByDate:  '12/05/2020', additionalEventsFromModules: 'click'});
      result.then(res => {})
      .catch((error) => {
        expect(error).toEqual('error');
      });
    });
  });

  describe('getRequestConfigByTab', () => {
    it('groupByFlagCodesAndClassesTypeNames: check getClassesTypeNamesByFlagCodes to be called', () => {
      service.getConfig = jasmine.createSpy().and.returnValue({
        tabs: {
          football: ''
        }
      });
      timeService.getSuspendAtTime = jasmine.createSpy().and.returnValue('12/05/2020');

      const result = service.getRequestConfigByTab('eventMethods');
      const resultParams = {
        breadcrumbsNavMenuFlags: [],
        date: 'eventMethods',
        excludeEventsClassIds: '227',
        modules: {
          dailyRacing: {
            classIds: '227'
          }
        },
        priceHistory: true,
        racingFormEvent: true,
        racingFormOutcome: true,
        suspendAtTime: '12/05/2020'
      };
      expect(result).toEqual(resultParams);
      expect(service.getConfig).toHaveBeenCalled();
      expect(timeService.getSuspendAtTime).toHaveBeenCalled();
    });
  });

  describe('racing service: groupByFlagCodesAndClassesTypeNames', () => {
    it('groupByFlagCodesAndClassesTypeNames: check getClassesTypeNamesByFlagCodes to be called', () => {
      spyOn(service, 'getClassesTypeNamesByFlagCodes');
      spyOn(service, 'getConfig').and.returnValue(requestParams);

      service.groupByFlagCodesAndClassesTypeNames(eventsDataMock);
     });

    it('groupByFlagCodesAndClassesTypeNames: check getLiveStreamGroups to be called', () => {
      spyOn(service, 'groupByFlagCodes').and.returnValue('groupByFlagCodes' as any);
      spyOn(service, 'getConfig').and.returnValue(requestParams);
      spyOn(service, 'getClassesTypeNamesByFlagCodes').and.returnValue(true as any);
      service['getLiveStreamGroups'] = jasmine.createSpy('getLiveStreamGroups').and.returnValue(true);

      const result = service.groupByFlagCodesAndClassesTypeNames(eventsDataMock);
      expect(result).toEqual({
        classesTypeNames: true,
        groupedRacing: 'groupByFlagCodes'
      } as any);
      expect(service['getLiveStreamGroups']).toHaveBeenCalledWith(true as any, 'groupByFlagCodes' as any);
    });
  });
  describe('getById, getGreyhoundEvent', () => {
    describe('racing post enabled', () => {
      const eventId = '123';
      const errHandler = jasmine.createSpy('errHandler');
      beforeEach(() => {
        cmsService.getSystemConfig.and.returnValue(of({
          raceInfo: {
            timeFormEnabled: true
          },
          RacingDataHub: {
            isEnabledForGreyhound: true,
            isEnabledForHorseRacing: true,
          }
        }));
      });
      it('getById: success', () => {
        service.getById(eventId, false).subscribe((res) => {
          expect(eventFactory.getEvent).toHaveBeenCalledWith(eventId, {priceHistory: true, externalKeysEvent: true}, false, false);
          expect(racingPostService.getHorseRacingPostById).toHaveBeenCalledWith(eventId);
          expect(racingPostService.mergeHorseRaceData).toHaveBeenCalledWith(
            { name: 'event' }, { Error: 'false', document: { 1: { raceType: 'horseracing' } } });
        }, errHandler);
        expect(errHandler).not.toHaveBeenCalled();
      });
      it('getGreyhoundEvent: success', () => {
        service.getGreyhoundEvent('123').subscribe(() => {
          expect(eventFactory.getEvent).toHaveBeenCalledWith(eventId, {priceHistory: true, externalKeysEvent: true}, false, false);
          expect(racingPostService.getGreyhoundRacingPostById).toHaveBeenCalledWith(eventId);
          expect(racingPostService.mergeGreyhoundRaceData).toHaveBeenCalledWith(
            { name: 'event' }, { Error: 'false', document: { 1: { raceType: 'greyhound' } } });
        }, errHandler);
        expect(errHandler).not.toHaveBeenCalled();
      });
    });
    describe('racing post disabled', () => {
      const eventId = '123';
      const errHandler = jasmine.createSpy('errHandler');
      beforeEach(() => {
        cmsService.getSystemConfig.and.returnValue(of({
          raceInfo: {
            timeFormEnabled: true
          },
          RacingDataHub: {
            isEnabledForGreyhound: false,
            isEnabledForHorseRacing: false,
          }
        }));
      });
      it('getById: success', () => {
        service.getById(eventId, true).subscribe((res) => {
          expect(eventFactory.getEvent).toHaveBeenCalledWith(eventId, {
            priceHistory: true,
            externalKeysEvent: true,
            racingFormOutcome: true,
            racingFormEvent: true
          }, false, true);
          expect(racingPostService.getHorseRacingPostById).not.toHaveBeenCalledWith(eventId);
          expect(racingPostService.mergeHorseRaceData).toHaveBeenCalled();
        }, errHandler);
        expect(errHandler).not.toHaveBeenCalled();
      });
      it('getGreyhoundEvent: success', () => {
        timeformService.getGreyhoundRaceById.and.returnValue(of([{ raceTitle: 'greyhound' }]));
        service.getGreyhoundEvent('123', true).subscribe((data) => {
          expect(eventFactory.getEvent).toHaveBeenCalledWith(eventId, {
            priceHistory: true,
            externalKeysEvent: true,
            racingFormOutcome: true,
            racingFormEvent: true
          }, false, true);
          expect(racingPostService.getGreyhoundRacingPostById).not.toHaveBeenCalledWith(eventId);
          expect(timeformService.getGreyhoundRaceById).toHaveBeenCalledWith(eventId);
          expect(racingPostService.mergeGreyhoundRaceData).not.toHaveBeenCalled();
          expect(timeformService.mergeGreyhoundRaceData).toHaveBeenCalledWith(
            [{ name: 'event' }, { raceTitle: 'greyhound' }]);
          expect(data).toEqual([{ name: 'updated event' }]);
        }, errHandler);
        expect(errHandler).not.toHaveBeenCalled();
      });

      describe('getGreyhoundEvent: success, edge cases (hello, coverage)', () => {
        it('multiple OB events (as array)', () => {
          eventFactory.getEvent.and.returnValue(Promise.resolve([{ name: 'event' }, { name: 'event2' }]));
        });
        it('no RacingData configuration', () => {
          cmsService.getSystemConfig.and.returnValue(of({ raceInfo: { timeFormEnabled: true } }));
        });
        afterEach(() => {
          service.getGreyhoundEvent('123', true).subscribe(() => {
            expect(timeformService.mergeGreyhoundRaceData).toHaveBeenCalledWith([{ name: 'event' }, { raceTitle: 'greyhound' }]);
          }, errHandler);
        });
      });
    });
    describe('racing post disabled, and timeform disabled', () => {
      const eventId = '123';
      const errHandler = jasmine.createSpy('errHandler');
      beforeEach(() => {
        cmsService.getSystemConfig.and.returnValue(of({
          raceInfo: {
            timeFormEnabled: false
          },
          RacingDataHub: {
            isEnabledForGreyhound: false,
            isEnabledForHorseRacing: false,
          }
        }));
      });
      it('getGreyhoundEvent: success', () => {

        service.getGreyhoundEvent('123', true).subscribe(() => {
          expect(eventFactory.getEvent).toHaveBeenCalledWith(eventId, {
            priceHistory: true,
            externalKeysEvent: true,
            racingFormOutcome: true,
            racingFormEvent: true
          }, false, true);
          expect(racingPostService.getGreyhoundRacingPostById).not.toHaveBeenCalledWith(eventId);
          expect(timeformService.getGreyhoundRaceById).not.toHaveBeenCalledWith(eventId);
          expect(racingPostService.mergeGreyhoundRaceData).not.toHaveBeenCalled();
          expect(timeformService.mergeGreyhoundRaceData).toHaveBeenCalled();
        }, errHandler);
        expect(errHandler).not.toHaveBeenCalled();
      });
    });
    describe('error handling', () => {
      const eventId = '123';
      const successHandler = jasmine.createSpy('errHandler');
      const errorMessage = { error: 'error' };
      beforeEach(() => {
        cmsService.getSystemConfig.and.returnValue(of({
          raceInfo: {
            timeFormEnabled: true
          },
          RacingDataHub: {
            isEnabledForGreyhound: true,
            isEnabledForHorseRacing: true,
          }
        }));
        eventFactory.getEvent.and.returnValue(throwError(errorMessage));
        spyOn(console, 'error');
      });
      it('getById: error', () => {
        service.getById(eventId, true).subscribe(successHandler, (err) => {
          expect(err).toEqual(errorMessage);
        });
        expect(successHandler).not.toHaveBeenCalled();
      });
      it('getGreyhoundEvent: error', () => {
        service.getGreyhoundEvent('123', true).subscribe(successHandler, (err) => {
          expect(err).toEqual(errorMessage);
        });
        expect(successHandler).not.toHaveBeenCalled();
      });
    });
  });


  describe('getAntepostEventsByFlag', () => {
    it('shoud test getAntepostEventsByFlag', fakeAsync(() => {
      const drilldownTagNamesMock = { drilldownTagNames: 'MKTFLAG_PR1, MKTFLAG_PB'};

      spyOn(service, 'getRequestConfigByTab').and.returnValue({
        eventDrilldownTagNamesIntersects: 'MKTFLAG_PR1, MKTFLAG_PB'
      });
      spyOn(service, 'navMenuGroupEventsByCountryCodes').and.returnValue([] as any);
      eventFactory.eventsByClasses = jasmine.createSpy().and.callFake((p1) => {
        return Promise.resolve([{
          id: 1,
          drilldownTagNames: 'MKTFLAG_PR1'
        }] );
      });
      service.getAntepostEventsByFlag(drilldownTagNamesMock);
      tick();
      expect(service.getRequestConfigByTab).toHaveBeenCalledWith('future');
      expect(service.navMenuGroupEventsByCountryCodes).toHaveBeenCalledWith([{
        id: 1,
        drilldownTagNames: 'MKTFLAG_PR1'
      }] as any);
    }));

    it('shoud return promise reject ', fakeAsync(() => {
      const drilldownTagNamesMock = { drilldownTagNames: 'MKTFLAG_PR1, MKTFLAG_PB'};

      spyOn(service, 'getRequestConfigByTab').and.returnValue({
        eventDrilldownTagNamesIntersects: 'MKTFLAG_PR1, MKTFLAG_PB'
      });
      spyOn(service, 'navMenuGroupEventsByCountryCodes').and.returnValue([] as any);
      eventFactory.eventsByClasses = jasmine.createSpy().and.callFake((p1) => {
        return Promise.reject([{
          id: 1,
          drilldownTagNames: 'MKTFLAG_PR1'
        }] );
      });
      service.getAntepostEventsByFlag(drilldownTagNamesMock);
      tick();
      expect(service.getRequestConfigByTab).toHaveBeenCalledWith('future');
    }));
  });

  describe('extendConfig', () => {
    it('shoud return object assign', () => {
      service['categoriesData'] = {
        racing: {
          sportModule: {
            specialsClassIds: []
          }
        }
      };
      const config =  {
        sportModule: 'sportModule'
      };
      const result = service.extendConfig(config);
      expect(result).toEqual(config);
    });

    it('should extend config request', () => {
      const specialsClassIds: string[] = ['123', '456'];

      service['categoriesData'] = {
        racing: {
          sportModule: {
            specialsClassIds
          }
        }
      };
      const config =  {
        sportModule: 'sportModule',
        request: {
          excludeEventsClassIds: specialsClassIds,
          modules: {
            dailyRacing: {
              classIds: specialsClassIds
            }
          }
        }
      } as any;
      expect(service.extendConfig(config)).toEqual(config);
    });
  });

  describe('racing service:: navMenuGroupEventsByCountryCodes', () => {

    beforeEach(() => {
      spyOn(service, 'getConfig').and.returnValue(requestParams);
      spyOn(service, 'filteredEventsByStatusANDTime').and.returnValue(groupedEventsByMeetings['Steepledowns'][0] as any);
    });

    it('navMenuGroupEventsByCountryCodes: filtered sport events with existed country codes', () => {
      const groupedEvents = service.navMenuGroupEventsByCountryCodes(eventsDataMock as any);

      // Check that sorting were done by sub regions
      expect(groupedEvents.groupedByFlagAndData[0].flag).toEqual('UK');
      expect(groupedEvents.groupedByFlagAndData[1].flag).toEqual('US');
    });
    it('eventTypeFlagCodeKey: should be null', () => {
      spyOn(service, 'getRacingEventTypeFlagCodeKey').and.returnValue(null);
      service.navMenuGroupEventsByCountryCodes(eventsDataMock as any);

      // Check that sorting were done by sub regions
      expect(service.filteredEventsByStatusANDTime).not.toHaveBeenCalled();
    });

    it('navMenuGroupEventsByCountryCodes: should be filtered by startTime and events contain just 1 element in array', () => {
      const groupedEvents = service.navMenuGroupEventsByCountryCodes(eventsDataMock as any);

      expect(groupedEvents.groupedByFlagAndData[0].data.length).toEqual(1);
      expect(groupedEvents.groupedByFlagAndData[1].data.length).toEqual(1);
    });

    it('navMenuGroupEventsByCountryCodes: should exist only filtered object with correct properties', () => {
      const groupedEvents = service.navMenuGroupEventsByCountryCodes(eventsDataMock as any);

      expect(groupedEvents.groupedByFlagAndData[0].data[0]).toEqual(jasmine.objectContaining({
        meeting: 'Steepledowns'
      }));
    });

    it('should not throw error if events undefined', () => {
      expect(() => service.navMenuGroupEventsByCountryCodes(undefined)).not.toThrowError();
    });
  });

  describe('racing service:: navMenuGroupEnhancedRaces', () => {
    it('navMenuGroupEnhancedRaces: filtered enhanced races by meetings', () => {
      localeService.getString = jasmine.createSpy();
      spyOn(service, 'filteredEventsByStatusANDTime').and.returnValue(groupedEventsByMeetings['Steepledowns'][0] as any);
      const groupedEvents = service.navMenuGroupEnhancedRaces(eventsDataMock as any);

      expect(groupedEvents).toEqual(jasmine.objectContaining({
          groupedByMeetings: jasmine.any(Object) as any,
          groupedByFlagAndData: jasmine.any(Array) as any
        } as any));

      expect(groupedEvents.groupedByFlagAndData[0]).toEqual(jasmine.objectContaining({
          flag: 'ENHRCS',
          data: jasmine.any(Array) as any
        } as any));

      expect(localeService.getString).toHaveBeenCalledWith('sb.extraPlaceTitle');
    });

    it('navMenuGroupEnhancedRaces: filtered without if', () => {
      localeService.getString = jasmine.createSpy();
      spyOn(service, 'filteredEventsByStatusANDTime').and.returnValue({
        eventStatusCode: 'B'
      } as any);
      const groupedEvents = service.navMenuGroupEnhancedRaces(eventsDataMock as any);

      expect(groupedEvents).toEqual(jasmine.objectContaining({
        groupedByMeetings: jasmine.any(Object) as any,
        groupedByFlagAndData: jasmine.any(Array) as any
      } as any));

      expect(groupedEvents.groupedByFlagAndData[0]).toEqual(jasmine.objectContaining({
        flag: 'ENHRCS',
        data: jasmine.any(Array) as any
      } as any));

      expect(localeService.getString).toHaveBeenCalledWith('sb.extraPlaceTitle');
    });
  });

  describe('racing service:: filteredEventsByStatusANDTime', () => {
    it('Not resulted sport events should be filtered by startTime property', () => {
      const filteredEvents = service.filteredEventsByStatusANDTime(groupedEventsByMeetings['Steepledowns'] as any);

      expect(filteredEvents).toEqual(jasmine.objectContaining({
        eventStatusCode: 'A',
        startTime: 1548787980000
      } as any));
    });

    it('Not resulted and not race-off sport events should be filtered by startTime', () => {
      groupedEventsByMeetings['Steepledowns'].push({
        eventStatusCode: 'A',
        isResulted: false,
        isLiveNowEvent: false,
        isStarted: true,
        startTime: 1548758100000
      } as any);

      const filteredEvents =
        service.filteredEventsByStatusANDTime(groupedEventsByMeetings['Steepledowns'] as any, true);

      expect(filteredEvents).toEqual(jasmine.objectContaining({
        eventStatusCode: 'A',
        startTime: 1548787980000
      } as any));
    });

    it('should return eventEntity', () => {
      const eventEntity = [{
        eventStatusCode: 'B',
        isResulted: false,
        isLiveNowEvent: false,
        isStarted: true,
        startTime: 1548758100000
      }];

      const filteredEvents =
        service.filteredEventsByStatusANDTime(eventEntity as any, true);

      expect(filteredEvents).toEqual({
        eventStatusCode: 'B',
        isResulted: false,
        isLiveNowEvent: false,
        isStarted: true,
        startTime: 1548758100000
      } as any);
    });
  });

  describe('setGroupedMarketHeader', () => {
    it('should set correct header for grouped market', () => {
      const groupedMarkets = {
        customOrder: 4,
        displayOrder: 110,
        header: [],
        label:  'To Finish',
        markets: [{}],
        name: 'To Finish',
        path: 'to-finish',
        subMarkets: ['To Finish Second', 'To Finish Third', 'To Finish Fourth', 'To Finish 2nd', 'To Finish 3rd']
      };
      service['TO_FINISH_MARKET'] = {
        SUB_MARKETS: ['To Finish Second', 'To Finish Third', 'To Finish Fourth', 'To Finish 2nd', 'To Finish 3rd']
      };
      const market = {
        isToFinish: true,
        templateMarketName: 'To Finish 2nd'
      };
      service.setGroupedMarketHeader(groupedMarkets, market);

      expect(groupedMarkets.header[0]).toEqual('2nd');
    });

    it('should check else path', () => {
      const groupedMarkets = {
        customOrder: 4,
        displayOrder: 110,
        header: [],
        label:  'Place Insurance',
        markets: [{}],
        name: 'Place Insurance',
        path: 'insurance',
        subMarkets: ['Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
          'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4',
          'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places']
      };
      service['INSURANCE_MARKETS'] = {
        SUB_MARKETS: ['Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
          'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4',
          'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places']
      };
      const market = {
        insuranceMarkets: false,
        isToFinish: false,
        templateMarketName: 'Insurance 3 Places'
      };
      service.setGroupedMarketHeader(groupedMarkets, market);

      expect(service.setGroupedMarketHeader).toBeTruthy();
    });

    it('should switch default case', () => {
      const groupedMarkets = {
        customOrder: 4,
        displayOrder: 110,
        header: [],
        label:  'Place Insurance',
        markets: [{}],
        name: 'Place Insurance',
        path: 'insurance',
        subMarkets: ['Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
          'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4',
          'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places']
      };
      service['INSURANCE_MARKETS'] = {
        SUB_MARKETS: ['Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
          'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4',
          'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places']
      };
      const market = {
        insuranceMarkets: true,
        isToFinish: true,
        templateMarketName: 'test'
      };
      service.setGroupedMarketHeader(groupedMarkets, market);

      expect(service.setGroupedMarketHeader).toBeTruthy();
    });

    it('should set correct header for grouped (insurance) markets', () => {
      const groupedMarkets = {
        customOrder: 4,
        displayOrder: 110,
        header: [],
        label:  'Place Insurance',
        markets: [{}],
        name: 'Place Insurance',
        path: 'insurance',
        subMarkets: ['Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
          'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4',
          'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places']
      };
      service['INSURANCE_MARKETS'] = {
        SUB_MARKETS: ['Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4',
          'Insurance - Place 2', 'Insurance - Place 3', 'Insurance - Place 4',
          'Insurance 2 Places', 'Insurance 3 Places', 'Insurance 4 Places']
      };
      const market = {
        insuranceMarkets: true,
        templateMarketName: 'Insurance 3 Places'
      };
      service.setGroupedMarketHeader(groupedMarkets, market);

      expect(groupedMarkets.header[0]).toEqual('3rd');
    });
  });

  describe('test configureTabs', () => {
    it('horseracing: should call filterTabs', () => {
      const name = 'horseracing';
      const isSpecialsPresent = false;
      const isNextRacesEnabled = false;
      service.filterTabs = jasmine.createSpy().and.callThrough();
      service.configureTabs(name, tabsMock, isSpecialsPresent);
      expect(service.filterTabs).toHaveBeenCalledWith(tabsMock, isSpecialsPresent, isNextRacesEnabled);
    });

    it('horseracing: should call filterTabs and should return array with hidden tabs: "tab-specials" & "tab-races"', () => {
      const name = 'horseracing';
      const isSpecialsPresent = false;
      const isNextRacesEnabled = false;
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      const actualResult = service.filterTabs(tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(actualResult).toEqual([
        {
          id: 'tab-specials',
          label: '',
          url: '',
          hidden: true
        },
        {
          id: 'tab-races',
          label: '',
          url: '',
          hidden: true
        },
        {
          id: 'tab-featured',
          label: '',
          url: ''
        }
      ]);
    });

    it('horseracing: should call filterTabs and should return array with hidden tab "tab-races"', () => {
      const name = 'horseracing';
      const isSpecialsPresent = true;
      const isNextRacesEnabled = false;
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      const actualResult = service.filterTabs(tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(actualResult).toEqual([
        {
          id: 'tab-specials',
          label: '',
          url: '',
          hidden: false
        },
        {
          id: 'tab-races',
          label: '',
          url: '',
          hidden: true
        },
        {
          id: 'tab-featured',
          label: '',
          url: ''
        }
      ]);
    });

    it('horseracing: should call filterTabs and should return array with hidden tab "tab-specials"', () => {
      const name = 'horseracing';
      const isSpecialsPresent = false;
      const isNextRacesEnabled = true;
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      const actualResult = service.filterTabs(tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(actualResult).toEqual([
        {
          id: 'tab-specials',
          label: '',
          url: '',
          hidden: true
        },
        {
          id: 'tab-races',
          label: '',
          url: '',
          hidden: false
        },
        {
          id: 'tab-featured',
          label: '',
          url: ''
        }
      ]);
    });

    it('horseracing: should call filterTabs and should return array without hidden tabs', () => {
      const name = 'horseracing';
      const isSpecialsPresent = true;
      const isNextRacesEnabled = true;
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      const actualResult = service.filterTabs(tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(actualResult).toEqual([
        {
          id: 'tab-specials',
          label: '',
          url: '',
          hidden: false
        },
        {
          id: 'tab-races',
          label: '',
          url: '',
          hidden: false
        },
        {
          id: 'tab-featured',
          label: '',
          url: ''
        }
        ]);
    });

    it('greyhound: should call filterTabs', () => {
      const name = 'greyhound';
      const isSpecialsPresent = false;
      const isNextRacesEnabled = false;
      service.filterTabs = jasmine.createSpy().and.callThrough();
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(service.filterTabs).toHaveBeenCalledWith(tabsMock, isSpecialsPresent, isNextRacesEnabled);
    });

    it('greyhound: should call filterTabs and should return array with hidden tabs: "tab-specials" & "tab-races"', () => {
      const name = 'greyhound';
      const isSpecialsPresent = false;
      const isNextRacesEnabled = false;
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      const actualResult = service.filterTabs(tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(actualResult).toEqual([
        {
          id: 'tab-specials',
          label: '',
          url: '',
          hidden: true
        },
        {
          id: 'tab-races',
          label: '',
          url: '',
          hidden: true
        },
        {
          id: 'tab-featured',
          label: '',
          url: ''
        }
      ]);
    });

    it('greyhound: should call filterTabs and should return array with hidden tab "tab-races"', () => {
      const name = 'greyhound';
      const isSpecialsPresent = true;
      const isNextRacesEnabled = false;
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      const actualResult = service.filterTabs(tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(actualResult).toEqual([
        {
          id: 'tab-specials',
          label: '',
          url: '',
          hidden: false
        },
        {
          id: 'tab-races',
          label: '',
          url: '',
          hidden: true
        },
        {
          id: 'tab-featured',
          label: '',
          url: ''
        }
      ]);
    });

    it('greyhound: should call filterTabs and should return array with hidden tab "tab-specials"', () => {
      const name = 'greyhound';
      const isSpecialsPresent = false;
      const isNextRacesEnabled = true;
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      const actualResult = service.filterTabs(tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(actualResult).toEqual([
        {
          id: 'tab-specials',
          label: '',
          url: '',
          hidden: true
        },
        {
          id: 'tab-races',
          label: '',
          url: '',
          hidden: false
        },
        {
          id: 'tab-featured',
          label: '',
          url: ''
        }
      ]);
    });

    it('greyhound: should call filterTabs and should return array without hidden tabs', () => {
      const name = 'greyhound';
      const isSpecialsPresent = true;
      const isNextRacesEnabled = true;
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      const actualResult = service.filterTabs(tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(actualResult).toEqual([
        {
          id: 'tab-specials',
          label: '',
          url: '',
          hidden: false
        },
        {
          id: 'tab-races',
          label: '',
          url: '',
          hidden: false
        },
        {
          id: 'tab-featured',
          label: '',
          url: ''
        }
      ]);
    });

    it('should not call filterTabs', () => {
      const name = 'notracingpage';
      const isSpecialsPresent = false;
      const isNextRacesEnabled = false;
      service.filterTabs = jasmine.createSpy().and.callThrough();
      service.configureTabs(name, tabsMock, isSpecialsPresent, isNextRacesEnabled);
      expect(service.filterTabs).not.toHaveBeenCalled();
    });
  });

  describe('todayEventsByClasses', () => {
    it('should not call filterTabs', () => {
      spyOn(service, 'getConfig').and.returnValue(Object.assign(requestParams, { request: { date: 'featured'} } ));
      eventFactory.eventsByClasses.and.returnValue(Promise.resolve([{ id: 1 }] ));

      service.todayEventsByClasses(false).then(res => {
        expect(res).toEqual( { events: [{ id: 1, lpAvailable: false, persistentInCache: true }] } );
      });
    });

    it('should not call filterTabs', () => {
      spyOn(service, 'getConfig').and.returnValue(Object.assign(requestParams, { request: { date: 'today'} } ));
      eventFactory.eventsByClasses.and.returnValue(Promise.resolve([{ id: 1 }] ));

      service.todayEventsByClasses(false).then(res => {
        expect(eventFactory.eventsByClasses).toHaveBeenCalledWith({
          date: 'today'
        });
        expect(res).toEqual( { events: [{ id: 1, lpAvailable: false, persistentInCache: true }] } );
      });
    });

    it('should not call filterTabs', () => {
      spyOn(service, 'getConfig').and.returnValue(Object.assign(requestParams, { request: { date: 'tomorrow'} } ));
      eventFactory.eventsByClasses.and.returnValue(Promise.resolve([{ id: 1 }] ));

      service.todayEventsByClasses(false).then(res => {
        expect(res).toEqual( { events: [{ id: 1, lpAvailable: false }] } );
      });
    });

    it('should return promise resolve', fakeAsync(() => {
      spyOn(service, 'getConfig').and.returnValue(Object.assign(requestParams, { request: { date: 'tomorrow'} } ));
      spyOn(service, 'arrangeEvents').and.callFake((p1, p2, p3) => {
        return  Promise.resolve( { events: { isStarted: true} } );
      });
      cmsService.getSystemConfig.and.returnValue(of(systemConfig));
      spyOn(ukToteService, 'addAvailablePoolTypes');
      eventFactory.eventsByClasses.and.returnValue(Promise.resolve([{ id: 1 }] ));

      const result = service.todayEventsByClasses(true);
      tick();
      result.then(res => {
        expect(res).toEqual({events: [true]});
        expect(cmsService.getSystemConfig).toHaveBeenCalledWith(false);
        expect(ukToteService.addAvailablePoolTypes).not.toHaveBeenCalled();
      });
    }));

    it('should return error', fakeAsync(() => {
      const config = Object.assign({ TotePools: { Enable_UK_Totepools: false } }, systemConfig);
      cmsService.getSystemConfig.and.returnValue(of(config));
      spyOn(ukToteService, 'addAvailablePoolTypes');
      spyOn(service, 'getConfig').and.returnValue(Object.assign(requestParams, { request: { date: 'tomorrow'} } ));
      spyOn(service, 'arrangeEvents').and.callFake((p1, p2, p3) => {
        return  Promise.reject('error');
      });
      eventFactory.eventsByClasses.and.returnValue(Promise.resolve([{ id: 1 }] ));

      service.todayEventsByClasses(true).catch((err) => {
        expect(err).toEqual('error');
        expect(ukToteService.addAvailablePoolTypes).not.toHaveBeenCalled();
      });
      tick();
    }));

    it('should return promise reject', fakeAsync(() => {
      const config = Object.assign({ TotePools: { Enable_UK_Totepools: true } }, systemConfig);
      cmsService.getSystemConfig.and.returnValue(of(config));
      spyOn(service, 'getConfig').and.returnValue(Object.assign(requestParams, { request: { date: 'tomorrow'} } ));
      spyOn(service, 'arrangeEvents').and.callFake((p1, p2, p3) => {
        return  Promise.reject('error');
      });
      spyOn(ukToteService, 'addAvailablePoolTypes').and.returnValue(Promise.resolve([]));
      eventFactory.eventsByClasses.and.returnValue(Promise.resolve([{ id: 1 }] ));
      service.todayEventsByClasses(true).catch((err) => {
        expect(err).toEqual('error');
        expect(ukToteService.addAvailablePoolTypes).toHaveBeenCalledWith([ { id: 1, lpAvailable: false } ]);
      });
      tick();
    }));
  });

  xdescribe('sortRacingMarketsByTabs', () => {
    it('should set path and label to the market', () => {
      const markets = [
        {
          templateMarketName: 'Win or Each Way',
          eventId: '12135493'
        }
      ];
      const eventId = '12135493';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].path).toEqual('win-or-each-way');
      expect(actualResult[0].label).toEqual('Win or Each Way');
      expect(routingHelperservice.encodeUrlPart).not.toHaveBeenCalled();
    });

    it('should not add market with incorrect eventId', () => {
      const markets = [
        {
          templateMarketName: 'Top 3 Finish',
          eventId: '12135493'
        },
        {
          templateMarketName: 'Win or Each Way',
          eventId: '12135494'
        }
      ];
      const eventId = '12135494';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].label).not.toEqual('Top 3 Finish');
      expect(actualResult[0].label).toEqual('Win or Each Way');
    });

    it('should group To Finish markets', () => {
      const markets = [
        {
          templateMarketName: 'Top 3 Finish',
          eventId: '12135493'
        },
        {
          templateMarketName: 'Top 2 Finish',
          eventId: '12135493'
        }
      ];
      const eventId = '12135493';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].markets[0].templateMarketName).toEqual('Top 3 Finish');
      expect(actualResult[0].markets[1].templateMarketName).toEqual('Top 2 Finish');
      expect(actualResult[0].markets[0].isTopFinish).toEqual(true);
    });

    it('should group To Finish markets and set isToFinish flag', () => {
      const markets = [
        {
          templateMarketName: 'Win or Each Way',
          eventId: '12135493'
        },
        {
          templateMarketName: 'To Finish Fourth',
          eventId: '12135493'
        }
      ];
      const eventId = '12135493';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[1].markets[0].templateMarketName).toEqual('To Finish Fourth');
      expect(actualResult[1].markets[0].isToFinish).toEqual(true);
    });

    it('should group insurance Markets', () => {
      const markets = [
        {
          templateMarketName: 'Insurance 2 Places',
          eventId: '12135493'
        },
        {
          templateMarketName: 'Insurance 3 Places',
          eventId: '12135493'
        }
      ];
      const eventId = '12135493';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].markets[0].templateMarketName).toEqual('Insurance 2 Places');
      expect(actualResult[0].markets[1].insuranceMarkets).toEqual(true);
    });

    it('should group Betting Without Markets', () => {
      const markets = [
        {
          templateMarketName: 'Betting Without',
          eventId: '12135493'
        },
        {
          templateMarketName: 'Insurance 3 Places',
          eventId: '12135493'
        }
      ];
      const eventId = '12135493';
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].markets[0].templateMarketName).toEqual('Betting Without');
      expect(actualResult[0].markets[0].isWO).toEqual(true);
    });

    it('should set label and path to not mapped market', () => {
      const eventId = '12135493';
      const markets = [{
        templateMarketName: 'Win/Win',
        name: 'Seven Emirates v Three Coins',
        eventId
      }, {
        templateMarketName: 'Trap Market',
        name: 'Trap Market',
        eventId
      }];
      const actualResult = service.sortRacingMarketsByTabs(markets as IMarket[], eventId);

      expect(actualResult[0].templateMarketName).toEqual('Win/Win');
    });
  });

  describe('isRacingSpecials', () => {
    const eventEntity: ISportEvent = {} as any;
    it('is horseracing specials tab', () => {
      eventEntity.drilldownTagNames = 'EVFLAG_SP';
      const expectedResult = true;
      const actualResult = service.isRacingSpecials(eventEntity);

      expect(actualResult).toEqual(expectedResult);
    });
    it('is greyhoundracing specials tab', () => {
      eventEntity.typeFlagCodes = 'SP';
      const expectedResult = true;
      const actualResult = service.isRacingSpecials(eventEntity);

      expect(actualResult).toEqual(expectedResult);
    });
    it('is not racing specials tab', () => {
      eventEntity.typeFlagCodes = 'typeFlagCodes';
      eventEntity.drilldownTagNames = 'drilldownTagNames';
      const expectedResult = false;
      const actualResult = service.isRacingSpecials(eventEntity);

      expect(actualResult).toEqual(expectedResult);
    });
  });

  it('@isRaceOff', () => {
    const ev = {
      isResulted: true,
      isLiveNowEvent: true,
      isStarted: false
    } as any;
    expect(service.isRaceOff(ev)).toBe(false);

    ev.isResulted = false;
    expect(service.isRaceOff(ev)).toBe(false);

    ev.isLiveNowEvent = false;
    expect(service.isRaceOff(ev)).toBe(false);

    ev.isStarted = true;
    expect(service.isRaceOff(ev)).toBe(true);
  });

  it('should sort races group based on displayOrder (Active Events)', () => {
    spyOn(service as any, 'isTimeWithinRange').and.returnValue(true);
    const eventsData = {
      groupedRacing: [
        {
          'flag': 'FR',
          'data': [
            {
              startTime: new Date().getTime() + (11 * 60 * 1000),
            }, {
              startTime: new Date().getTime() + (12 * 60 * 1000)
            }
          ]
        }, {
          'flag': 'ZA',
          'data': [
            {
              startTime: 1593009900000
            }, {
              startTime: 1593012000000
            }
          ]
        },{
          'flag': 'US',
          'data': [
            {
              startTime: new Date().getTime() + (11 * 60 * 1000),
            }, {
              startTime: new Date().getTime() + (12 * 60 * 1000)
            }
          ]
        }
      ],
      selectedTab: 'featured'
    } as any;
    const response = service.sortRaceGroup(eventsData, null);
    expect(response.groupedRacing[0].flag).toBe('ZA');
  });

  it('should sort races group based on displayOrder (No Active Events)', () => {
    spyOn(service as any, 'isTimeWithinRange').and.returnValue(true);
    const eventsData = {
      groupedRacing: [
        {
          'flag': 'FR',
          'data': [
            {
              startTime: new Date().getTime() + 10 * 60 * 1000
            }, {
              startTime: new Date().getTime() + 13 * 60 * 1000
            }, {
              startTime: new Date().getTime() + 13 * 60 * 1000
            }, {
              startTime: new Date().getTime() + 12 * 60 * 1000
            }
          ]
        }, {
          'flag': 'ZA',
          'data': [
            {
              startTime: new Date().getTime() + 12 * 60 * 1000
            }, {
              startTime: new Date().getTime() + 13 * 60 * 1000
            }
          ]
        }
      ]
    } as any;
    const response = service.sortRaceGroup(eventsData, null);
    expect(response.groupedRacing[0].flag).toBe('FR');
  });

  it('should sort based on displayOrder', () => {
    const eventsData = [
      {
        flag: 'FR',
        displayOrder: 3
      }, {
        flag: 'ZA',
        displayOrder: 4
      }, {
        flag: 'UK',
        displayOrder: 4
      }, {
        flag: 'AU',
        displayOrder: 2
      }
    ] as any;
    const response = service['sortCountries'](eventsData);
    expect(response[0].flag).toBe('AU');
  });

  describe('getFirstActiveEventFromGroup', () => {
    it('should not return active event if one conditions satisfies (false|true)', () => {
      const racingEvents = [{
        startTime: 1550837769000
      }] as any;
      const race = service.getFirstActiveEventFromGroup(racingEvents, 'UK');
      expect(race).not.toBeNull();
    });
    it('should not return active event if one conditions satisfies (false|true)', () => {
      const racingEvents = [{
        startTime: 1550837769000,
        isFinished: true
      }] as any;
      const race = service.getFirstActiveEventFromGroup(racingEvents, 'UK');
      expect(race).toBeNull();
    });
    it('should not return active event if one conditions satisfies (true|false)', () => {
      const racingEvents = [{
        startTime: new Date().getTime() + (15 * 60 * 1000)
      }] as any;
      const race = service.getFirstActiveEventFromGroup(racingEvents, 'UK');
      expect(race).toBeNull();
    });
    it('should not return active event if one conditions satisfies (true|false) and suspended', () => {
      const racingEvents = [{
        startTime: new Date().getTime() + (15 * 60 * 1000),
        eventStatusCode: 'S'
      }] as any;
      const race = service.getFirstActiveEventFromGroup(racingEvents, 'VR');
      expect(race).toBeNull();
    });
    it('should not return active event if both conditions does not satisfy', () => {
      const racingEvents = [{
        startTime: new Date().getTime() + (15 * 60 * 1000),
        isFinished: true
      }] as any;
      const race = service.getFirstActiveEventFromGroup(racingEvents, 'UK');
      expect(race).toBeNull();
    });
    it('should not return active event if both conditions does not satisfy(Suspende Event"', () => {
      const racingEvents = [{
        startTime: new Date().getTime() + (15 * 60 * 1000),
        isFinished: true,
        eventStatusCode: 'S'
      }] as any;
      const race = service.getFirstActiveEventFromGroup(racingEvents, 'UK');
      expect(race).toBeNull();
    });
    it('should return active event if both conditions  satisfy and is US', () => {
      const racingEvents = [{
        startTime: 1550837769000,
        eventStatusCode: 'A'
      }] as any;
      const race = service.getFirstActiveEventFromGroup(racingEvents, 'US');
      expect(race).not.toBeNull();
    });
  });

  describe('isActiveGroup', () => {
    it('should find unfinished race based on currentday', () => {
      const racingEvents = [{
        startTime: 1550837769000,
        correctedDay: 'racing.dayWednesday',
        eventStatusCode: 'A'
      }] as any;
      const race = service['isActiveGroup'](racingEvents, 'racing.dayWednesday', 'UK');
      expect(race).not.toBeNull();
    });
    it('should find unfinished race based when currentday is not provided', () => {
      const racingEvents = [{
        startTime: 1550837769000,
        eventStatusCode: 'A'
      }] as any;
      const race = service['isActiveGroup'](racingEvents, null);
      expect(race).not.toBeNull();
    });
    it('should find unfinished race when isStarted is true', () => {
      const racingEvents = [{
        startTime: 1550837769000,
        eventStatusCode: 'A',
        isStarted: true
      }] as any;
      const race = service['isActiveGroup'](racingEvents, null);
      expect(race).not.toBeNull();
    });

    it('isRacingSuspended - method to be called when event is active', () => {
      service.isRacingSuspended = jasmine.createSpy('service.isRacingSuspended');
      const racingEvents = [{
        startTime: 1550837769000,
        eventStatusCode: 'A',
        isFinished: true
      }] as any;
      const race = service['isActiveGroup'](racingEvents, null);
      expect(race).not.toBeNull();
      expect(service.isRacingSuspended).toHaveBeenCalled();
    });

    it('isRacingSuspended when there is no isFinished', () => {
      const racingGroup = {
        eventStatusCode: 'S'
      } as any;
      const res = service.isRacingSuspended(racingGroup);
      expect(res).toBe(true);
    });

    it('isRacingSuspended when isFinished is true', () => {
      const racingGroup = [{
        eventStatusCode: 'S',
        isFinished: true
      }] as any;
      const res = service.isRacingSuspended(racingGroup);
      expect(res).toBe(false);
    });

    it('isRacingSuspended When isFinished is false scenario', () => {
      const racingGroup = [{
        isFinished: false,
        eventStatusCode: 'P'
      }] as any;
      const res = service.isRacingSuspended(racingGroup);
      expect(res).toBe(false);
    });
});

  describe('#validateRacesForToday', () => {
    it('should return first switcher if there are no resulted races', () => {
      const racingGroup = [{
        correctedDayValue: 'racing.tomorrow'
      }, {
        correctedDayValue: 'racing.tomorrow'
      }, {
        correctedDayValue: 'racing.tomorrow'
      }] as any;
      const switchers = [{
        viewByFilters: 'racing.tomorrow',
      }] as any;
      const filter = service.validateRacesForToday(racingGroup, 'racing.today', switchers);
      expect(filter).toBe('racing.today');
    });
    it('should return existing filter if there are no resulted races', () => {
      const racingGroup = [{
        correctedDayValue: 'racing.today'
      }, {
        correctedDayValue: 'racing.today'
      }, {
        correctedDayValue: 'racing.today'
      }] as any;
      const switchers = [{
        viewByFilters: 'racing.today',
      }] as any;
      const filter = service.validateRacesForToday(racingGroup, 'racing.today', switchers);
      expect(filter).toBe('racing.today');
    });
    it('should return tommorrow filter if all today races are resulted', () => {
      const racingGroup = [{
        isResulted: true,
        correctedDayValue: 'racing.today'
      }, {
        correctedDayValue: 'racing.today',
        isResulted: true,
      }, {
        correctedDayValue: 'racing.tomorrow'
      }] as any;
      const switchers = [{
        viewByFilters: 'racing.today',
      },{
        viewByFilters: 'racing.tomorrow',
      }] as any;
      const filter = service.validateRacesForToday(racingGroup, 'racing.today', switchers);
      expect(filter).toBe('racing.tomorrow');
    });
  });

  it('should return false if current time is not within time range', () => {
    spyOn(service as any, 'validateTimeRange').and.returnValue(false);
    const response = service['isTimeWithinRange'](new Date().getTime());
    expect(response).toBe(false);
  });

  it('should return false if current time is not within time range', () => {
    spyOn(service as any, 'validateTimeRange').and.returnValue(true);
    const response = service['isTimeWithinRange'](new Date().getTime());
    expect(response).toBe(true);
  });

  describe('#validateTimeRange', () => {
    it('should return false if current time is not within time range', () => {
      const response = service['validateTimeRange'](7, 6, 18);
      expect(response).toBe(false);
    });
    it('should return true if current time satisfies first condition', () => {
      const response = service['validateTimeRange'](5, 6, 18);
      expect(response).toBe(true);
    });
    it('should return true if current time satisfies first condition', () => {
      const response = service['validateTimeRange'](19, 6, 18);
      expect(response).toBe(true);
    });
  });

  describe('#getSortingFromCms', () => {
    const EDP_MARKETS = [
      {
          'name': 'Win or Each Way',
          'brand': 'ladbrokes',
          'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
          'birDescription' : 'this BIR description',
          'isHR': true,
          'isGH': true,
          'isNew': false
      },
      {
          'name': 'Tricast',
          'brand': 'ladbrokes',
          'description': 'S2: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
          'isHR': false,
          'isGH': true,
          'isNew': true
      }
    ] as any;
    const collections = [{
      name: 'Forecast',
      label: 'Forecast'
    },
    {
      name: 'Tricast',
      label: 'Tricast'
    },
    {
      name: '',
      label: 'Win or Each Way'
    }] as any;
    it('should sort as per racing edp markets', () => {
      const sortedMarkets = service.getSortingFromCms(collections, EDP_MARKETS, false);
      expect(sortedMarkets).not.toBeNull();
    });
    it('should not return sorted markets if there are no racing edp markets in cms', () => {
      const sortedMarkets = service.getSortingFromCms(collections, [], false);
      expect(sortedMarkets).not.toBeNull();
    });
    it('should return sorted markets if EDP_Markets.length > collections.length', () => {
      const extraMarkets = [{
        'name': 'Forecast',
        'brand': 'ladbrokes',
        'description': 'S2: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
        'isHR': false,
        'isGH': true,
        'isNew': true
      },
      {
          'name': 'Win Only',
          'brand': 'ladbrokes',
          'description': 'S2: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
          'isHR': false,
          'isGH': true,
          'isNew': true
      }];
      EDP_MARKETS.push(...extraMarkets);
      const sortedMarkets = service.getSortingFromCms(collections, EDP_MARKETS, true);
      expect(sortedMarkets).not.toBeNull();
    });
    it('should get the cms system-config data and assign the HorseRacingBIR.marketsEnabled to birMarketsEnabled', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        HorseRacingBIR: {
          marketsEnabled: ['Win or Each Way']
        }
      }));
      service.getSortingFromCms(collections, EDP_MARKETS, true);
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(service['birMarketsEnabled']).toEqual(['Win or Each Way']);
    });
    it('should get the cms system-config data and not assign the HorseRacingBIR.marketsEnabled to birMarketsEnabled if system config is null', () => {
      cmsService.getSystemConfig.and.returnValue(of(null));
      service.getSortingFromCms(collections, EDP_MARKETS, true);
      expect(service['birMarketsEnabled']).toBeUndefined();
    });
    it('should get the cms system-config data and not assign the HorseRacingBIR.marketsEnabled to birMarketsEnabled if null', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        HorseRacingBIR: {}
      }));
      service.getSortingFromCms(collections, EDP_MARKETS, true);
      expect(service['birMarketsEnabled']).toBeUndefined();
    });
    it('should return sorted markets if EDP_Markets.length > collections.length', () => {
      const extraMarkets = [{
        'name': 'Forecast',
        'brand': 'ladbrokes',
        'description': 'S2: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
        'isHR': false,
        'isGH': true,
        'isNew': true
      },
      {
        'name': 'Win Only',
        'brand': 'ladbrokes',
        'description': 'S2: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
        'birDescription': 'this is Birdesc',
        'isHR': false,
        'isGH': true,
        'isNew': true
      }];
      EDP_MARKETS.push(...extraMarkets);
      const sortedMarkets = service.getSortingFromCms(collections, EDP_MARKETS, true);
      expect(sortedMarkets).not.toBeNull();
    });
    it('birdescription should be null if not available in edp markets', () => {
      const EDP_MARKETS = [
        {
          'name': 'Win or Each Way',
          'brand': 'ladbrokes',
          'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
          'birDescription': null,
          'isHR': true,
          'isGH': true,
          'isNew': false
        }
      ] as any;
      const collections = [
        {
          name: '',
          label: 'Win or Each Way'
        }] as any;
      filtersService.orderBy.and.returnValue([{
        'name': 'Win or Each Way',
        'brand': 'ladbrokes',
        'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
        'birDescription': null,
        'isHR': true,
        'isGH': true,
        'isNew': false
      }])
      const sortedMarkets = service.getSortingFromCms(collections, EDP_MARKETS, false);
      expect(sortedMarkets[0].birDescription).toBeNull();
    });
    it('birdescription should be null if birmarkets is undefined in edp markets', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        HorseRacingBIR: {}
      }));
      const EDP_MARKETS = [
        {
          'name': 'Win or Each Way',
          'brand': 'ladbrokes',
          'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
          'birDescription': 'this is bir desc',
          'isHR': true,
          'isGH': true,
          'isNew': false
        }
      ] as any;
      const collections = [
        {
          name: '',
          label: 'Win or Each Way'
        }] as any;
      filtersService.orderBy.and.returnValue([{
        'name': 'Win or Each Way',
        'brand': 'ladbrokes',
        'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
        'birDescription': null,
        'isHR': true,
        'isGH': true,
        'isNew': false
      }]);
      const sortedMarkets = service.getSortingFromCms(collections, EDP_MARKETS, false);
      expect(sortedMarkets[0].birDescription).toBeNull();
    });
    it('birdescription should be null if birmarkets is defined in edp markets but market is not available', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        HorseRacingBIR: {
          marketsEnabled: ['Win only']
        }
      }));
      const EDP_MARKETS = [
        {
          'name': 'Win or Each Way',
          'brand': 'ladbrokes',
          'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
          'birDescription': 'this is bir desc',
          'isHR': true,
          'isGH': true,
          'isNew': false
        }
      ] as any;
      const collections = [
        {
          name: '',
          label: 'Win or Each Way'
        }] as any;
      filtersService.orderBy.and.returnValue([{
        'name': 'Win or Each Way',
        'brand': 'ladbrokes',
        'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
        'birDescription': null,
        'isHR': true,
        'isGH': true,
        'isNew': false
      }]);
      const sortedMarkets = service.getSortingFromCms(collections, EDP_MARKETS, false);
      expect(sortedMarkets[0].birDescription).toBeNull();
    });
    it('birdescription should be equal string from cms in edp markets', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        HorseRacingBIR: {
          marketsEnabled: ['Win or Each Way']
        }
      }));
      const EDP_MARKETS = [
        {
          'name': 'Win or Each Way',
          'brand': 'ladbrokes',
          'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
          'birDescription': 'this is bir desc',
          'isHR': true,
          'isGH': true,
          'isNew': false
        }
      ] as any;
      const collections = [
        {
          name: '',
          label: 'Win or Each Way'
        }] as any;
      filtersService.orderBy.and.returnValue([{
        'name': 'Win or Each Way',
        'brand': 'ladbrokes',
        'description': 'S1: Pick the finishing order of the first two runnersPick the finishing order of the first two runners',
        'birDescription': 'this is bir desc',
        'isHR': true,
        'isGH': true,
        'isNew': false
      }])
      const sortedMarkets = service.getSortingFromCms(collections, EDP_MARKETS, false);
      expect(sortedMarkets[0].birDescription).toEqual('this is bir desc');
    });
  });

  it('@getFeatured', fakeAsync(() => {
    service['getFeatured'](true).then((data) => {
      expect(data).toBeDefined();
    });
    tick();
  }));

  describe('#isToteForecastTricast', () => {
    it('should return true if Forecast', () => {
      localeService.getString = jasmine.createSpy('getString').and.returnValue('Forecast');
      const response = service['isToteForecastTricasMarket']('Forecast');
      expect(response).toBe(true);
    });
    it('should return true if tricast', () => {
      localeService.getString = jasmine.createSpy('getString').and.returnValue('Tricast');
      const response = service['isToteForecastTricasMarket']('Tricast');
      expect(response).toBe(true);
    });
    it('should return true if Totepool', () => {
      localeService.getString = jasmine.createSpy('getString').and.returnValue('Totepool');
      const response = service['isToteForecastTricasMarket']('Totepool');
      expect(response).toBe(true);
    });
    it('should return false if win only', () => {
      localeService.getString = jasmine.createSpy('getString').and.returnValue('Totepool');
      const response = service['isToteForecastTricasMarket']('win only');
      expect(response).toBe(false);
    });
  });

  describe('#filterRacingGroup', () => {
    it('should return unchanged racing, if racing is null', () => {
      expect(service.filterRacingGroup(null)).toBe(null);
    });
    it('should return unchanged racing, if racing is empty', () => {
      expect(service.filterRacingGroup([]).length).toBe(0);
    });
    it('should return racing, if racing is not empty', () => {
      const today = new Date();
      const request = [{
       startTime: today.setDate(today.getDate() - 2)
      },{
        startTime: today.setDate(today.getDate() + 2)
      },{
       startTime: today
      }] as any;
      expect(service.filterRacingGroup(request).length).toBeDefined();
   });
  });
  it('should call getNextRacesData', () => {
    const filterAccess = { 
    "UK&IRE": true,
    INT: true, 
    VR: true,
    FR: true,
    AE : true,
    ZA : true,
    IN : true,
    US : true,
    AU : true,
    CL : true
  };
    spyOn(service, 'getConfig').and.returnValue({request:{typeFlagCodes: 'UK,IE,FR,AE,ZA,IN,US,AU,CL,INT,VR',
    groupByFlagCodesSortOrder: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
  }});
    nextRacesModule.storedEvents.push({
      "id": 240780807,
      "name": "Neighmarket",
      "eventStatusCode": "A",
      "isActive": "true",
      "isDisplayed": "true",
      "displayOrder": 32,
      "siteChannels": "@,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,e,f,p,t,y,z,",
      "eventSortCode": "MTCH",
      "startTime": 1688845020000,
      "rawIsOffCode": "-",
      "classId": 36043,
      "typeId": 126242,
      "sportId": "39",
      "liveServChannels": "sEVENT0240780800,",
      "liveServChildrenChannels": "SEVENT0240780800,",
      "categoryId": "39",
      "categoryCode": "France",
      "categoryName": "France Sports",
      "categoryDisplayOrder": "369",
      "className": "France Horse Racing 2 (PT)",
      "classDisplayOrder": 0,
      "classSortCode": "FR",
      "typeName": "Playford Park 2",
      "typeDisplayOrder": 0,
      "typeFlagCodes": "FR,",
      "isOpenEvent": "true",
      "isNext1HourEvent": "true",
      "isNext3HourEvent": "true",
      "isNext6HourEvent": "true",
      "isNext12HourEvent": "true",
      "isNext24HourEvent": "true",
      "isNext2DayEvent": "true",
      "isNext1WeekEvent": "true",
      "isAvailable": "true",
      "cashoutAvail": "N",
      "raceLength": "14.050",
      "raceLengthUnit": "FR",
      "responseCreationTime": "2023-07-08T19:35:36.151Z",
      "localTime": "20:37",
      "originalName": "20:37 Neighmarket",
      "isUS": false,
      "markets": [],
      "correctedDay": "sb.daySaturday",
      "correctedDayValue": "sb.today",
      "liveEventOrder": 1
  });
    const data = service.getNextRacesData(filterAccess, nextRacesModule);
    expect(data.groupedRacing.length).toBe(4);
 });

 it('should call getNextRacesData when flag not available', () => {
  const filterAccess = { 
  VRR: true, 
};
  spyOn(service, 'getConfig').and.returnValue({request:{typeFlagCodes: 'UK,IE,FR,AE,ZA,IN,US,AU,CL,INT,VR',
  groupByFlagCodesSortOrder: ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'],
}});
  const data = service.getNextRacesData(filterAccess,nextRacesModule);
  expect(data.groupedRacing.length).toBe(3);
});
});
