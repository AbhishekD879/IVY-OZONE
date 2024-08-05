import { IPoolBet } from 'app/bpp/services/bppProviders/bpp-providers.model';

export class StraightTrifectaBet {

  betObject: IPoolBet;

  constructor(items, poolType, poolId) {
    this.betObject = {
      poolType,
      betNo: 134,
      poolItem: [
        {
          position: '1',
          poolId,
          outcome: items['1st'].id
        },
        {
          position: '2',
          poolId,
          outcome: items['2nd'].id
        },
        {
          position: '3',
          poolId,
          outcome: items['3rd'].id
        }
      ]
    };
  }
}
