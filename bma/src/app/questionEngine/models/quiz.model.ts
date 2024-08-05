import { Question } from '@app/questionEngine/models/question.model';
import { ISplashPage } from '@app/questionEngine/models/splash-page.model';
import { IResultPage } from '@app/questionEngine/models/result-page.model';
import { QeQuickLinkModel } from '@app/questionEngine/models/qeQuickLink.model';
import { QuestionEngineQuestionDetailsModel } from '@app/questionEngine/models/questionEngineQuestionDetails.model';
import { QuizPopupModel } from '@app/questionEngine/models/quizPopup.model';
import { ICorrectAnswersPrizesModel } from '@app/questionEngine/models/quiz-summary-item.model';
import { IEventDetailsModel } from '@app/questionEngine/models/eventDetails.model';
import { IUpsellModel } from '@app/questionEngine/models/upsell.model';
import { IQuizConfigurationModel } from '@questionEngine/models/quizConfiguration.model';

export interface IQuizModel {

  quizLoginRule: string;
  quizBackgroundSvgFilePath: string;
  sourceId: string;
  quizConfiguration: IQuizConfigurationModel;

  id: string;
  entryDeadline: Date | string;
  firstQuestion: Question;
  firstAnsweredQuestion: Question;
  splashPage?: ISplashPage;
  endPage?: IResultPage;
  qeQuickLinks: QeQuickLinkModel;
  defaultQuestionsDetails: QuestionEngineQuestionDetailsModel;
  quizLogoSvgFilePath: string;
  exitPopup: QuizPopupModel;
  submitPopup: QuizPopupModel;
  upsell?: IUpsellModel;

  correctAnswersPrizes: ICorrectAnswersPrizesModel[];

  displayFrom: Date | string;
  displayTo: Date | string;

  title: string;
  eventDetails: IEventDetailsModel;
}
