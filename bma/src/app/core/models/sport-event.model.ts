import { IMarket } from './market.model';
import { ITeams } from './teams.model';
import { ILiveClock } from '@core/models/live-clock.model';
import { IPoolEntity } from '@core/models/pool.model';
import { IRacingPostVerdict } from '@racing/models/racing-post-verdict.model';
import { ICountDownTimer } from '@app/core/services/time/time-service.model';
import { ISportTeamColors } from '@app/sb/models/sport-configuration.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IDelta } from '@app/core/models/delta-object.model';

export interface IEventData {
  collection: IMarket[];
  event: ISportEvent[];
}

export interface ISportEvent {
  cashoutAvail: string;
  categoryCode: string;
  categoryId: string;
  categoryName: string;
  displayOrder: number;
  eventSortCode: string;
  eventStatusCode: string;
  id: number;
  liveServChannels: string;
  liveServChildrenChannels: string;
  typeId: string;
  typeName: string;
  name: string;
  startTime: string;
  yards?: string;
  distance?: string;
  raceType?: string;
  horses?: IHorse[];
  drilldownTagNames?: string;
  eventIsLive?: boolean;
  eventTerms?: string;
  isUS?: boolean;
  isBCH?: boolean;
  originalName?: string;
  responseCreationTime?: string;
  markets?: IMarket[];
  objId?: string;
  flags?:string[];
  racingFormEvent?: {
    class?: string;
    distance?: string;
    going?: string;
    overview?: string;
    title?: string;
    postPick?: string;
    newspapers?: [ISportEventNewspaper];
    horses?: [ISportEventHorses];
    courseGraphics?: string;
    raceType?: string;
    grade?: string;
  };

  liveStreamAvailable?: boolean;
  marketSelector?: string;
  isGpAvailable?: boolean;
  racingPostVerdict?: IRacingPostVerdict;
  // TODO: Dynamic properties remove dynamic param
  streamProviders?: {
    ATR: boolean;
    IMG: boolean;
    Perform: boolean;
    RPGTV: boolean;
    RacingUK: boolean;
    iGameMedia: boolean;
  };

  marketsCount?: number;
  outcomeId?: number;
  svgId?: string;
  isStarted?: boolean;
  groupedLimit?: number;
  liveEventOrder?: number;
  isAvailable?: string | boolean;
  mediaTypeCodes?: string;
  isLiveNowOrFutureEvent?: string;
  isNext24HourEvent?: string;
  isOpenEvent?: string | boolean;
  classFlagCodes?: string;
  classSortCode?: string;
  sportId?: string;
  siteChannels?: string;
  filteredStartTime?: string;
  comments?: IEventComments;
  typeNames?: string;
  eventCorectedDay?: string;
  categoryDisplayOrder?: string;
  initClock?: ILiveClock;
  isActive?: boolean;
  startTimeFiltered?: string;
  isDisplayed?: boolean;
  filteredTime?: string;
  linkedEventId?: number;
  displayed?: any;
  clock?: any;
  isResulted?: any;
  poolTypes?: string[];
  index?: number;
  localTime?: string;
  liveSimAvailable?: boolean;
  isUKorIRE?: boolean;
  isFinished?: any;
  silksAvailable?: boolean;
  sortedMarkets?: IMarket[];
  oddsCardHeaderType?: string | void;
  nameOverride?: string;
  aggregation?: any;
  typeFlagCodes?: any;
  pool?: IPoolEntity;
  className?: any;
  classId?: any;
  classDisplayOrder?: any;
  countdownTimer?: ITimer;
  liveTimer?: ITimer;
  typeDisplayOrder?: any;
  selected?: number;
  unavailable?: boolean;
  target?: any;
  children?: any[];
  outcomeStatus?: boolean; // Comes in event from featured MicroService only !
  outcomeStatusCode?: boolean; // Comes in event from featured MicroService only !
  hideEvent?: boolean; // Comes in event from featured MicroService only !,
  startTimeUnix?: number;
  viewType?: string;
  raceStage?: string;
  resulted?: boolean;
  isLiveNowEvent?: boolean | string;
  SSResponse?: any;
  externalKeys?: {
    OBEvLinkScoop6?: number;
    OBEvLinkNonTote?: number;
    OBEvLinkPlacepot7?: number;
  };
  goalScorers?: any[];
  goalScorersShowAll?: boolean;
  goalScorersToShow?: number;
  goalScorersHeader?: string | string[];
  coupon?: boolean;
  atLeastOneWinnerIsPresent?: any;
  uiClass?: any;
  country?: string;

