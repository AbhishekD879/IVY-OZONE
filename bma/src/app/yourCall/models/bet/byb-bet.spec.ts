import { BYBBet } from './byb-bet';

describe('#BYBBet', () => {
  let bet: BYBBet;

  beforeEach(() => {
    bet = new BYBBet({
      stake: '10',
      currencyName: 'UAH',
      betOddsFract: '1/10',
      channel: 'f',
      dashboardData: {
        game: {
          obTypeId: '123',
          obEventId: '321'
        }
      },
      odds: '10.00',
      oddsFract: {},
      currencySymbol: '$',
      currency: 'USD',
      token: 'token',
      oddsFormat: 'frac'
    });
  });

  describe('getPotentialPayout', () => {
    let superGetPotentialPayoutSpy;

    beforeEach(() => {
      bet.stake = '10.00';
      superGetPotentialPayoutSpy = spyOn(BYBBet.prototype['__proto__'], 'getPotentialPayout').and.returnValue('40');
    });

    it('should getPotentialPayou with betOdds when freebetValue is defined', () => {
      bet.stake = 0;
      bet.freebetValue = 4;
      bet.betOdds = '10.00';

      expect(bet.getPotentialPayout()).toEqual('36.00');
    });

    it('should getPotentialPayou with betOdds when freebetValue is defined', () => {
      bet.freebetValue = undefined;
      bet.stake = undefined;
      bet.betOdds = '40.00';

      expect(bet.getPotentialPayout()).toEqual('40.00');
    });

    it('should invoke super "getPotentialPayout" when stake is defined', () => {
      expect(bet.getPotentialPayout()).toEqual('40.00');
      expect(superGetPotentialPayoutSpy).toHaveBeenCalled();
    });

    it('should invoke super "getPotentialPayout" when stake is 0 and "freebetValue" is empty', () => {
      bet.stake = 0;
      bet.freebetValue = undefined;

      expect(bet.getPotentialPayout()).toEqual('40.00');
      expect(superGetPotentialPayoutSpy).toHaveBeenCalled();
    });

    it('should invoke super "getPotentialPayout" when stake is not 0 and "freebetValue" exist', () => {
      bet.freebetValue = 1;
      bet.stake = 3;

      expect(bet.getPotentialPayout()).toEqual('39.00');
      expect(superGetPotentialPayoutSpy).toHaveBeenCalled();
    });


    it('should return proper value and not invoke super "getPotentialPayout" when stake is 0 and ' +
      'freebetValue is defined', () => {
      bet.stake = 0;
      bet.freebetValue = 0.1;

      expect(bet.getPotentialPayout()).toEqual('0.90');
      expect(superGetPotentialPayoutSpy).not.toHaveBeenCalled();
    });
  });

  it('constructor', () => {
    expect(bet).toBeTruthy();
  });

  describe('#formatBet', () => {
    it('should call normalize with cahannel', () => {
      bet.normalize = jasmine.createSpy().and.returnValue({
        stake: '10',
        currency: 'UAH',
        token: 'token',
        price: '1/10',
        channel: 'f'
      });
      const result = bet.formatBet();

      expect(result).toEqual({
        stake: '10',
        currency: 'UAH',
        token: 'token',
        price: '1/10',
        channel: 'f'
      });
    });
  });

  describe('#normalize', () => {
    it('should call normalize with cahannel', () => {
      const result = bet.normalize({
        stake: '10',
        currencyName: 'UAH',
        token: 'token',
        betOddsFract: '1/10',
        channel: 'f'
      } as any);

      expect(result).toEqual({
        stake: '10',
        currency: 'UAH',
        token: 'token',
        price: '1/10',
        channel: 'f'
      });
    });

    it('should call normalize without cahannel', () => {
      const result = bet.normalize({
        stake: '10',
        currencyName: 'UAH',
        token: 'token',
        betOddsFract: '1/10'
      } as any);

      expect(result).toEqual({
        stake: '10',
        currency: 'UAH',
        token: 'token',
        price: '1/10',
        channel: 'e'
      });
    });

    it('should call normalize with freebet', () => {
      const result = bet.normalize({
        stake: '10',
        currencyName: 'UAH',
        token: 'token',
        betOddsFract: '1/10',
        freebet: {
          freebetTokenId: '2',
          freebetTokenValue: '4'
        }
      } as any);

      expect(result).toEqual({
        stake: '10',
        currency: 'UAH',
        token: 'token',
        price: '1/10',
        channel: 'e',
        freebet: {
          id: '2',
          stake: '4'
        }
      });
    });
  });
});
