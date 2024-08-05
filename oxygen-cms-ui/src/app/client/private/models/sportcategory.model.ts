import {SvgFilename} from './svgfilename.model';
import {Base} from './base.model';
import {InplaySportModule} from './inplaySportModule.model';

export const TARGET_URI_PATTERN = '^(sport\\/)[\\w-]+';
export const HORSE_RACING_SPORT = 21;
export const GREYHOUNDS_SPORT = 19;

export interface SportCategory extends Base {
  alt: string;
  categoryId: number;
  disabled: boolean;
  tier: string;
  heightMedium: number;
  heightMediumIcon: number;
  heightSmall: number;
  heightSmallIcon: number;
  imageTitle: string;
  inApp: boolean;
  isTopSport: boolean;
  key: string;
  lang: string;
  link: string;
  path: string;
  showInMenu: boolean;
  sortOrder: number;
  spriteClass: string;
  ssCategoryCode: string;
  outrightSport: boolean;
  multiTemplateSport: boolean;
  oddsCardHeaderType: string;
  typeIds: string;
  dispSortNames: string;
  primaryMarkets: string;
  svg: string;
  svgId: string;
  targetUri: string;
  uriMedium: string;
  uriMediumIcon: string;
  uriSmall: string;
  uriSmallIcon: string;
  widthMedium: number;
  widthMediumIcon: number;
  widthSmall: number;
  widthSmallIcon: number;
  collectionType: string;
  showInAZ: boolean;
  showInHome: boolean;
  showInPlay: boolean;
  heightLarge: number;
  heightLargeIcon: number;
  uriLarge: string;
  widthLarge: number;
  widthLargeIcon: number;
  scoreBoardUri: string;
  filename: SvgFilename;
  icon: SvgFilename;
  svgFilename: SvgFilename;
  showScoreboard: boolean;
  highlightCarouselEnabled: boolean;
  quickLinkEnabled: boolean;
  inplayEnabled: boolean;
  inplaySportModule: InplaySportModule;
  showFreeRideBanner?: boolean;
  message?: string;
  topMarkets:string;
  aggrigatedMarkets:AggregatedMarket[];
  messageLabel?: string;
  isRealSport(): boolean;
  isFRRealSport(): boolean;
  isReactionsEnabled: boolean;
  inplayStatsConfig: StatsConfig;
}
export interface AggregatedMarket{
  marketName: string;
  titleName:string;
}

export interface StatsConfig{
  showStatsWidget: boolean;
  note: string;
}

