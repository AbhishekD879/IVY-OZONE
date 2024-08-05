import { Observable } from 'rxjs';
import { BetslipStorageService } from './betslip-storage.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ISportEvent } from '@core/models/sport-event.model';

describe('BetslipStorageService', () => {
  let service: BetslipStorageService;
  let storageService;
  let localeService;
  let betslipDataService;
  let betSelectionsService;
  let fracToDecService;
  let pubSubService;
  let nativeBridgeService;

  beforeEach(() => {
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
      remove: jasmine.createSpy('remove').and.returnValue('vsm-betmanager-coralvirtuals-en-selections'),
      cleanBetslip: jasmine.createSpy('cleanBetslip'),
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    betslipDataService = {
      getActiveSinglesIds: jasmine.createSpy('getActiveSinglesIds'),
      setDefault: jasmine.createSpy('setDefault'),
      bets: jasmine.createSpy('bets')

    };
    betSelectionsService = {
      flush: jasmine.createSpy('flush'),
      removeSelectionById: jasmine.createSpy('removeSelectionById'),
      bets: {
        params: { 
          lottoData:{isLotto: true}
         }
        }
    };
    fracToDecService = {
      getDecimal: jasmine.createSpy('getDecimal')
    };
    pubSubService = {
      API: pubSubApi,
      publishSync: jasmine.createSpy('publishSync'),
      publish: jasmine.createSpy('publish')
    };
    nativeBridgeService = {
      syncPlayerBetSlip: jasmine.createSpy('syncPlayerBetSlip'),
      onCloseBetSlip: jasmine.createSpy('onCloseBetSlip'),
      accaNotificationChanged: jasmine.createSpy('accaNotificationChanged'),
      syncWithNative: jasmine.createSpy('syncWithNative'),
    };
    service = new BetslipStorageService(
      storageService,
      localeService,
      betslipDataService,
      betSelectionsService,
      fracToDecService,
      pubSubService,
      nativeBridgeService
    );
  });

  it('updateStorage (bet not found)', () => {
    storageService.get = () => [];
    service.updateStorage({}, '1');
    expect(storageService.set).not.toHaveBeenCalled();
  });

  it('updateStorage (price update)', () => {
    const stake = {
      outcomesIds: ['1'], price: { priceNum: 1, priceDen: 2 }
    };
    storageService.get = () => [stake];

    service.updateStorage({ lp_num: 3, lp_den: 4 }, '1');

    expect(fracToDecService.getDecimal).toHaveBeenCalledWith(3, 4);
    expect(stake.price.priceNum).toBe(3);
    expect(stake.price.priceDen).toBe(4);
    expect(storageService.set).toHaveBeenCalledWith('betSelections', [stake]);
  });

  it('updateStorage (handicap update)', () => {
    const stake = {
      outcomesIds: ['1'], handicap: { raw: '5' }
    };
    storageService.get = () => [stake];

    service.updateStorage({ raw_hcap: '-5' }, '1');

    expect(stake.handicap.raw).toBe('-5');
    expect(storageService.set).toHaveBeenCalledWith('betSelections', [stake]);
  });
  it('updateStorage (ew_avail update)', () => {
    const stake = {
      outcomesIds: ['1'], handicap: { raw: '5' },
      details: { isEachWayAvailable: false }
    };
    storageService.get = () => [stake];

    service.updateStorage({ ew_avail: 'Y' }, '1');

    expect(stake.details.isEachWayAvailable).toBe(true);
  });
  describe('restoreUserStakeData', () => {
    it('should restore single bets data', () => {
      const dataInStorage = [{
        id: 'SGL|111',
        userFreeBet: '1',
        details: {
          draws: [{
            id: '1234'
          }]
        }
      }, {
        id: 'SGL|222',
        userFreeBet: '1',
        userEachWay: true,
        details: {
          isEachWayAvailable: true,
          draws: [{
            id: '1234'
          }]
        }
      }, {
        id: 'FORECAST|111|222'
      }];

      const bets: any[] = [{
        type: 'SGL',
        outcomeId: '111',
        stake: {},
        Bet: {
          freeBets: [{ id: '1' }, { id: '2' }],
          params: {
            lottoData: { 
              id: '123',
              isLotto : true,
              details:{
                stake:{perLine: 1}
              },
              accaBets:[{ stake:1}]
           }
          }
        }
      }, {
        type: 'SGL',
        outcomeId: '222',
        stake: {},
        Bet: {
          freeBets: [{ id: '1' }],
          params: {
            lottoData: undefined
          }
        }
      }, {
        type: 'SGL',
        combiName: 'FORECAST',
        outcomeId: '111|222',
        stake: {},
        Bet: {
          params: {
            lottoData: { 
              id:'123',
              isLotto : true,
              details:{
                stake:{perLine: 1}
              },
              accaBets:[{ stake:1}]
           }
          }
        }
      }, {
        type: 'DBL'
      }, {
        type: 'SGL',
        outcomeId: '999'
      }];



      storageService.get.and.callFake(n => n === 'betSelections' ? dataInStorage : null);

      service.restoreUserStakeData(bets);

      expect(storageService.get).toHaveBeenCalledWith('betSelections');
      expect(localeService.getString).toHaveBeenCalledWith('bs.noFreeBetsAvalaible');
    });
    it('should restore single bets data and details is undefined', () => {
      const dataInStorage = [{
        id: 'SGL|111',
        userFreeBet: '1'
      }, {
        id: 'SGL|222',
        userFreeBet: '1',
        userEachWay: true,
        details: null
      }, {
        id: 'FORECAST|111|222'
      }];

      const bets: any[] = [{
        type: 'SGL',
        outcomeId: '111',
        stake: {},
        Bet: {
          freeBets: [{ id: '1' }, { id: '2' }],
          params: {
            lottoData: { 
              id:'123',
              isLotto : false,
              details:{
                stake:{perLine: 1}
              },
              accaBets:[{ stake:1}]
           }
          }
        }
      }, {
        type: 'SGL',
        outcomeId: '222',
        stake: {},
        Bet: {
          freeBets: [{ id: '1' }],
          params: {
            lottoData: { 
              id: '123',
              isLotto : false,
              details:{
                stake:{perLine: 1}
              },
              accaBets:[{ stake:1}]
           }
          }
        }
      }, {
        type: 'SGL',
        combiName: 'FORECAST',
        outcomeId: '111|222',
        stake: {},
        Bet: {
          params: {
            lottoData: { 
              id: '123',
              isLotto : false,
              details:{
                stake:{perLine: 1}
              },
              accaBets:[{ stake:1}]
           }
          }
        }
      }, {
        type: 'DBL'
      }, {
        type: 'SGL',
        outcomeId: '999'
      }];

      storageService.get.and.callFake(n => n === 'betSelections' ? dataInStorage : null);

      service.restoreUserStakeData(bets);

      expect(storageService.get).toHaveBeenCalledWith('betSelections');
      expect(localeService.getString).toHaveBeenCalledWith('bs.noFreeBetsAvalaible');
    });
    it('should restore single bets data and details.isEachWayAvailable is undefined', () => {
      const dataInStorage = [{
        id: 'SGL|111',
        userFreeBet: '1'
      }, {
        id: 'SGL|222',
        userFreeBet: '1',
        userEachWay: true,
        details: null
      }, {
        id: 'FORECAST|111|222'
      }];

      const bets: any[] = [{
        type: 'SGL',
        outcomeId: '111',
        stake: {},
        Bet: {
          freeBets: [{ id: '1' }, { id: '2' }],
          params: {
            lottoData: { 
              id:'SGL|111',
              isLotto : true,
              details:{
                stake:{perLine: 1}
              },
              accaBets:[{ stake:1}]
           }
          }
        }
      }, {
        type: 'SGL',
        outcomeId: '222',
        stake: {},
        Bet: {
          freeBets: [{ id: '1' }],
          params: {
            lottoData: { 
              id: '123',
              isLotto : true,
              details:{
                stake:{perLine: 1}
              },
              accaBets:[{ stake:1}]
           }
          }
        }
      }, {
        type: 'SGL',
        combiName: 'FORECAST',
        outcomeId: '111|222',
        stake: {},
        Bet: {
          params: {
            lottoData: { 
              id: '123',
              isLotto : true,
              details:{
                stake:{perLine: 1}
              },
              accaBets:[{ stake:1}]
           }
          }
        }
      }, {
        type: 'DBL'
      }, {
        type: 'SGL',
        outcomeId: '999'
      }];

      storageService.get.and.callFake(n => n === 'betSelections' ? dataInStorage : null);

      service.restoreUserStakeData(bets);

      expect(storageService.get).toHaveBeenCalledWith('betSelections');
      expect(localeService.getString).toHaveBeenCalledWith('bs.noFreeBetsAvalaible');
    });

    it('should restore multiple stakes', () => {
      storageService.get.and.callFake(n => n === 'multipleUserStakes' ? [] : null);
      service.restoreUserStakeData([]);
      expect(storageService.get).toHaveBeenCalledTimes(5);
    });
  });

  it('#clearStateInStorage should clear overask data', () => {
    service.clearStateInStorage();

    expect(storageService.remove).toHaveBeenCalledWith('overaskIsInProcess');
    expect(storageService.remove).toHaveBeenCalledWith('overaskUsername');
    expect(storageService.remove).toHaveBeenCalledWith('overaskPlaceBetsData');
  });

  it('#cleanBetslip should clean betslip storage and overask state', () => {
    service.cleanBetslip(true, false);

    expect(storageService.remove).toHaveBeenCalledWith('vsm-betmanager-coralvirtuals-en-selections');
    expect(storageService.remove).toHaveBeenCalledWith('vsbr-selection-map');
    expect(storageService.remove).toHaveBeenCalledWith('lastMadeBet');
    expect(storageService.remove).toHaveBeenCalledWith('lastMadeBetSport');
    expect(pubSubService.publishSync).toHaveBeenCalledWith('OVERASK_CLEAN_BETSLIP', {
      closeSlideOut: true,
      isOveraskCanceled: false
    });
    expect(betSelectionsService.flush).toHaveBeenCalledTimes(1);
  });

  it('removeFanzoneSelections', () => {
    storageService.get.and.returnValue([{'outcomesIds': ['240480152']}, {'outcomesIds': ['240480151']}] as any);
    service.removeFanzoneSelections('240480152');
    expect(storageService.get).toHaveBeenCalled();
    expect(storageService.set).toHaveBeenCalled();
  })

  it('#cleanBetslip should set default param value', () => {
    service.cleanBetslip(undefined, true);
    expect(pubSubService.publishSync).toHaveBeenCalledWith('OVERASK_CLEAN_BETSLIP', {
      closeSlideOut: false,
      isOveraskCanceled: true
    });
  });

  it('storeMultipleUserStakes', () => {
    betslipDataService.bets = [{
      params : {
        lottoData: {
          id:'124',
          isLotto :false
        }
       },
      type: 'SGL',
      info: () => ({})
    },
    {
      params : {
        lottoData:  undefined
       },
      type: 'SGL',
      info: () => ({})
    }, {
      type: 'DBL',
      stake: {},
      freeBet: null,
      info: () => ({}),
      params : {
        lottoData: {
          id:'124',
          isLotto :false
        }
       },
    }, {
      type: 'TBL',
      stake: {},
      freeBet: { id: 1 },
      info: () => ({}),
      params : {
        lottoData: {
          id:'124',
          isLotto :true
        }
       },
    }];

    service['storeMultipleUserStakes']();

    expect(storageService.set).toHaveBeenCalledWith(
      'multipleUserStakes', jasmine.any(Object)
    );
    expect(betslipDataService.getActiveSinglesIds).toHaveBeenCalledTimes(1);
  });

  it('storeMultipleUserStakes lotoData Undefined ' , () => {
    betslipDataService.bets = [{  params : {   lottoData:  undefined   }, type: 'SGL', info: () => ({}) },];

    service['storeMultipleUserStakes']();
    expect(storageService.set).toHaveBeenCalledWith(   'multipleUserStakes', jasmine.any(Object) );
    expect(betslipDataService.getActiveSinglesIds).toHaveBeenCalledTimes(1);
  });

  it('setFreeBet', () => {
    betSelectionsService.data = [{
      id: '1', type: 'SGL', details: { selections: []}, zip: () => { }
    }, {
      id: '2', type: 'SGL', details: { selections: []}, zip: () => { }
    }];

    service.setFreeBet({
      id: '1', selectedFreeBet: { id: 'fb1' }
    } as any);
    service.setFreeBet({
      id: '2', selectedFreeBet: null
    } as any);

    expect(storageService.set).toHaveBeenCalledWith('multipleUserStakes', jasmine.any(Object));
    expect(storageService.set).toHaveBeenCalledWith('betSelections', jasmine.any(Array));
  });

  it('storeSuspended', () => {
    const selections: any[] = [{}];
    service.storeSuspended(selections);
    expect(storageService.set).toHaveBeenCalledWith('betSuspendedSelections', selections);
  });

  describe('filterSelections', () => {
    it('no selections', () => {
      service.filterSelections([]);
      expect(pubSubService.publish).toHaveBeenCalledWith('FLUSH_VS_STORAGE');
    });

    it('no difference', () => {
      storageService.get.and.returnValue([{
        outcomesIds: [1, 2]
      }]);
      service.filterSelections([
        { id: 1 }, { id: 2 }
      ] as any);
      expect(storageService.set).not.toHaveBeenCalled();
    });

    it('store selections', () => {
      storageService.get.and.returnValue([{
        outcomesIds: [1, 2]
      }, {
        outcomesIds: [3, 4]
      }]);
      service.filterSelections([
        { id: 1 }, { id: 2 }
      ] as any);
      expect(storageService.set).toHaveBeenCalledWith('betSelections', jasmine.any(Array));
      expect(betSelectionsService.removeSelectionById).toHaveBeenCalledTimes(1);
    });
  });

  it('getOutcomesForWrapper', () => {
    const selections: any[] = [
      {
        outcomesIds: [1],
        price: { id: 1, priceType: 'LP', priceNum: 1, priceDen: 2, priceDec: 3 }
      },
      { outcomesIds: [2], price: {} },
      { outcomesIds: [3] }
    ];
    expect(service['getOutcomesForWrapper'](selections)).toEqual(jasmine.any(Array));

    service['getOutcomesForWrapper']();
    expect(storageService.get).toHaveBeenCalledWith('betSelections');
  });

  describe('restoreMultipleUserStakes', () => {
    it('no active singles', () => {
      storageService.get.and.returnValue({ activeSinglesCount: 0 });
      betslipDataService.bets = [{
        info: () => ({
          type: 'SGL',
          Bet: {
            lottoData: { 
              id: { includes: jasmine.createSpy() },
              isLotto : true,
              details:{
                stake:1
              },
              accaBets:[{ stake:1}]
           },
            price: { type: 'LP' }
          }
        }),
        params: {
          lottoData: {
            isLotto: false
          }
        }
      }];
      service['restoreMultipleUserStakes']();
      expect(betslipDataService.getActiveSinglesIds).not.toHaveBeenCalled();
    });

    it('active singles present', () => {

      storageService.get.and.returnValue({
        activeSinglesCount: 2, activeSinglesIds: [1],
        stakeData: [{
          betId: 0,
          // userEachWay: true
        }, {
          betId: 1,
          // userEachWay: true,
          stake: 2
        }, {
          betId: 9,
          userEachWay:true
        }]
      });
      betslipDataService.getActiveSinglesIds.and.returnValue('1');
      betslipDataService.bets = [{
        params:{
          eachWayAvailable: 'Y',
          lottoData: {
            id:'124',
            isLotto :false
          }
        },
        info: () => ({
          type: 'SGL', Bet: {params:{
            eachWayAvailable: 'Y'
          }, price: { type: 'LP' } }
        }),
        stake: {}, betOffer: {}
      }, {
        params : {
          lottoData:{}
         },
        info: () => ({
          type: 'SGL', Bet: { price: { type: 'LP' } }
        }),
        stake: {}, betOffer: {},
       
      }, {
        params : {
          lottoData: {
            id:'124',
            isLotto :false
          }
         },
        info: () => ({ 
          type: 'DBL' , Bet: { price: { type: 'LP' } }
        }),
       
      }, {
        params : {
          lottoData: {
            id:'124',
            isLotto :false
          }
         },
        info: () => ({
          type: 'SGL', Bet: { price: { type: 'DIVIDEND' } }
        })
      }];
      service['betslipDataService'] = betslipDataService;
      service['restoreMultipleUserStakes']();
      expect(betslipDataService.getActiveSinglesIds).toHaveBeenCalled();
    });
  });

  it('restoreMultiplesFreeBetData', () => {
    storageService.get.and.returnValue({
      stakeData: [
        { betId: 0 },
        { betId: 1, userFreeBet: 1, storeId: 1 },
        { betId: 2, userFreeBet: 2, storeId: 2 },
        { betId: 3 }
      ]
    });

    service['restoreMultiplesFreeBetData']([{
      Bet: {
        params: {
           lottoData: { 
            id: { includes: jasmine.createSpy() },
            isLotto : true,
            details:{
              stake:1
            },
            accaBets:[{ stake:1}]
         }
        },
      }
    }, {
      Bet: {
        params: {
          lottoData: { 
            id: '123',
            isLotto : true,
            details:{
              stake:1
            },
            accaBets:[{ stake:1}]
         }
        },
        storeId: 1,
        freeBets: [{}, { id: 1 }]
      },
      stake: {}
    }, {
      Bet: {
        params: {
        lottoData: { 
              id: '123',
              isLotto : true,
              details:{
                stake:1
              },
              accaBets:[{ stake:1}]
           }
        },
        storeId: 2,
        freeBets: [{}, { id: 2 }]
      },
      stake: {},
      isEachWay: true
    }] as any);

    expect(storageService.get).toHaveBeenCalledWith('multipleUserStakes');
    expect(localeService.getString).toHaveBeenCalledTimes(2);
  });

  it('getOutcomesIds', () => {
    expect(service.getOutcomesIds().length).toBe(0);
    expect(
      service.getOutcomesIds([{ outcomesIds: ['1'] }] as any).length
    ).toBe(1);
  });

  it('should return event and set null to event property', () => {
    const sportEventObservable = {} as Observable<ISportEvent[]>;
    betSelectionsService.bets[0] = {
      params: { 
        lottoData:{isLotto: true}
       }
    };
    const multipleSelectionData =[]

    service.eventToBetslipObservable = sportEventObservable;

    const actualResult = service.useEventToBetslipObservable();

    expect(actualResult).toBe(sportEventObservable);
    expect(service.eventToBetslipObservable).toBeNull();
    expect(multipleSelectionData).toEqual([]);
    
  });

  it('syncWithNative', () => {
    service.syncWithNative();
    expect(pubSubService.publish).toHaveBeenCalledWith('SYNC_BETSLIP_TO_NATIVE', []);
  });
});
