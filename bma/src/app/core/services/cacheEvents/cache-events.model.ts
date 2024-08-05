import { ISportEvent } from '@core/models/sport-event.model';
import { IFeaturedModel } from '@featured/models/featured.model';
import { IConstant } from '@core/services/models/constant.model';

export interface IStoredData {
  event: { data?: ISportEvent[], updated?: number };
  toteEvents?: { data?: ISportEvent[] };
  liveEventsStream: IConstant;
  multiplesEvents: IConstant;
  inPlayWidget: IConstant;
  inplaySection: IConstant;
  LSWidget: IConstant;
  coupons: IConstant;
  ribbonEvents: IConstant;
  privateMarkets: IConstant;
  index: IConstant;
  marketsIndex: IConstant;
  outcomesIndex: IConstant;
  currentMatches: IConstant;
  favouritesMatches: IConstant;
  nextRacesHome: IConstant;
  surfaceBetEvents: IConstant;
  nextRaces: IConstant;
}

export interface IIndexConfig {
  addToIndexCounter: number;
  addToIndexLimit: number;
}

export interface ILevel2Deepness {
  multiplesEvents: string;
  ribbonEvents: string;
  coupons?: string;
}

export interface IPathToData {
  ribbonEvents: string;
}

export interface IEventsIndex {
  [key: number]: { [key: number]: IEventsIndexDetail };
}

export interface IEventsIndexDetail {
  reference?: ISportEvent;
  path?: Array<number | string>;
  expire?: number;
}

export interface INumberIndex {
  [key: number]: string;
}

export interface ICached {
  data: IFeaturedModel;
  updated: number;
}
