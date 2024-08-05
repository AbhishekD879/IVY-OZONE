export interface IGtmEvent {
  eventCategory?: string;
  eventAction: string;
  eventLabel?: string;
  location?: string;
  "component.EventDetails"?:string;
  selectionID?: string;
  tracking?: any;
  betData?: any;
}

export interface IGtmBannerEvent extends IGtmEvent {
  event: string;
  position: number;
  vipLevel: string;
  personalised: boolean;
}

export interface IGtmCashOutEvent extends IGtmEvent {
  cashOutOffer: number;
  cashOutType: string;
  partialPercentage?: number;
  oddsBoost: string;
}

export interface IGATrackingModel {
  isHomePage?: boolean,
  event: string,
  GATracking: {
    eventAction: string,
    eventCategory: string,
    eventLabel: string,
  }
}