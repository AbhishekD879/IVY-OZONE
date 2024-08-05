import { WinPoolBetsModel } from './wn.model';

describe('WinPoolBetsModel', () => {
  let model: WinPoolBetsModel;
  const ip = '192.168.3.1';
  beforeEach(() => {
    model = new WinPoolBetsModel({
      pools: [{ poolType: 'WN' }],
      markets: [{ outcomes: [] }]
    }, ip);
  });

  it('constructor', () => {
    expect(model).toBeDefined();
    expect(model.BPPService).toBe('placeWinPoolBet');
    expect(model['stakesMap']).toBeDefined();
    expect(model['_fieldsControls']).toEqual({ clearField: [] });
    expect(model['_totalStake']).toBe(0);
  });

  it('#changeValue with value', () => {
    model['setStake'] = jasmine.createSpy();
    model['refreshTotalStake'] = jasmine.createSpy();

    model.changeValue({ value: '2.344', outcomeId: '1' });
    expect(model['setStake']).toHaveBeenCalledWith('1', 2.34);
    expect(model['refreshTotalStake']).toHaveBeenCalled();
  });

  it('#changeValue without value', () => {
    model['setStake'] = jasmine.createSpy();
    model['refreshTotalStake'] = jasmine.createSpy();

    model.changeValue({ value: '', outcomeId: '1' });
    expect(model['setStake']).toHaveBeenCalledWith('1', 0);
    expect(model['refreshTotalStake']).toHaveBeenCalled();
  });

  it('clearBets', () => {
    model['stakesMap'] = { '1': {}, '2': {} } as any;
    model['setStake'] = jasmine.createSpy();
    model['refreshTotalStake'] = jasmine.createSpy();
    model['clearFields'] = jasmine.createSpy();

    model.clearBets();

    expect(model['setStake']).toHaveBeenCalledTimes(2);
    expect(model['refreshTotalStake']).toHaveBeenCalled();
    expect(model['clearFields']).toHaveBeenCalled();
  });

  it('get fieldsControls', () => {
    model['_fieldsControls'] = {} as any;
    expect(model.fieldsControls).toBe(model['_fieldsControls']);
  });

  it('get totalStake', () => {
    model['_totalStake'] = {} as any;
    expect(model.totalStake).toBe(model['_totalStake']);
  });

  it('get bet', () => {
    model['stakesMap'] = { x: 1, y: 2 } as any;
    model['filterZeroStake'] = jasmine.createSpy().and.returnValue(true);
    model['generateBet'] = jasmine.createSpy();

    const result: any = model.bet;

    expect(model['filterZeroStake']).toHaveBeenCalledTimes(2);
    expect(model['generateBet']).toHaveBeenCalledTimes(2);
    expect(result).toEqual({ requests: jasmine.any(Array) });
    expect(result.requests.length).toBe(2);
  });

  it('generateBet', () => {
    const stake = {
      numericValue: 3, outcomeId: '1'
    };

    const bet = model['generateBet'](stake);

    expect(bet.betslip.stake.amount).toBe(stake.numericValue);
    expect(bet.bet[0].stake.stakePerLine).toBe(stake.numericValue);
    expect(bet.bet[0].stake.amount).toBe(stake.numericValue);
    expect(bet.leg[0].poolLeg.legPart[0].outcomeRef.id).toBe(stake.outcomeId);
  });

  it('generateStakesMap', () => {
    const outcomes: any[] = [{ id: '1'}, { id: '2' }];
    expect(model['generateStakesMap'](outcomes)).toEqual({
      '1': jasmine.objectContaining({ outcomeId: '1' }),
      '2': jasmine.objectContaining({ outcomeId: '2' })
    } as any);
  });

  it('clearFields', () => {
    model['_fieldsControls'] = {
      clearField: [jasmine.createSpy()]
    };
    model['clearFields']();
    expect(model['_fieldsControls'].clearField[0]).toHaveBeenCalled();
  });

  it('refreshTotalStake', () => {
    model['stakesMap'] = {
      '1': { numericValue: 1 },
      '2': { numericValue: 2 }
    } as any;
    model['refreshTotalStake']();
    expect(model['_totalStake']).toBe(3);
  });

  it('setStake', () => {
    model['stakesMap'] = { '1': {} } as any;
    model['setStake']('1', 10);
    expect(model['stakesMap']['1'].numericValue).toBe(10);
  });

  it('filterZeroStake', () => {
    expect(model['filterZeroStake']({ numericValue: 2 })).toBe(2);
    expect(model['filterZeroStake']({ numericValue: '3' })).toBe(3);
  });
});
