export interface IQuestionsToAnswersIds {
  [questionId: string]: string[];
}

export interface IUserAnswersModel {
  username: string;
  customerId: string;
  quizId: string;
  sourceId: string;
  questionIdToAnswerId: IQuestionsToAnswersIds;
}
