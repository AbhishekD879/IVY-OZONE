import FootballJackpotBet from './football-jackpot-bet.class';

describe('FootballJackpotBet', () => {
  let model: FootballJackpotBet;
  let bet;
  let betHistoryMainService;
  let userService;
  let locale;
  let timeService;
  let cashOutMapIndex;
  let currencyPipe;

  const part = [{
    startTime: new Date().toISOString(),
    outcome: {
      name: '1',
      event: {
        startTime: new Date().toISOString(),
      },
      market: {},
      result: {
        value: 1,
        confirmed: 'Y'
      },
      eventCategory: {
        id: 16
      },
      outcomeResult: 'W'
    },
    price: [{
      priceNum: '1',
      priceDen: '2'
    }]
  }];

  beforeEach(() => {
    bet = {
      id: 1234,
      betType: {
        code: 'qwertyui'
      },
      leg: [{
        legType: {
          code: 'qwertyui'
        },
        name: 'legName',
        part: part
      }],
      stake: {
        stakePerLine: 1,
        value: 2,
        tokenValue: 1,
        poolStake: -1
      },
      cashoutValue: 10,
      partialCashoutAvailable: 'Y',
      source: 'f',
      date: '12/12/2020',
      numLines: 1,
      receipt: 'receipt',
      numLinesWin: 'numLinesWin',
      numLegs: 1,
      settled: 'Y',
      poolType: 'poolType',
      poolLeg: [],
      refund: {
        value: 'value'
      },
      winnings: {
        value: 'value'
      }
    } as any;
    betHistoryMainService = {
      getBetStatus: jasmine.createSpy('getBetStatus').and.returnValue('status')
    };
    userService = {
      currencySymbol: '$'
    };
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('footballJackpot')
    };
    timeService = {};
    cashOutMapIndex = {};
    currencyPipe = {
      transform: jasmine.createSpy('transform')
    };

    model = new FootballJackpotBet(
      bet,
      betHistoryMainService,
      userService,
      locale,
      timeService,
      cashOutMapIndex,
      currencyPipe
    );
  });

  describe('constructor', () => {
    it('should init values', () => {
      expect(model.isFootballJackpotBetModel).toEqual(true);
      expect(model.betTitle).toEqual('footballJackpot');
      expect(model.showLegsNumberInTitle).toEqual(true);
      expect(model.legs).toEqual([{
        name: 'legName',
        type: 'H',
        adjustedResult: 'legName',
        startTime: undefined,
        isResulted: true,
        outcomeResult: 'W',
        outcomeClass: 'check-mark',
        isVoid: false
      }]);
      expect(model.showEstimatedReturns).toEqual(false);
      expect(model.showStakeAndLines).toEqual(true);
    });
  });

  describe('#_getOutcomeClass', () => {
    it('should return check-mark', () => {
      const result = model._getOutcomeClass('W');

      expect(result).toEqual('check-mark');
    });
    it('should return x-mark', () => {
      const result = model._getOutcomeClass('L');

      expect(result).toEqual('x-mark');
    });
    it('should return undefined', () => {
      const result = model._getOutcomeClass('Z');

      expect(result).toEqual(undefined);
    });
  });

  describe('#_isResulted', () => {
    it('should return true', () => {
      const result = model._isResulted({confirmed: 'Y'} as any);

      expect(result).toEqual(true);
    });
    it('should return false', () => {
      const result = model._isResulted({confirmed: 'Z'} as any);

      expect(result).toEqual(false);
    });
    it('should return true', () => {
      const result = model._isResulted({} as any);

      expect(result).toEqual(undefined);
    });
  });

  describe('#getAdjustedResult', () => {
    it('should return H result', () => {
      const result = model.getAdjustedResult('1', 'legName');

      expect(result).toEqual('legName');
    });
    it('should return D result', () => {
      const result = model.getAdjustedResult('2', 'legName');

      expect(result).toEqual('Draw');
    });
    it('should return A result', () => {
      const result = model.getAdjustedResult('3', 'legName v legName1');

      expect(result).toEqual('legName1');
    });
    it('should return undefined', () => {
      const result = model.getAdjustedResult('4', 'legName');

      expect(result).toEqual(undefined);
    });
  });

  describe('#_getTeamName', () => {
    it('should return class', () => {
      const result = model._getTeamName('one v two', 'Y');

      expect(result).toEqual('two');
    });
    it('should return undefined', () => {
      const result = model._getTeamName('legName', 'Y');

      expect(result).toEqual(undefined);
    });
  });

  describe('#setSelection', () => {
    it('should return H', () => {
      const result = model.setSelection('1');

      expect(result).toEqual('H');
    });
    it('should return D', () => {
      const result = model.setSelection('2');

      expect(result).toEqual('D');
    });
    it('should return A', () => {
      const result = model.setSelection('3');

      expect(result).toEqual('A');
    });
    it('should return undefined', () => {
      const result = model.setSelection('4');

      expect(result).toEqual(undefined);
    });
  });
});
