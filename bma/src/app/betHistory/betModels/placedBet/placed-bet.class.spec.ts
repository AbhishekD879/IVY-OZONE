import { PlacedBet } from './placed-bet.class';

describe('PlacedBet', () => {
  let model: PlacedBet;

  let bet,
    betModelService,
    currency,
    currencySymbol,
    cashOutMapIndex,
    cashOutErrorMessage;
  const part = [{
    startTime: new Date().toISOString(),
    outcome: [{
      name: 'Wimbeldon To Win',
      event: {
        startTime: new Date().toISOString(),
      },
      market: {},
      result: {
        value: 1
      },
      eventCategory: {
        id: 16
      }
    }],
    price: [{
      priceNum: '1',
      priceDen: '2'
    }],
    eventId: 100500
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
        part: part,
      }],
      stake: {
        stakePerLine: 1
      },
      settled: 'N',
      cashoutValue: 10,
      partialCashoutAvailable: 'N',
      potentialPayout: 0
    };
    betModelService = {
      getBetTimeString: jasmine.createSpy(),
      createOutcomeName: jasmine.createSpy().and.returnValue(part),
      getPotentialPayout: jasmine.createSpy('getPotentialPayout').and.returnValue(0)
    };
    currency = {};
    currencySymbol = '$';
    cashOutMapIndex = {
      create: jasmine.createSpy(),
    };
    cashOutErrorMessage = {
      getErrorMessage: jasmine.createSpy(),
    };

    model = new PlacedBet(
      bet,
      betModelService,
      currency,
      currencySymbol,
      cashOutMapIndex,
      cashOutErrorMessage
    );
  });
  describe('constructor', () => {
    beforeEach(() => {
      model.betId = '1234';
    });
    it('constructor should create cashOutMapIndex', () => {
      expect(model.potentialPayout).toEqual(0);
      expect(cashOutMapIndex.create).toHaveBeenCalled();
    });
    it('constructor hould create cashOutMapIndex for settled bets', () => {
      bet.settled = 'Y';
      expect(model.potentialPayout).toEqual(0);
      expect(cashOutMapIndex.create).toHaveBeenCalled();
    });
  });

});
