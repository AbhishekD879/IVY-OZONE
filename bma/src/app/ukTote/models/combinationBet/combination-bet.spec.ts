import { CombinationBet } from './combination-bet';
describe('CombinationBet', () => {
  it('should construct tote combination bet', () => {
    const items = {
      any: [
        {
          id: '2'
        },
        {
          id: '1'
        },
        {
          id: '3'
        }
      ]
    },
      poolType = 'UTRI',
      poolId = 123456,
      validToteCombinationBet = {
        poolType: 'UTRI',
        betNo: 134,
        poolItem: [
          {
            poolId: 123456,
            outcome: '2'
          },
          {
            poolId: 123456,
            outcome: '1'
          },
          {
            poolId: 123456,
            outcome: '3'
          }
        ]
      },
      combinationBet = new CombinationBet(items, poolType, poolId);
    expect(combinationBet.betObject).toEqual(validToteCombinationBet);
  });
});
