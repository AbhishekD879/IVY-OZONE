import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ISportEvent } from '@core/models/sport-event.model';

export interface IFreeBetState {
  available: boolean;
  data: IFreebetToken[];
  betTokens?: IFreebetToken[];
  fanZone?: IFreebetToken[];
  freeBetFanzoneData?: IFreebetToken[];
}

export interface IFreeBetBetslipFormat {
  expiry: string;
  id: string;
  offerName: string;
  value: string;
  type: string;
}

export interface IStoreFreeBets {
  data: IFreebetToken[];
  error?: string;
}

export interface IFreebetLink {
  eventData?: ISportEvent;
  categoryId: string;
}

export interface IFreebetCategory {
  categoryId: number;
  categoryName: string;
  betNowLink: string;
}

export interface IFreebetBetLevelMap {
  [betLevel: string]: {[categoryId: string]: IFreebetCategory};
}
