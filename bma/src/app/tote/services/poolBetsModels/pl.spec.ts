import { PlacePoolBetsModel } from './pl.model';

describe('PlacePoolBetsModel', () => {
  let model: PlacePoolBetsModel;
  const ip = '192.168.3.1';
  beforeEach(() => {
    model = new PlacePoolBetsModel({
      pools: [{ poolType: 'PL' }],
      markets: [{ outcomes: [] }]
    }, ip);
  });

  it('constructor', () => {
    expect(model).toBeTruthy();
  });

  it('constructor2', () => {
    model = new PlacePoolBetsModel({
      pools: [{ poolType: 'PL' }],
      markets: [{ outcomes: [] }]
    }, ip, 'PL');
    expect(model).toBeTruthy();
  });
});
