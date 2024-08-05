import { ShowPoolBetsModel } from './sh.model';

describe('ShowPoolBetsModel', () => {
  let model: ShowPoolBetsModel;
  const ip = '192.168.3.1';
  beforeEach(() => {
    model = new ShowPoolBetsModel({
      pools: [{ poolType: 'SH' }],
      markets: [{ outcomes: [] }]
    }, ip);
  });

  it('constructor', () => {
    expect(model).toBeTruthy();
  });

  it('constuctor2', () => {
    model = new ShowPoolBetsModel({
      pools: [{ poolType: 'SH' }],
      markets: [{ outcomes: [] }]
    }, ip, 'SH');
    expect(model).toBeTruthy();
  });
});
