export interface IFiveASidePlayers {
  home: IFiveASidePlayer[];
  away: IFiveASidePlayer[];
  allPlayers: IFiveASidePlayer[];
}

export interface IFiveASidePlayer {
  id: number;
  name: string;
  teamName: string;
  teamColors: ITeamColors;
  appearances: number;
  cleanSheets: number;
  tackles: number;
  passes: number;
  crosses: number;
  assists: number;
  shots: number;
  shotsOnTarget: number;
  shotsOutsideTheBox: number;
  goalsInsideTheBox: number;
  goalsOutsideTheBox: number;
  goals: number | string;
  cards: number;
  cardsRed: number | string;
  cardsYellow: number | number;
  position: {
    long: string;
    short: string;
  };
  penaltySaves: number;
  conceeded: number;
  saves: number;
  isGK: boolean;
}

export interface ITeamColors {
  primaryColour: string;
  secondaryColour: string;
  teamsImage?: ITeamsImage;
  fiveASideToggle?: boolean;
  highlightCarouselToggle?: boolean;
}
export interface ITeamColours {
  teamName: string;
  colors: ITeamColors;
  teamsImage?: ITeamsImage;
  fiveASideToggle?: boolean;
  highlightCarouselToggle?: boolean;
}

export interface ITeamColorsData extends ITeamColors {
  teamName: string;
  id: string;
  sportId: string;
  secondaryNames: Array<string>;
}

export interface ITeamsExist {
  filename: string;
  fiveASideToggle: boolean;
}

export interface ITeamsImage extends File {
  originalname?: string;
  filename?: string;
  svg ?: string;
}
