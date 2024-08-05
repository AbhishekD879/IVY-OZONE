import { ISilkStyleModel } from '@core/services/raceOutcomeDetails/silk-style.model';

export interface IRacesListResponse {
  cypher: IRacesList;
}

export interface IRacesList {
  meetings: IMeeting[];
  runners: IRunner[];
}

export interface IMeeting {
  courseShort: string;
  course?: string;
}

export interface IRunner {
  raceId: string;
  horseId: string;
  raceDate: string;
  time: string;
  dayValue: string;
  course: string;
  courseShort: string;
  horseName: string;
  starRating: string;
  odds: string;
  oddsLength: string;
  trainerForm: string;
  jockeyAbility: string;
  wellHandicapped: string;
  marketMover: string;
  courseWinner: string;
  distanceWinner: string;
  courseDistanceWinner: string;
  winnerLastTime: string;
  winnerLast3Starts: string;
  placedLastTime: string;
  placedLast3Starts: string;
  beatenFavLastTime: string;
  firstTimeHeadGear: string;
  headGear: string;
  provenGoing: string;
  provenDistance: string;
  form: string;
  potential: string;
  draw: string;
  horseToFollow: string;
  supercomputerSelection: string;
  attitude: string;
  jumping: string;
  fitness: string;
  improver: string;
  firstTimeOut: string;
  firstRunAfterWindOp: string;
  vibe: string;
  jockeyName: string;
  jockeyAliasName: string;
  trainerName: string;
  trainerAliasName: string;
  bookmakerEventId: string;
  bookmakerCompetitorId: string;
  silkID: string;
  silkStyle?: ISilkStyleModel;
  number: string;
  formString: string;
  decimalOdds: number;
  odds32: string;
  odds16: string;
  odds4: string;
  odds1: string;
  odds8: string;
  odds0: string;
  oddsToDisplay?: string;
}
