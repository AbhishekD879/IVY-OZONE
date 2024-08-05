export interface ICouponEventsRequestParams {
  categoryId: string;
  siteChannels: string;
  isNotStarted: boolean;
  startTime: string;
  suspendAtTime: string;
  marketsCount: boolean;
  endTime?: string;
}
