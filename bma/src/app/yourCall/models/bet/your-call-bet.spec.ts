import { YourCallBet } from './your-call-bet';

describe('YourCallBet', () => {
  let model: YourCallBet;

  beforeEach(() => {
    model = new YourCallBet({
      dashboardData: {
        game: {
          obTypeId: '123',
          obEventId: '321'
        },
        categoryId: '41',
        classId: '96'
      },
      odds: '10.00',
      oddsFract: {},
      currencySymbol: '$',
      currency: 'USD',
      token: 'token',
      oddsFormat: 'frac',
      channel: 'e'
    });
  });

  it('constructor', () => {
    expect(model).toBeTruthy();
    expect(model.stakeAmount).toEqual(0);
    expect(model.channel).toEqual('e');
    expect(model.classId).toBe('96');
    expect(model.categoryId).toBe('41');
  });

  describe('#onStakeChange', () => {
    it('should calculate new potentialPayout and stakeAmount', () => {
      model.stake = '10.00';
      model.onStakeChange();

      expect(model.stakeAmount).toEqual(10);
      expect(model.potentialPayout).toEqual('100.00');
    });

    it('should calculate new potentialPayout and stakeAmount when could not parse stake', () => {
      model.stake = '';
      model.onStakeChange();

      expect(model.stakeAmount).toEqual(0);
      expect(model.potentialPayout).toEqual('0.00');
    });
  });

  describe('#onOddsChange', () => {
    it('should call onStakeChange and set equal betOdds and betOddsFract', () => {
      model.onStakeChange = jasmine.createSpy();
      model.onOddsChange('1', 'betOddsFract');

      expect(model.betOdds).toEqual('1');
      expect(model.betOddsFract).toEqual('betOddsFract');
      expect(model.onStakeChange).toHaveBeenCalled();
    });
  });
});
