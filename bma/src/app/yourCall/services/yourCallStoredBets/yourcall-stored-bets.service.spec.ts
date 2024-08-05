import { YourcallStoredBetsService } from '@yourcall/services/yourCallStoredBets/yourcall-stored-bets.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('YourcallStoredBetsService', () => {
  let service: YourcallStoredBetsService;
  let userService: any;
  let pubSubCbMap: any;
  let pubSubService: any;
  let storageService: any;
  let _clearStoredBets: any;

  beforeEach(() => {
    userService = {
      register: jasmine.createSpy('register'),
    };

    pubSubCbMap = {};

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((name, channel, cb) => {
        pubSubCbMap[channel] = cb;
      }),
      API: pubSubApi
    };

    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };

    service = new YourcallStoredBetsService(userService, pubSubService, storageService);

    _clearStoredBets = spyOn(service, '_clearStoredBets');
  });

  describe('constructor', () => {
    it('should handle SESSION_LOGIN event', () => {
      pubSubCbMap['SESSION_LOGIN']();
      expect(service['isUserLoggedIn']).toBeTruthy();
    });

    it('should handle SESSION_LOGOUT event (user logged in)', () => {
      service['isUserLoggedIn'] = true;
      pubSubCbMap['SESSION_LOGOUT']();
      expect(service._clearStoredBets).toHaveBeenCalled();
    });

    it('should handle SESSION_LOGOUT event (user logged out)', () => {
      service['isUserLoggedIn'] = false;
      pubSubCbMap['SESSION_LOGOUT']();
      expect(service._clearStoredBets).not.toHaveBeenCalled();
    });

    it('should handle REMOVE_BYB_STORED_EVENT event', () => {
      spyOn(service, 'removeEvent');
      pubSubCbMap['REMOVE_BYB_STORED_EVENT'](1);
      expect(service.removeEvent).toHaveBeenCalledWith(1 as any, null);
    });
  });

  describe('initStorage', () => {
    beforeEach(() => {
      storageService.set.calls.reset();
    });

    it('should call storageService.set if storage or storage.v doesn\'t exist or clear is true', () => {
      storageService.get.and.returnValue(null);
      service['v'] = 1;
      service.initStorage(true);

      expect(storageService.set).toHaveBeenCalled();
    });

    it('should not call storageService.set if storage or storage.v exist or clear is false', () => {
      storageService.get.and.returnValue({v: 1});

      service['v'] = 1;
      service.initStorage(false);

      expect(storageService.set).not.toHaveBeenCalled();
    });
  });

  describe('getStoredBets', () => {
    let isValidBet: any;
    let initStorage: any;

    beforeEach(() => {
      spyOn(service, '_reValidateBets');

      isValidBet = spyOn(service, 'isValidBet');
      initStorage = spyOn(service, 'initStorage');
    });

    it('should return correct result if _isValidate return false', () => {
      initStorage.and.returnValue({testId: 12});
      isValidBet.and.returnValue(false);

      const actual: any = service.getStoredBets();

      expect(actual.testId).toBeFalsy();
      expect(service['_reValidateBets']).not.toHaveBeenCalled();
    });

    it('should return correct result if _isValidate return true', () => {
      isValidBet.and.returnValue(true);
      initStorage.and.returnValue({testId: 12});
      spyOn<any>(Object.prototype.hasOwnProperty, 'call').and.returnValue(false);

      const actual: any = service.getStoredBets();

      expect(actual.testId).toEqual(12);
      expect(service['_reValidateBets']).not.toHaveBeenCalled();
    });

    it('should return correct result if allStoredBets has not eventId property', () => {
      isValidBet.and.returnValue(true);
      initStorage.and.returnValue({});

      service.getStoredBets();

      expect(service['_reValidateBets']).not.toHaveBeenCalled();
    });

    it('should return correct result if allStoredBets has not eventId property', () => {
      isValidBet.and.returnValue(true);
      initStorage.and.returnValue({testId: 12});

      service.getStoredBets();

      expect(service['_reValidateBets']).toHaveBeenCalled();
    });
  });

  describe('isValidBet', () => {
    let now, futureTime, threeHoursAgo;

    beforeEach(() => {
      now = Date.now();
      futureTime = now + 9999;
      threeHoursAgo = now - service['threeHours'];
    });

    it('should return true if last modify was less than 3 hours', () => {
      expect(service.isValidBet({
        startTime: futureTime,
        lastModified: threeHoursAgo + 1000
      } as any)).toBeTruthy();
    });

    it('should return false if last modify was more than 3 hours', () => {
      expect(service.isValidBet({
        startTime: futureTime,
        lastModified: threeHoursAgo - 60
      } as any)).toBeFalsy();
    });

    it('should return false if bet has started', () => {
      expect(service.isValidBet({
        startTime: now - 1,
        lastModified: threeHoursAgo + 1000
      } as any)).toBeFalsy();
    });
  });

  describe('modifyStoredBet', () => {
    let market: any;
    let storage: any;
    let initStorageService: any;

    beforeEach(() => {
      market = {
        someProvider: {},
        someKey: 'testKey',
      };

      storage = {
        myId: {
          lastModified: null,
          markets: {
            someProvider: {
              testKey: {
                selections: null
              }
            }
          }
        }
      };

      spyOn(service, '_reValidateBets');
      spyOn(service, '_collectSelections').and.returnValue('some selections' as any);

      initStorageService = spyOn(service, 'initStorage');
    });

    afterEach(() => {
      initStorageService.calls.reset();
    });

    it('should return correct result if _isValidate return false', () => {
      initStorageService.and.returnValue(storage);
      service.modifyStoredBet('myId', market, '0923423482', false);

      expect(service._reValidateBets).toHaveBeenCalled();
      expect(storageService.set).toHaveBeenCalled();
    });

    it('should create new event if eventId does not exist', () => {
      initStorageService.and.returnValue(storage);
      service.modifyStoredBet('unknownId', market, '123456');

      expect(service._reValidateBets).toHaveBeenCalled();
      expect(storageService.set).toHaveBeenCalled();
    });

    it('should return correct result if edit true', () => {
      initStorageService.and.returnValue(storage);
      service.modifyStoredBet('myId', market, '0923423482', true);

      expect(service._reValidateBets).toHaveBeenCalled();
      expect(storageService.set).toHaveBeenCalled();
    });

    it('should return correct result if edit true', () => {
      initStorageService.and.returnValue(storage);
      service.modifyStoredBet('myId', market, '0923423482', true);

      expect(service._reValidateBets).toHaveBeenCalled();
      expect(storageService.set).toHaveBeenCalled();
    });

    it('should return correct result and skip if statements', () => {
      market.provider = 'someProvider';
      market.key = 'testKey';

      initStorageService.and.returnValue(storage);

      service.modifyStoredBet('myId', market, '0923423482', true);

      expect(service._reValidateBets).toHaveBeenCalled();
      expect(storageService.set).toHaveBeenCalled();
    });
  });

  describe('_collectSelections', () => {
    it('should return correct result if selections is array and type is not playerBets', () => {
      const actual = service._collectSelections([{title: 'first'}, {title: 'second'}] as any, 'any type');

      expect(actual).toEqual(['first', 'second']);
    });

    it('should return correct result if selections is array and type is playerBets', () => {
      const actual: any = service._collectSelections([
        {player: 'player1', statistic: 'statistic1', value: 'value1'},
        {player: 'player2', statistic: 'statistic2', value: 'value2'}
      ] as any, 'playerBets');

      expect(actual[0].playerName).toEqual('player1');
      expect(actual[0].statisticTitle).toEqual('statistic1');
      expect(actual[0].value).toEqual('value1');
      expect(actual.length).toEqual(2);
    });

    it('should return selection title within array if selections is object', () => {
      const actual = service._collectSelections({title: 'first'} as any);

      expect(actual).toEqual(['first']);
    });

    it('should return empty array if selections is not defined', () => {
      const actual = service._collectSelections(null);

      expect(actual).toEqual([]);
    });
  });


  describe('reValidateEvent', () => {
    beforeEach(() => {
      spyOn(service, '_reValidateBets');
    });

    it('should call storageService after validate', () => {
      spyOn(service, 'initStorage').and.returnValue({someId: 'test'} as any);

      service.reValidateEvent('someId');

      expect(service._reValidateBets).toHaveBeenCalled();
      expect(service['storageService'].set).toHaveBeenCalled();
    });

    it('should not call _reValidateBets if initStorage doesn\'t return values', () => {
      spyOn(service, 'initStorage').and.returnValue({} as any);

      service.reValidateEvent('someId');

      expect(service._reValidateBets).not.toHaveBeenCalled();
      expect(service['storageService'].set).toHaveBeenCalled();
    });
  });

  describe('_clearStoredBets', () => {
    let initStorageMethod: any;

    beforeEach(() => {
      initStorageMethod = spyOn(service, 'initStorage');
    });

    it('should call initStorage method with true param', () => {
      _clearStoredBets.and.callThrough();
      service._clearStoredBets();

      expect(initStorageMethod).toHaveBeenCalledWith(true);
    });
  });

  describe('removeEvent', () => {
    let initStorageResult: any;

    beforeEach(() => {
      initStorageResult = {
        someEventId: {
          markets: {
            someProvideId: {
              data: 'test'
            }
          }
        }
      };

      spyOn(service, 'initStorage').and.returnValue(initStorageResult);
    });

    it('should return event market if provideId is defined', () => {
      service.removeEvent('someEventId', 'someProvideId');

      expect(service['storageService'].set).toHaveBeenCalled();
      expect(initStorageResult.someEventId.markets.someProvideId).toBeFalsy();
    });

    it('should return event if provideId is not defined', () => {
      service.removeEvent('someEventId', '');

      expect(service['storageService'].set).toHaveBeenCalled();
      expect(initStorageResult.someEventId).toBeFalsy();
    });
  });

  describe('_reValidateBets', () => {
    let storeBets: any;

    beforeEach(() => {
      storeBets = {
        someId: {
          markets: {
            someProvider: {
              first: {
                selections: {
                  length: 0
                }
              }
            }
          }
        }
      };
    });

    it('should return undefined if storedBets false', () => {
      expect(service._reValidateBets({} as any, 'id')).toBeUndefined();
    });

    it('should return undefined if event has not markets', () => {
      delete storeBets.someId.markets;

      expect(service._reValidateBets(storeBets as any, 'someId')).toBeUndefined();
    });

    it('should return correct result if event is in storeBets object', () => {
      service._reValidateBets(storeBets as any, 'someId');

      expect(storeBets.someId).toBeUndefined();
    });

    it('should return correct result if skipped if statements', () => {
      storeBets.someId.markets.someProvider.first.selections.length = 1;
      service._reValidateBets(storeBets as any, 'someId');

      expect(storeBets.someId).not.toBeUndefined();
    });

    it('should return correct result if storedBets doesn\'t have markets', () => {
      storeBets.someId.markets.length = 1;
      service._reValidateBets(storeBets as any, 'someId');

      expect(storeBets.someId).not.toBeUndefined();
    });
  });
});
