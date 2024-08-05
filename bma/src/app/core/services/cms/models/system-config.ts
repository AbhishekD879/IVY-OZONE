import { ISportEvent } from '@app/core/models/sport-event.model';

export interface ISystemConfig {
  [name: string]: any;

  Betslip?: any;
  Connect?: IRetailConfig; // TODO: rename to retail after changes in cms.
  Banners?: IBannersModel;
  Layouts?: ILayoutsModel;
  Header?: IHeaderModel;
  LCCP?: ILCCPModule;
  Generals?: IGeneralModel;
  ExternalUrls?: IExternalUrls;
  RouletteJourney?: IRouletteModel;
  GreyhoundNextRacesToggle?: IGreyhoundNextRacesConfig;
  GreyhoundFullResults?: IGreyhoundFullResultsConfig;
  RacingDataHub?: IRacingDataHub;
  NextRaces?: INextRaces;
  GreyhoundNextRaces?: IGreyhoundNextRaces;
  NextRacesToggle?: INextRacesToggle;
  Promotions?: IPromotionsConfig;
  VirtualScrollConfig?: IVirtualScrollConfig;
  Overask?: IOverAskSysConfigModel;
  SportCompetitionsTab?: ISportCompetitionsTab;  
  MainBetslipStakes?: IMainBetslipStakes;
  racingPostTip?: IRacePostTip;
  nextRacesToBetslip?: INextRacesToBetslip;
  MyBetsDateLimit?: IMyBetsDateLimit;
  MybetsMatchCommentary?: IMybetsMatchCommentary;
  DesktopHomePageOrder?: IDesktopHomePageOrder;
  HorseRacingBIR?: IHorseRacingBIR;
  Freebets?: IFreebetsPopupDetails;
  OddsBoostMsgConfig?:IOddsBoostMsgConfigDetails;
  BonusSupErrorMsg?: BonusSupErrorMsg;
  SeoSchemaConfig?: ISeoSchemaConfig;
  VirtualEntryPointConfig?: IVirtualEntryPointConfig;
  VirtualHubHomePage?: IVirtualHomePageSystemConfig;
  StreamBetWeb?: IStreamBetWeb;
  streamBetTutorialConfig?: IStreamBetTutorialConfig;
  streamBetTutorialConfigNative?: IStreamBetTutorialConfigNative;
}
export interface IMainBetslipStakes {
  BetslipStakes?: string[];
}
export interface IMainBetslipStakes {
  BetslipStakes?: string[];
}

export interface BonusSupErrorMsg {
  errorMsg?: string;
  url?: string;
}

export interface IFreebetsPopupDetails {
  header?: string;
  boostEnabled?: string;
  boostActive?: string;
  freeBetsAvailableText?: string;
  useFreeBetText?: string;
  addFreeBet?: string;
  freeBetAdded?: string;
  plusFreeBet?: string;
  addSelections?: string;
  plusTokenAndFreeBet?: string;
  plusToken?: string;
  betTokenAdded?: string;
  addBetToken?: string;
  addTokenAndFreeBet?: string;
  betTokensAvailableText?: string;
  freebetAndTokensAvailableText?: string;
  freebetDescription?: string;
  fanZonesAvailableText?: string;
  addFanZone?: string;
  fanZoneAdded?: string;
  fanzoneTabName?: string;
}

export interface IOddsBoostMsgConfigDetails {
  noThanks?: string;
  yesPlease?:string;
  okThanks?:string;
  continueWith?:string;
  cancelBoostPriceMessage?:string;
  cantBoostMessage?:string;
}

export interface IMyBetsDateLimit {
  settledBets?: number;
  openBets?: number;
  maxValue?: number;
  cashout?: number;
}

export interface IRetailConfig {
  digitalCoupons: boolean;
  footballFilter: boolean;
  login: boolean;
  menu: boolean;
  overlay: boolean;
  promotions: boolean;
  shopBetHistory: boolean;
  shopBetTracker: boolean;
  shopLocator: boolean;
  upgrade: boolean;
  savedBetCodes: boolean;
  inShopBets?: boolean;
}

export interface ICompetitionsConfig {
  'A-ZClassIDs': string;
  InitialClassIDs: string;
}

interface IHeaderModel {
  gameButtonLink: string;
  rr: string;
  showInApp: string;
  tt: string;
}

