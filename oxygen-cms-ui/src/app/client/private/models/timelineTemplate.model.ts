import {Base} from '@app/client/private/models/base.model';
import {Filename} from '@app/client/public/models/filename.model';

export interface TimelineTemplate extends Base {
  name: string;
  postIconSvgId: string;
  headerIconSvgId: string;
  headerText: string;
  yellowHeaderText: string;
  subHeader: string;
  isYellowSubHeaderBackground: boolean;
  eventId: string;
  selectionId: string;
  topRightCornerImage: Filename;
  betPromptHeader: string;
  text: string;
  showLeftSideRedLine: boolean;
  showLeftSideBlueLine: boolean;
  showTimestamp: boolean;
  showRedirectArrow: boolean;
  postHref: string;
  showRacingPostLogoInHeader: boolean;

  isSpotlightTemplate: boolean;
  isVerdictTemplate: boolean;
}
