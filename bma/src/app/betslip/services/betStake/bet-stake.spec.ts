import { BetStake } from './bet-stake';

describe('test BetHistoryRunService', () => {
  let service: BetStake;
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

    service = new BetStake(params, userService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('init properties', () => {
    expect(service.max).toEqual(1);
    expect(service.min).toEqual(1);
    expect(service.amount).toEqual(1);
    expect(service.lines).toEqual(1);
    expect(service.perLine).toEqual('');
    expect(service.freeBetAmount).toEqual(1);
  });

  it('should return max stake', () => {
    service['stakeMax'] = 123;

    expect(service.max).toEqual(123);
  });

  it('should set max stake', () => {
    service.max = 111;

    expect(service['stakeMax']).toEqual(111);
  });

  it('should return currency', () => {
    expect(service['currency']).toEqual('$');
  });

  it('should return amount', () => {
    expect(service['amount']).toEqual(1);

    service.lines = 0;
    expect(service['amount']).toEqual(1);
  });

  it('should set amount', () => {
    service['amount'] = 123;
    expect(service['_amount']).toEqual(123);
  });

  it('should return stakePerLine', () => {
    expect(service['perLine']).toEqual('');
  });

  it('should return stakePerLine(defined value)', () => {
    service['stakePerLine'] = '.12';
    expect(service['perLine']).toEqual('0.12');
  });

  it('should set stakePerLine', () => {
    service['perLine'] = '111';
    expect(service['stakePerLine']).toEqual('111');
  });

  it('should set freeBetAmount', () => {
    service['freeBetAmount'] = 3;
    expect(service['_freeBetAmount']).toEqual(3);
  });

  it('should get freeBetAmount', () => {
    expect(service['freeBetAmount']).toEqual(1);
  });

  it('should return clone of BetStake model', () => {
    const clone = service.clone();
    expect(clone instanceof BetStake).toBeTruthy();
  });

  it('should return object with stake, currencyRef and currency values', () => {
    expect(service.doc()).toEqual(jasmine.objectContaining({
      stake: {
        amount: 1,
        stakePerLine: 1,
        freebet: 1,
        currencyRef: {
          id: '$'
        }
      }
    }));
  });

  it('doc should return object wihtout freebet', () => {
    service.freeBetAmount = 0;
    expect(service.doc()).toEqual(jasmine.objectContaining({
      stake: {
        amount: 1,
        stakePerLine: 1,
        currencyRef: { id: '$' }
      }
    }));
  });
});
