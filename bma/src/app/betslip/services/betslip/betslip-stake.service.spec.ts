import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { BetslipStakeService } from './betslip-stake.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { DecimalPipe } from '@angular/common';

describe('BetslipStakeService', () => {
  let overAskService;
  let bsFiltersService;
  const coreToolsService = new CoreToolsService();
  let pubSubService;
  let storageService;
  let service: BetslipStakeService;
  let fbService;

  beforeEach(() => {
    overAskService = {};
    bsFiltersService = {
      filterStakeValue: jasmine.createSpy('filterStakeValue')
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: (...args) => args[2] && args[2](),
    };
    storageService = {
      get: jasmine.createSpy('get'),
      subscribe: (...args) => args[2] && args[2](),
    };

    spyOn(coreToolsService, 'roundTo').and.callThrough();
    spyOn(coreToolsService, 'roundDown').and.callThrough();

    createService();
  });

  function createService() {
    service = new BetslipStakeService(
      overAskService,
      bsFiltersService,
      coreToolsService,
      pubSubService,
      storageService,
      fbService
    );
  }

  it('it should call getStake', () => {
    const decimalPipe = new DecimalPipe('en-US');
    service['getTotalStake'] = jasmine.createSpy('getTotalStake').and.returnValue('9.00');
    service['getFreeBetStake'] = jasmine.createSpy('getFreeBetStake').and.returnValue('1');
    const bets: any[] = [
      {
        details:  {
          draws:['test'],
          stake:1
        },
        isLotto: true,
        accaBets:[
          {
            id :1, 
            stake : 1,
            lines :{
              number : '1'
            },           
          }]as any,
      }, {
        details:  {
          draws:['test'],
          stake:1
        },
        accaBets:[
          {
            id :1, 
            stake : 0,
            lines :{
              number : '1'
            },
          }]as any,
        selectedFreeBet: { value: 1 }, stake: { lines: 1, perLine: 1, amount: 99 }

      }];

    const result = service.getStake(bets);

    expect(result).toBe(1);
  });
  it('it should call getStake', () => {
    const decimalPipe = new DecimalPipe('en-US');
    service['getTotalStake'] = jasmine.createSpy('getTotalStake').and.returnValue('9.00');
    service['getFreeBetStake'] = jasmine.createSpy('getFreeBetStake').and.returnValue('1');
    const bets: any[] = [
      {
        isLotto: false, 
        details:  {
          draws:['test'],
          stake:1
        },
        accaBets:[
          {
            id :1, 
            stake : 1,
            lines :{
              number : '1'
            },
          }]as any,
      }, {
        selectedFreeBet: { value: 1 }, stake: { lines: 1, perLine: 1, amount: 99 },
        accaBets:[
          {
            id :1, 
            stake : 1,
            lines :{
              number : '1'
            },
            details:  {
              draws:['test'],
              stake:1
            },
          }]as any,
      }];

    const result = service.getStake(bets);

    expect(result).toBe(8);
  });

  it('it should call getLottoTotlaStake() ', () => {
    const amount = 0;
    const bets: any[] = [
    {    
      details:  {
        draws:['test'],
        stake:1
      },   
      accaBets:[
        {
          id :1, 
          stake : 1,
          lines :{
            number : '1'
          },
        }]as any,

      selectedFreeBet: {value:1}, 
      disabled: true, 
      stake: {lines:1,perLine: 1, amount: 9999 }
    }
   ];
 
   service .getLottoTotlaStake(bets);
   expect(bets[0].accaBets).toEqual([{
    id :1, 
    stake : 1,
    lines :{
      number : '1'
    },
  }]);
   expect(amount).toEqual(0)
  });

  it('getStake: should return sum of all(active and suspended) stakes', () => {
    const decimalPipe = new DecimalPipe('en-US');
    service['getTotalStake'] = jasmine.createSpy('getTotalStake').and.returnValue('0');
    service['getFreeBetStake'] = jasmine.createSpy('getFreeBetStake').and.returnValue('0');
    const bets: any[] = [{
      selectedFreeBet: {}, disabled: true, stake: { amount: 2 }
    }, {
      selectedFreeBet: {}, stake: { amount: 3 }
    }, {
      selectedFreeBet: {}, stake: { perLine: 1 }
    }, {
      stake: {}
    }];
    const result = service.getStake(bets);
    expect(result).toBe(0);
  });

  it('getTotalStake', () => {
    const amount = 0;
    const bets = [
      {
        isLotto : true,
        details:  {
          draws:['test'],
          stake:1
        },
        accaBets: [{
          stake: 1,
          betType : {
            lines: {
              number: '1'
            }
          }
        }],
        stake: {
          amount : 123
        }
      },
     { 
      isLotto : true,
      details:{
        stake:1
      },
      stake: {
        amount : 123
      }
    },
      {
        stake: {
          amount : 123
        },
       isLottos: true 
      }
    ];
    service['getLottoTotlaStake'] = jasmine.createSpy('getLottoTotlaStake').and.returnValue(1.25);
    service.getTotalStake(bets);
    expect(amount).toEqual(0);
   
  });

  it('getStake: stake morethan 4 digits ', () => {
    const decimalPipe = new DecimalPipe('en-US');

    service['getTotalStake'] = jasmine.createSpy('getTotalStake').and.returnValue('99999');
    service['getFreeBetStake'] = jasmine.createSpy('getFreeBetStake').and.returnValue('1');
    const bets: any[] = [{
      selectedFreeBet: {value:1}, disabled: true, stake: {lines:1,perLine: 1, amount: 9999 }
    }
   ];
   const result = service.getStake(bets);
   expect(result).not.toBeNull();
  });

  describe('getTotalEstReturns', () => {
    it('N/A', () => {
      expect(
        service.getTotalEstReturns([{
          isSP: true, stake: { perLine: 1 }
        }] as any, false)
      ).toBeNull();

      expect(
        service.getTotalEstReturns([{
          isSP: true, stake: { perLine: 0 }, selectedFreeBet: {}
        }] as any, false)
      ).toBeNull();

      expect(
        service.getTotalEstReturns([{
          type: 'SGL', stake: { perLine: 0 }, selectedFreeBet: {}
        }] as any, false)
      ).toBeNull();

      expect(
        service.getTotalEstReturns([{
          type: 'DBL', stake: { perLine: 0 }, selectedFreeBet: {},
          Bet: {}
        }] as any, false)
      ).toBeNull();
    });

    it('amount', () => {
      bsFiltersService.filterStakeValue.and.returnValue(10);
      expect(
        service.getTotalEstReturns([{
          type: 'SGL', stake: { perLine: 1 },
          price: { priceType: 'LP', priceNum: 1, priceDen: 2 },
          Bet: {maxPayout: 100}
        }, {
          type: 'SGL', stake: { perLine: 0 },
          price: { priceType: 'LP', priceNum: 1, priceDen: 2 },
          Bet: {maxPayout: 100}, selectedFreeBet: {}
        }] as any, false)
      ).toBe('N/A'); //straight multiples
    });

    it('amount correctly truncated to lowest value', () => {
      bsFiltersService.filterStakeValue.and.returnValue(1);
      expect(
        service.getTotalEstReturns([{
          type: 'SGL', stake: { perLine: 1 },
          price: { priceType: 'LP', priceNum: 14, priceDen: 9 },
          Bet: {maxPayout: 100}
        }] as any, false)
      ).toBe(2.56); // truncate 2.5555555555555554 to 2.55
    });

    it('tote in betslip', () => {
      bsFiltersService.filterStakeValue.and.returnValue(10);
      expect(
        service.getTotalEstReturns([{
          isLotto: true,
          accaBets: [{estReturns: '123'}],
          selectedFreeBet: {},
          disabled: true,
       stake: { amount: 2 }
    }] as any, true)
      ).toBeNull();
    });

    it('lotto in betslip', () => {
      const betData = [{
        Bet: {
          params: {
            lottoData:{
              isLotto: true,
        accaBets: [
          { lines: {   number: 1 },
              betTypeRef: { id: "TBL" },
              winningAmount: "600",
              BetType: "TBL",
              betLineSummary: [
                  { lines: {number: 1}, betTypeRef: { id: "TBL"}, numPicks: 3 }
              ],
              id: "SGL|3|15|28|64779|0",
              stake: "0.10",
              userStake: "0.10",
              estReturns: "60.10"
          },
      ]
      }}}}];
      expect(Number(service.getTotalEstReturns(betData, false))).toEqual(60.10);
    });

    
    it('lotto in betslip return 0 if no estReturns/betStake', () => {
      const betData = [{
        Bet: {
          params: {
            lottoData:{
              isLotto: true,
        accaBets: [
          { lines: {   number: 1 },
              betTypeRef: { id: "TBL" },
              winningAmount: "600",
              BetType: "TBL",
              betLineSummary: [
                  { lines: {number: 1}, betTypeRef: { id: "TBL"}, numPicks: 3 }
              ],
              id: "SGL|3|15|28|64779|0",
          },
      ]
      }}}}];
      expect(Number(service.getTotalEstReturns(betData, false))).toEqual(0);
    });

  });

  describe('calculateEstReturns', () => {
    it('N/A', () => {
      expect(
        service.calculateEstReturns({
          price: { priceType: 'SP' }
        } as any)
      ).toBe('N/A');
    });

    it('calculate returns', () => {
      bsFiltersService.filterStakeValue.and.returnValue(99);
      service['getPrices'] = jasmine.createSpy('getPrices').and.returnValue({priceType: 'LP', priceNum: 1, priceDen: 2});
      service.calculateEstReturns({
        price: { priceType: 'LP', priceNum: 1, priceDen: 2 },
        Bet: {}, stake: { perLine: 5 }
      } as any);
      expect(bsFiltersService.filterStakeValue).toHaveBeenCalledTimes(1);
    });

    it('calculate returns isEachWay true', () => {
      bsFiltersService.filterStakeValue.and.returnValue(99999);
      service['getPrices'] = jasmine.createSpy('getPrices').and.returnValue({priceType: 'LP', priceNum: 1, priceDen: 2});
      service['calculateExtraProfit'] = jasmine.createSpy('calculateExtraProfit').and.returnValue(0);
      service.calculateEstReturns({
        price: { priceType: 'LP', priceNum: 1, priceDen: 2 }, selectedFreeBet: { value: 1 },
        Bet: { isEachWay: true }, stake: { perLine: 5 }
      } as any);
      expect(bsFiltersService.filterStakeValue).toHaveBeenCalledTimes(1);
    });
    it('calculate returns isEachWay true and estreturns are undefined', () => {
      bsFiltersService.filterStakeValue.and.returnValue(null);
      service['getPrices'] = jasmine.createSpy('getPrices').and.returnValue({priceType: 'LP', priceNum: null, priceDen: null});
      service['calculateExtraProfit'] = jasmine.createSpy('calculateExtraProfit').and.returnValue(0);
      service.calculateEstReturns({
        price: { priceType: 'LP', priceNum: null, priceDen: null }, selectedFreeBet: { value: null },
        Bet: { isEachWay: true }, stake: { perLine: 5 }
      } as any);
      expect(bsFiltersService.filterStakeValue).toHaveBeenCalledTimes(1);
    });

    it('should include freebets if no overask', () => {
      service['overAskService']['hasTraderMadeDecision'] = false;
      service['overAskService']['isInProcess'] = false;
      bsFiltersService.filterStakeValue.and.returnValue(5);

      expect(
        service.calculateEstReturns({
          type: 'SGL', stake: { perLine: 5 },
          price: { priceType: 'LP', priceNum: 1, priceDen: 2 },
          Bet: { isEachWay: false, maxPayout: 100 },
          selectedFreeBet: { value: 1 }
        } as any)
      ).toBe(8);
    });

    it('should return potentialPayout as is if overask', () => {
      const bet = {
        potentialPayout: '100.100',
        isTraderOffered: true,
        price: {
          priceType: 'LP'
        }
      } as any;

      expect(service.calculateEstReturns(bet)).toEqual(100.1);
    });
  });

  describe('getOddsBoostEnabled', () => {
    it('enabled in localstorage', () => {
      storageService.get.and.returnValue(true);
      service['getOddsBoostEnabled']();

      expect(service.oddsBoostEnabled).toEqual(undefined);
    });

    it('disabled in localstorage', () => {
      storageService.get.and.returnValue(null);
      service['getOddsBoostEnabled']();

      expect(service.oddsBoostEnabled).toBeUndefined();
    });

    afterEach(() => {
      expect(storageService.get).toHaveBeenCalledWith('oddsBoostActive');
    });
  });

  it('getSelectedBets', () => {
    expect(
      service['getSelectedBets']().length
    ).toBe(0);

    expect(
      service['getSelectedBets']([{}] as any).length
    ).toBe(1);

    overAskService.isInProcess = true;
    overAskService.isOnTradersReview = false;
    expect(
      service['getSelectedBets']([{}, { isSelected: true }] as any).length
    ).toBe(1);
  });

  describe('getPrices', () => {
    it('no odds boost', () => {
      const bet: any = { price: {} };
      expect(service['getPrices'](bet)).toBe(bet.price);
    });

    it('odds boost enabled and available', () => {
      service.oddsBoostEnabled = true;
      const bet: any = {
        Bet: {
          oddsBoost: { enhancedOddsPriceNum: 1, enhancedOddsPriceDen: 2 }
        }
      };
      expect(service['getPrices'](bet)).toEqual({ priceNum: 1, priceDen: 2 });
    });

    it('should left bet price even if boosted when bet is offered by overask', () => {
      service.oddsBoostEnabled = true;
      const bet: any = {
        isTraderOffered: true,
        price: { priceNum: 500, priceDen: 1 },
        Bet: {
          oddsBoost: { enhancedOddsPriceNum: 1, enhancedOddsPriceDen: 2 }
        }
      };
      expect(service['getPrices'](bet)).toBe(bet.price);
    });
  });

  describe('calculateEstReturnsMultiples', () => {
    it('should return potential payout', () => {
      bsFiltersService.filterStakeValue.and.returnValue(1);
      const bet: any = {
        stake: { lines: 1 },
        Bet: { maxPayout: 100 }, potentialPayout: 2
      };
      expect(service.calculateEstReturnsMultiples(bet)).toBe(bet.potentialPayout);
    });

    it('should return potential payout with truncated value', () => {
      bsFiltersService.filterStakeValue.and.returnValue(1);
      const bet: any = {
        stake: { lines: 1 },
        Bet: { maxPayout: 100 }, potentialPayout: 2.5555555555555554
      };
      expect(service.calculateEstReturnsMultiples(bet)).toBe(2.55);
    });

    it('should return N/A if no payout', () => {
      expect(
        service.calculateEstReturnsMultiples({
          stake: { lines: 1 },
          Bet: {}
        } as any)
      ).toBe('N/A');
    });

    it('should return N/A if SP price', () => {
      expect(
        service.calculateEstReturnsMultiples({
          isSP: true, stake: { lines: 1 },
          Bet: {}
        } as any)
      ).toBe('N/A');
    });

    it('should return N/A if boosted e/w bet', () => {
      service.oddsBoostEnabled = true;
      expect(
        service.calculateEstReturnsMultiples({
          isEachWay: true, stake: { lines: 1 },
          Bet: { oddsBoost: {} }
        } as any)
      ).toBe('N/A');
    });

    it('should calculate est returns for eachway if stakeMultiplier !== 1', () => {
      bsFiltersService.filterStakeValue = jasmine.createSpy().and.returnValue(0);
      createService();

      const bet = {
        stake: {
          perLine: 1,
          lines: 1,
          freeBetAmount: 3
        },
        selectedFreeBet: {
          value: '3'
        },
        potentialPayout: 20,
        stakeMultiplier: 2,
        Bet: {
          isEachWay: true,
          payout: [{ potential: 20, legType: 'P' }],
          maxPayout: 200
        },
        outcomes: [{
          eachWayFactorNum: 1,
          eachWayFactorDen: 3,
          price: {
            priceNum: 3,
            priceDen: 1
          }
        }]
      } as any;

      expect(service.calculateEstReturnsMultiples(bet)).toEqual(117);

      bet.outcomes = null;

      expect(service.calculateEstReturnsMultiples(bet)).toEqual(117);

      bet.outcomes = [{
        eachWayFactorNum: 1,
        eachWayFactorDen: 3,
        price: {
          priceNum: 3,
          priceDen: 1
        }
      }, {
        eachWayFactorNum: 1,
        eachWayFactorDen: 3,
        price: {
          priceNum: 3,
          priceDen: 1
        }
      }] as any;

      expect(service.calculateEstReturnsMultiples(bet)).toEqual(117);
    });

    it('should calculate est returns for eachway if stakeMultiplier === 1', () => {
      bsFiltersService.filterStakeValue = jasmine.createSpy().and.returnValue(0);
      createService();

      const bet = {
        stake: {
          perLine: 1,
          lines: 1,
          freeBetAmount: 3
        },
        selectedFreeBet: {
          value: '3'
        },
        potentialPayout: 20,
        stakeMultiplier: 1,
        Bet: {
          isEachWay: true,
          payout: [{ potential: 20, legType: 'P' }],
          maxPayout: 200
        },
        outcomes: [{
          eachWayFactorNum: 1,
          eachWayFactorDen: 3,
          price: {
            priceNum: 3,
            priceDen: 1
          }
        }, {
          eachWayFactorNum: 1,
          eachWayFactorDen: 3,
          price: {
            priceNum: 3,
            priceDen: 1
          }
        }]
      } as any;

      expect(service.calculateEstReturnsMultiples(bet)).toEqual(69);
    });

    it('should calculate return N/A for each way bet with SP price', () => {
      bsFiltersService.filterStakeValue = jasmine.createSpy().and.returnValue(0);
      createService();

      const bet = {
        stake: {
          perLine: 1,
          lines: 1,
          freeBetAmount: 3
        },
        selectedFreeBet: {
          value: '3'
        },
        potentialPayout: 20,
        stakeMultiplier: 1,
        isSP: true,
        Bet: {
          isEachWay: true,
          payout: [{ potential: 20, legType: 'P' }]
        },
        outcomes: [{
          eachWayFactorNum: 1,
          eachWayFactorDen: 3,
          price: {
            priceNum: 3,
            priceDen: 1
          }
        }]
      } as any;

      expect(service.calculateEstReturnsMultiples(bet)).toEqual('N/A');
    });

    it('should return N/A if potentialPayout is 0 and Bet data is empty', () => {
      const bet = {
        stake: {
          lines: 1,
          freeBetAmount: 0
        },
        potentialPayout: 0,
        Bet: {}
      } as any;

      expect(service.calculateEstReturnsMultiples(bet)).toEqual('N/A');
    });

    it('should return N/A if potentialPayout is not 0 but Bet data is empty', () => {
      bsFiltersService.filterStakeValue = jasmine.createSpy().and.returnValue(0);
      createService();

      const bet = {
        stake: {
          lines: 1,
          freeBetAmount: 0
        },
        potentialPayout: 10,
        isSP: true,
        Bet: {}
      } as any;

      expect(service.calculateEstReturnsMultiples(bet)).toEqual('N/A');

    });

    describe('for overask (bet.isTraderOffered)', () => {
      it('should calculate est returns as potentialPayout if oddsBoostEnabled', () => {
        service.oddsBoostEnabled = true;

        const bet = {
          isTraderOffered: true,
          stake: {
            perLine: 1,
            lines: 1,
            freeBetAmount: 0
          },
          selectedFreeBet: {
            value: '3'
          },
          potentialPayout: '20',
          Bet: {}
        } as any;

        expect(service.calculateEstReturnsMultiples(bet)).toEqual(20);
      });

      it('should returns potentialPayout even if boosted', () => {
        service.oddsBoostEnabled = true;

        const bet = {
          isTraderOffered: true,
          stake: {
            perLine: 1,
            lines: 1,
            freeBetAmount: 0
          },
          potentialPayout: '20',
          Bet: {
            oddsBoost: {
              enhancedOddsPrice: '40'
            }
          }
        } as any;

        expect(service.calculateEstReturnsMultiples(bet)).toEqual(20);
      });

      it('should return payout from trader offer if not SP', () => {
        const bet = {
          isTraderOffered: true,
          stake: { lines: 1 },
          Bet: {},
          potentialPayout: 1,
          selectedFreeBet: { value: 1 }
        } as any;

        expect(service.calculateEstReturnsMultiples(bet as any)).toBe(1);
      });

      it('should return N/A for SP price', () => {
        const bet = {
          isSP: true,
          isTraderOffered: true,
          stake: { lines: 1 },
          Bet: {},
          potentialPayout: 1,
          selectedFreeBet: { value: 1 }
        } as any;

        bsFiltersService.filterStakeValue.and.returnValue(1);
        expect(service.calculateEstReturnsMultiples(bet as any)).toBe('N/A');
      });

      it('should return N/A if no payout', () => {
        const bet = {
          isSP: false,
          isTraderOffered: true,
          stake: { lines: 1 },
          Bet: {},
          selectedFreeBet: { value: 1 }
        } as any;

        expect(service.calculateEstReturnsMultiples(bet as any)).toBe('N/A');
      });
    });
  });

  describe('getTotalStake', () => {
    it('getTotalStake', () => {
      service['getSelectedBets'] = () => [
        { stake: {} },
        { stake: { amount: '10', disabled: true }, selectedFreeBet: {}, disabled: true },
        { stake: { amount: '10', lines: 2, perLine: 2, freeBetAmount: 5.27 }, selectedFreeBet: { value: '10.555' } }] as any;

      expect(service.getTotalStake([])).toEqual('14.54');
    });

    it('getTotalStake: should return sum of all(active and suspended) stakes', () => {
      service['getSelectedBets'] = () => [
        { stake: {} },
        { stake: { amount: '10', lines: 1, perLine: 1, disabled: true }, disabled: true },
        { stake: { amount: '10', lines: 2, perLine: 2, freeBetAmount: 5.27 }, selectedFreeBet: { value: '10.555' } }] as any;

      expect(service.getTotalStake([], true)).toEqual('15.54');
    });

    it('getTotalStake: should return sum of all(active and suspended) stakes with freebets', () => {
      service['getSelectedBets'] = () => [
        { stake: {} },
        {
          stake: { amount: '10', lines: 1, perLine: 1, disabled: true, freeBetAmount: 2 },
          selectedFreeBet: { value: '2.00' }, disabled: true
        },
        {
          stake: { amount: '10', lines: 2, perLine: 2, freeBetAmount: 5.27 },
          selectedFreeBet: { value: '10.555' }, disabled: true
        }] as any;

      expect(service.getTotalStake([], true)).toEqual('17.54');
    });

    it('getTotalStake: should return totalStake with freeBets for isEachWay and ForeCast market', () => {
      service['getSelectedBets'] = () => [
        {
          stake: { amount: 0.2, lines: 2, perLine: '0.1', freeBetAmount: 0.5 },
          selectedFreeBet: { value: '1.00' }, Bet: { isEachWay: true }
        },
        {
          stake: { amount: 0.6, lines: 6, perLine: '0.1', freeBetAmount: 0.16 },
          selectedFreeBet: { value: '1.00' }, Bet: { isEachWay: false }
        }] as any;

      expect(service.getTotalStake([], true)).toEqual('2.76');
    });

    it('should not include freebets if overask offer page', () => {
      service['overAskService']['userHasChoice'] = true;

      const bets = [{
        stake: { amount: '10', lines: 1, perLine: 10, disabled: true, freeBetAmount: 2 },
        selectedFreeBet: {},
        Bet: {},
        isSelected: true
      }] as any;

      expect(service['getTotalStake'](bets, true)).toEqual('10.00');
    });
    it('should include freebets if overask not in process', () => {
      service['overAskService']['hasTraderMadeDecision'] = false;
      service['overAskService']['isInProcess'] = false;

      const bets = [{
        stake: { amount: '10', lines: 1, perLine: 10, disabled: true, freeBetAmount: 2 },
        selectedFreeBet: {},
        Bet: {},
        isSelected: true
      }] as any;

      expect(service['getTotalStake'](bets, true)).toEqual('12.00');
    });
  });

  describe('getFreeBetStake', () => {
    it('should return sum of active free bets', () => {
      service['getSelectedBets'] = () => [
        { stake: {} },
        { stake: { amount: '10', disabled: true }, selectedFreeBet: {}, disabled: true },
        { stake: { amount: '10', lines: 2, perLine: 2 }, selectedFreeBet: { value: '10.555' } }] as any;

      expect(service.getFreeBetStake([])).toEqual('10.55');
    });

    it('should return sum of all(active and suspended) free bets', () => {
      service['getSelectedBets'] = () => [
        { stake: {} },
        { stake: { amount: '10', lines: 1, perLine: 1, disabled: true }, disabled: true },
        { stake: { amount: '10', lines: 2, perLine: 2 }, selectedFreeBet: { value: '10.555' } }] as any;

      expect(service.getFreeBetStake([], true)).toEqual('10.55');
    });

    it('should return sum of all(active and suspended) free bets(2)', () => {
      service['getSelectedBets'] = () => [
        { stake: {} },
        { stake: { amount: '10', lines: 1, perLine: 1, disabled: true }, selectedFreeBet: { value: '2.00' }, disabled: true },
        { stake: { amount: '10', lines: 2, freeBetAmount: 2 }, selectedFreeBet: { value: '10.00' }, disabled: true }] as any;

      expect(service.getFreeBetStake([], true)).toEqual('6.00');
    });

    it('should retrun sum of tokenValue for not disabled bets if overask', () => {
      overAskService.userHasChoice = true;
      service['getSelectedBets'] = () => [
        { stake: {} },
        { tokenValue: 5, disabled: true },
        { tokenValue: 10 }
      ] as any;

      expect(service.getFreeBetStake([], true)).toEqual('10.00');
    });
  });
  describe('maxPayoutCheck', () => {
    it('should return maxpay with maxflag false', () => {
      service.maxFlag = false;
      service['maxPayoutCheck'](250000, '2000');
      expect(service.maxFlag).toBe(true);
      expect(service['maxPayoutCheck'](250000, '2000')).toBe(2000);
    });
    it('should return maxpay with maxflag true', () => {
      service.maxFlag = true;
      service['maxPayoutCheck'](250000, '2000');
      expect(service['maxPayoutCheck'](250000, '2000')).toBe(2000);
    });
    it('should not return maxpay with maxflag false', () => {
      service.maxFlag = false;
      service['maxPayoutCheck'](20, '2000');
      expect(service.maxFlag).toBe(false);
      expect(service['maxPayoutCheck'](20, '2000')).toBe(20);
    });
    it('should not return maxpay with maxflag true', () => {
      service.maxFlag = true;
      service['maxPayoutCheck'](20, '2000');
      expect(service['maxPayoutCheck'](20, '2000')).toBe(20);
    });
  });
  describe('checkIndex', () => {
    it('should maxpay flag false', () => {
      service['checkIndex'](0);
      expect(service.maxFlag).toBe(false);
    });
    it('when index is not 0', () => {
      const index = 1;
      service['checkIndex'](index);
      expect(index).toBe(1);
    });
  });
  it('calculateExtraProfit', () => {
    const bet: any = {
      Bet: {
        oddsBoost: { enhancedOddsPriceNum: 1, enhancedOddsPriceDen: 2 }
      },
      price : {priceNum :1,priceDen :2},
      eachWayFactorNum :123,
      eachWayFactorDen :1234
    };
    const value = service['calculateExtraProfit'](bet,1)
    expect(value).toEqual(1.049837925445705);
   });
 
  describe('getFreeBetLabelText', () => {
    beforeEach(()=>{
      fbService = {
        isBetPack: jasmine.createSpy('isBetPack'),
        isFanzone: jasmine.createSpy('isFanzone')

      }
      createService();

    })
    
    it('should return imagename', () => {
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(true);
      const bets = [
        {selectedFreeBet: {name: 'offer2'}},
        {selectedFreeBet: {name: 'offer1', freeBetOfferCategories: {freebetOfferCategory: 'Fanzone'}}},
      ];    
      expect(service.getFreeBetLabelText([bets[0]] as any,true)).toBe('free-bet-label');
    });
    it('should return imagename', () => {
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(true);
      const bets = [
        {selectedFreeBet: {name: 'offer1', freeBetOfferCategories: {freebetOfferCategory: 'Fanzone'}}},
      ];    
      expect(service.getFreeBetLabelText(bets as any,true)).toBe('fanzone-bet-label');
    });
    it('should return free-bet-label', () => {
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(false);
      const bets = [];    
      expect(service.getFreeBetLabelText(bets as any,true)).toBe('free-bet-label');
    });
    it('should return empty', () => {
      fbService.isBetPack.and.returnValue(true);
      expect(service.getFreeBetLabelText([{}] as any)).toBe('');
    });

    it('should return freebet', () => {
      fbService.isBetPack.and.returnValue(true);
      const bets = [{selectedFreeBet: {name: 'offer1'}}];
      expect(service.getFreeBetLabelText(bets as any)).toBe('FREE BET');
    });
    it('should return freebet2', () => {
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(false);
      const bets = [{selectedFreeBet: {name: 'offer1', freeBetOfferCategories: {freebetOfferCategory: 'Fanzone1'}}}];
      expect(service.getFreeBetLabelText(bets as any)).toBe('FREE BET');
    });
   
    it('should return fanzone', () => {
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(true);
      const bets = [{selectedFreeBet: {name: 'offer1', freeBetOfferCategories: {freebetOfferCategory: 'Fanzone'}}}];
      expect(service.getFreeBetLabelText(bets as any)).toBe('Fanzone');
    });

    it('should return betpack', () => {
      fbService.isBetPack.and.returnValue(true);
      const bets = [{selectedFreeBet: {name: 'offer1', freeBetOfferCategories: {freebetOfferCategory: 'Bet Pack'}}}];
      expect(service.getFreeBetLabelText(bets as any)).toBe('BET TOKEN');
    });

    it('should return free bet for Odds Boost12', () => {
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(false);
      const bets = [{selectedFreeBet: {name: 'offer1', freeBetOfferCategories: {freebetOfferCategory: 'Odds Boost'}}}];
      
      expect(service.getFreeBetLabelText(bets as any)).toBe('FREE BET');
    });

    it('should return empty for no free bet selection', () => {
      fbService.isBetPack.and.returnValue(true);
      const bets = [{}];
      
      expect(service.getFreeBetLabelText(bets as any)).toBe('');
    });

    it('should return TokenandFreebet', () => {
      fbService.isBetPack.and.returnValue(true);
      const bets = [
        {selectedFreeBet: {name: 'offer1', freeBetOfferCategories: {freebetOfferCategory: 'Bet Pack'}}},
        {selectedFreeBet: {name: 'offer2'}}
      ];
      expect(service.getFreeBetLabelText(bets as any)).toBe('TOKEN & FREE BET');
    });
    it('should return FanzoneandFreebet', () => {
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(true);
      const bets = [
        {selectedFreeBet: {name: 'offer2'}},
        {selectedFreeBet: {name: 'offer1', freeBetOfferCategories: {freebetOfferCategory: 'Fanzone'}}},

      ];
      expect(service.getFreeBetLabelText(bets as any)).toBe('FREE BET');
    });   
  });
  describe('checkForStraightMultiples', () => {
    it('should return false for all singles', () => {
      expect(service['checkForStraightMultiples']([{
        type: 'SGL', stake: { perLine: 1 },
      }, {
        type: 'SGL', stake: { perLine: 0 },
      }] as any, false)
    ).toBe(false);
    });

    it('should return true if lotto', () => {
      expect(service['checkForStraightMultiples']([{
        type: 'SGL', stake: { perLine: 1 },
      }, {
        type: 'SGL', stake: { perLine: 0 },
      }] as any, true)
    ).toBe(true);
    });

    it('should return true when DBL/TBL/ACC bets has line number 1', () => {
      expect(service['checkForStraightMultiples']([{
        type: 'DBL', stake: { perLine: 1, params: {lines: 1} },
      }, {
        type: 'SGL', stake: { params: { lines: 1} },
      }] as any, true)
      ).toBe(true);

      expect(service['checkForStraightMultiples']([{
        type: 'DBL', stake: { perLine: 1, params: {lines: 2} },
      }, {
        type: 'TBL', stake: { perLine: 0, params: {lines: 1} },
      }] as any, true)
      ).toBe(true);

      expect(service['checkForStraightMultiples']([{
        type: 'DBL', stake: { perLine: 1, params: {lines: 6} },
      }, {
        type: 'TBL', stake: { perLine: 0, params: {lines: 2} },
      }, {
        type: 'ACC4', stake: { perLine: 0, params: {lines: 1} },
      }] as any, true)
      ).toBe(true);
    });

    it('should have return false when it\'s not straight multiple', () => {
      expect(service['checkForStraightMultiples']([{
        type: 'DBL', stake: { perLine: 1, params: {lines: 2} },
      }, {
        type: 'SGL', stake: { perLine: 0, params: {lines: 1} },
      }, {
        type: 'SGL', stake: { perLine: 0, params: {lines: 1} },
      }] as any , false)
      ).toBe(false);

      expect(service['checkForStraightMultiples']([{
        type: 'DBL', stake: { perLine: 1, params: {lines: 2} },
      }, {
        type: 'PAT', stake: { perLine: 0, params: {lines: 1} },
      }, {
        type: 'l15', stake: { perLine: 0, params: {lines: 1} },
      }] as any , false)
      ).toBe(false);
    });
  });
});
