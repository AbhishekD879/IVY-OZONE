export interface ISportsConfig {
  dispSortName: string[];
  id: string;
  isOutrightSport: boolean | null;
  isMultiTemplateSport: boolean | null;
  oddsCardHeaderType: any;
  path: string;
  primaryMarkets: string;
  typeIds: string[];
  viewByFilters: string[];
}

export interface ISportsConfigObject {
  [key: string]: ISportsConfig;
}
