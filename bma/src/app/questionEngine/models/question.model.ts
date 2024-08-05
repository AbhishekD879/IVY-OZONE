import { QuestionEngineQuestionDetailsModel } from '@app/questionEngine/models/questionEngineQuestionDetails.model';
import { IResultPage } from '@questionEngine/models/result-page.model';

export interface IAnswerModel {
  id: string;
  text: string;
  questionAskedId: string;
  nextQuestionId: string;
  correctAnswer: boolean;
  selectionId?: string;
  userChoice: boolean;
  endPage?: IResultPage;
}

export abstract class Question {
  id: string;
  answers: IAnswerModel[];
  nextQuestions: INextQuestions = {};
  questionType: string;
  text: string;
  questionDetails: QuestionEngineQuestionDetailsModel;

  public static flatten(question: Question): Array<Question> {
    let nextQuestions = [];

    if (question.nextQuestions) {
      nextQuestions = Question.flatMap(
        question.answers
          .map(answer => question.nextQuestions[answer.nextQuestionId])
          .filter(q => q)
          .filter(Question.distinct),
        Question.flatten
      );
    }
    return [question, ...nextQuestions];
  }

  private static flatMap(questions: Question[], callback: (questions: Question, index: number) => Question[]): Question[] {
    return Array.prototype.concat(...questions.map(callback));
  }

  private static distinct(question: Question, index: number, questions: Question[]): boolean {
    return questions.indexOf(question) === index;
  }
}

export interface INextQuestions {
  [questionId: string]: Question;
}
