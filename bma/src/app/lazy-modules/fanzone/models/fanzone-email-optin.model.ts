export interface ICmsEmailOptin {
  id: string;
  createdBy: string;
  createdByUserName: string;
  updatedBy: string;
  updatedByUserName: string;
  createdAt: string;
  updatedAt: string;
  brand: string;
  fanzoneEmailPopupTitle: string;
  fanzoneEmailPopupDescription: string;
  fanzoneEmailPopupOptIn: string;
  fanzoneEmailPopupRemindMeLater: string;
  fanzoneEmailPopupDontShowThisAgain: string;
  seasonStartDate: string;
  seasonEndDate: string;
}

export interface IEmailOptin{
  fanzoneUser?: boolean;
  remindMeLaterCount?: number; 
  remindMeLaterPrefDate?: string; 
  dontShowMeAgainPref?: boolean;
  undisplayFanzoneGamesPopup?: boolean;
  undisplayFanzoneGamesTooltip?: boolean;
  newSignPostingSeenDate?: string;
  showRelegatedPopupDate?: string;
  showSYCPopupDate?: string;
}

export interface ICommunicationSettings {
  "communicationTypes": IOption[];
}

export interface IOption {
  id: number;
  name: string;
  selected: boolean
}