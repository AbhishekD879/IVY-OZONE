import PoolBetBase from './pool-bet-base.class';
import quadpodBet from './../../mocks/quadpotBet.mock';

describe('PoolBetBase', () => {
  let bet;
  let betHistoryMainService;
  let userService;
  let localeService;
  let timeService;
  let cashOutMapIndexService;
  let instance: PoolBetBase;
  let currencyPipe;

  beforeEach(() => {
    bet = Object.assign({}, quadpodBet);

    betHistoryMainService = {
      getBetStatus: jasmine.createSpy('getBetStatus').and.returnValue('pending')
    };
    userService = {
      currencySymbol: '$'
    };
    localeService = {};
    timeService = {};
    cashOutMapIndexService = {
      create: jasmine.createSpy('cashOutMapIndexService.create')
    };

    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };

    instance = new PoolBetBase(
      bet,
      betHistoryMainService,
      userService,
      localeService,
      timeService,
      cashOutMapIndexService,
      currencyPipe
    );
  });

  it('constructor', () => {
    expect(instance.date).toBe('2019-05-15 12:26:00');
    expect(instance.id).toBe('44037');
    expect(betHistoryMainService.getBetStatus).toHaveBeenCalled();
    expect(instance.lines).toBe(2);
    expect(instance.receipt).toBe('P/0187387/0000128');
    expect(instance.stake).toBe('4.00');
    expect(instance.totalStake).toBe('5.88$');
    expect(instance.tokenValue).not.toBeDefined();
    expect(instance.winLines).toBe('0');
    expect(instance.currency).toBe('$');
    expect(instance.numLegs).toBe(4);
    expect(instance.isSettled).toBeFalsy();
    expect(instance.showLegsNumberInTitle).toBeFalsy();
    expect(instance.showEstimatedReturns).toBeTruthy();
    expect(instance.showStakeAndLines).toBeFalsy();
    expect(instance.totalReturns).toBeNull();
    expect(instance.poolType).toBe('Quadpot');
    expect(instance.leg).toBeDefined();
    expect(instance.event).toEqual([]);
    expect(instance.outcome).toEqual([]);
    expect(instance.market).toEqual([]);
    expect(instance.events).toEqual({});
    expect(instance.markets).toEqual({});
    expect(instance.outcomes).toEqual({});
  });

  describe('isSuspended', () => {
    it('should return false if bet no one leg is suspended', () => {
      expect(instance.isSuspended).toBeFalsy();
    });
    it('should return true if bet no one leg is suspended', () => {
      instance.leg[0].status = 'suspended';
      expect(instance.isSuspended).toBeTruthy();
    });
  });

  describe('_getTotalReturns', () => {
    it('should return winnings value for settled non void bet', () => {
      instance.isSettled = true;
      instance.status = 'won';
      expect(instance._getTotalReturns()).toEqual('5.00$');
    });
    it('should return refund value for settled void bet', () => {
      instance.isSettled = true;
      instance.status = 'void';
      expect(instance._getTotalReturns()).toEqual('3.00$');
    });
    it('should return null for open bet', () => {
      instance.isSettled = false;
      expect(instance._getTotalReturns()).toBeNull();
    });
  });

  describe('_normalizeDate', () => {
    it('should format date string to have correct TZD sign', () => {
      expect(instance._normalizeDate('2018-03-12 13:39:20')).toEqual('2018-03-12T13:39:20');
    });
  });

  describe('_fillIdsProperties', () => {
    it('should fill ids properties for events, markets and outcomes', () => {
      instance._fillIdsProperties();
      expect(instance.event).toEqual([ '9771687', '9771688', '9771689', '9771690' ]);
      expect(instance.market).toEqual([ '145099699', '145099700', '145099701', '145099702' ]);
      expect(instance.outcome).toEqual([ '542164253', '542164254', '542164264', '542164279', '542164288' ]);
      expect(instance.leg.map(leg => leg.eventId)).toEqual([ '9771687', '9771688', '9771689', '9771690' ]);
      expect(instance.leg.map(leg => leg.marketId)).toEqual([ '145099699', '145099700', '145099701', '145099702' ]);
      const parts = instance.leg.map(leg => leg.part).reduce((x, y) => x.concat(y), []);
      expect(parts.map(part => part.eventId)).toEqual([ '9771687', '9771687', '9771688', '9771689', '9771690' ]);
      expect(parts.map(part => part.outcomeId)).toEqual([ '542164253', '542164254', '542164264', '542164279', '542164288' ]);
      expect(parts.map(part => part.marketId)).toEqual([ '145099699', '145099699', '145099700', '145099701', '145099702' ]);
    });
  });

  describe('_updateCashoutMapIndex', () => {
    it('should properly update cashOutMapIndexService service', () => {
      const eventIds = [ '9771687', '9771688', '9771689', '9771690' ];
      const marketIds = [ '145099699', '145099700', '145099701', '145099702' ];
      const outcomeIds = [ '542164253', '542164254', '542164264', '542164279', '542164288' ];
      instance._updateCashoutMapIndex(instance.leg);
      for (let i = 0; i < eventIds.length; i++) {
        expect(cashOutMapIndexService.create).toHaveBeenCalledWith('event', eventIds[i], instance.id, false);
      }

      for (let i = 0; i < marketIds.length; i++) {
        expect(cashOutMapIndexService.create).toHaveBeenCalledWith('market', marketIds[i], instance.id, false);
      }

      for (let i = 0; i < outcomeIds.length; i++) {
        expect(cashOutMapIndexService.create).toHaveBeenCalledWith('outcome', outcomeIds[i], instance.id, false);
      }
    });
  });

  describe('addCurrency', () => {
    it('should `t add currency for undefined and zero', () => {
      expect(instance['addCurrency'](undefined, '£')).toEqual(undefined);
    });
    it('should add currency for number', () => {
      expect(instance['addCurrency'](5.88, '£')).toEqual('5.88£');
      expect(currencyPipe.transform).toHaveBeenCalledWith(5.88, '£', 'code');
    });
    it('should not add currency to N/A', () => {
      expect(instance['addCurrency']('N/A', '£')).toEqual('N/A');
    });
    it('should not add currency to zero', () => {
      expect(instance['addCurrency']('0.00', '£')).toEqual('0.00£');
    });
  });
});
