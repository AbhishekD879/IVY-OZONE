import { IQuickbetBetModel, IQuickbetIdModel } from '@app/quickbet/models/quickbet-common.model';

export interface IQuickbetOveraskResponseModel {
  bet: IQuickbetBetModel[];
  betslip: IQuickbetResponseBetslip;
}

interface IQuickbetResponseBetslip {
  betRef: IQuickbetBetRef[];
  clientUserAgent: string;
  documentId: string;
  isAccountBet: string;
  slipPlacement: IQuickbetSlipPlacement;
  stake: IQuickbetStake;
}

interface IQuickbetBetRef {
  documentOd: string;
}

interface IQuickbetSlipPlacement {
  channelRef: IQuickbetIdModel;
}

interface IQuickbetStake {
  amount: string;
  currencyRef: IQuickbetIdModel;
  stakePerLine: string;
}
