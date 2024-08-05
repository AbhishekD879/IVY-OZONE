import { ISportEvent } from '@core/models/sport-event.model';
import { IPromotion } from '@core/services/cms/models/promotion/promotion.model';
import { IParticipantFromName, IParticipants } from '@app/bigCompetitions/services/participants/participants.model';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';

export interface IBCModule {
  id: string;
  name: string;
  type: string;
  markets: ICompetitionMarket[];
  events: IBigCompetitionSportEvent[];
  knockoutEvents: IKnockoutEvent[];
  knockoutRounds: IKnockoutRound[];
  maxDisplay: number;
  viewType: string;
  aemPageName?: string;
  typeId: string;
  promotionsData?: {
    promotions: IPromotions[]
  };
  groupModuleData?: {
    data: IModuleData[];
    seasonId: number;
    numberQualifiers: number;
    details?: {};
    areaId?: number;
    competitionId?: number;
    sportId?: number
  };
  specialModuleData?: {
    typeIds: string[];
    eventIds: string[];
    linkUrl: string;
  };
}

interface IPromotions {
  description: string;
  disabled: boolean;
  heightMedium: number;
  htmlMarkup: string;
  isSignpostingPromotion: boolean;
  promoKey: string;
  promotionText: string;
  shortDescription: string;
  showToCustomer: string[];
  targetUri: string;
  title: string;
  uriMedium: string;
  useDirectFileUrl: boolean;
  validityPeriodEnd: string;
  validityPeriodStart: string;
  vipLevels: string[];
  widthMedium: number;
}

interface IKnockoutRound {
  abbreviation: string;
  active: boolean;
  name: string;
  number: number;
}

export interface IKnockoutEvent {
  eventId: number;
  homeTeam: string;
  awayTeam: string;
  homeTeamRemark: string;
  awayTeamRemark: string;
  venue: string;
  startTime: string;
  round: string;
  abbreviation: string;
  resulted: boolean;
  result: ICompetitionMatchResult;
  eventName: string;
  obEvent: ISportEvent;
  participants: IParticipantFromName;
}

export interface ICompetitionMatchResult {
  score?: string[];
  aet?: string[];
  pen?: string[];
}

interface IModuleData {
  teams: ITeams[];
  ssEvents: ISportEvent[];
}

interface ITeams {
  name: string;
}

export interface IBCData {
  hasSubtabs: boolean;
  id: string;
  path: string;
  title: string;
  uri: string;
  competitionModules: ICompetitionModules[];
  competitionTabs: ICompetitionTab[];
  typeId?: number;
  name?: string;
  clazzId?: number;
  categoryId?: number;
  svgBgId?: string;
  background: string;
  competitionParticipants?: IParticipants[];
}

export interface ICompetitionTab {
  id: string;
  path: string;
  url: string;
  uri: string;
  competitionSubTabs: ICompetitionSubTab[];
  hasSubtabs?: boolean;
  name?: string;
}

export interface ICompetitionSubTab {
  id: string;
  path: string;
  url: string;
  name?: string;
}

export interface ICompetitionModules {
  id: string;
  type: string;
  name: string;
  maxDisplay: number;
  viewType: string;
  markets: ICompetitionMarket[];
  promotionsData?: {
    promotions: IPromotion[];
  };
  results: IResultsGroups[];
  surfaceBets?: string[];
  highlightCarousels?: string[];
  brand?: IBCHBrand;
}

export interface IBCHBrand {
  device: string;
  brand: string;
}
export interface IResultsGroups {
  limit: number;
  matches: IResultsMatches[];
  date: string;
}

export interface IResultsMatches {
  teamA: IResultsTeam;
  teamB: IResultsTeam;
  index?: number;
}

interface IResultsTeam {
  goalScorers: string;
  name: string;
  score: string;
}

export interface ICompetitionMarket {
  collapsed: boolean;
  marketId: string;
  maxDisplay: number;
  nameOverride: string;
  viewType: string;
  isExpanded?: boolean;
  data?: ISportEvent;
}
