import { ISportEvent } from '@core/models/sport-event.model';

export interface IFavouritesConfig {
  sportName?: string;
  fromWhere?: string;
  location?: string;
  event?: ISportEvent;
  isSyncWithNative?: boolean;
}

export interface IFavouritesText {
  introductoryText: string;
  loginButtonText: string;
}
