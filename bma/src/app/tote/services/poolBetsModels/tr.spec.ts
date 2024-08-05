import { TrPoolBetsModel } from './tr.model';

describe('TrPoolBetsModel', () => {
  let model: TrPoolBetsModel;
  const ip = '192.168.3.1';
  beforeEach(() => {
    model = new TrPoolBetsModel({
      pools: [{ poolType: 'TR' }]
    }, ip);
  });

  it('constructor', () => {
    expect(model).toBeDefined();
  });

  it('constructor2', () => {
    model = new TrPoolBetsModel({
      pools: [{ poolType: 'TR' }]
    }, ip, 'TR');
    expect(model).toBeDefined();
  });
});
