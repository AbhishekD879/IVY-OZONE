import { WinPoolBetsModel } from '@app/tote/services/poolBetsModels/wn.model';
import { PlacePoolBetsModel } from '@app/tote/services/poolBetsModels/pl.model';
import { ShowPoolBetsModel } from '@app/tote/services/poolBetsModels/sh.model';
import { ExPoolBetsModel } from '@app/tote/services/poolBetsModels/ex.model';
import { TrPoolBetsModel } from '@app/tote/services/poolBetsModels/tr.model';
import { ILegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IPoolBet {
  betslip: IPoolBetBetslip;
  leg: IPoolBetLeg[];
  bet: IPoolBetBet[];
  betId?: number;
  poolTitle?: string;
  stakeAmount?: number;
  legParts?: ILegPart[];
  requests?;
}

interface IPoolBetBetslip {
  documentId: string;
  stake: IPoolBetBetslipStake;
  clientUserAgent: string;
  isAccountBet: string;
  slipPlacement: IPoolBetBetslipSlipPlacement;
  betRef: IPoolBetBetslipBetRef[];
}

  interface IPoolBetBetslipStake {
    amount: number;
    currencyRef: IPoolBetBetslipStakeCurrencyRef;
  }

    interface IPoolBetBetslipStakeCurrencyRef {
      id: string;
    }

  interface IPoolBetBetslipSlipPlacement {
    IPAddress: string;
    channelRef: { id: string };
  }

  interface IPoolBetBetslipBetRef {
    documentId: string;
  }

interface IPoolBetLeg {
  documentId: string;
  poolLeg: IPoolBetLegPoolLeg;
}

  interface IPoolBetLegPoolLeg {
    poolRef: IPoolBetLegPoolLegRef;
    legPart: IPoolBetLegPoolLegPart[];
  }

    interface IPoolBetLegPoolLegRef {
      id: string;
    }

    export interface IPoolBetLegPoolLegPart {
      outcomeRef: { id: string; };
      places?: number;
    }

interface IPoolBetBet {
  documentId: string;
  betslipRef: IPoolBetBetBetslipRef;
  betTypeRef: IPoolBetBetBetslipBetTypeRef;
  stake: IPoolBetBetStake;
  lines: IPoolBetBetLines;
  legRef: IPoolBetBetLegRef[];
  leg?;
  receipt?;
}

  interface IPoolBetBetBetslipRef {
    documentId: string;
  }

  interface IPoolBetBetBetslipBetTypeRef {
    id: string;
  }

  interface IPoolBetBetStake {
    stakePerLine: number;
    amount: number;
    currencyRef: IPoolBetBetStakeCurrencyRef;
  }

    interface IPoolBetBetStakeCurrencyRef {
      id: string;
    }

  interface IPoolBetBetLines {
    number: string;
  }

  interface IPoolBetBetLegRef {
    documentId: string;
    ordering?: string;
  }

type IPoolBetsTypes = WinPoolBetsModel
  | PlacePoolBetsModel
  | ShowPoolBetsModel
  | ExPoolBetsModel
  | TrPoolBetsModel;

export type IPoolBetsModels = IPoolBetsTypes &
  { stakeValue?: Function };
