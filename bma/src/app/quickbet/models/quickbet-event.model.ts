import { IQuickbetMarketModel } from './quickbet-market.model';

export interface IQuickbetEventModel {
  categoryId?: string;
  categoryName?: string;
  eventSortCode?: string;
  eventStatusCode?: string;
  id?: string;
  isStarted?: boolean;
  markets?: IQuickbetMarketModel[];
  name?: string;
  responseCreationTime?: string;
  startTime?: string;
  typeId?: string;
  typeName?: string;
  classId?: string;
  className?: string;
  isLiveNowEvent?: boolean;
  isRacingSport?: boolean;
  eventIsLive?: boolean;
  eventName?: string;
  eventId?: string;
}
