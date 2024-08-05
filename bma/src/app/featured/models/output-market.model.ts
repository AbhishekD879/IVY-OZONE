import { IOutputOutcome } from '../../inPlay/models/output-outcome.model';

export interface IMarketData {
  id: string;
  name: string;
  isLpAvailable: boolean;
  isSpAvailable: boolean;
  isGpAvailable: boolean;
  eachWayFactorNum: number;
  eachWayFactorDen: number;
  eachWayPlaces: number;
  liveServChannels: string;
  priceTypeCodes: string;
  ncastTypeCodes: string;
  cashoutAvail: string;
  handicapType: string;
  viewType: string;
  marketMeaningMajorCode: string;
  marketMeaningMinorCode: string;
  terms: string;
  isMarketBetInRun: boolean;
  rawHandicapValue: number;
  dispSortName: string;
  marketStatusCode: string;
  templateMarketId: number;
  templateMarketName: string;
  nextScore: number;
  drilldownTagNames: string;
  outcomes: IOutputOutcome[];
}
