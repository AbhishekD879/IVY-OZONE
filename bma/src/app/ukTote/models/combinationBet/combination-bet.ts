export class CombinationBet {

  poolItem;
  betObject;

  constructor(items, poolType, poolId) {
    this.poolItem = this.createCombinationPoolItem(items, poolId);
    this.betObject = {
      poolType,
      betNo: 134,
      poolItem: this.poolItem
    };
  }

  private createCombinationPoolItem(items, poolId) {
    const poolItem = [];
    for (let index = 0; index < items.any.length; index++) {
      const temp = {
        poolId,
        outcome: items.any[index].id
      };
      poolItem.push(temp);
    }
    return poolItem;
  }
}
