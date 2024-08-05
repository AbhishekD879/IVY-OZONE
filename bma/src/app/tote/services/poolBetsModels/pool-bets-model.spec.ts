import { PoolBetsModel } from './pool-bets-model';

describe('PoolBetsModel', () => {
  let model: PoolBetsModel;
  const ip = '192.168.3.1';
  const eventEntity: any = {
    pools: [{
      id: '1',
      poolType: 'T'
    }]
  };

  beforeEach(() => {
    model = new PoolBetsModel(eventEntity, ip, 'T');
  });

  it('constructor', () => {
    expect(model).toBeTruthy();
    expect(model.eventEntity).toBe(eventEntity);
    expect(model['poolType']).toBe('T');
    expect(model['poolId']).toBe('1');
  });

  it('get betModel', () => {
    const bet = model.betModel;
    expect(bet).toEqual(jasmine.any(Object));
    expect(bet.bet[0].betTypeRef.id).toBe(model['poolType']);
    expect(bet.leg[0].poolLeg.poolRef.id).toBe(model['poolId']);
  });

  it('get betLegModel', () => {
    expect(model.betLegModel).toEqual({
      outcomeRef: { id: '' }
    });
  });

  it('get stakeModel', () => {
    expect(model.stakeModel).toEqual({
      outcomeId: '', numericValue: 0
    });
  });
});
