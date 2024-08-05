import { MARKETS_GROUP } from './markets-group.constant';

describe('MARKETS_GROUP', () => {
  it('it should change templateMarketName', () => {
    const markets = MARKETS_GROUP.find(config => config.name === 'Over/Under Total Goals');
    expect(markets.periods[0].marketsNames).toEqual('Over/Under Total Goals');
  });
});
