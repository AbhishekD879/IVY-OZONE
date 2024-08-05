import { ISportEvent } from '@core/models/sport-event.model';
import { IBetDetail, IBetDetailLeg, IBetDetailLegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface ITypesAndIds {
  outcome?: string[];
  market?: string[];
  event: string[];
}

export interface ICashOutCtrl {
  ctrlName: string;
  isDestroyed: boolean;
}

export interface ICashOutBet extends IBetDetail {
  id: string;
  currencySymbol: string;
  isCashOutUnavailable: boolean;
  isCashOutBetError: boolean;
  isPartialCashOutAvailable: boolean;
  partialCashoutAvailable: string;
  partialCashoutStatus: string;
  inProgress: string;
  isConfirmed: boolean;
  panelMsg: {};
  attemptPanelMsg: {};
  market: string[];
  outcome: string[];
  event: string[];
  events: ISportEvent;
  leg: ICashOutBetLeg[];
  isAccaEdit?: boolean;
  shouldActivate?: boolean;
}

export interface ICashOutBetLeg extends IBetDetailLeg {
  eventEntity: ISportEvent;
  status: string;
  part: ICashOutBetLegPart[];
  removing?: boolean;
}

export interface ICashOutBetLegPart extends IBetDetailLegPart {
  outcomeId: string;
}

