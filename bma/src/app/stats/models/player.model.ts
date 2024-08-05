import { IStatsBase } from './base.model';
import { IStatsPlayerValues } from './player-values.model';

export interface IStatsPlayer extends IStatsBase {
  'Date of birth': IStatsPlayerValues;
  'First name': IStatsPlayerValues;
  'Full name': IStatsPlayerValues;
  'Height': IStatsPlayerValues;
  'Last name': IStatsPlayerValues;
  'Nationality': IStatsPlayerValues;
  'Position': IStatsPlayerValues;
  'Preferred foot': IStatsPlayerValues;
  'Shirt number': IStatsPlayerValues;
  'Weight': IStatsPlayerValues;
}
