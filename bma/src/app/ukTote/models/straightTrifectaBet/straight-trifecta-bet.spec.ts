import { StraightTrifectaBet } from './straight-trifecta-bet';
describe('StraightTrifectaBet', () => {
  it('should construct tote straight Trifecta bet', () => {
    const items = {
        '1st': {
          id: '2'
        },
        '2nd': {
          id: '1'
        },
        '3rd': {
          id: '3'
        }
      },
      poolType = 'UTRI',
      poolId = 123456,
      validToteTrifectaBet = {
        poolType: 'UTRI',
        betNo: 134,
        poolItem: [
          {
            position: '1',
            poolId: 123456,
            outcome: '2'
          },
          {
            position: '2',
            poolId: 123456,
            outcome: '1'
          },
          {
            position: '3',
            poolId: 123456,
            outcome: '3'
          },
        ]
      },
      straightTrifectaBet = new StraightTrifectaBet(items, poolType, poolId);
    expect(straightTrifectaBet.betObject).toEqual(validToteTrifectaBet);
  });
});
