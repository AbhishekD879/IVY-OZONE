
import { OlympicsService } from './olympics.service';
import { of as observableOf } from 'rxjs';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { ISportCMSConfig, ISportConfig } from '@app/olympics/models/olympics.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { fakeAsync, tick } from '@angular/core/testing';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';

describe('OlympicsService', () => {
  let timeService,
    templateService,
    cacheEventsService,
    simpleFiltersService,
    siteServerRequestHelperService,
    loadByPortionsService,
    buildUtilityService,
    liveStreamService,
    gamingService,
    service;

  let sportCMSConfig: ISportCMSConfig;
  const routingState = {};
  const cmsService = {} as any,
    sportsConfigHelperService = new SportsConfigHelperService(cmsService as any),
    coreToolsService = new CoreToolsService(),
    routingHelperService = new RoutingHelperService(sportsConfigHelperService as any, routingState as any);

  beforeEach(() => {
    timeService = {
      apiDataCacheInterval: {}
    };
    templateService = {
      filterBetInRunMarkets: jasmine.createSpy().and.returnValue([]),
      filterMultiplesEvents: jasmine.createSpy().and.returnValue([])
    };
    cacheEventsService = {
      storedData: {},
      stored: jasmine.createSpy(),
      store: jasmine.createSpy(),
      async: jasmine.createSpy()
    };
    simpleFiltersService = {
      getFilterParams: jasmine.createSpy()
    };
    siteServerRequestHelperService = {
      getOutrightsByTypeIds: jasmine.createSpy().and.returnValue(observableOf([]).toPromise()),
      getMarketsCountByEventsIds: jasmine.createSpy().and.returnValue(observableOf([]).toPromise())
    };
    loadByPortionsService = {
      get: jasmine.createSpy().and.callFake((fn: Function) => observableOf(fn()).toPromise())
    };
    buildUtilityService = {
      buildEventsWithOutMarketCounts: jasmine.createSpy().and.returnValue([]),
      buildEventsWithMarketCounts: jasmine.createSpy().and.returnValue([])
    };
    liveStreamService = {
      addLiveStreamAvailability: jasmine.createSpy().and.returnValue(() => [])
    };
    gamingService = {
      getConfig: jasmine.createSpy().and.returnValue({}),
      setConfig: jasmine.createSpy().and.returnValue({})
    };

    service = new OlympicsService(
      timeService,
      templateService,
      cacheEventsService,
      simpleFiltersService,
      coreToolsService,
      siteServerRequestHelperService,
      loadByPortionsService,
      buildUtilityService,
      liveStreamService,
      gamingService,
      cmsService,
      sportsConfigHelperService,
      routingHelperService
    );

    sportCMSConfig = {
      sport: 'football',
      dispSortName: ['sort'],
      primaryMarkets: 'markets',
      targetUri: 'football',
      categoryId: '1',
      viewByFilters: ['filters'],
      typeIds: [1],
      imageTitle: 'imageTitle',
      tabs: {
        ['tab-live']: { tablabel: '', visible: true },
        ['tab-matches']: { tablabel: '', visible: true },
        ['tab-outrights']: { tablabel: '', visible: true },
        ['tab-specials']: { tablabel: '', visible: false }
      } as any
    } as any;
  });

  describe('conctructor', () => {
    it('should create service instance', () => {
      expect(service instanceof OlympicsService).toBeTruthy();
      expect(service.extensionName).toEqual('olympics');
    });
  });

  describe('config property', () => {
    it('should return gamingService.getConfig()', () => {
      const conf = service.config;
      expect(gamingService.getConfig).toHaveBeenCalled();
      expect(conf).toBeTruthy();
    });
  });

  describe('getCMSConfig', () => {
    let data: ISportCMSConfig[];

    beforeEach(() => {
      data = [
        { categoryId: '1', targetUriCopy: 'football', defaultTab: 'matches' },
        { categoryId: '2', targetUriCopy: 'tennis', defaultTab: 'matches', sport: 'tennis' },
        { categoryId: '3', targetUriCopy: 'dummy', defaultTab: 'matches', disabled: true },
        { categoryId: '4', imageTitle: 'Basketball', defaultTab: 'matches' }
      ] as ISportCMSConfig[];
      cmsService.getSports = jasmine.createSpy().and.returnValue(observableOf(data));
    });

    it('should return config data', () => {
      service.getCMSConfig().subscribe((config: ISportCMSConfig[]) => {
        expect(config.length).toEqual(3);
      });
    });

    it('should return config data #1', () => {
      service.getCMSConfig().subscribe((config: ISportCMSConfig[]) => {
        expect(config[0].sport).toEqual('football');
        expect(config[0].targetUri).toEqual('/olympics/football/matches/today');
      });
    });

    it('should return config data #2', () => {
      service.getCMSConfig().subscribe((config: ISportCMSConfig[]) => {
        expect(config[1].sport).toEqual('tennis');
        expect(config[1].targetUri).toBeUndefined();
      });
    });

    it('should return config data #3', () => {
      service.getCMSConfig().subscribe((config: ISportCMSConfig[]) => {
        expect(config[2].sport).toEqual('basketball');
      });
    });
  });

  describe('generateCommonSportConfig', () => {
    it('should return ISportConfig data #1', () => {
      const data: ISportConfig = service.generateCommonSportConfig(sportCMSConfig);
      expect(data.config.extension).toEqual(service.extensionName);
      expect(data.tabs).toBeTruthy();
    });

    it('should return ISportConfig data #2', () => {
      spyOn(service, 'isVisible').and.returnValue(true);
      const data: ISportConfig = service.generateCommonSportConfig(sportCMSConfig);
      expect(data.config.extension).toEqual(service.extensionName);
      expect(data.tabs).toBeTruthy();
    });
  });

  describe('generateOutrightSportConfig', () => {
    it('should generate ISportConfig object', () => {
      const data = service.generateOutrightSportConfig(sportCMSConfig);
      expect(data).toBeTruthy();
    });
  });

  describe('generatePreMatchSportConfig', () => {
    it('should generate ISportConfig object', () => {
      const data = service.generatePreMatchSportConfig(sportCMSConfig);
      expect(data).toBeTruthy();
      expect(data.config).toBeTruthy();
    });
  });

  describe('getSportsConfigs', () => {
    it('should return ISportBaseConfig object', () => {
      const data = service.getSportsConfigs([sportCMSConfig]);
      expect(data.football.path).toEqual('football');
      expect(data.football.id).toEqual('1');
    });
  });

  describe('generateSportConfig', () => {
    it('should return ISportConfig object by generateOutrightSportConfig()', () => {
      spyOn(service, 'generateOutrightSportConfig').and.callThrough();
      sportCMSConfig.isOutrightSport = true;
      const data = service.generateSportConfig('football', [sportCMSConfig]);
      expect(data).toBeTruthy();
      expect(service.generateOutrightSportConfig).toHaveBeenCalled();
    });

    it('should return ISportConfig object by generatePreMatchSportConfig()', () => {
      spyOn(service, 'generatePreMatchSportConfig').and.callThrough();
      sportCMSConfig.isOutrightSport = false;
      const data = service.generateSportConfig('football', [sportCMSConfig]);
      expect(data).toBeTruthy();
      expect(service.generatePreMatchSportConfig).toHaveBeenCalled();
    });

    it('should return {} object by generatePreMatchSportConfig()', () => {
      const data = service.generateSportConfig('tennis', [sportCMSConfig]);
      expect(data).toBeUndefined();
    });
  });

  describe('getMenuConfigs', () => {
    it('should return sanitized object', () => {
      const data = service.getMenuConfigs([sportCMSConfig]);
      expect(data[0].sport).toEqual('football');
      expect(data[0].dispSortName).toBeUndefined();
    });
  });

  describe('getCollectionsTabs', () => {
    it('should return ISportEventTab', () => {
      const sportEvent: ISportEvent = {
        id: 123,
        name: 'eventName',
        // markets: [{ name: 'MAIN'}, { name: 'Special' }],
        categoryName: 'football'
      } as ISportEvent;
      const marketsByCollection: ISportEvent[] = [
        { name: 'MAIN', markets: [] },
        { name: 'Special', markets: []}
      ] as ISportEvent[];
      const tabs = service.getCollectionsTabs(marketsByCollection, sportEvent);
      expect(tabs.length).toEqual(2);
      expect(tabs[0].marketName).toEqual('main');
    });
  });

  describe('olympicsService', () => {
    it('should return ISportServiceConfig', () => {
      const data = service.olympicsService({} as ISportConfig);
      expect(data.extension).toEqual(service.extensionName);
      expect(typeof data.outrights).toEqual('function');
      expect(typeof data.specials).toEqual('function');
      expect(typeof data.todayEventsByTypesIds).toEqual('function');
      expect(typeof data.getCollectionsTabs).toEqual('function');
      expect(data.sportConfig).toBeTruthy();
    });
  });

  describe('extendCacheParams', () => {
    it('should extend corresponding services', () => {
      service.extendCacheParams();
      expect(timeService.apiDataCacheInterval[`olympicsEvents`]).toEqual(60000);
      expect(timeService.apiDataCacheInterval[`olympicsCoupons`]).toEqual(5 * 60000);
      expect(cacheEventsService.storedData[`olympicsEvents`]).toEqual({});
      expect(cacheEventsService.storedData[`olympicsCoupons`]).toEqual({});
    });
  });

  describe('specialsByTypesIds', () => {
    it('should return Promise', fakeAsync(() => {
      gamingService.getConfig.and.returnValue({ request: { typeIds: [1] }});
      service.specialsByTypesIds().then(() => {
        expect(siteServerRequestHelperService.getOutrightsByTypeIds).toHaveBeenCalled();
        expect(buildUtilityService.buildEventsWithOutMarketCounts).toHaveBeenCalled();
        expect(liveStreamService.addLiveStreamAvailability).toHaveBeenCalled();
      });
      tick();
    }));

    it('should return Promise<[]>', fakeAsync(() => {
      gamingService.getConfig.and.returnValue({ request: { typeIds: [] }});
      service.specialsByTypesIds().then(data => {
        expect(data).toEqual([]);
      });
      tick();
    }));
  });

  describe('outrightsByTypesIds', () => {
    it('should return Promise', fakeAsync(() => {
      gamingService.getConfig.and.returnValue({ request: { typeIds: [1] }});
      service.outrightsByTypesIds().then(() => {
        expect(siteServerRequestHelperService.getOutrightsByTypeIds).toHaveBeenCalled();
        expect(buildUtilityService.buildEventsWithOutMarketCounts).toHaveBeenCalled();
        expect(liveStreamService.addLiveStreamAvailability).toHaveBeenCalled();
        expect(templateService.filterBetInRunMarkets).toHaveBeenCalled();
        expect(templateService.filterMultiplesEvents).toHaveBeenCalled();
      });
      tick();
    }));

    it('should return Promise<[]>', fakeAsync(() => {
      gamingService.getConfig.and.returnValue({ request: { typeIds: [], outrightsSport: true }});
      service.outrightsByTypesIds().then(data => {
        expect(data).toEqual([]);
      });
      tick();
    }));
  });

  describe('todayEventsByTypesIds', () => {
    it('should return Promise', fakeAsync(() => {
      spyOn(service, 'filterEventsWithPrices').and.callThrough();
      gamingService.getConfig.and.returnValue({ request: { typeIds: [1] }});
      service.todayEventsByTypesIds().then(() => {
        expect(siteServerRequestHelperService.getOutrightsByTypeIds).toHaveBeenCalled();
        expect(buildUtilityService.buildEventsWithMarketCounts).toHaveBeenCalled();
        expect(liveStreamService.addLiveStreamAvailability).toHaveBeenCalled();
        expect(service['filterEventsWithPrices']).toHaveBeenCalled();
      });
      tick();
    }));

    it('should return Promise<[]>', fakeAsync(() => {
      gamingService.getConfig.and.returnValue({ request: { typeIds: [] }});
      service.todayEventsByTypesIds().then(data => {
        expect(data).toEqual([]);
      });
      tick();
    }));
  });

  describe('loadCounts', () => {
    it('should return Promise', fakeAsync(() => {
      gamingService.getConfig.and.returnValue({ request: { typeIds: [1] }});
      const eventEntities = [{ event: { id: '1' }}];
      service['loadCounts'](eventEntities).then(() => {
        expect(loadByPortionsService.get).toHaveBeenCalled();
        expect(siteServerRequestHelperService.getMarketsCountByEventsIds).toHaveBeenCalled();
      });
      tick();
    }));
  });

  describe('cachedEvents', () => {
    it('should return cached function', () => {
      cacheEventsService.stored.and.returnValue(true);
      cacheEventsService.async.and.returnValue(() => 'stored');
      expect(service['cachedEvents'](jasmine.anything)({ date: null, typeIds: []})()).toEqual('stored');
    });
  });

  describe('filterEventsWithPrices', () => {
    it('should filter eventd by market price', () => {
      const events = [
        { markets: [{ outcomes: [{ prices: [ { id: '1' }, { id: '2'}] }]}] },
        { markets: [] }
      ];
      const result = service['filterEventsWithPrices'](events);
      expect(result.length).toEqual(1);
    });
  });

  describe('getDefaultTab', () => {
    it('should return matches/today', () => {
      expect(service['getDefaultTab']('matches')).toEqual('matches/today');
    });

    it('should return default_tab', () => {
      expect(service['getDefaultTab']('default_tab')).toEqual('default_tab');
    });
  });
});
