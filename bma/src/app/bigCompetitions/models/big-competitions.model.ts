import { ISportEvent } from '@core/models/sport-event.model';
import { IParticipantFromName } from '@app/bigCompetitions/services/participants/participants.model';
import { IConstant } from '@core/services/models/constant.model';

export interface IBigCompetitiomsParams {
  name: string;
  tab: string;
  subTab: string;
}

export interface IBigCompetitionSportEvent extends ISportEvent {
  participants: IParticipantFromName;
}

export interface IGroupModule {
  id: string;
  name: string;
  type: string;
  maxDisplay: number;
  viewType: string;
  aemPageName: string;
  isExpanded: boolean;
  markets: IGroupMarket[];
  specialModuleData: {
    typeIds: string[],
    eventIds: string[],
    linkUrl: string;
  };
  groupModuleData: IGroupData;
  events: ISportEvent[];
  errors: string[]; // todo
  results: string[]; // todo
}

export interface IGroupMarket {
  marketId: string;
  maxDisplay: number;
  collapsed: boolean;
}

export interface IGroupData {
  sportId: number;
  areaId: number;
  competitionId: number;
  seasonId: number;
  numberQualifiers: number;
  details: IConstant;
  data: IGroupModuleData[];
}

export interface IGroupModuleData {
  competitionId: number;
  seasonId: number;
  tableId: number;
  tableName: string;
  teams: IGroupTeam[];
  ssEvents: ISportEvent[];
}

export interface IGroupTeam {
  name: string;
  obName: string;
}
