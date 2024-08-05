import { IQuickbetSelectionPriceModel } from './quickbet-selection-price.model';
import { IGtmEventModel } from './quickbet-gtm-event.model';

export interface IQuickbetSelectionResponseModel {
  eventIsLive: boolean;
  goToBetslip: boolean;
  handicap: number;
  modifiedPrice: IQuickbetSelectionPriceModel;
  price: IQuickbetSelectionPriceModel;
  typeName: string;
  GTMObject?: IGtmEventModel;
  outcomes: IQuickbetOutcomeResponseModel[];
  type?: string;
  skipOnReconnect?: boolean;
  additional?: {
    scorecastMarketId: number;
  };

  eventId: number;
  isOutright: boolean;
  isSpecial: boolean;
  selectionInfo?: any;
  templateMarketName?: string;
  eventName?: string;
  outcomeName?: string;
  newOdds?: string;
  isStreamBet?: boolean;
  details ?: any;
}

interface IQuickbetOutcomeResponseModel {
  correctPriceType: string;
  correctedOutcomeMeaningMinorCode: number;
  displayOrder: number;
  icon: boolean;
  id: string;
  liveServChannels: string;
  name: string;
  outcomeMeaningMajorCode: string;
  outcomeMeaningMinorCode: string;
  outcomeStatusCode: string;
  price: IQuickbetSelectionPriceModel;
}
