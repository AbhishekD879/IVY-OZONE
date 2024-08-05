import { ITimeFormEntry } from '@core/models/time-form-entry.model';

export interface ITimeFormData {
  actualRaceTimeLocal: string;
  bigRace: boolean;
  entries: ITimeFormEntry[];
  handicapRace: boolean;
  meetingId: number;
  officialGoing: number;
  openBetIds: number[];
  performances: any;
  prizes: string;
  raceDistance: number;
  raceGradeName: string;
  raceId: number;
  raceNumber: number;
  raceStateName: string;
  raceTitle: string;
  raceTypeName: string;
  scheduledRaceTimeGmt: string;
  scheduledRaceTimeLocal: string;
  smartStats: string;
  trackId: number;
  trackProfile: string;
  trackShortName: string;
  updateDate: string;
  uuid: string;
  verdict: string;

  winnerPrediction: {
    greyHoundFullName: string;
  };
  positions: {
    trainer: string;
    positionPrediction: string;
    greyHoundFullName: string;
    stars: string
  }[];
}