interface ILayoutsModel {
  ShowLeftMenu: string;
  ShowRightMenu: string;
  ShowTopMenu: string;
}

interface IBannersModel {
  newName: boolean;
  transitionDelay: string;
}

interface ILCCPModule {
  gameFrequency: string;
  gameFrequencyValues: string;
  hourlyAlerts: string;
}

interface IGeneralModel {
  betSlipAnimation: string;
  title: string;
}

export interface IExternalUrls {
  [key: string]: string;
}

interface IRouletteModel {
  isRouletteEnabled: boolean;
  successNavigationUrl: string;
  timeToRedirect?: number;
}

export interface IInplayModule {
  enabled: boolean;
  virtualScroll: boolean;
}

export interface IGreyhoundNextRacesConfig {
  nextRacesTabEnabled: boolean;
  nextRacesComponentEnabled: boolean;
}

export interface IGreyhoundFullResultsConfig {
  enabled: boolean;
}

export interface INextRacesToggle {
  nextRacesTabEnabled: boolean;
  nextRacesComponentEnabled: boolean;
}

export interface IRacingDataHub {
  isEnabledForGreyhound?: boolean;
  isEnabledForHorseRacing?: boolean;
}
interface IVirtualsInNextRaces {
  isVirtualRacesEnabled: string;
  virtualRacesIncluded: string[];
}

export interface INextRaces extends IVirtualsInNextRaces {
  isInUK: string;
  isInternational: string;
  isIrish: string;
  numberOfEvents: string;
  numberOfSelections: string;
  showPricedOnly: string;
  title: string;
  typeDateRange: {
    from: string;
    to: string;
  };
  typeID: string;
}

export interface IGreyhoundNextRaces extends IVirtualsInNextRaces {
  numberOfEvents: string;
  numberOfSelections: string;
}

export interface IPromotionsConfig {
  expandedAmount: string;
  groupBySections: boolean;
}

export interface IVirtualScrollConfig {
  enabled: boolean;
  iOSInnerScrollEnabled: boolean;
  androidInnerScrollEnabled: boolean;
}

export interface IOverAskSysConfigModel {
  title: string;
  bottomMessage: string;
  topMessage: string;
  traderOfferNotificationMessage: string;
  traderOfferExpiresMessage: string;
}

export type ICombinedRacingConfig = Pick<ISystemConfig, 'NextRaces' | 'RacingDataHub' | 'GreyhoundNextRaces'>;

export interface ISportCompetitionsTab {
  eventsLimit: number;
}

export interface IVirtualSportsConfig {
  [key: string]: boolean;
}

export interface IMybetsMatchCommentary {
  enabled?: boolean;
}
export interface IDesktopHomePageOrder {
  featured?: number;
  inPlay?: number;
  nextRace?: number;
  yourCall?: number;
}
export interface IRacePostTip {
  enabled?: boolean;
}

export interface INextRacesToBetslip {
  enabled?: boolean;
  raceData?: ISportEvent[];
  isTipPresent: boolean;
}

export interface IHorseRacingBIR {
  streamEnabled?: boolean;
  marketsEnabled?: string[];
  floatingMsgEnabled?: string;
  inplaySignpostEnabled?: boolean;
}
export interface IMybetsMatchCommentary {
  enabled?: boolean;
}

export interface ISeoSchemaConfig{
  schemaConfig ?: string[];
}

export interface IVirtualEntryPointConfig{
  enabled?: boolean;
}

export interface IVirtualHomePageSystemConfig {
  featureZone?: boolean;
  headerBanner?: boolean;
  nextEvents?: boolean;
  otherSports?: boolean;
  topSports?: boolean;
  topSportsBackgroundID?: string;
  featureZoneBackgroundID?: string;
  enabled?:boolean;
}
export interface IStreamBetWeb{
  enabled?: boolean;
  sportIds?: string[];
  streamProviders?: string[];
  tutorialVideoUrl?: string;
  isAndroidStream?: boolean;
  isAndroidStreamURL?: string;
  isIOSStream?: boolean;
  toasterMsgNative?: string;
  toasterMsgWeb?: string;
  tutorialVideoLimit?: number;
}
export interface IStreamBetTutorialConfig{
  title?: string;
  descriptionOne?: string;
  descriptionTwo?: string;
}
export interface IStreamBetTutorialConfigNative{
  title?: string;
  descriptionOne?: string;
  descriptionTwo?: string;
}
