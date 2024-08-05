import { ISportServiceConfig } from '@core/models/sport-service-config.model';

export interface IInitialSportTab {
  id: string;
  label: string;
  url: string;
  name?: string;
  displayInConnect?: boolean;
  hidden?: boolean;
  subTabs?: IInitialSportTab[];
  enabled?: boolean;
  index?: number;
  displayName?: string;
}

export interface IInitialSportConfig {
  config: ISportServiceConfig;
  filters: {
    LIVE_VIEW_BY_FILTERS?: string[];
    VIEW_BY_FILTERS?: string[];
    RACING_FILTERS?: string[];
    RESULTS_FILTERS?: string[];
  };
  order: {
    BY_LEAGUE_ORDER?: string[];
    BY_LEAGUE_EVENTS_ORDER?: string[];
    BY_TIME_ORDER?: string[];
    EVENTS_ORDER?: string[];
  };
  sectionTitle?: {
    ENHRCS?: string;
    INT: string;
    UK: string;
    VR: string;
    US?: string;
    ZA?: string;
    AE?: string;
    CL?: string;
    IN?: string;
    AU?: string;
    FR?: string;
    ALL?: string;
  };
  isRunnerNumber?: boolean;
  MARKETS_NAME_SORT_ORDER?: Array<string>;
  GROUPED_MARKETS_NAME?: Array<string>;
  RACE_MARKET_ORDER?: Array<string>;
  PRESIM_STOP_TRACK_INTERVAL?: number;
  MARKET_FLEX_TABS?: number;
  tabs: IInitialSportTab[];
}
