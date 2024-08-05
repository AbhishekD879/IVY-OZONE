export interface ISportConfigRequestTab {
  [tabName: string]: {
    isActive?: boolean;
    isNotStarted?: boolean;
    outrightsSport?: boolean;
    dispSortName?: string[];
    dispSortNameIncludeOnly?: string[];
    marketTemplateMarketNameIntersects?: string;
    marketDrilldownTagNamesNotContains?: string;
    marketDrilldownTagNamesContains?: string;
    date?: string;
    templateMarketNameOnlyIntersects?: boolean;
    marketsCount?: boolean;
  };
}
