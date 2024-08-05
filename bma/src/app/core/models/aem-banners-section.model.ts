export interface IParams {
  page?: string;
  brand?: string;
  channel?: string;
  locale?: string;
  userType?: string;
  imsLevel?: any;
  device?: string;
  maxOffers?: number;
  atJsLoadingTimeout?: number;
}

export interface IAemConfig {
  server: string;
  at_property: string;
  betslip_at_property: string;
  offer_modules_at_property?: string;
}

export interface IAEMCarousel {
  settings: any;
  _options: {
    brand?: string;
    locale?: string;
    server?: string;
    channel?: string;
    userType?: string;
    maxOffers?: number;
  };
}

export interface IOfferFromServer {
  id?: string;
  imgUrl: string;
  offerTitle: string;
  webUrl?: string;
  appUrl?: string;
  roxanneWebUrl?: string;
  roxanneAppUrl?: string;
  webTarget?: string;
  appTarget?: string;
  webTandC: string;
  webTandCLink?: string;
  mobTandCLink?: string;
  personalised?: boolean;
}

export interface ISitecoreOfferFromServer {
  type: string;
  teasers: ISiteCoreTeaserFromServer[];
}

export interface IOfferGroupsFromServer {
  target?: ISiteCoreTeaserFromServer[];
  library?: ISiteCoreTeaserFromServer[];
  pinned?: ISiteCoreTeaserFromServer[];
  rg?: ISiteCoreTeaserFromServer[];
}

export interface IOfferReport {
  providers?: any;
  offers: IOffer[];
}

export interface ICMSBannerConfig {
  enabled: boolean;
  timePerSlide: number;
  maxOffers: number;
}

export interface IOffer {
  previousOdds?: string;
  currentOdds?: string;
  tracked?: boolean;
  bannerStatus?: boolean;
  name?: any;
  active?: boolean;
  brand?: string;
  imgUrl?: string;
  altText?: string;
  title?: string;
  link?: string;
  target?: string;
  tcText?: string;
  tcLink?: string;
  position?: number;
  lazy?: boolean;
  imgClass?: string;
  personalised?: boolean;
  imageLoaded?: boolean;
  Id?: string;
  animatedbannerimage?: string;
  foregroundimage?: string;
  introductorytext?: string;
  subtitle?: string;
  itemName?: string;
  outcomeId?: string;
  foregroundAltText?: string;
  tcTarget?: string;
  index?: number;
  fetchpriority?: string;
}

export interface IAEMTargetBetslipParameters {
  page?: string;
  categoryId?: string;
  typeId?: string;
  eventId?: string;
  marketId?: string;
  selectionId?: string;
}

export interface ISiteCoreTeaserFromServer {
  type?: string;
  teasers?: ISiteCoreTeaserFromServer[];
  name?: string;
  active?: boolean;
  id?: string;
  brand?: string;
  imgUrl?: string;
  altText?: string;
  title?: string;
  animatedbannerimage?: string;
  backgroundImage?: IbackgroundImage;
  bannerLink?: IbannerLink;
  foregroundImage?: IforegroundImage;
  introductoryText?: string;
  keyTermsAndConditions?: string;
  subTitle?: string;
  termsAndConditionsLink?: ItermsAndConditionsLink;
  itemId?: string;
  itemName?: string;
  liveOddsBannerSelectionID?: string;
  previousOddsValue?: string;
}

export interface IContenTeasers {
  teasers: ISiteCoreTeaserFromServer[];
  type: string;
}

export interface ItermsAndConditionsLink {
  attributes?: Itarget;
  text?: string;
  url?: string;
}

export interface IforegroundImage {
  alt?: string;
  height?: number;
  src?: string;
  width?: number;
}

export interface IbannerLink {
  attributes?: Itarget;
  text?: string;
  url?: string;
}

export interface IbackgroundImage {
  alt?: string;
  height?: number;
  src?: string;
  width?: number;
}
export interface Itarget {
  target?: string;
}
export const AT_JS_LOADING_TIMEOUT: number = 2000;
