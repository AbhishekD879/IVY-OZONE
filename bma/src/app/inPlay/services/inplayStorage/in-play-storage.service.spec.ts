import { of as observableOf } from 'rxjs';
import { InPlayStorageService } from './in-play-storage.service';
import { ISportDataStorage } from '@app/inPlay/models/sport-data.model';
import { watchLiveItem } from '@app/inPlay/constants/watch-live-ribbon.constant';
import { fakeAsync, flush } from '@angular/core/testing';

describe('InPlayStorageService', () => {
  let service: InPlayStorageService;
  let windowRefService;
  let pubSubService;
  let wsUpdateEventService;
  let cmsService;
  let routingState;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy()
      }
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      API: {
        EVENT_COUNT_UPDATE: 'EVENT_COUNT_UPDATE'
      }
    };

    wsUpdateEventService = {
      subscribe: jasmine.createSpy()
    };

    routingState = {
      getCurrentUrl: jasmine.createSpy()
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy()
    };

    routingState = {
      getCurrentUrl: jasmine.createSpy().and.returnValue('fakeUrl')
    };

    service = new InPlayStorageService(
      windowRefService,
      pubSubService,
      wsUpdateEventService,
      cmsService,
      routingState
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('isOutDated', () => {
    expect(service.isOutDated(4070901600000, 1000)).toBeFalsy();
    expect(service.isOutDated(946677600000, 2000)).toBeTruthy();
  });

  it('cacheRibbon', () => {
    service.clearLink = jasmine.createSpy().and.returnValue('fake/uri');

    const data: any = {
      items: [{
        targetUri: 'target/uri',
        targetUriCopy: 'target/uri/copy'
      }]
    };

    expect(service.cacheRibbon(data)).toBe(service.ribbonCache);
    expect(service.clearLink).toHaveBeenCalledWith('target/uri');
    expect(service.clearLink).toHaveBeenCalledWith('target/uri/copy');
    expect(data.items[0].targetUri).toBe('fake/uri');
    expect(data.items[0].targetUriCopy).toBe('fake/uri');
    expect(service.ribbonCache.data).toBe(data.items);
    expect(service.ribbonCache.lastUpdated).toEqual(jasmine.any(Number));
  });

  it('onVirtualsUpdate should add virtualsData', () => {
    const data = {} as any;
    service.onVirtualsUpdate(data);
    expect(pubSubService.publish).toHaveBeenCalled();
  });

  describe('#onRibbonUpdate', () => {
    it('onRibbonUpdate should add watchlive item', () => {
      const data: any = {
        items: [{
          targetUri: 'target/uri',
          targetUriCopy: 'target/uri/copy',
          categoryId: 'categoryId'
        }]
      };
      service.isWatchLiveEnabled = true;
      service.clearLink = jasmine.createSpy();
      cmsService.getSystemConfig.and.returnValue(observableOf({ InPlayWatchLive: { enabled: true } }));
      service.onRibbonUpdate(data);
      expect(service.isHomeScreen).toBeFalsy();
      expect(service.clearLink).toHaveBeenCalledTimes(4);
      expect(pubSubService.publish).toHaveBeenCalledWith('EVENT_COUNT_UPDATE', [data.items]);
      expect(service.ribbonCache.data).toBe(data.items);
      expect(service.ribbonCache.lastUpdated).toEqual(jasmine.any(Number));
      expect(data.items.length).toEqual(2);
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    });

    it('onRibbonUpdate should not add watchlive item', () => {
      const data: any = {
        items: [{
          targetUri: 'target/uri',
          targetUriCopy: 'target/uri/copy',
          categoryId: 'categoryId'
        }]
      };
      service.isWatchLiveEnabled = false;
      service.clearLink = jasmine.createSpy().and.returnValue('fake/uri');
      cmsService.getSystemConfig.and.returnValue(observableOf({}));
      service.onRibbonUpdate(data);

      expect(data.items.length).toEqual(1);
    });

    it('updateUniqueTabsData should remove allsports and add watchlive', () => {
      service['routingState'].getCurrentUrl = jasmine.createSpy('getCurrentUrl')
        .and.returnValue('/in-play/watchlive');
      service.isWatchLiveEnabled = true;

      const allSportsTabMock = {
        targetUri: 'in-play/allsports',
        targetUriCopy: 'allsports',
        categoryId: 0,
        liveStreamEventCount: 10,
        upcommingLiveStreamEventCount: 20
      };

      const ribbonDataMock: any = {
        items: [
          allSportsTabMock,
          {
            targetUri: 'in-play/football',
            targetUriCopy: 'football',
            categoryId: 16
          }]
      };

      service.updateUniqueTabsData(ribbonDataMock);

      expect(ribbonDataMock.items[0].categoryId).toEqual(watchLiveItem.categoryId);
      expect(ribbonDataMock.items[0].liveStreamEventCount).toEqual(allSportsTabMock.liveStreamEventCount);
      expect(ribbonDataMock.items[0].upcommingLiveStreamEventCount).toEqual(allSportsTabMock.upcommingLiveStreamEventCount);
    });

    it('updateUniqueTabsData should not remove allsports for Home Inplay Tab', () => {
      service['routingState'].getCurrentUrl = jasmine.createSpy('getCurrentUrl')
        .and.returnValue('/home/in-play');
      const allSportsTabMock = {
        targetUri: 'in-play/allsports',
        targetUriCopy: 'allsports',
        categoryId: 0,
        liveStreamEventCount: 10,
        upcommingLiveStreamEventCount: 20
      };

      const ribbonDataMock: any = {
        items: [
          allSportsTabMock,
          {
            targetUri: 'in-play/football',
            targetUriCopy: 'football',
            categoryId: 16
          }]
      };

      service.updateUniqueTabsData(ribbonDataMock);

      expect(ribbonDataMock.items[0]).toEqual(allSportsTabMock);
    });

    it('updateUniqueTabsData should not update WatchLIve Counters when not on watchlive page', () => {
      service['routingState'].getCurrentUrl = jasmine.createSpy('getCurrentUrl')
        .and.returnValue('/in-play/football');
      service.isWatchLiveEnabled = true;
      watchLiveItem.liveStreamEventCount = null;
      watchLiveItem.upcommingLiveStreamEventCount = null;

      const allSportsTabMock = {
        targetUri: 'in-play/allsports',
        targetUriCopy: 'allsports',
        categoryId: 0,
        liveStreamEventCount: 10,
        upcommingLiveStreamEventCount: 20
      };
      const ribbonDataMock: any = {
        items: [
          allSportsTabMock,
          {
            targetUri: 'in-play/football',
            targetUriCopy: 'football',
            categoryId: 16
          }]
      };

      service.updateUniqueTabsData(ribbonDataMock);

      expect(ribbonDataMock.items[0].categoryId).toEqual(watchLiveItem.categoryId);
      expect(ribbonDataMock.items[0].liveStreamEventCount).toBeNull();
      expect(ribbonDataMock.items[0].upcommingLiveStreamEventCount).toBeNull();
    });
  });

  describe('#onStructureUpdate', () => {
    it('shoud call onStructureUpdate if regular keys present', () => {
      service.structureCache.data = {
        livenow: { eventCount: 1 },
        upcoming: { eventCount: 2 }
      } as any;
      service['updateSportCategories'] = jasmine.createSpy();

      const data: any = {
        livenow: { eventCount: 10 },
        upcoming: { eventCount: 20 }
      } as any;

      service.onStructureUpdate(data);

      expect(service['updateSportCategories']).toHaveBeenCalledWith(
        service.structureCache.data.livenow, data.livenow
      );
      expect(service['updateSportCategories']).toHaveBeenCalledWith(
        service.structureCache.data.upcoming, data.upcoming
      );
    });

    it('shoud not call onStructureUpdate if no liveStream key in incoming data', () => {
      service.structureCache.data = {
        livenow: { eventCount: 1 },
        upcoming: { eventCount: 2 },
        liveStream: { eventCount: 3 },
      } as any;
      service['updateSportCategories'] = jasmine.createSpy();

      const data: any = {
        livenow: { eventCount: 10 },
        upcoming: { eventCount: 20 },
        liveStream: undefined,
      } as any;

      service.onStructureUpdate(data);

      expect(service['updateSportCategories']).not.toHaveBeenCalledWith(
        service.structureCache.data.liveStream, data.liveStream
      );
    });
  });


  it('cacheStructure', () => {
    const data: any = {
      livenow: { eventCount: 10 },
      upcoming: { eventCount: 20 }
    } as any;

    service.cacheStructure(data);

    expect(service.structureCache.data.livenow).toBe(data.livenow);
    expect(service.structureCache.data.upcoming).toBe(data.upcoming);
    expect(service.structureCache.lastUpdated).toEqual(jasmine.any(Number));
  });

  describe('updateStructureCacheSportData', () => {
    let sportData;

    beforeEach(() => {
      sportData = { eventCount: 1 } as any;

      service.structureCache = {
        data: {
          livenow: {
            eventsBySports: [{ categoryId: '13', eventsByTypeName: [] }]
          }
        },
        lastUpdated: null
      } as any;
      jasmine.clock().install();
    });

    function runFunction() {
      service.updateStructureCacheSportData(sportData, 'LIVE_EVENT', '13');
    }

    it(`should update eventsBySports in structureCache`, () => {
      runFunction();

      expect(service.structureCache.data.livenow.eventsBySports[0]).toBe(sportData);
    });

    it(`should set link on sportData to eventsBySports in structureCache`, () => {
      runFunction();

      sportData.eventCount = 123;

      expect(service.structureCache.data.livenow.eventsBySports[0].eventCount).toEqual(123);
    });

    it(`should update lastUpdated in structureCache`, () => {
      const baseTime = new Date(2013, 9, 23);
      jasmine.clock().mockDate(baseTime);

      runFunction();

      expect(service.structureCache.lastUpdated).toEqual(baseTime.getTime());
    });

    it(`should add eventsBySportsCached's property to sportData if sportData do Not have it`, () => {
      service.structureCache.data.livenow.eventsBySports[0].isExpanded = true;

      runFunction();

      expect(sportData.isExpanded).toBeTruthy();
    });

    it(`should Not change sportData's on eventsBySportsCached property if sportData have it`, () => {
      service.structureCache.data.livenow.eventsBySports[0].eventCount = 3;

      runFunction();

      expect(sportData.eventCount).toEqual(1);
    });

    afterEach(() => {
      jasmine.clock().uninstall();
    });
  });

  it('initSportsCache', () => {
    service.timeOuts = 10;
    service.sportDataCache = null;

    service.initSportsCache();

    expect(service.timeOuts).toEqual(jasmine.any(Number));
    expect(service.sportDataCache).toEqual(jasmine.any(Object));
  });

  it('destroySportsCache', () => {
    service.sportDataCache = {};
    service.allEvents = [];
    service.timeOuts = 456;

    windowRefService.nativeWindow.setTimeout = jasmine.createSpy().and.callFake(cb => {
      // Call `setTimeout` callback right away (sync) for testing purpose
      cb();
    });

    service.destroySportsCache();

    expect(service.sportDataCache).toBeUndefined();
    expect(service.allEvents).toBeUndefined();
    expect(service.timeOuts).toBeUndefined();
  });

  it('storeSport', () => {
    const params: any = { topLevelType: 'TLT', categoryId: 'CID' };
    const data: any = {};
    service.storeSportData = jasmine.createSpy();

    service.storeSport(params, data);
    expect(data.eventsByTypeName).toBeDefined();
    expect(service.storeSportData).toHaveBeenCalledWith(data, params.topLevelType, params.categoryId);
  });

  it('getSportCompetition', () => {
    const topLevelType = 'TLP';
    const sportId = 'SID';
    const competitionId = 'CID';

    service.sportDataCache = {
      [topLevelType]: {
        [sportId]: {
          data: {
            eventsByTypeName: [{ typeId: competitionId }]
          }
        }
      }
    } as any;

    expect(service.getSportCompetition(topLevelType, sportId, competitionId)).toBe(
      service.sportDataCache[topLevelType][sportId].data[0]
    );
    expect(service.getSportCompetition(topLevelType, sportId, 'C_ID')).toBeFalsy();
  });

  it('resetCompetitionEvents', () => {
    const topLevelType = 'TPT';
    const sportId = 'SID';
    const competitionId = 'CID';
    const eventsList: any[] = [{ id: 1, categoryId: 'CID2' }];
    const isAggregated: boolean = true;
    spyOn(service, 'addEvents').and.callThrough();
    service.getSportCompetition = jasmine.createSpy().and.returnValue({});

    service.resetCompetitionEvents(topLevelType, sportId, competitionId, isAggregated, eventsList);
    expect(service.getSportCompetition).toHaveBeenCalledWith(topLevelType, sportId, competitionId);
    expect(service.addEvents).toHaveBeenCalledWith(eventsList, isAggregated);
    expect(Object.keys(service.allEvents)).toContain('1');
  });

  it('should handle case when there are no competition to update', () => {
    const topLevelType = 'TPT';
    const sportId = 'SID';
    const competitionId = 'CID2';
    const eventsList: any[] = [{ id: 1, categoryId: 'CID2' }];
    const isAggregated: boolean = true;
    spyOn(service, 'addEvents').and.callThrough();

    service.sportDataCache = {
      TPT: {
        SID: {
          data: {
            eventsByTypeName: [{
              typeId: 'CID1'
            }]
          }
        }
      }
    } as ISportDataStorage;

    service.resetCompetitionEvents(topLevelType, sportId, competitionId, isAggregated, eventsList);
    expect(service.addEvents).toHaveBeenCalledWith(eventsList, isAggregated);
    expect(Object.keys(service.allEvents)).toContain('1');
  });

  describe('addCompetition', () => {
    const topLevelType = 'TLT';
    const sportId = 'SID';
    const competition: any = { events: [{id: 1}], typeId: 'CID' };
    const isAggregated: boolean = true;

    beforeEach(() => {
      service.sportDataCache = {
        [topLevelType]: {
          [sportId]: { data: { eventsByTypeName: [] } }
        }
      } as any;
      service.allEvents = {};
    });

    it('addCompetition', () => {
      competition.events = [{id: 1, markets: []},{id: 2, markets: []}];
      service.allEvents = {2: {markets: []}}
      service.addCompetition(topLevelType, sportId, competition, isAggregated);
      expect(service.sportDataCache[topLevelType][sportId].data.eventsByTypeName[0]).toBe(competition);

      competition.typeName = 'TN';
      service.addCompetition(topLevelType, sportId, competition, isAggregated);
      expect(service.sportDataCache[topLevelType][sportId].data.eventsByTypeName.length).toBe(1);
    });
  });

  describe('removeCompetition', () => {
    const topLevelType = 'TLT';
    const sportId = 'SID';
    const competitionId = 'CID';

    beforeEach(() => {
      service.allEvents = {
        '1': { id: 1, categoryId: 'CID1' }
      };
      service.sportDataCache = {
        [topLevelType]: {
          [sportId]: {
            data: {
              eventsByTypeName: [{
                typeId: competitionId,
                events: [{ id: 1 }]
              }]
            }
          }
        }
      } as any;
    });

    it('should remove Competition', () => {
      service.removeCompetition(topLevelType, sportId, competitionId);

      expect(service.sportDataCache[topLevelType][sportId].data.eventsByTypeName.length).toBe(0);
    });

    describe('no Events in category', () => {
      beforeEach(() => {
        service.sportDataCache = {
          [topLevelType]: {
            [sportId]: {
              data: {
                eventsByTypeName: [{
                  typeId: competitionId
                }]
              }
            }
          }
        } as any;
      });

      it(`should not slice from allEvents if Not event `, () => {
        service.removeEvents = jasmine.createSpy('removeEvents');

        service.removeCompetition(topLevelType, sportId, competitionId);

        expect(service.removeEvents).not.toHaveBeenCalled();
      });
    });
  });

  describe('storeSportData', () => {
    it('storeSportData', fakeAsync(() => {
      spyOn(service, 'updateStructureCacheSportData');

      service.sportDataCache = null;

      const data: any = {};
      const topLevelType = 'TLT';
      const categoryId = 'CID';


      expect(service.storeSportData(data, topLevelType, categoryId)).toBe(data);

      flush();

      expect(service.sportDataCache).toEqual(jasmine.any(Object));
      expect(service.sportDataCache[topLevelType]).toEqual(jasmine.any(Object));
      expect(service.sportDataCache[topLevelType][categoryId]).toEqual({
        data, lastUpdated: jasmine.any(Number)
      });
    }));

    it(`should update 'structureCache`, fakeAsync(() => {
      spyOn(service, 'updateStructureCacheSportData');

      service.storeSportData({ test: { eventsBySports: [] } } as any, 'test', '');

      flush();

      expect(service.updateStructureCacheSportData).toHaveBeenCalled();
    }));
    it('should return undefined for updateStructureCacheSportData', () => {
      service.structureCache = {
        data: {}
      } as any;
      const result = service.updateStructureCacheSportData({ test: { eventsBySports: [] } } as any, 'test', '');
      expect(result).toBeUndefined();
    });
  });

  it('isOutdatedStructure', () => {
    service.isOutDated = jasmine.createSpy();
    service.structureCache.lastUpdated = Date.now();

    service.isOutdatedStructure();
    expect(service.isOutDated).toHaveBeenCalledWith(
      service.structureCache.lastUpdated, service.intervals.structureCache
    );
  });

  it('isOutdatedRibbon', () => {
    service.isOutDated = jasmine.createSpy();
    service.ribbonCache.lastUpdated = Date.now();

    service.isOutdatedRibbon();
    expect(service.isOutDated).toHaveBeenCalledWith(
      service.ribbonCache.lastUpdated, service.intervals.ribbonCache
    );
  });

  it('clearLink', () => {
    expect(service.clearLink('#/sport/football')).toBe('/football');
    expect(service.clearLink('/volleyball')).toBe('/volleyball');
  });

  it('addSportCategories', () => {
    const ids = ['1', '2'];
    const cachedCategories: any[] = [];
    const updateCategories: any[] = [
      { showInPlay: true, categoryId: '1' },
      { showInPlay: false, categoryId: '2' }
    ];

    service['addSportCategories'](ids, cachedCategories, updateCategories);
    expect(cachedCategories[0]).toBe(updateCategories[0]);
  });

  it('removeSportCategories', () => {
    const categories: any[] = [
      { categoryId: '1' }, { categoryId: '2' }, { categoryId: '3' }
    ];
    service['removeSportCategories'](['1', '2'], categories);
    expect(categories.length).toBe(1);
  });

  it('updateSportCategories', () => {
    const cacheData: any = {
      eventsBySports: [{ categoryId: '1' }, { categoryId: '2' }]
    };
    const updateData: any = {
      eventsBySports: [{ categoryId: '1' }, { categoryId: '3', showInPlay: true }]
    };

    service['removeSportCategories'] = jasmine.createSpy().and.callFake(service['removeSportCategories']);
    service['addSportCategories'] = jasmine.createSpy().and.callFake(service['addSportCategories']);

    service['updateSportCategories'](cacheData, updateData);

    expect(service['removeSportCategories']).toHaveBeenCalledWith(
      ['2'], cacheData.eventsBySports
    );
    expect(service['addSportCategories']).toHaveBeenCalledWith(
      ['3'], cacheData.eventsBySports, updateData.eventsBySports
    );
    expect(cacheData.eventsBySports.length).toBe(2);
    expect(cacheData.eventsBySports[0].categoryId).toBe('1');
    expect(cacheData.eventsBySports[1].categoryId).toBe('3');
  });

  it('should call addEvents', () => {
    service.allEvents = {
      '1': { id: 1, categoryId: 'CID1', markets: [] }
    };

    const eventsList: any[] = [
      { id: 1, categoryId: 'CID1', markets: [] },
      { id: 2, categoryId: 'CID2' },
      { id: 3, categoryId: 'CID3' },
    ];
    service.addEvents(eventsList, true);
    expect(Object.keys(service.allEvents)).toContain('1');
    expect(Object.keys(service.allEvents)).toContain('2');
    expect(Object.keys(service.allEvents)).toContain('3');
  });

  describe('removeEvents', () => {
    it('should call removeEvents with events array', () => {
      service.allEvents = {
        '1': { id: 1, categoryId: 'CID1' },
        '2': { id: 2, categoryId: 'CID2' },
        '3': { id: 3, categoryId: 'CID3' },
      };

      service.removeEvents([{ id: 1, categoryId: 'CID1' } as any]);
      expect(Object.keys(service.allEvents)).not.toContain('1');
      expect(Object.keys(service.allEvents)).toContain('2');
      expect(Object.keys(service.allEvents)).toContain('3');
    });

    it('should call removeEvents with eventIds array', () => {
      service.allEvents = {
        '1': { id: 1, categoryId: 'CID1' },
        '2': { id: 2, categoryId: 'CID2' },
        '3': { id: 3, categoryId: 'CID3' },
      };

      service.removeEvents([1, 2]);
      expect(Object.keys(service.allEvents)).not.toContain('1');
      expect(Object.keys(service.allEvents)).not.toContain('2');
      expect(Object.keys(service.allEvents)).toContain('3');
    });
    it('should not fail in edge case', () => {
      service.removeEvents([null, undefined, {}] as any);
    });
  });
});
