export interface IBetTrackerParams {
  mode: string;
  username: string;
  sessionToken?: string;
  accountBusinessPhase?: string;
  cardNumber: string;
  devicePlatform: string;
  betType?: string;
  fromDate?: string;
  toDate?: string;
  RECAPTCHA_SITE_KEY?: string;
}
