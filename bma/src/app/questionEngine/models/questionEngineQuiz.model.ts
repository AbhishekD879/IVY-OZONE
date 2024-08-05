import { Question } from '@app/questionEngine/models/question.model';
import { QuestionEngineSplashPageModel } from '@app/questionEngine/models/questionEngineSplashPage.model';
import { QuestionEngineResultsPageModel } from '@app/questionEngine/models/questionEngineResultsPage.model';
import { LinksModel } from '@app/questionEngine/models/links.model';
import { QuestionEngineQuestionDetailsModel } from '@app/questionEngine/models/questionEngineQuestionDetails.model';
import { QuizPopupModel } from '@app/questionEngine/models/quizPopup.model';
import { ICorrectAnswersPrizesModel } from '@app/questionEngine/models/quiz-summary-item.model';
import { IEventDetailsModel } from '@app/questionEngine/models/eventDetails.model';
import { IQuizConfigurationModel } from '@questionEngine/models/quizConfiguration.model';

// QuestionEngineQuizModel --> DTO
export class QuestionEngineQuizModel {
  quizLoginRule: string;
  quizBackgroundSvgFilePath: string;
  sourceId?: string;
  backgroundSvgUrl?: string;
  quizConfiguration?: IQuizConfigurationModel;

  id: string;
  entryDeadline: Date | string;
  firstQuestion: Question;
  firstAnsweredQuestion: Question;
  isLive: boolean;
  splashPage: QuestionEngineSplashPageModel;
  resultsPage: QuestionEngineResultsPageModel;
  quickLinks: LinksModel[];
  defaultQuestionsDetails: QuestionEngineQuestionDetailsModel;
  quizLogoSvgFilePath: string;
  exitPopup: QuizPopupModel;
  submitPopup: QuizPopupModel;
  correctAnswersPrizes: ICorrectAnswersPrizesModel[] = [];
  questionsList: Array<Question> = []; // flatten question tree
  eventDetails: IEventDetailsModel;
  displayTo: Date | string;
}
