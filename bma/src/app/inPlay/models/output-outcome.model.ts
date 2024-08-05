import { IOutputPrice } from './output-price.model';
import { IOutputRacingFormOutcome } from './output-racing-form-outcome.model';

export interface IOutputOutcome {
  id: string;
  name: string;
  outcomeMeaningMajorCode: string;
  outcomeMeaningMinorCode: string;
  outcomeMeaningScores: string;
  runnerNumber: string;
  isResulted: boolean;
  outcomeStatusCode: string;
  liveServChannels: string;
  correctPriceType: string;
  icon: boolean;
  correctedOutcomeMeaningMinorCode: number;
  nonRunner: boolean;
  prices: IOutputPrice[];
  displayOrder: number;
  racingFormOutcome: IOutputRacingFormOutcome;
}
