export interface IBetStake {
  amount: number;
  currency: string;
  freeBetAmount?: number;
  isTraderOffered: boolean;
  lines: number;
  max: number;
  min: number;
  perLine: string | number;
  stakeMultiplier: number;
  time: string;
  type: string;
  typeId: number;
  winOrEach: boolean;
}
