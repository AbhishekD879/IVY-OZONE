import { IQuickbetSelectionModel } from './quickbet-selection.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';

describe('test IQuickbetSelectionModel', () => {
  let model: IQuickbetSelectionModel;
  let selection: any;
  let userService: any;
  let fracToDecService: any;
  let clientUserAgentService: any;
  const coreToolsService = new CoreToolsService();
  let storedState: any;
  let timeSyncService;
  beforeEach(() => {
    userService = {
      currencySymbol: '$'
    };
    selection = {};
    clientUserAgentService = {};
    fracToDecService = {};
    storedState = {
      userStake: false,
      userEachWay: false
    };
    timeSyncService = {
      ip: '192.168.3.1'
    };

    model = new IQuickbetSelectionModel(selection, storedState, userService, fracToDecService,
      clientUserAgentService, coreToolsService, timeSyncService);
  });

  it('constructor', () => {
    expect(model).toBeTruthy();
  });

  it('constructor  storedState userStake should be false false;', () => {
    storedState['userStake'] = false;
    expect(model).toBeTruthy();
  });

  describe('getPotentialPayout', () => {
    it('properly calculate potential payout and truncate value', () => {
      model.stake = '1';
      model.isLP = true;
      model.price = {
        priceNum: 14,
        priceDen: 9
      };
      expect((model as any).getPotentialPayout()).toEqual('2.56');
    });

    it('result should be 7.95', () => {
      model.stake = '';
      model.isLP = true;
      model.isEachWay = true;
      model.eachWayFactorNum = 14;
      model.eachWayFactorDen = 9;
      model.freebetValue = 4;
      model.price = {
        priceNum: 14,
        priceDen: 9
      };
      const result = model['getPotentialPayout']();
      expect(result).toEqual('7.95');
    });
  });

  describe('onStakeChange', () => {
    it('result should be', () => {
      model.stake = '';
      model.isLP = true;
      model['getPotentialPayout'] = jasmine.createSpy('getPotentialPayout').and.returnValue(1);
      model['onStakeChange']();
      expect(model['stakeAmount']).toEqual(0);
    });
  });

  describe('updateCurrency', () => {
    it('currency should be currencySymbol', () => {
      model.currency = '1';
      model.updateCurrency();
      userService.currencySymbol = jasmine.createSpy('currencySymbol').and.returnValue('$');
      expect(model.currency).toEqual('$');
    });
  });

  describe('updateHandicapValue', () => {
    it('currency should be handicapValue', () => {
      model.handicapValue = 'handicapValue';
      model.outcomeName = 'outcomeName';
      model.updateHandicapValue('updateHandicapValue');
      expect(model.handicapValue).toEqual('updateHandicapValue');
    });

    it('currency should be updateHandicapValue', () => {
      model.handicapValue = 'updateHandicapValue';
      model.outcomeName = 'outcomeName';
      model.updateHandicapValue('updateHandicapValue');
      expect(model.handicapValue).toEqual('updateHandicapValue');
    });

  });

  describe('formatHandicap', () => {
    it('currency should be currencySymbol', () => {
      const result = model.formatHandicap('123');
      expect(result).toEqual('+123.0');
    });

    it('currency should be -1', () => {
      const result = model.formatHandicap('-1');
      expect(result).toEqual('-1.0');
    });

  });

  describe('setOddsValue', () => {
    it('currency should be currencySymbol', () => {
      const eventData = {
        price: {
          priceNum: 111,
          priceDen: 222
        },
        oldOddsValue: {},
        oddsSelector: []
      } as any;
      fracToDecService.getFormattedValue = jasmine.createSpy('getFormattedValue').and.callFake((p1, p2) => {
        return p1 + p2;
      });
      model['setOddsValue'](eventData);
      expect(fracToDecService.getFormattedValue).toHaveBeenCalledWith(111, 222);
    });
  });

  describe('getPrices', () => {
    it('currency should be currencySymbol', () => {
      const price = {
        priceNum: 111,
        priceDen: 222,
        id: '112',
        priceDec: 111,
        priceType: 'priceType',
        isPriceChanged: true,
        isPriceUp: true,
        isPriceDown: true,
        priceTypeRef: {
          id: 'iid'
        }
      };
      model['isBoostActive'] = true;
      model['oddsBoost'] = {
        enhancedOddsPriceNum: 223,
        enhancedOddsPriceDen: 223
      } as any;

      const result = model['getPrices'](price);
      expect(result).toEqual({
        priceNum: 223,
        priceDen: 223
      });
    });
  });

  describe('formatBet', () => {
    beforeEach(() => {
      userService.bppToken = jasmine.createSpy('bppToken').and.returnValue('token');
      userService.currency = jasmine.createSpy('currency').and.returnValue('currency');
      clientUserAgentService.getId = jasmine.createSpy('getId').and.returnValue('1test23');
      timeSyncService.ip = jasmine.createSpy('ip').and.returnValue('http://0.0.0.0:9876/');
    });
    it('currency should be currencySymbol', () => {
      model['isEachWay'] = true;
      model['stake'] = 'stake';
      const result = model.formatBet();
      expect(result['clientUserAgent']).toEqual('1test23');
    });
    it('currency should be currencySymbol', () => {
      model['isEachWay'] = false;
      model['stake'] = '';
      const result = model.formatBet();
      expect(result['clientUserAgent']).toEqual('1test23');
    });

    it('currency should be currencySymbol', () => {
      model['isEachWay'] = false;
      model['stake'] = '';
      model['isLP'] = true;
      model['price'] = {
        priceNum: 111,
        priceDen: 222
      };
      model['freebet'] = {
        freebetTokenId: '22322'
      };
      model['freebetValue'] = 233;
      model['isBoostActive'] = true;
      model['handicapValue'] = '12212';
      const result = model.formatBet();
      expect(result['handicap']).toEqual(12212);
    });
  });

  describe('calculateExtraProfit', () => {
    it('should return 0', () => {
      const eventData = {
        price: {
          priceNum: 111,
          priceDen: 222
        },
        oldOddsValue: {},
        oddsSelector: []
      } as any;
      model.isEachWay = false;
      const result = model['calculateExtraProfit'](1, eventData.price);
      expect(result).toEqual(0);
    });

    it('should return 0 ', () => {
      const eventData = {
        price: {
          priceNum: 111,
          priceDen: 222
        },
        oldOddsValue: {},
        oddsSelector: []
      } as any;
      model.isEachWay = false;
      const result = model['calculateExtraProfit'](0, eventData.price);
      expect(result).toEqual(0);
    });

    it('should return 5 ', () => {
      const eventData = {
        price: {
          priceNum: 222,
          priceDen: 111
        },
        oldOddsValue: {},
        oddsSelector: []
      } as any;
      model.eachWayFactorNum = 222;
      model.eachWayFactorDen = 111;

      model.isEachWay = true;
      const result = model['calculateExtraProfit'](1, eventData.price);
      expect(result).toEqual(5);
    });
  });


  describe('setStatus', () => {
    it('eventStatusCode for event should be  set S', () => {
      model.setStatus(true, 'event');
      expect(model.eventStatusCode).toEqual('S');
    });

    it('eventStatusCode for event should be set A', () => {
      model.setStatus(false, 'event');
      expect(model.eventStatusCode).toEqual('A');
    });
    it('marketStatusCode for market should be set S', () => {
      model.setStatus(true, 'market');
      expect(model.marketStatusCode).toEqual('S');
    });

    it('marketStatusCode for market should be  set A', () => {
      model.setStatus(false, 'market');
      expect(model.marketStatusCode).toEqual('A');
    });
   it('outcomeStatusCode for outcome should be set S', () => {
      model.setStatus(true, 'outcome');
      expect(model.outcomeStatusCode).toEqual('S');
    });

    it('outcomeStatusCode for outcome should be set A', () => {
      model.setStatus(false, 'outcome');
      expect(model.outcomeStatusCode).toEqual('A');
    });
  });

  describe('restore quickbet with freebet', () => {
    beforeEach(() => {
      model = new IQuickbetSelectionModel(selection, { freebet: { name: 'freebet'}} as any, userService, fracToDecService,
        clientUserAgentService, coreToolsService, timeSyncService);
    });
    it('constructor', () => {
      expect(model).toBeTruthy();
      expect(model.freebet).toEqual({ name: 'freebet' } as any);
    });
  });
});
