import { ExPoolBetsModel } from './ex.model';

describe('ExPoolBetsModel', () => {
  let model: ExPoolBetsModel;
  const ip = '192.168.3.1';
  beforeEach(() => {
    model = new ExPoolBetsModel({
      pools: [{ poolType: 'EX' }]
    }, ip);
  });

  it('constructor', () => {
    expect(model).toBeTruthy();
    expect(model['_fieldsControls']).toEqual({ clearField: [] });
    expect(model['_totalStake']).toBe(0);
  });

  it('changeValue', () => {
    expect(model.outcomeIds).toBeUndefined();
    model.changeValue(['1']);
    expect(model.outcomeIds).toEqual(['1']);
  });

  it('stakeValue', () => {
    model.stakeValue('');
    expect(model['_totalStake']).toBe(0);

    model.stakeValue('10');
    expect(model['_totalStake']).toBe(10);

    model.stakeValue('20.123');
    expect(model['_totalStake']).toBe(20.12);
  });

  it('clearBets', () => {
    model['clearFields'] = jasmine.createSpy();
    model.clearBets();
    expect(model['_totalStake']).toBe(0);
    expect(model['clearFields']).toHaveBeenCalled();
  });

  it('get fieldsControls', () => {
    model['_fieldsControls'] = {} as any;
    expect(model.fieldsControls).toBe(model['_fieldsControls']);
  });

  it('get totalStake', () => {
    model['_totalStake'] = 10;
    expect(model.totalStake).toBe(model['_totalStake']);
  });

  it('get bet', () => {
    const value: any = {};
    model['generateBet'] = jasmine.createSpy().and.returnValue(value);
    expect(model.bet).toBe(value);
    expect(model['generateBet']).toHaveBeenCalled();
  });

  it('generateBet', () => {
    model['_totalStake'] = 5;
    model['generateLegPart'] = jasmine.createSpy().and.returnValue({});

    const bet = model['generateBet']();

    expect(bet.betslip.stake.amount).toBe(model['_totalStake']);
    expect(bet.bet[0].stake.stakePerLine).toBe(model['_totalStake']);
    expect(bet.bet[0].stake.amount).toBe(model['_totalStake']);
    expect(bet.leg[0].poolLeg.legPart).toBeDefined();
    expect(model['generateLegPart']).toHaveBeenCalled();
  });

  it('generateLegPart', () => {
    model.outcomeIds = ['1', '2'];
    const result = model['generateLegPart']();
    expect(result).toEqual(jasmine.any(Array));
    expect(result.length).toBe(2);
  });

  it('clearFields', () => {
    model['_fieldsControls'] = {
      clearField: [jasmine.createSpy()]
    } as any;

    model['clearFields']();

    expect(model['_fieldsControls']['clearField'][0]).toHaveBeenCalled();
  });
});
