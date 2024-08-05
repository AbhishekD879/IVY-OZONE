import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

export interface ICSEvent extends ISportEvent {
  isDelay?: boolean;
  isActive?: boolean;
  time?: string;
  teams?: ICSTeams;
  combinedOutcomes?: IOutcome;
}

export interface ICSTeams {
  teamA: {
    name: string;
    score: number;
    scores: number[];
  };
  teamH: {
    name: string;
    score: number;
    scores: number[];
  };
}

export interface ITeamsScores {
  teamA: number[];
  teamH: number[];
}
