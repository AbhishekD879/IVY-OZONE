import {Base} from './base.model';
import {CompetitionMarket} from './competitionmarket.model';
import {KnockoutsMatch} from './knockoutsmatch.model';
import { RoundNameModel } from './roundName.model';
import { SpecialTabModule } from './specialTabModule.model';

export interface CompetitionGroup {
  sportId: number;
  areaId: number;
  competitionId: number;
  seasonId: number;
  numberQualifiers: number;
  details: {
    [key: string]: string;
  };
}

export interface CompetitionModule extends Base {
  name: string;
  enabled: boolean;
  type: string;
  maxDisplay: number;
  promoTag: string;
  status: string;
  markets: Array<CompetitionMarket>;
  displayOrder: number;
  typeId: string;
  viewType: string;
  aemPageName: string;
  groupModuleData: CompetitionGroup;
  knockoutModuleData: {
    events: Array<KnockoutsMatch>
    rounds: Array<RoundNameModel>
  };
  specialModuleData: SpecialTabModule;
  eventIds: Array<number>;
  resultModuleSeasonId: number;
  categoryIDs: Array<number>;
  surfaceBets: Array<number>;
  highlightCarousels: Array<number>;
}

export interface StatsCenterCompetition {
  id: number;
  name: string;
  uniqIdentifier: number;
  areaId: number;
  sportId: number;
}

export interface StatsCenterSeason {
  id: number;
  name: string;
  startDate: string;
  endDate: string;
  year: number;
  competitionId: number;
  areaId: number;
  sportId: number;
  uniqueId: string;
  competitionIds: string[];
}

export interface StatsCenterGroups {
  allCompetitions: Array<StatsCenterCompetition>;
  allSeasons: Array <StatsCenterSeason>;
  areaId: number;
  areaName: string;
  competitionId: number;
  competitionName: string;
  sportId: number;
  sportName: string;
}
