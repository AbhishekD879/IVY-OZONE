import { IMarketData } from './outcome-market.model';
import { IModuleClock } from './module-clock.model';

export interface ISportEventData {
    id: number;
    marketsCount: number;
    name: string;
    nameOverride: string;
    outcomeId: number;
    outcomeStatus: boolean;
    eventSortCode: string;
    startTime: string;
    liveServChannels: string;
    liveServChildrenChannels: string;
    liveServLastMsgId: string;
    categoryId: string;
    categoryCode: string;
    categoryName: string;
    typeName: string;
    cashoutAvail: string;
    eventStatusCode: string;
    isUS: boolean;
    eventIsLive: boolean;
    displayOrder: number;
    markets: IMarketData[];
    primaryMarkets: IMarketData[];
    comments: Comment;
    isStarted: boolean;
    isFinished: boolean;
    outright: boolean;
    responseCreationTime: string;
    liveStreamAvailable: boolean;
    drilldownTagNames: string;
    typeFlagCodes: string;
    typeId: string;
    initClock: IModuleClock;
    ssName: string;
}
