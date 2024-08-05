export interface IBetHistorySingleSummary {
  /**
   * The difference between totalReturns and totalStakes, positive or negative value with currency
   */
  profit: string;
  totalStakes: string;
  totalReturns: string;

  /**
   * The specific css class in case of profit or loss
   */
  iconClass?: string;

  /**
   * Label indicates the total summary or specific bet type
   * @example
   * All Betting & Gaming, Sports, Lotto, Pools
   */
  label?: string;
}

export interface IBetHistoryAllSummary {
  [key: string]: IBetHistorySingleSummary;
}
