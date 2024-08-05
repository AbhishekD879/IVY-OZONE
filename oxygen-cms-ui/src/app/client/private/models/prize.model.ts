export class Prize {
  constructor(public correctSelections: number,
              public prizeType: string,
              public amount: number,
              public currency: string = '£',
              public promotionId: string = '') {}
}
