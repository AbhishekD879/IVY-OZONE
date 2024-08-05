import { ISportEvent } from './sport-event.model';
import { IRacingMarket } from '@core/models/racing-market.model';

export interface IRacingEvent extends ISportEvent {
  markets: IRacingMarket[];
  sortedMarkets?: IRacingMarket[];
  resultedWEWMarket: IRacingMarket;
  voidResult?: boolean;
  categoryDisplayOrder?: string;
  classSortCode: string;
  correctedDay: string;
  externalKeys: {
    OBEvLinkNonTote: number;
  };
  isActive?: boolean;
  isAvailable: string;
  isNext24HourEvent: string;
  isOpenEvent: string;
  isResulted: undefined;
  isUKorIRE: boolean;
  isUS: boolean;
  linkedEventId: number;
  liveEventOrder: number;
  liveSimAvailable: boolean;
  localTime: string;
  raceNumber: string;
  rawIsOffCode: string;
  siteChannels: string;
  sportId: string;
  isReplayStreamAvailable:boolean;
}


