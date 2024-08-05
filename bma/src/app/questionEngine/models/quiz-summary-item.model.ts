export interface IQuizSummaryItemModel {
  question: string;
  selectedAnswer: string;
  correctAnswer?: boolean;
  prizeType?: string;
}

export interface ICorrectAnswersPrizesModel {
  requiredCorrectAnswers: number;
  amount: number;
  currency: string;
  prizeType: string;
}
