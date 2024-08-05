export interface ICoupon {
  cashoutAvail: boolean;
  categoryCode: string;
  categoryDisplayOrder: string;
  categoryId: string;
  categoryName: string;
  couponSortCode: string;
  displayOrder: number;
  hasLiveNowOrFutureEvent: string;
  hasOpenEvent: string;
  id: string;
  name: string;
  responseCreationTime: string;
  siteChannels: string;
}

export interface ICouponWithEvents extends ICoupon {
  isEventsLoaded: boolean;
  isEventsAvailable: boolean;
  events: any;
  isExpanded: boolean;
}
