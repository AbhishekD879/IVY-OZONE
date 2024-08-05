import { IQuizModel } from '@app/questionEngine/models/quiz.model';

export interface IPrevQuizModel {
  totalRecords: number;
  quizzes: IQuizModel[];
}
