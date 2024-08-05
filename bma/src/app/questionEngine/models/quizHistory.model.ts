import { IQuizModel } from '@app/questionEngine/models/quiz.model';

export interface IQuizHistoryModel {
  previousCount: number;
  live: IQuizModel;
  previous: IQuizModel[];
}
