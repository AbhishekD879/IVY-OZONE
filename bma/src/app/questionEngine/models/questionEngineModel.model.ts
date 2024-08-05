import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';

export class QuestionEngineModel {
  baseQuiz: QuestionEngineQuizModel;
  previous: QuestionEngineQuizModel[];
  previousCount: number;
}
