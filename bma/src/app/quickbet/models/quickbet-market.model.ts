export interface IQuickbetMarketModel {
  name?: string;
  id?: string;
  marketName?: string;
  marketId?: string;
  hasLP?: boolean;
  hasGP?: boolean;
  isGpAvailable?: boolean;
  marketStatusCode?: string;
  isEachWayAvailable?: boolean;
  eachWayFactorDen?: string;
  eachWayFactorNum?: string;
  isMarketBetInRun?: boolean;
  outcomes?: IQuickbetOutcomeModel[];
  isSpAvailable?: boolean;
  outcomeId?: string;
  outcomeName?: string;
  outcomeStatusCode?: string;
  outcomeMeaningMinorCode?: string;
  isLpAvailable?: boolean;
  handicapValue?: string;
  oldHandicapValue?: string;
  drilldownTagNames?: string;
}

export interface IQuickbetOutcomeModel {
  id?: string;
  name?: string;
  outcomeMeaningMajorCode?: string;
  outcomeMeaningMinorCode?: string;
  outcomeStatusCode?: string;
}
