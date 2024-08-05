import { YourCallEvent } from './yourcall-event';
import { YourCallDashboardItem } from './yourcallDashboardItem/yourcall-dashboard-item';
import {
  IBetPlacement
} from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IAddSelectionData {
  game: YourCallEvent;
  selections: YourCallDashboardItem[];
}

export interface IYourcallBYBBetPLacementResponce {
  data: {
    betPlacement: IYourcallBetPlacement[];
    betFailure?: any;
    token: string;
    betError?: string;
  };
}

export interface IYourcallDSBetPLacementResponce {
  data: IYourcallBetPlacement;
}


export interface IYourcallBetPlacement extends IBetPlacement {
  events?: any[];
  obBetId?: string;
}

export interface IYourcallOddsData {
  data: {
    odds?: string;
    priceDen: number;
    priceNum: number;
  };
}

export interface IYourcallFormattedOdds {
  dec?: string;
  frac?: string;
}

export interface IYourcallBetError {
  code?: string;
  description?: string;
  message?: string;
  subErrorCode?: string;
}

export interface IYourcallBetFailure {
  betFailureCode: number;
  betFailureDesc: string;
}
