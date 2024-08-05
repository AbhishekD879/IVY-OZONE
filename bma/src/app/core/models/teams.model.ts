export interface ITeamPlayer {
  id: string;
  score?: string;
  isActive?: boolean;
  periodScore?: number;
  currentPoints?: string;
}

export interface ITeams {
  away?: ICommentsTeam;
  home?: ICommentsTeam;
  player_1?: ITeamPlayer;
  player_2?: ITeamPlayer;
  type?: string;
}

export interface ICommentsTeam {
  eventId?: string | number;
  id?: string;
  currentPoints?: any;
  score?: any;
  name?: string;
  role?: string;
  roleCode?: string;
  type?: string;
  periodScore?: string; // games score for Sets/Games/Points score template (Tennis)
  extraTimeScore?: string;
  penaltyScore?: string;
  inn2?: any;
}

export interface IPropertiesForUpdate {
  name: string;
  updateHard: boolean;
}
