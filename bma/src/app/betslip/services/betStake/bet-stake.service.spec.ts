import { BetStake } from './bet-stake';
import { BetStakeService } from '@betslip/services/betStake/bet-stake.service';

describe('test BetStakeService', () => {
  let service: BetStakeService;
  let userService;
  let params;

  beforeEach(() => {
    userService = {
      currency: '$'
    };
    params = {
      max: '1',
      min: '1',
      amount: '1',
      lines: 1,
      currency: '',
      perLine: '',
      freeBetAmount: '1'
    };

    service = new BetStakeService(userService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('should return new instance of BetStake', () => {
    const bet = service.construct(params);

    expect(bet instanceof BetStake).toBeTruthy();
  });

  it('should return new instance of BetStake with params', () => {
    const bet = service.parse(params, 1);

    expect(bet instanceof BetStake).toBeTruthy();
  });
});
