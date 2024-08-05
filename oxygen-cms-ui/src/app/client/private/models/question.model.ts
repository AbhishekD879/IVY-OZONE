import {QuestionDetailsModel} from '@app/client/private/models/questionDetails.model';
import {EndPage} from '@app/client/private/models/end-page.model';

export interface Answer {
  id: string;
  text: string;
  questionAskedId: string;
  nextQuestionId: string;
  correctAnswer: boolean;
  endPage: EndPage;
}

interface TitleData {
  isValid: boolean;
}

export abstract class Question {
  id: string;
  answers: Answer[];
  questionType: string;
  text: string;
  titleLength: TitleData = {
    isValid: true
  };
  hint: string;
  questionDetails: QuestionDetailsModel;
  nextQuestions: NextQuestions = {};

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

  public static unflatten(questions: Array<Question>): Question {
    const firstQuestion = questions[0];
    firstQuestion.answers.forEach(answer => answer.questionAskedId = firstQuestion.id);

    questions.reduce((prev, next) => {
      prev.nextQuestions = {};
      prev.nextQuestions[next.id] = next;
      prev.answers.forEach(answer => {
        answer.questionAskedId = prev.id;
        answer.nextQuestionId = next.id;
      });
      next.answers.forEach(answer => answer.questionAskedId = next.id);

      return next;
    });

    return firstQuestion;
  }

  private static flatMap(questions: Question[], callback: (questions: Question, index: number) => Question[]): Question[] {
    return Array.prototype.concat(...questions.map(callback));
  }

  private static distinct(question: Question, index: number, questions: Question[]): boolean {
    return questions.indexOf(question) === index;
  }
}

export interface NextQuestions {
  [questionId: string]: Question;
}
