import { ILeg as IBppLeg, IRangeBase } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface ILeg extends IBppLeg {
  winPlace?: string;
  [key: string]: any;
  places?: string;
  outcomeCombiRef?: { id: string; }[];
  outcomeRef?: { id: string; }[];
  range?: IRangeBase;
}

export type ILegList = ILeg[];
export type IBetslipLeg = ILeg;
