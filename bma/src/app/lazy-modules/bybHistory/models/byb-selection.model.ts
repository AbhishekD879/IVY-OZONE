import { IBetHistoryPart } from '@app/betHistory/models/bet-history.model';

export interface IBybSelection {
  part: IBetHistoryPart;
  title: string;
  desc?: string;
  progress?: IBybSelectionProgress;
  status?: string;                  // 'Won|Lose|Winning|Losing'
  config?: IBybConfig;
  showBetStatusIndicator?: boolean;
  showTooltip?: boolean;
  isVoided?: boolean;
  partSettled?: boolean;
  betRunningStatus?: boolean;
  betCompletion?: boolean;
  isCleanSheetMarket?: boolean;
}

export interface IBybSelectionStatus {
  status: string;  // 'Won|Lose|Winning|Losing'
  progress?: IBybSelectionProgress;
}

export interface IBybSelectionProgress {
  current: number;
  target: number;
  desc: string;
}

export interface IBybDefaultSelectionStatus {
  status: undefined | string;
  partSettled: boolean;
  showBetStatusIndicator: undefined;
}

export interface IBybConfig {
  name: string;
  hasLine: boolean;
  statCategory: string;
  template: string;                   // Binary|Range
  isHomeAwayAvailable?: boolean;
  period: string;                     // 1h|2h|total|15 mins|30 mins|60 mins|75 mins|first|last
  generalInformationRequired: string; // teams|team|player
  methodName?: string;
  isSpecificMarket?: boolean;
  isBoth?: boolean; // uses for win Halves cases
}

export interface IConditions {
  [key: string]: Boolean;
}