  obTypeId?: number;
  timeformData?: any;
  correctedDay?: string;
  correctedDayValue?: string;
  rawIsOffCode?: any;
  linkedEntityId?: string | number;
  toteEventId?: number;
  primaryMarkets?: IMarket[];
  isExtraPlaceOffer?: boolean;
  buildYourBetAvailable?: boolean;
  marketId?: any;
  selectionId?: any;
  persistentInCache?: boolean;
  scoreType?: string;
  isVirtual?: boolean;
  time?: string;
  dateTime?: string;
  courseName?: string;
  countDowntimer?: ICountDownTimer | string;
  segmentOrder?: number;
  assetManagements?: Array<ISportTeamColors>;
  displayOnDesktop?: boolean;
  isCouponScoreboardOpened?: boolean;
  couponStatId?: string;
  isShowStatsEnabled?: boolean;
  regularTimeFinished?: boolean;
  isExpanded?: boolean;
  competitionSection?: ITypeSegment;
  compIndex?: number;
  url?: string;
  effectiveGpStartTime?: any;
  delta?: IDelta;
}

export interface ISportEventNewspaper {
  flag: string;
  name: string;
  rpSelectionUid: number;
  rpTip: string;
  selection: string;
  tips: string;
}

export interface ISportEventHorses {
  horseName: string;
  isMostTipped: string;
  nonRunner?: string;
}

interface ITimer {
  startTime: string;
  timeLeft: number;
  minutes?: number;
  seconds?: number;
  start: Function;
  stop: Function;
  postUpdate: Function;
  update: Function;
  isDisplayed?: boolean;
}

export interface IEventComments {
  teams: ITeams;
  facts?: any[];
  latestPeriod?: { [index: string]: any };
  setsScores?: { [key: string]: number; }[];
  runningSetIndex?: number;
  runningGameScores?: { [index: string]: any };
}

export interface ISportEventGroup {
  [key: string]: ISportEvent[];
}

export interface ICombinedSportEvents {
  groupedByMeetings: ISportEventGroup;
  groupedByFlagAndData: IGroupedSportEvent[];
  sportEventsData?: ISportEvent[];
}

export interface IGroupedSportEvent {
  flag: string;
  data: ISportMeeting[];
}

export interface ISportMeeting {
  meeting: string;
  events: ISportEvent;
}

export interface IHorse {
  name: string;
  jockey: string;
  horseName: string;
  trainer: string;
  spotlight: string;
  isBeatenFavourite?: any;
  silk: string;
  runnerNumber?: string;
  isMostTipped?: boolean;
}

export interface IEventMostTipData extends ISportEvent {
  powerHorse?: IHorse;
  powerHorses?: IHorse[];
  isMostPowerHorse?: boolean;
  horses?: IHorse[];
}

export interface IRecentRaceTipsData {
  races: ISportEvent[];
  nextRace: boolean;
}
export interface IMapping {
  id: string;
  system: string;
}

export interface IBooking {
  booked: string;
  bookingRequestTime: string;
  bookingTime: string;
  bookingError: string;
}

export interface IFeedMappings {
  provider: string;
  id: string;
  booking: IBooking;
}

export interface IProviderType {
  name: string;
  providerId: string;
  role: string;
}

export interface IParticipantType {
  [key: string]: IProviderType;
}


export interface ISportByMapping {
  [name: string]: any;
  id?: string;
  name?: string;
  startTime?: string;
  sport?: string;
  competition?: string;
  mappings?: IMapping[];
  feedMappings?: IFeedMappings[];
  participants?: IParticipantType;
}

export interface IWindow extends Window {
  SIR: Function;
  frontRowSeat?: IFrontRowSeat;
}

export interface IChildCount {
  count: string;
  id: string;
  refRecordId: string;
}

export interface IFrontRowSeat {
  eventCentreUtils: IEventCenterUtils;
  eventCentre: Function;
}

export interface IEventCenterUtils {
  MessageTopics: IMessageTopics;
}

export interface IMessageTopics {
  HANDSHAKE_FAILED: Object;
  VIDEO_PLAYBACK_AUTH_REQUEST: Object;
  VIDEO_PLAYBACK_AUTH_RESPONSE: Object;
}