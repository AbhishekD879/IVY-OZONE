import {SportsQuickLink} from '@app/client/private/models/sportsquicklink.model';

export interface ICreatedLinkData {
  link: SportsQuickLink;
  imageToUpload: any;
}

export interface IQuickLinkGroups {
  [key: string]: IQuickLinkGroup;
}

export interface IQuickLinkGroup {
  isValid: boolean;
  matches: SportsQuickLink[];
  matchedGroupsCount?: number;
  disabled?: boolean;
  name?: string;
  matchedGroups: IQuickLinkGroup[];
}

export interface IQuickLinkCreatedData {
  createdSportsQuickLinkData: ICreatedLinkData,
  savedSportsQuickLink: SportsQuickLink
}