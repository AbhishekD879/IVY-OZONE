import { IOutcomePrice } from '@core/models/outcome-price.model';
import { IConstant } from '@core/services/models/constant.model';
import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';

export interface IBetslipMarket extends IMarket {
  eventId: string;
  collectionIds: string;
  collectionNames: string;
  marketMeaningMinorCode: string;
  isActive: string;
  siteChannels: string;
  liveServChildrenChannels: string;
  drilldownTagNames: string;
  isAvailable: string;
  maxAccumulators: string;
  minAccumulators: string;
  isEachWayAvailable: boolean;
  eachWayFactorNum: string;
  eachWayFactorDen: string;
}

export interface IBetslipOutcome extends IOutcome {
  marketId: string;
  isActive: string;
  siteChannels: string;
  liveServChildrenChannels: string;
  isAvailable: string;
  cashoutAvail: string;
}

export interface IBetslipEvent extends ISportEvent {
  isActive: boolean;
  siteChannels: string;
  rawIsOffCode: string;
  sportId: string;
  categoryDisplayOrder: string;
  classSortCode: string;
  classFlagCodes: string;
  isOpenEvent: true;
  isAvailable: true;
  originalName: string;
  correctedDay: string;
  liveEventOrder: number;
  startTime: string;
  typeName: string;
}

export interface ISelectionRealtedData extends IBetslipOutcome {
  details: {
    info: {
      sport: string;
      event: string;
      time: number;
      localTime: string;
      market: string;
      sportId: string;
      className: string;
      isStarted?: boolean;
    };
    isRacing: boolean;
    outcomeStatusCode: string;
    marketStatusCode: string;
    eventStatusCode: string;
    classId: number;
    categoryId: number;
    typeId: number;
    eventId: string;
    marketId: string;
    templateMarketId: string;
    outcomeId: string;
    handicap?: string;
    isMarketBetInRun: boolean;
    eventliveServChannels: string;
    marketliveServChannels: string;
    outcomeliveServChannels: string;
    market: string;
    selectionName: string;
    prices: Partial<IOutcomePrice>;
    isSPLP: boolean;
    pricesAvailable: boolean;
    isEachWayAvailable?: boolean;
    isGpAvailable?: boolean;
    eachwayCheckbox: IConstant | null;
  };
}
