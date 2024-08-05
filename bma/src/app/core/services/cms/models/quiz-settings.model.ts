export interface IQuizSettings {
  id: string;
  popupTitle: string;
  popupText: string;
  quizId: string;
  yesText: string;
  remindLaterText: string;
  dontShowAgainText: string;
}

export interface IQuizPopupSettings {
  id: string;
  quizId: string;
  enabled: boolean;
  pageUrls: string;
  sourceId: string;
}
