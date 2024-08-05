export interface IFanzonePreferences {
  brand: string;
  confirmCTA: string;
  confirmText: string;
  createdAt: string;
  createdBy: string;
  createdByUserName: string;
  ctaText: string;
  exitCTA: string;
  id: string;
  pageName: string;
  pcDescription: string;
  pcKeys: IPreferenceOptions[];
  subscribeText: string;
  updatedAt: string;
  updatedBy: string;
  updatedByUserName: string;
  showToggle?: boolean;
  optInCTA?: string;
  noThanksCTA?: string;
  notificationDescriptionDesktop?: string;
  unsubscribeDescription?: string;
  notificationPopupTitle?: string;
  unsubscribeTitle?: string;
  pushPreferenceCentreTitle?: string;
  routeToFz?: boolean;
  genericTeamNotificationTitle?: string;
  genericTeamNotificationDescription?: string;
}
export interface IPreferenceOptions {
  name: string;
  key: string;
  value?: boolean;
}

export interface IFanzoneData {
  teamId?: string;
  teamName?: string;
  communication?: Array<string>;
  isFanzoneExists?: boolean;
  showSYCPopupOn?: string;
  subscriptionDate?: string;
  tempTeam?: ITempData;
  isResignedUser?: boolean;
}

export interface ITempData {
  teamId?: string;
  teamName?: string;
}