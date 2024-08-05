export interface ISportCMSConfig {
  alt: string;
  categoryId: string;
  defaultTab: string;
  disabled: boolean;
  dispSortName: string[];
  id: string;
  imageTitle: string;
  inApp: string;
  isMultiTemplateSport: null | boolean;
  isOutrightSport: boolean;
  oddsCardHeaderType: ISportCMSConfigCardHeader;
  primaryMarkets: string;
  relUri: boolean;
  showInPlay: boolean;
  sport: string;
  sportName: string;
  ssCategoryCode: string;
  svg: string;
  svgId: string;
  tabs: ISportCMSConfigTab[];
  targetUri: string;
  targetUriCopy: string;
  typeIds: number[];
}

export interface ISportConfig {
  config: {
    categoryType?: string;
    extension?: string;
    name?: string;
    tier?: number;
    title?: string;
    path?: string;
    defaultTab?: string;
    request: {
      eventSortCode?: string;
      outrightsSport?: string;
      siteChannels?: string;
      categoryId?: string;
      isActive?: boolean;
      typeIds?: number[];
    }
    tabs?: ISportConfigRequestTab;
    eventMethods?: { [tabName: string]: string }
  };
  filters?: {
    VIEW_BY_FILTERS?: string[];
    LIVE_VIEW_BY_FILTERS?: string[];
  };
  order?: { [key: string]: string[] };
  tabs?: ISportConfigTab[];
}

export interface ISportBaseConfig {
  dispSortName: string[];
  id: string;
  isMultiTemplateSport: null | boolean;
  isOutrightSport: boolean;
  oddsCardHeaderType: ISportCMSConfigCardHeader;
  path: string;
  primaryMarkets: string;
  typeIds: string[];
  viewByFilters: string[];
}

export interface ISportConfigTab {
  label: string;
  id?: string;
  url?: string;
  name?: string;
  hidden?: boolean;
  subTabs?: ISportConfigSubTab[];
}

export interface ISportConfigSubTab {
  url?: string;
  label?: string;
  id?: string;
  hidden?: boolean;
  name?: string;
  onClick?: Function;
}

interface ISportConfigRequestTab {
  [tabName: string]: {
    isActive?: boolean;
    isNotStarted?: boolean;
    outrightsSport?: boolean;
    dispSortName?: string[];
    dispSortNameIncludeOnly?: string[];
    marketTemplateMarketNameIntersects?: string;
    marketDrilldownTagNamesNotContains?: string;
    marketDrilldownTagNamesContains?: string;
  };
}

interface ISportCMSConfigCardHeader {
  outcomesTemplateType1: string | null;
  outcomesTemplateType2: string | null;
  outcomesTemplateType3: string | null;
}

export interface ISportCMSConfigTab {
  [tabName: string]: {
    tablabel: string;
    visible: boolean;
  };
}

export interface ISportEventTab {
  id: string;
  marketName: string;
  label: string;
  url: string;
}

