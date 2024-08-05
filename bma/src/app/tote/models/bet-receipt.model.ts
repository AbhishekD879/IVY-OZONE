export interface IBetReceipt {
  betId: string;
  currency: string;
  legParts: IBetReceiptLegPart[];
  outcomeId: string;
  poolTitle: string;
  stakeAmount: string;
}

interface IBetReceiptLegPart {
  outcomeName: string;
  outcomeRef: IBetReceiptLegPartOutcomeRef;
}

interface IBetReceiptLegPartOutcomeRef {
  id: string;
}
