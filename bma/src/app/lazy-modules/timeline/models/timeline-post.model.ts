import { ISportEvent } from '@core/models/sport-event.model';

export interface IPostTemplate {
  id: string;
  name: string;
  headerIconSvgId: string;
  isVerdictTemplate: boolean;
  isSpotlightTemplate: boolean;
  headerText: string;
  isYellowHeaderBackground: boolean;
  subHeader: string;
  yellowHeaderText: string;
  isYellowSubHeaderBackground: boolean;
  eventId: string;
  selectionId: string;
  topRightCornerImage: string;
  betPromptHeader: string;
  text: string;
  showLeftSideRedLine: boolean;
  showLeftSideBlueLine: boolean;
  showTimestamp: boolean;
  includeRacingPostLogo: boolean;
  postHref: string;
  showRacingPostLogoInHeader: boolean;
  showRedirectArrow: boolean;
  postIconSvgId: string;
  topRightCornerImagePath: string;
}

export interface IPost {
  id: string;
  title: string;
  text: string;
  createdDate: string;
  brand: string;
  template: IPostTemplate;
  campaignId: string;
  pinned: boolean;
  selectionEvent: ITimelineSelection;
}

export interface ITimelineSelection {
  obEvent: ISportEvent;
  isNA: boolean;
}

export interface ITimelineConfig {
  brand: string;
  enabled: boolean;
}
