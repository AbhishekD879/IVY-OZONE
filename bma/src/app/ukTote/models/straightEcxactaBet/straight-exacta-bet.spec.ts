import { StraightExactaBet } from './straight-exacta-bet';
describe('StraightExactaBet', () => {
  it('should construct tote straight Exacta bet', () => {
    const items = {
        '1st': {
          id: '2'
        },
        '2nd': {
          id: '1'
        }
      },
      poolType = 'UEXA',
      poolId = 123456,
      validToteExactaBet = {
        poolType: 'UEXA',
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
        ]
      },
      exactaBet = new StraightExactaBet(items, poolType, poolId);
    expect(exactaBet.betObject).toEqual(validToteExactaBet);
  });
});
