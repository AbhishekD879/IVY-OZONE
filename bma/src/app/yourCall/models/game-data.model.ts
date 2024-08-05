import { IYourcallSelection } from '@yourcall/models/selection.model';

export interface IYourcallGameData {
  betType: number;
  created: string;
  game: IYourCallGame;
  id: number;
  markets: IYourcallGameMarket[];
  statistic: IYourcallGameStatistic;
  updated: any;

  player1: {
    name: string;
    id: string;
  };
  team: {
    id: string;
  };
  selections: IYourcallSelection[];
}

export interface IYourCallGame {
  id: number;
  date: string;
  homeTeam: IYourCallGameTeam;
  visitingTeam: IYourCallGameTeam;
  sportId: number;
  status: number;
  byb: {
    homeTeam: { id: number; };
    visitingTeam: { id: number; };
  };
}

export interface IYourCallGameTeam {
  abbreviation: string;
  id?: number;
  title: string;
  players: any;
}

export interface IYourcallGameMarket {
  condition: number;
  id: number;
  isActive: number;
  odds: number;
  settlement: {
    result: string;
    value: number
    voidReason: any;
  };
  type: number;
  value: number;

  // DYNAMIC ADDED DATA
  title: string;
  statisticId: number;
  dashboardTitle?: string;
  name: string;
}

export interface IYourcallGameStatistic {
  id: number;
  title: string;
  phraseTitle: string[];
}
