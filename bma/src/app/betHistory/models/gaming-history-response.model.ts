export interface ISingleSummary {
  amount: string;
  currencyCode: string;
}

export interface ITotalSummary {
  totalApprovedWithdraws: ISingleSummary;
  totalBets: ISingleSummary;
  totalDeposits: ISingleSummary;
  totalWins: ISingleSummary;
}

export interface IWalletTransaction {
  actionType: string;
  amount: ISingleSummary;
  balanceChanges: any;
  clientType: string;
  direction: string;
  templateTags: {
    game_category: string;
    game_name: string;
  };
  transactionDateInUms: string;
}

export interface IGamingHistoryResponse {
  summary: ITotalSummary;
  walletTransactions: IWalletTransaction[];
}

