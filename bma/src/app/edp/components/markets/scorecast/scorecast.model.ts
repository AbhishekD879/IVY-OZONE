import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';

export interface IScorecast extends IOutcome {
  scorerOutcomeId: string;
  scorecastPrices: string;
}

export interface ITeam {
  name: string;
  outcomeMeaningMinorCode: number;
}


export interface IOutcomesByTeam {
  [key: string]: IOutcome[];
}

export interface IScoreCastMarkets {
  [key: string]: IScorecastMarket;
}

export interface IScorecastMarket {
  teamsGoalscorers?: {
    [key: string]: IOutcome[];
  };
  market: IMarket;
  name: string;
  localeName: string;
  goalscorerMarket: IMarket;
  outcome: IOutcome;
  scorecasts: IScorecast[];
}

export interface IScorecastLookupTablePrice {
  price_cs_lo: number;
  price_cs_hi: number;
  price_fg_lo: number;
  price_fg_hi: number;
  price_num: number;
  price_den: number;
}

export interface IScorecastLookupTable {
  W: [IScorecastLookupTablePrice];
  L: [IScorecastLookupTablePrice];
  D: [IScorecastLookupTablePrice];
}
