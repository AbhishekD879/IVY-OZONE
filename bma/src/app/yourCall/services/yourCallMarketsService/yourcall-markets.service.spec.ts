import { YourcallMarketsService } from './yourcall-markets.service';
import { of } from 'rxjs';
import { fakeAsync, flush, tick } from '@angular/core/testing';
import { resolve } from 'bluebird';

describe('#YourcallMarketsService', () => {
  let service: YourcallMarketsService;
  let coreTools;
  let yourcallProviderService;
  let yourcallDashboardService;
  let yourcallStoredBetsService;
  let yourcallService;
  let yourCallMarketsProviderService;
  let pubsubService;
  let gtmService;
  let CMS;
  let awsService;
  let playerBetsMarket;
  let bybSelectedSelectionsService;

  const dataToStore = 'dataToStore';

  beforeEach(() => {
    playerBetsMarket = {
      name: 'Player Bets',
      bybMarket: 'Player Bets',
      incidentGrouping: 0,
      marketGrouping: 0,
      id: '',
      brand: '',
      createdBy: '',
      createdAt: '',
      updatedBy: '',
      updatedAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      sortOrder: 1
    };
    coreTools = {
      hasOwnDeepProperty: jasmine.createSpy().and.returnValue(true),
      getOwnDeepProperty: jasmine.createSpy().and.returnValue('BYB'),
    };
    yourcallProviderService = {
      API: 'BYB',
      use: jasmine.createSpy(),
      useOnce: jasmine.createSpy('useOnce').and.returnValue({
        getGameInfo: jasmine.createSpy('getGameInfo').and.returnValue(Promise.resolve({
          data: {
            homeTeam: {
              id: 'id1'
            },
            visitingTeam: {
              id: 'id2'
            },
            status: '1',
            hasPlayerProps: false
          }
        }))
      }),
      getMatchMarkets: jasmine.createSpy('getMatchMarkets'),
      getEDPMarkets: jasmine.createSpy('getEDPMarkets').and.returnValue(Promise.resolve([playerBetsMarket])),
      isValidResponse: jasmine.createSpy('isValidResponse'),
      getStatistics: jasmine.createSpy('getStatistics'),
      getStatValues: jasmine.createSpy('getStatValues'),
      getPlayers: jasmine.createSpy('getPlayers'),
      getMarketSelections: jasmine.createSpy('getMarketSelections')
    };
    yourcallDashboardService = {
      finishBatchAdd: jasmine.createSpy(),
      add: jasmine.createSpy(),
      edit: jasmine.createSpy(),
      clear: jasmine.createSpy(),
      remove: jasmine.createSpy()
    };
    yourcallStoredBetsService = {
      removeEvent: jasmine.createSpy(),
      modifyStoredBet: jasmine.createSpy(),
      reValidateEvent: jasmine.createSpy(),
      getStoredBets: jasmine.createSpy('getStoredBets').and.returnValue({1: { startTime: 123 }})
    };
    yourcallService = {
      whenYCReady: jasmine.createSpy('whenYCReady').and.returnValue(of(true)),
      isEnabledYCTab: true,
      isFiveASideAvailable: true,
      isAvailableForCompetition: jasmine.createSpy('isAvailableForCompetition').and.returnValue(true),
      isFiveASideAvailableForCompetition: jasmine.createSpy('isFiveASideAvailableForCompetition').and.returnValue(true)
    };
    yourCallMarketsProviderService = {
      getInstance: jasmine.createSpy('getInstance')
    };
    pubsubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        YC_MARKET_TOGGLED: 'YC_MARKET_TOGGLED'
      }
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    CMS = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        BYBCategories: {
          '123': 'Football'
        }
      }))
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };

    bybSelectedSelectionsService= {
      callGTM: jasmine.createSpy('callGTM').and.returnValue(true)
    };
    service = new YourcallMarketsService(
      coreTools,
      yourcallProviderService,
      yourcallDashboardService,
      yourcallStoredBetsService,
      yourcallService,
      yourCallMarketsProviderService,
      pubsubService,
      gtmService,
      CMS,
      awsService,
      bybSelectedSelectionsService
      );
    service['obGameId'] = '24';
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service.order).toEqual(0);
  });

  describe('#setCache', () => {
    it('should set data to local cache', () => {
      service.setCache('data', dataToStore);

      expect(service['cache']).toEqual({
        '24': {
          'BYB:data': 'dataToStore'
        }
      });
    });

    it('should set path', () => {
      service['cache'] = {
        '24': {}
      };
      service.setCache('data', dataToStore);

      expect(service['cache']).toEqual({
        '24': {
          'BYB:data': 'dataToStore'
        }
      });
    });
  });

  describe('#getCache', () => {
    it('should get data from cache by key', () => {
      service.setCache('data', dataToStore);
      const result = service.getCache('data');

      expect(result).toEqual('dataToStore');
    });

    it('should return null if no data in cache', () => {
      service.setCache('data', dataToStore);
      const result = service.getCache('nodata');

      expect(result).toEqual(null);
    });
  });

  describe('#clearCache', () => {
    it('should clear game cache', () => {
      service.setCache('data', dataToStore);
      service['obGameId'] = '25';
      service.setCache('data', dataToStore);

      service.clearCache();

      expect(service['cache']).toEqual({
        '24': {
          'BYB:data': 'dataToStore'
        }
      });
    });

    it('should clear all cache', () => {
      service.setCache('data', dataToStore);
      service.clearCache(true);

      expect(service['cache']).toEqual({});
    });
  });

  describe('#setProvider', () => {
    it('should put to provider correct api', () => {
      service.setProvider('BYB');

      expect(yourcallProviderService.use).toHaveBeenCalledWith('BYB');
    });
  });

  describe('#isAnyStoredBets', () => {
    it('should check stored bets', () => {
      const result = service.isAnyStoredBets('12345');
      service.clearCache(true);

      expect(coreTools.hasOwnDeepProperty).toHaveBeenCalledWith({}, '12345.markets.BYB');
      expect(result).toBeTruthy();
    });
  });

  describe('#betsArrayToRestore', () => {
    it('should return array of stored selections/bets that should be restored', () => {
      service.storedBets[service['obGameId']] = {
        markets: {
          'BYB': {
            testBet: {
              selections: ['123']
            }
          }
        }
      };

      const result = service.betsArrayToRestore('testBet');

      expect(result).toEqual(['123']);
    });
  });

 describe('#getStoredBetsMarketsNames', () => {
    it('should return array of stored Markets Names that should be restored', () => {
      service.storedBets['12345'] = {
        markets: {
          'BYB': {
            testBet: {
              selections: ['123']
            }
          }
        }
      };

      const result = service.getStoredBetsMarketsNames('12345');

      expect(result).toEqual(['testBet']);
    });

    it('should push keys', () => {
      service.markets = [{
        key: 'testBet',
        parent: {
          key: 'parent key'
        }
      }];
      service.storedBets['12345'] = {
        markets: {
          'BYB': {
            testBet: {
              selections: ['123']
            }
          }
        }
      };
      const result = service.getStoredBetsMarketsNames('12345');

      expect(result).toEqual(['testBet', 'parent key']);
    });
  });

  describe('#isRestoredNeeded', () => {
    it('should check whether restore is needed for market and return true', () => {
      service.storedBets['24'] = {
        markets: {
          'BYB': {
            testBet: {
              selections: ['123']
            }
          }
        }
      };

      const result = service.isRestoredNeeded('testBet');

      expect(result).toEqual(true);
    });

    it('should return false', () => {
      coreTools.hasOwnDeepProperty.and.returnValue(false);

      const result = service.isRestoredNeeded('testBet');

      expect(result).toEqual(false);
    });
  });

  describe('#restoredMarketDone', () => {
    it('should mark that restore process is done for particular market and if all markets are restored - starts odds calculations', () => {
      service.storedBets['24'] = {
        markets: {
          'BYB': {
            testBet: {
              isRestored: false,
              selections: ['123']
            }
          }
        }
      };

      service.restoredMarketDone('testBet');

      expect(yourcallDashboardService.finishBatchAdd).toHaveBeenCalled();
    });

    it('should not call finishBatchAdd', () => {
      service.storedBets['24'] = {
        markets: {
          'BYB': {
            testBet: {
              isRestored: true,
              selections: ['123']
            },
            some: false
          }
        }
      };

      service.restoredMarketDone('testBet');

      expect(yourcallDashboardService.finishBatchAdd).not.toHaveBeenCalled();
    });
  });

  describe('#restoreBet', () => {
    it('should restore bet if market loaded', () => {
      spyOn<any>(service, 'restoreMarketBet');

      const market = {
        isLoaded: () => {
          return true;
        }
      };

      service.restoreBet((market as any));

      expect(service['restoreMarketBet']).toHaveBeenCalled();
    });

    it('should restore bet if market not loaded', () => {
      const market = {
        isLoaded: () => {
          return false;
        },
        registerAfterLoad: () => {
          return;
        }
      };

      spyOn<any>(market, 'registerAfterLoad');

      service.restoreBet((market as any));

      expect(market.registerAfterLoad).toHaveBeenCalled();
    });

    it('should call restoreMarketBet', () => {
      service['restoreMarketBet'] = jasmine.createSpy('restoreMarketBet');
      const market = {
        isLoaded: () => {
          return false;
        },
        registerAfterLoad : (subject) => {
          subject.next();
          subject.complete();
        }
      };

      service.restoreBet((market as any));
 expect(service['restoreMarketBet']).toHaveBeenCalled();
    });

    it('should restore bet if market not loaded', () => {
      const market = {
        isLoaded: () => {
          return false;
        },
        registerAfterLoad: () => {
          return;
        }
      };
      spyOn<any>(market, 'registerAfterLoad');
      service.restoreBet((market as any));
      expect(market.registerAfterLoad).toHaveBeenCalled();
    })
    
  });

  describe('filterStatistics', () => {
    it('should filter proper markets', () => {
      const playerFeed = [{
        title: 'To Keep a Clean Sheet'
      }, {
        title: 'B Market'
      }, {
        title: 'Goals conceded'
      }] as any;
      expect(service['filterStatistics'](playerFeed)).toEqual([{
        title: 'B Market'
      }] as any);
    });

    it('should set empty array [] if markets are not exits', () => {
      const playerFeed = [{
        title: 'To Keep a Clean Sheet'
      }] as any;
      expect(service['filterStatistics'](playerFeed)).toEqual([]);
    });
    it('should set empty array [] if markets are empty', () => {
      const playerFeed = [] as any;
      expect(service['filterStatistics'](playerFeed)).toEqual([]);
    });
  });

  describe('#getPlayerById', () => {
    it('should get player from players by id', () => {
      (service.players as any) = [ { id: 12 }, { id: 13 } ];

      const result = service.getPlayerById('13');

      expect(result).toEqual(service.players[1]);
    });
  });

  describe('#showMarkets', () => {
    it('should check if markets are available (player markets)', () => {
      (service.players as any) = [ { id: 12 } ];

      const result = service.showMarkets();

      expect(result).toEqual(true);
    });

    it('should check if markets are available (grouped markets)', () => {
      (service.players as any) = [];
      (service['gfmMarkets'] as any) = [ { id: 11 } ];

      const result = service.showMarkets();

      expect(result).toEqual(true);
    });

    it('should check if markets are available and return false if no markets', () => {
      (service.players as any) = [];
      (service['gfmMarkets'] as any) = [];

      const result = service.showMarkets();

      expect(result).toEqual(false);
    });
  });

  describe('#selectValue', () => {
    const market = { id: '1234' ,getTitle: () => 'title1' , getSelectionTitle: () => 'selection'};
    const slelection = { id: '4321' };
    beforeEach(() => {
      spyOn(service, 'addSelection');
      spyOn(service, 'removeSelection');
    });
    it('should select/unselect market selection', () => {
      spyOn(service, 'isSelected').and.returnValue(true);
      spyOn<any>(service, 'trackMarketRemovingSelection');

      service.selectValue((market as any), (slelection as any));

      expect(service.removeSelection).toHaveBeenCalled();
      // expect(service['trackMarketRemovingSelection']).toHaveBeenCalled();
    });

    it('should cSelect/unselect market selection', () => {
      spyOn(service, 'isSelected').and.returnValue(false);

      service.selectValue((market as any), (slelection as any));

      expect(service.addSelection).toHaveBeenCalled();
    });
  });

  describe('#removeSelectedValues', () => {
    beforeEach(() => {
      service.markets = [
        { id: '1234', clearSelections: jasmine.createSpy(), provider: 'BYB'},
        { id: '4321', clearSelections: jasmine.createSpy(), provider: 'BYB'}
      ];
    });

    it('should remove all selections', () => {
      service.removeSelectedValues();

      expect(yourcallStoredBetsService.removeEvent).toHaveBeenCalledWith('24', 'BYB');
      expect(service.markets[0].clearSelections).toHaveBeenCalled();
      expect(service.markets[1].clearSelections).toHaveBeenCalled();
    });
  });

  describe('#generateParamsFromArray', () => {
    it('should generate fields for request form object', () => {
      const array = [
        { key: 'value' }
      ];
      const result = service.generateParamsFromArray('paramName', array);

      expect(result).toEqual({
        'paramName[0][key]': 'value'
      });
    });
  });

  describe('#getGame', () => {
    it('should get game', () => {
      service.getGame('12345', '123').then(game => {
        expect(game).toEqual(jasmine.any(Object)); // huge game object
      });
    });

    it('should get game for Five A Side', () => {
      yourcallService.isEnabledYCTab = false;
      yourcallService.isFiveASideAvailable = true;
      service.getGame('12345', '123').then(game => {
        expect(game).toEqual(jasmine.any(Object)); // huge game object
      });
    });

    it('should get game for BYB', () => {
      yourcallService.isEnabledYCTab = true;
      yourcallService.isFiveASideAvailable = false;
      service.getGame('12345', '123').then(game => {
        expect(game).toEqual(jasmine.any(Object)); // huge game object
      });
    });

    it('should not get game neither for BYB nor for Five A Side', () => {
      yourcallService.isEnabledYCTab = false;
      yourcallService.isFiveASideAvailable = false;
      service.getGame('12345', '123').then(game => {
        expect(game).toEqual({});
      });
    });

    it('should not get game', () => {
      yourcallProviderService.useOnce.and.returnValue({
        getGameInfo: () => {
          return { data: null };
        }
      });
      service.getGame('12345', '123').then(game => {
        expect(game).toEqual({});
      });
    });

    it('should not get game when isLeagueAvailableBYB and isLeagueAvailableFiveASide false', () => {
      yourcallService.isFiveASideAvailableForCompetition.and.returnValue(false);
      yourcallService.isAvailableForCompetition.and.returnValue(false);
      service.getGame('12345', '123').then(game => {
        expect(game).toEqual({});
      });
    });

    it('should not get game when isLeagueAvailableBYB false and isLeagueAvailableFiveASide true', () => {
      yourcallService.isFiveASideAvailableForCompetition.and.returnValue(true);
      yourcallService.isAvailableForCompetition.and.returnValue(false);
      service.getGame('12345', '123').then(game => {
        expect(game).toEqual(jasmine.any(Object)); // huge game object
      });
    });

    it('should not get game when isLeagueAvailableBYB true and isLeagueAvailableFiveASide false', () => {
      yourcallService.isFiveASideAvailableForCompetition.and.returnValue(false);
      yourcallService.isAvailableForCompetition.and.returnValue(true);
      service.getGame('12345', '123').then(game => {
        expect(game).toEqual(jasmine.any(Object)); // huge game object
      });
    });
  });

  describe('#isSelected', () => {
    const slelection = { id: '4321' };
    it('should check if value is selected and return true', () => {
      const market = { id: '1234', isSelected: jasmine.createSpy().and.returnValue(true) };
      const result = service.isSelected((market as any), (slelection as any));

      expect(result).toEqual(true);
      expect(market.isSelected).toHaveBeenCalledWith(slelection);
    });

    it('should check if value is selected and return false', () => {
      const market = { id: '1234', isSelected: jasmine.createSpy().and.returnValue(false) };
      const result = service.isSelected((market as any), (slelection as any));

      expect(result).toEqual(false);
      expect(market.isSelected).toHaveBeenCalledWith(slelection);
    });
  });

  describe('#addSelection', () => {
    const market = { id: '1234', addSelection: jasmine.createSpy() };
    const slelection = { id: '4321' };
    const isBatchAdd = true;
    it('should add selection', () => {
      (service.game as any) = {
        startDate: '123431231'
      };
      service.addSelection((market as any), (slelection as any), isBatchAdd);

      expect(market.addSelection).toHaveBeenCalledWith(slelection);
      expect(yourcallStoredBetsService.modifyStoredBet).toHaveBeenCalledWith('24', market, '123431231');
      expect(yourcallDashboardService.add).toHaveBeenCalledWith(market, slelection, isBatchAdd);
    });
   it('should call yourcallDashboardService.add with isBatchAdd = true', () => {
      (service.game as any) = {
        startDate: '123431231'
      };
      service.addSelection((market as any), (slelection as any));

      expect(market.addSelection).toHaveBeenCalledWith(slelection);
      expect(yourcallStoredBetsService.modifyStoredBet).toHaveBeenCalledWith('24', market, '123431231');
      expect(yourcallDashboardService.add).toHaveBeenCalledWith(market, slelection, false);
    });
  });

  describe('#editSelection', () => {
    const market = { id: '1234', editSelection: jasmine.createSpy() };
    const slelection = { id: '4321' };
    const newSlelection = { id: '4321' };
    it('should edit player bets selection', () => {
      service.editSelection((market as any), (slelection as any), (newSlelection as any));

      expect(market.editSelection).toHaveBeenCalledWith(slelection, newSlelection);
      expect(yourcallStoredBetsService.modifyStoredBet).toHaveBeenCalledWith('24', market);
      expect(yourcallDashboardService.edit).toHaveBeenCalledWith(market, slelection, newSlelection);
    });
  });

  describe('#removeSelection', () => {
    const market = { id: '1234', removeSelection: jasmine.createSpy() };
    const slelection = { id: '4321' };
    it('should remove selection', () => {
      service.removeSelection((market as any), (slelection as any));

      expect(market.removeSelection).toHaveBeenCalledWith(slelection);
      expect(yourcallStoredBetsService.modifyStoredBet).toHaveBeenCalledWith('24', market);
      expect(yourcallDashboardService.remove).toHaveBeenCalledWith(market, slelection);
    });
  });

  describe('#clear', () => {
    beforeEach(() => {
      service.storedBets = {
        storedBets: 'storedBets'
      };
      (service.players as any) = [ { id: 1 } ];
      service.markets = [ { id: '123123' } ];
      (service['gfmMarkets'] as any) = [ { id: '123123' } ];
      service.order = 12;
      spyOn(service, 'clearCache');
    });
    it('should clear data', () => {
      service.clear(true);

      expect(service.storedBets).toEqual({});
      expect(service.players).toEqual(null);
      expect(service.markets).toEqual([]);
      expect(service['gfmMarkets']).toEqual([]);
      expect(service.order).toEqual(0);
      expect(yourcallStoredBetsService.reValidateEvent).toHaveBeenCalledWith('24');
      expect(yourcallDashboardService.clear).toHaveBeenCalled();
      expect(service.clearCache).toHaveBeenCalled();
    });

    it('should clear ALL data', () => {
      service.clear(false);

      expect(service.storedBets).toEqual({});
      expect(service.players).toEqual(null);
      expect(service.markets).toEqual([]);
      expect(service['gfmMarkets']).toEqual([]);
      expect(service.order).toEqual(0);
      expect(service.game).toEqual(null);
      expect(service['obGameId']).toEqual(null);
      expect(yourcallStoredBetsService.reValidateEvent).toHaveBeenCalledWith('24');
      expect(yourcallDashboardService.clear).toHaveBeenCalled();
      expect(service.clearCache).toHaveBeenCalled();
    });
  });

  describe('#clearProvider', () => {
    beforeEach(() => {
      spyOn(service, 'clearCache');
      service.order = 12;
      service.storedBets = {
        storedBets: 'storedBets'
      };
    });

    it('should do actions before switch provider', () => {
      service.clearProvider();

      expect(service.order).toEqual(0);
      expect(service.storedBets).toEqual({});
      expect(yourcallStoredBetsService.reValidateEvent).toHaveBeenCalledWith('24');
      expect(yourcallDashboardService.clear).toHaveBeenCalled();
    });
  });

  describe('getGame', () => {
    it('should return empty obj if BYBCategories is NOT equal to catId', () => {
      CMS.getSystemConfig = jasmine.createSpy().and.returnValue(of({ BYBCategories: '1' }));

      service.getGame('1', 'BYBCategoriesWrong').then(res => {
        expect(res).toEqual({});
      });
    });

    it('should return empty obj if yourcallService.isEnabledYCTab and yourcallService.isFiveASideAvailable are set to false', () => {
      yourcallService.whenYCReady = jasmine.createSpy().and.returnValue(of([]));
      yourcallService.isEnabledYCTab =  false;
      yourcallService.isFiveASideAvailable =  false;

      CMS.getSystemConfig = jasmine.createSpy().and.returnValue(of({ BYBCategories: { test: '123' } }));

      service.getGame('1', 'test').then(res => {
        expect(yourcallService.whenYCReady).toHaveBeenCalled();
        expect(res).toEqual({});
      });
    });
    it('should catch error afte yourcallProviderService.useOnce', () => {
      CMS.getSystemConfig = jasmine.createSpy().and.returnValue(of({ BYBCategories: { cat: ''} }));
      yourcallService.whenYCReady = jasmine.createSpy().and.returnValue(of([]));
      yourcallProviderService.useOnce.and.returnValue({
        getGameInfo: jasmine.createSpy('getGameInfo').and.returnValue(Promise.reject('error'))
      });

      service.getGame('1', 'cat').then(data => {
        expect(data).toEqual({});
        expect(awsService.addAction).toHaveBeenCalledWith('bybGetGameError', { error: 'error' });
      });

    });
  });

  it('createMarkets should create marked instances', fakeAsync(() => {
    service.createMarkets();
    flush();
    expect(yourCallMarketsProviderService.getInstance).toHaveBeenCalledWith({
      provider: 'BYB',
      title: 'Player Bets',
      key: 'Player Bets',
      grouping: 'Player Bets',
      _game: undefined, marketType: undefined, popularMarket: undefined, marketDescription: undefined, stat: undefined 
    });
  }));

  describe('#getMatchMarkets', () => {
    it('should catch error', () => {
      yourcallProviderService.getMatchMarkets.and.returnValue(Promise.reject());
      yourcallProviderService.isValidResponse.and.returnValue(true);
      service.getMatchMarkets().then(data => {
        expect(data).toEqual([] as any);
      });
    });

    it('should catch error when isValidResponse = falsee', () => {
      yourcallProviderService.getMatchMarkets.and.returnValue(Promise.reject());
      yourcallProviderService.isValidResponse.and.returnValue(false);
      service.setCache = jasmine.createSpy('setCache');
      service.getMatchMarkets().then(() => {
        expect(service.setCache).not.toHaveBeenCalled();
      });
    });

    it('should set data to gfmMarkets after getMatchMarkets call', fakeAsync(() => {
      service.setCache = jasmine.createSpy('setCache');
      yourcallProviderService.getMatchMarkets.and.returnValue(Promise.resolve({
        data: {
          id: 1,
          markets: []
        }
      } as any));
      service.getMatchMarkets().then();

      tick();
      expect(service.setCache).toHaveBeenCalledWith('gfmMarkets', {
        id: 1,
        markets: []
      });
      expect(service['gfmMarkets']).toEqual({
        id: 1,
        markets: []
      } as any);
    }));

    it('should  set data to gfmMarkets if cached', fakeAsync(() => {
      service.getCache = jasmine.createSpy('getCache').and.returnValue({
        id: 1,
        markets: []
      });
      service.getMatchMarkets().then();

      tick();
      expect(service['gfmMarkets']).toEqual({
        id: 1,
        markets: []
      } as any);
    }));
  });

  describe('#getStatisticsForPlayer', () => {
    let params;

    beforeEach(() => {
      params = {
        obEventId: '2',
        playerId: 1
      };
    });

    it('should call errorHandler', fakeAsync(() => {
      yourcallProviderService.getStatistics.and.returnValue(Promise.reject('error'));
      service['errorHandler'] = jasmine.createSpy('errorHandler');
      service.getStatisticsForPlayer(params).then();

      tick();

      expect(service['errorHandler']).toHaveBeenCalledWith('error', jasmine.any(Function), 'getStatistics');
    }));

    it('should set data to playerStatsCahce', fakeAsync(() => {
      yourcallProviderService.getStatistics.and.returnValue(Promise.resolve({
        data: [
          { id: 1, title: 'title', max: 5, min: 1 },
          { id: 2, title: 'cards' }
        ]
      }));
      service.getStatisticsForPlayer(params).then();

      tick();
      expect(service.playerStatsCache['21']).toEqual({
        allData: [{ id: 1, title: 'title', max: 5, min: 1 }, { id: 2, title: 'cards' }],
        data: [{ id: 1, title: 'title', max: 5, min: 1 }]
      } as any);
    }));

    it('should resolve if playerStatsCache has data', () => {
      service.playerStatsCache = {
        '21': {}
      } as any;

      service.getStatisticsForPlayer(params).then(data => {
        expect(data).toEqual({} as any);
      });

    });
  });

  describe('#getStatValues', () => {
    let params;

    beforeEach(() => {
      params = {
        obEventId: '2',
        playerId: 1,
        statId: 1
      };
    });

    it('should call errorHandler', fakeAsync(() => {
      yourcallProviderService.getStatValues.and.returnValue(Promise.reject('error'));
      service['errorHandler'] = jasmine.createSpy('errorHandler');
      service.getStatValues(params).then();

      tick();

      expect(service['errorHandler']).toHaveBeenCalledWith('error', jasmine.any(Function), 'getStatValues');
    }));

    it('should set data to statsValuesCache', fakeAsync(() => {
      yourcallProviderService.getStatValues.and.returnValue(Promise.resolve({
        data: {
          id: 1,
          max: 5,
          min: 1
        }
      }));
      service.getStatValues(params).then();

      tick();
      expect(service.statsValuesCache['211']).toEqual({
        data: {
          id: 1,
          max: 5,
          min: 1
        }
      } as any);
    }));

    it('should resolve statsValuesCache[playerStatisticId]', () => {
      service.statsValuesCache = {
        '211': 'playerStatisticId'
      };
      service.getStatValues(params).then(data => {
        expect(data).toEqual('playerStatisticId' as any);
      });
    });
  });

  describe('#getEDPMarkets', () => {
    it('should catch error', () => {
      yourcallProviderService.getEDPMarkets.and.returnValue(Promise.reject('error'));

      service.getEDPMarkets().then(data => {
        expect(data).toEqual([]);
      });
    });
    it('should resolve if cache', () => {
      service.getCache = jasmine.createSpy('getCache').and.returnValue({cache: []});

      service.getEDPMarkets().then(data => {
        expect(data).toEqual({ cache: [] });
      });
    });
  });

  describe('#getPlayers', () => {
    it('should catch error', () => {
      service.game = {
        obGameId: '12345'
      } as any;
      yourcallProviderService.getPlayers.and.returnValue(Promise.reject('error'));
      yourcallProviderService.isValidResponse.and.returnValue(true);

      (service.getPlayers() as Promise<any>).then((data) => {
        expect(data as any).toEqual({} as any);
      });
    });
    it('should catch error', () => {
      service.game = {
        obGameId: '12345'
      } as any;
      yourcallProviderService.getPlayers.and.returnValue(Promise.reject('error'));
      yourcallProviderService.isValidResponse.and.returnValue(false);

      service.getPlayers();
      expect().nothing();
    });
  });

  describe('#createMarkets', () => {
    it('should return empty array', fakeAsync(() => {
      yourcallProviderService.API = 'byb1';
      service.createMarkets();

      tick();
      expect(service.markets).toEqual([] as any);
    }));

    it('should sort markets', fakeAsync(() => {
      let i = 0;
      service.getEDPMarkets = jasmine.createSpy('getEDPMarkets').and.returnValue(Promise.resolve([{
        name: 'market2',
        provider: 'byb'
      }, {
        provider: 'byb1',
        name: 'market1'
      }, {
        provider: 'byb1',
        name: 'market3'
      }]));
      yourCallMarketsProviderService.getInstance.and.callFake(() => {
          i++;
          return {
            id: '1234',
            provider: 'BYB',
            key: `market${i}`
          };
      });

      service.createMarkets();

      tick();

      expect(service.markets).toEqual([{
        id: '1234',
        provider: 'BYB',
        key: 'market2'
      }, {
        id: '1234',
        provider: 'BYB',
        key: 'market1'
      }, {
        id: '1234',
        provider: 'BYB',
        key: 'market3'
      }] as any);
    }));
  });

  describe('#onMarketToggled', () => {
    it('should call pubsubService', () => {
      service.onMarketToggled(2);

      expect(pubsubService.publish).toHaveBeenCalledWith('YC_MARKET_TOGGLED', 2);
    });
  });

  describe('#prepareMarket', () => {
    it('should call onMarketToggled', fakeAsync(() => {
      const market = {
        id: '1234',
        toggleLoading: jasmine.createSpy('toggleLoading'),
        populate: jasmine.createSpy('populate'),
        provider: 'BYB'
      };
      service.onMarketToggled = jasmine.createSpy('onMarketToggled');
      service['invokeLoadMethod'] = jasmine.createSpy('invokeLoadMethod').and.returnValue(Promise.resolve([]));
      service.prepareMarket(market);

      tick();
      expect(market.toggleLoading).toHaveBeenCalled();
      expect(market.populate).toHaveBeenCalledWith([]);
      expect(service.onMarketToggled).toHaveBeenCalled();
    }));
  });

  describe('#loadMarket', () => {
    it('should call onMarketToggled', fakeAsync(() => {
      const market = {
        id: '1234',
        toggleLoading: jasmine.createSpy('toggleLoading'),
        populate: jasmine.createSpy('populate'),
        provider: 'BYB'
      };
      service.game = {
        obEventId: '12345'
      } as any;
      service.onMarketToggled = jasmine.createSpy('onMarketToggled');
      service['loadMarketSelections'] = jasmine.createSpy('loadMarketSelections').and.returnValue(Promise.resolve([]));
      service.loadMarket(market as any);

      tick();
      expect(market.toggleLoading).toHaveBeenCalled();
      expect(market.populate).toHaveBeenCalledWith([]);
      expect(service.onMarketToggled).toHaveBeenCalled();
    }));
  });

  describe('#loadMarketSelections', () => {
    let data;

    beforeEach(() => {
      data = {
        obEventId: 2,
        marketIds: '1',
      };
    });

    it('should call errorHandler', fakeAsync(() => {
      yourcallProviderService.getMarketSelections.and.returnValue(Promise.reject('error'));
      service['errorHandler'] = jasmine.createSpy('errorHandler');
      service.loadMarketSelections(data).then();

      tick();

      expect(service['errorHandler']).toHaveBeenCalledWith('error', jasmine.any(Function), 'getMarketSelections');
    }));

    it('should call setCache', fakeAsync(() => {
      yourcallProviderService.getMarketSelections.and.returnValue(Promise.resolve({
        data: {}
      }));
      service.setCache = jasmine.createSpy('setCache');
      service.loadMarketSelections(data).then();

      tick();
      expect(service.setCache).toHaveBeenCalledWith('marketSelections:1', {});
    }));

    it('should resolve if cached', () => {
      service.getCache = jasmine.createSpy('getCache').and.returnValue({data: []});

      service.loadMarketSelections(data).then(d => {
        expect(d).toEqual({data: []} as any);
      });

    });
  });

  describe('#loadPlayers', () => {
    it('should catch error', fakeAsync(() => {
      service.getPlayers = jasmine.createSpy('getPlayers').and.returnValue(Promise.reject());

      service.loadPlayers().then((data) => {
        expect(data).toEqual(undefined);
      });
    }));
    it('should not have players in homeTeam and visitingTeam', fakeAsync(() => {
      service.game = {
        homeTeam: {
          players: []
        },
        visitingTeam: {
          players: []
        }
      } as any;
      yourcallProviderService.getPlayers.and.returnValue(Promise.resolve({
        data: []
      }));
      service.loadPlayers().then();

      tick();
      expect(service.game.homeTeam.players).toEqual([]);
      expect(service.game.visitingTeam.players).toEqual([]);
    }));
    it('should have players in homeTeam and visitingTeam', fakeAsync(() => {
      service.game = {
        homeTeam: {
          players: []
        },
        visitingTeam: {
          players: []
        },
        byb: {
          homeTeam: {
            id: 1
          },
          visitingTeam: {
            id: 2
          }
        }
      } as any;
      yourcallProviderService.getPlayers.and.returnValue(Promise.resolve({
        data: [{
          team: {
            id: 1,
            name: 'player1'
          }
        }, {
          team: {
            id: 2,
            name: 'player2'
          }
        }]
      }));
      service.loadPlayers().then();

      tick();
      expect(service.game.homeTeam.players).toEqual([{
        team: {
          id: 1,
          name: 'player1'
        }
      }]);
      expect(service.game.visitingTeam.players).toEqual([{
        team: {
          id: 2,
          name: 'player2'
        }
      }]);
    }));
  });
  describe('#getAgregatedMarketsData', () => {
    it('should call populateMarkets', fakeAsync(() => {
      service['populateMarkets'] = jasmine.createSpy('populateMarkets');
      service['getMatchMarkets'] = jasmine.createSpy('getMatchMarkets');
      service['loadPlayers'] = jasmine.createSpy('loadPlayers');
      service['createMarkets'] = jasmine.createSpy('createMarkets');

      service.getAgregatedMarketsData().then();

      tick();

      expect(service['populateMarkets']).toHaveBeenCalled();
      expect(service.storedBets).toEqual({1: { startTime: 123 }});
    }));
  });
  describe('#track', () => {
    it('should track trackMarketEditingSelection', () => {
      service.trackMarketEditingSelection();

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'dashboard',
        eventLabel: 'edit bet'
      });
    });
    it('should track trackTabsSwitching', () => {
      service.trackTabsSwitching('tabName');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'switch tab',
        eventLabel: 'tabName'
      });
    });
    it('should track trackSelectingPlayerBet', () => {
      service.trackSelectingPlayerBet('playerName', 'playerStat', 'playerStatNum');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'build bet',
        eventLabel: 'select player bet',
        playerName: 'playerName',
        playerStat: 'playerStat',
        playerStatNum: 'playerStatNum'
      });
    });

   it('should track trackMarketRemovingSelection', () => {
      service['trackMarketRemovingSelection']({ name: 'name', provider: 'BYB' } as any);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'dashboard',
        eventLabel: 'remove selection',
        market: 'name'
      });
    });
  });

  describe('#errorHandler', () => {
    it('should call isValidResponse', () => {
      (resolve as Function) = jasmine.createSpy('resolve');
      yourcallProviderService.isValidResponse = jasmine.createSpy().and.returnValue(true);
      service['errorHandler']('error', resolve, 'reason');

      expect(yourcallProviderService.isValidResponse).toHaveBeenCalledWith('error', 'reason');
    });

    it('should call isValidResponse without resolve', () => {
      (resolve as Function) = jasmine.createSpy('resolve');
      yourcallProviderService.isValidResponse = jasmine.createSpy().and.returnValue(false);
      service['errorHandler']('error', resolve, 'reason');

      expect(yourcallProviderService.isValidResponse).toHaveBeenCalledWith('error', 'reason');
      expect(resolve).not.toHaveBeenCalled();
    });
  });

  describe('#populateMarkets', () => {
    beforeEach(() => {
      service.markets = [{
        id: '1234',
        provider: 'BYB',
        populate: jasmine.createSpy('populate'),
        grouping: 'Player Bets 1',
        add: jasmine.createSpy('add')
      }];
    });

    it('should not call getInstance', () => {
      service.markets[0].provider = 'BYB1';
      service['populateMarkets']();

      expect(yourCallMarketsProviderService.getInstance).not.toHaveBeenCalled();
    });

    it('should call market populate if grouping "Player Bets"', () => {
      service.markets[0].grouping = 'Player Bets';
      service.players = [
        {
          name: 'Messi',
          id: 1,
          position: {
            title: 'forward'
          }
        },
        {
          name: 'Allison',
          id: 2,
          position: {
            title: 'Goalkeeper'
          }
        }
       ] as any;
      service['populateMarkets']();

      expect(service.markets[0].populate).toHaveBeenCalled();
      expect(service.markets[0].available).toEqual(true);
      expect(service.markets[0].type).toEqual('playerBets');
      expect(service.markets[0].players).toEqual(service.players);
      expect(service.markets[0].filteredPlayers).toEqual([{
          name: 'Messi',
          id: 1,
          position: {
            title: 'forward'
          }
        }]);
    });

    it('should set available false when data markets is empty', () => {
      service['populateMarkets']();

      expect(service.markets[0].available).toEqual(false);
    });

    it('should push child to markets', () => {
      yourCallMarketsProviderService.getInstance.and.returnValue({
        setData: jasmine.createSpy('setData').and.returnValue({
            id: '1234678',
            provider: 'BYB',
        }),
        name: 'name',
        groupName: 'groupName',
        id: '1',
        provider: 'BYB'
      } as any);

      service['gfmMarkets'] = [{
        marketGroupName: 'Player Bets 1',
        markets: [{
          groupName: 'groupName',
          title: 'new title'
        }]
      }] as any;
       service['populateMarkets']();

      expect(service.markets[0].add).toHaveBeenCalledWith({
        id: '1234678',
        provider: 'BYB'
      });
      expect(yourCallMarketsProviderService.getInstance).toHaveBeenCalledWith({
        provider: 'BYB',
        key: 'new title',
        groupName: 'groupName',
        parent: {
          id: '1234',
          provider: 'BYB',
          populate: jasmine.any(Function),
          grouping: 'Player Bets 1',
          add: jasmine.any(Function)
        },
        _game: undefined
      });
      expect(service.markets).toEqual([{
        id: '1234',
        provider: 'BYB',
        populate: jasmine.any(Function),
        grouping: 'Player Bets 1',
        add: jasmine.any(Function)
      }, {
        id: '1234678',
        provider: 'BYB'
      }] as any);
    });

    describe('#filterStatistics', () => {
      it('should filter statistics', () => {
        const result = service['filterStatistics']([{ title: 'Cards' }, { title: 'Cards1'}] as any);

        expect(result).toEqual([{ title: 'Cards1'}] as any);
      });
    });

    describe('#invokeLoadMethod', () => {
      it('should return empty array', () => {
        (service['invokeLoadMethod']({ provider: 'BYB1'} as any) as Promise<any>).then(data => {
        expect(data).toEqual([] as any);
        });
      });

      it('should return empty array', fakeAsync(() => {
        service.loadMarketSelections = jasmine.createSpy('loadMarketSelections');
        service.game = {
          obEventId: '12345'
        } as any;
        service['invokeLoadMethod']({ provider: 'BYB', id: '1'} as any);

        tick();
        expect(service.loadMarketSelections).toHaveBeenCalledWith({
          obEventId: '12345' as any,
          marketIds: '1'
        } as any);
      }));
    });

    describe('#mergeEventData', () => {
      it('should return undefined', () => {
        const result = service['mergeEventData'](null, null);

        expect(result).toEqual(undefined);
      });
    });

    describe('#restoreMarketBet', () => {
      it('should call restoredMarketDone', () => {
        service.betsArrayToRestore = jasmine.createSpy('betsArrayToRestore').and.returnValue(['title']);
        service.addSelection = jasmine.createSpy('addSelection');
        service.restoredMarketDone = jasmine.createSpy('restoredMarketDone');

        service['restoreMarketBet']({ selections: [{ title: 'title'}], key: 'key'} as any);

        expect(service.addSelection).toHaveBeenCalledWith({ selections: [{ title: 'title'}], key: 'key'} as any, { title: 'title'} as any, true);
        expect(service.restoredMarketDone).toHaveBeenCalledWith('key');
      });
    });

    describe('#loadSelectionData', () => {
      it('loadSelectionData', () => {
        spyOn(service, 'loadMarketSelections');
        service.game = {obEventId : 11} as any;
        service.loadSelectionData({id: 10} as any);
        expect(service.loadMarketSelections).toHaveBeenCalled();
      });
    });

    describe('#restoreGSMarketBet', () => {
      it('restoreGSMarketBet', () => {
        const market = {selections : [{title: 'ronaldo'}]}
        spyOn(service, 'betsArrayToRestore').and.returnValue(['ronaldo','. messi'])
        spyOn(service,'addSelection');
        spyOn(service,'restoredMarketDone');
        spyOn(service, 'checkForFormattedName' as any).and.returnValue('MESSI');
        service['restoreGSMarketBet'](market as any);
        expect(service.restoredMarketDone).toHaveBeenCalled();
      });

      it('restoreGSMarketBet with mysterious names', () => {
        const market = {selections : [{title: 'ronaldoz'}]}
        spyOn(service, 'betsArrayToRestore').and.returnValue(['ronaldo','. messi'])
        spyOn(service,'addSelection');
        spyOn(service,'restoredMarketDone');
        spyOn(service, 'checkForFormattedName' as any).and.returnValue('MESEIE');
        service['restoreGSMarketBet'](market as any);
        expect(service.restoredMarketDone).toHaveBeenCalled();
      });
    });

    //checkForFormattedName
    describe('#checkForFormattedName', () => {
      it('checkForFormattedName', () => {
        const retVal = service['checkForFormattedName']('messi' as any);
        expect(retVal).toBe('MESSI')
      });

      it('checkForFormattedName with dot', () => {
        const retVal = service['checkForFormattedName']('. messi' as any);
        expect(retVal).toBe('MESSI')
      });
    });

    //restoreBet
    describe('#restoreBet new', () => {
      it('restoreBet with true', () => {
        const market = {key: 'ANYTIME GOALSCORER' , isLoaded : () => true};
        // spyOn(service['restoreGSMarketBet']);
        service['restoreGSMarketBet'] = jasmine.createSpy('restoreGSMarketBet');
        service.restoreBet(market as any);
        expect(service['restoreGSMarketBet']).toHaveBeenCalled();
      });

      it('restoreBet with false', () => {
        const market = {key: 'ANYTIME GOALSCORER' , isLoaded : () => false, registerAfterLoad: ()=> true};
        // spyOn(service['restoreGSMarketBet']);
        service['restoreGSMarketBet'] = jasmine.createSpy('restoreGSMarketBet');
        service.restoreBet(market as any);
        expect(service['restoreGSMarketBet']).not.toHaveBeenCalled();
      });


      it('should call restoreMarketBet', () => {
        service['restoreGSMarketBet'] = jasmine.createSpy('restoreGSMarketBet');
        const market = {
          key: 'ANYTIME GOALSCORER',
          isLoaded: () => {
            return false;
          },
          registerAfterLoad: (subject) => {
            subject.next();
            subject.complete();
          }
        };

        service.restoreBet((market as any));
        expect(service['restoreGSMarketBet']).toHaveBeenCalled();
      });
    });
  });
});
