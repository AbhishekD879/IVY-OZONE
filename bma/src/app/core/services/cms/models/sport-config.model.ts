import { ISportConfigTab } from './sport-config-tab.model';
import { ISportConfigRequestTab } from './sport-config-request-tab.model';
import { ISportConfigEventMethods } from './sport-config-event-methods.model';

export interface ISportConfig {
  isFootball?: boolean;
  config: {
    eventRequest?: {
      scorecast?: boolean
    }
    categoryType?: string;
    extension?: string;
    name?: string;
    tier?: number;
    title?: string;
    path?: string;
    defaultTab?: string;
    isOutrightSport?: boolean;
    request: {
      aggregatedMarkets?: any;
      eventSortCode?: string;
      outrightsSport?: string;
      siteChannels?: string;
      categoryId?: string;
      isActive?: boolean;
      typeIds?: number[];
      marketsCount?: boolean;
      dispSortName?: string[];
      dispSortNameIncludeOnly?: string[];
      marketTemplateMarketNameIntersects?: string;
      templateMarketNameOnlyIntersects?: boolean;
    },
    tabs?: ISportConfigRequestTab;
    eventMethods?: ISportConfigEventMethods;
    scoreboardConfig?: any;
    oddsCardHeaderType?: string | any;
    isMultiTemplateSport?: boolean;
  };
  tabs?: ISportConfigTab[];
  isOutrightSport?: boolean;
  specialsTypeIds?: number[];
}
