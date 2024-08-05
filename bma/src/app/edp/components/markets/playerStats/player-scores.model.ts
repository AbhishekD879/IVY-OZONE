export interface IPlayersScores {
  [key: string]: ISubModel | any[];
}

export interface ISubScores {
  score: string;
  number: number;
  outcomeid: string;
}

interface ISubModel {
  [key: string]: {
    activeScoreOutcome?: string;
    displayOrder?: string;
    displayArray: any[];
    name: string;
    id: string;
    scores: ISubScores[] | any[];
  };
}

export interface ISwitcherFields {
  viewName: string;
  filter: string;
}

export interface IPlayerGTM {
  playerName: string;
  playerStat: string;
  playerStatNum: number;
}

export interface IToggleState {
  templateMarketName?: string;
  wasCollapsed: boolean;
  wasExpanded: boolean;
}
