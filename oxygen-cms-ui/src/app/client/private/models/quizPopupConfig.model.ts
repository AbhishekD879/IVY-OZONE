import {Base} from '@app/client/private/models/base.model';

export interface QuizPopupConfig extends Base {
  enabled: boolean;
  pageUrls: string;
  popupTitle: string;
  popupText: string;
  quizId: string;
  yesText: string;
  remindLaterText: string;
  dontShowAgainText: string;
}
