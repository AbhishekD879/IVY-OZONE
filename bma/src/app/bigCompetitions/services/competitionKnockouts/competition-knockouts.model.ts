export interface IKnockoutData {
  knockoutRounds: IKnockoutRounds[];
  knockoutEvents: IKnockoutEvents[];
}

export interface IKnockoutRounds {
  name: string;
  active: boolean;
  abbreviation: string;
  number: number;
}

export interface IKnockoutEvents {
  abbreviation: string;
  awayTeam: string;
  homeTeam: string;
  round: string;
}

export interface IEventsByRoundMap {
  roundNames: IKnockoutRounds[];
}

