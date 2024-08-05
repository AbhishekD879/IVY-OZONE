import { IBetTermsChange } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetTags } from './bet-history.model';

export interface ICashoutBet {
  panelMsg: IPanelMsg;
  attemptPanelMsg: IPanelMsg;
  inProgress: boolean;
  isDisable: boolean;
  isCashOutUnavailable: boolean;
  isCashOutBetError: boolean;
  isPartialCashOutAvailable: boolean;
  isPartialActive: boolean;
  partialCashOutPercentage: number;
  cashoutValue: any;
  betType: string;
  betId: string;
  betTags?: IBetTags;
  currencySymbol: string;
  lastTimeUpdate: number;
  handleSuccess: any;
  handleError: any;
  stake: string;
  stakePerLine: string;
  potentialPayout?: any;
  isConfirmed: boolean;
  betTermsChange?: IBetTermsChange[];
  cashoutSuccessMessage?: string;
  setCashoutSuccessState?: Function;
  gtmCashoutValue?: number | string;
  bonus?: string;
  refund?: string;
  setCashedOutState?: Function;
  cashoutStatus: string;
  availableBonuses?: any;
}

export interface ICashoutStatuses {
  BET_WORTH_NOTHING: string;
}

export interface IPanelMsg {
  type?: string;
  msg?: string;
}
