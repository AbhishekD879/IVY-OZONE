export type IRacingPostMapping<T> = { [key in keyof T]?: string; };

export interface IRacingPostMappingConfig<T, U> {
  eventKeysMap: IRacingPostMapping<T>;
  outcomeKeysMap: IRacingPostMapping<U>;
  runnersKeys: {
    runnersPropName: string;
    runnerNumberPropName: string;
  };
}

export interface IRacingPostResponse<T> {
  Error: string;
  document: { [key: string]: T };
}

export type IRacingPostHRResponse = IRacingPostResponse<IRacingPostHRRaceData>;

export interface IRacingPostHRRaceData {
  yards: string;
  verdict: string;
  goingCode: string;
  raceName: string;
  raceClass: string;
  horses: IRacingPostHorse[];
  courseGraphicsLadbrokes: string;
  newspapers: IRacingPostHRNewspaper[];
  results?: IRaceResultsData;
  raceType: string;
}

export interface IRacingPostHorse {
  trainer: string;
  rating: string;
  horseAge: string;
  jockey: string;
  silkLadbrokes: string;
  formfigs: string;
  weightLbs: string;
  spotlight: string;
  officialRating: string;
  rpRating: string;
  draw: string;
  courseDistanceWinner: string;
  isBeatenFavourite: boolean;
  starRating: string;
  silk: string;
  form?: string[];
  saddle?: string;
  isMostTipped?: boolean;
  horseName: string;
  allowance?: number;
  rpHorseId?: number;
}

export interface IRaceResultsData{
  nonRunners?: string,
  raceComments?: string,
  winSecs?: string,
  abandonReason?: string,
  offtime?: string,
  runners?: IRaceResultRunnersData[];
}

export interface IRaceResultRunnersData{
  comment?: string;
  saddle?: string;
  jockeyName?: string;
  distanceToWinner?: string;
  position?: string;
  horseName?: string;
  distanceHif?: string;
  rpHorseId?: number;
  odds?: string;
  raceOutcomeCode?: string;
  raceOutcomeDesc?: string;
}

export type IRacingPostGHResponse = IRacingPostResponse<IRacingPostGHRaceData>;

export interface IRacingPostGHRaceData {
  distance: string;
  raceType: string;
  postPick: string;
  grade?: string;
  runners: IRacingPostGreyhound[];
  results?: IRaceGHResultsData;
  totalRunners: number;
}
export interface IRacingPostGreyhound {
  comment?: string;
  last5Runs?: string;
  trap?: string;
  trainerName: string;
}

export interface IRacingPostHRNewspaper {
  flag: string;
  name: string;
  rpSelectionUid: number;
  rpTip: string;
  selection: string;
  tips: string;
}

export interface IRacingDataHubConfig {
  isEnabledForGreyhound?: boolean;
  isEnabledForHorseRacing?: boolean;
  timeFormEnabled?: boolean;
}

export interface IRaceGHResultsData {
  runners: IRaceGHResultsRunnersData[];
}

export interface IRaceGHResultsRunnersData {
  bendPosition: string;
  dogName: string;
  dogUid: number;
  fullCloseUpComment: string;
  position: string;
  raceOutcomeCode: string;
  raceOutcomeDesc: string;
  spOddsDesc: string;
  trainerName: string;
  trapNumber: string;
}