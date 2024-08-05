import { IMarket } from '@core/models/market.model';
import { IMarketLinks } from '@core/services/cms/models/edp-market.model';

export interface IGroupedMarket {
  name: string;
  headerLabel: string;
  header: IGroupedMarketHeader[];
  localeName: string;
  marketsAvailable: boolean;
  sortByHeader: boolean;
  template: string;
  lessCount: number;
  outcomesSort: string[];
  marketSort: string[];
  marketsTemplates: string[];
  marketsNames: string;
  cashoutAvail: string | boolean;
  type: string[] | string;
  markets: IMarket[] | any;
  periods: IMarketPeriod[];
  noGoalscorer?: INoGoalScorer;
  drilldownTagNames?: string;
  marketOptaLink?: IMarketLinks;
  sortOrder: {
    [key: string]: number
  };
  headerToMarket: {
    [key: string]: {
      name: string;
      sortOrder: number;
    }
  };
}

export interface INoGoalScorer {
  name: string;
  priceTypeCodes: string;
  outcomes: {}[];
}

export interface IMarketsGroup {
  id: number;
  name: string;
  localeName: string;
  marketsGroup: boolean;
  displayOrder: number;
}

export interface IMarketPeriod {
  name?: string;
  localeName: string;
  marketsNames: string | string[];
  marketsTemplates?: string[];
  markets: IMarket[];
}

export interface IGroupedMarketHeader {
  name: string;
  sortOrder: number;
}
