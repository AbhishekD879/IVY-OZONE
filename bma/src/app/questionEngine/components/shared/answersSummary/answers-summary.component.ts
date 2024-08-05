import { Component, Input, OnInit } from '@angular/core';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { ICorrectAnswersPrizesModel, IQuizSummaryItemModel } from '@app/questionEngine/models/quiz-summary-item.model';
import { IAnswerModel, Question } from '@app/questionEngine/models/question.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';

@Component({
  selector: 'answers-summary',
  templateUrl: './answers-summary.component.html',
  styleUrls: ['./answers-summary.component.scss'],
})

export class AnswersSummaryComponent implements OnInit {
  @Input() quiz: QuestionEngineQuizModel;

  gameSummaryState: boolean = false;
  correctAnswerResult: string;
  correctAnswerCounter: number = 0;
  public validSummary: boolean;
  public showSummary: boolean = false;
  public showPrizes: boolean = false;
  public prize: number = 0;
  public prizeResult: string;
  public correctAnswersPrizes: ICorrectAnswersPrizesModel[];
  public quizSummary: IQuizSummaryItemModel[] = [];
  public homeTeamWon: boolean;
  public awayTeamWon: boolean;
  public homeTeamScore: number; // todo would be once to have Home, Away Team models with all data
  public awayTeamScore: number;
  private prizeType: string;

  constructor(
    private questionEngineService: QuestionEngineService
  ) {

  }

  ngOnInit(): void {
    if (!!(this.quiz && this.quiz.questionsList && this.quiz.resultsPage && this.quiz.defaultQuestionsDetails)) {
      this.validSummary = true;
      const { questionsList, resultsPage, eventDetails } = this.quiz;

      this.questionSummaryHandler(questionsList);
      this.showSummary = resultsPage.showAnswersSummary;
      this.showPrizes = resultsPage.showPrizes;
      if (eventDetails && eventDetails.actualScores && eventDetails.actualScores.length === 2) {
        this.homeTeamScore = eventDetails.actualScores && eventDetails.actualScores[0];
        this.awayTeamScore = eventDetails.actualScores && eventDetails.actualScores[1];
        this.homeTeamWon = this.homeTeamScore > this.awayTeamScore;
        this.awayTeamWon = this.awayTeamScore > this.homeTeamScore;
      }
    } else {
      this.validSummary = false;
      return;
    }
  }

  trackByFn(index: number): string {
    return `${index}`;
  }

  public hasDefaultQuestionsDetailsInfo(): boolean {
    return !!(this.quiz.defaultQuestionsDetails.topLeftHeader || this.quiz.defaultQuestionsDetails.topRightHeader);
  }

  public toggleGameSummaryInfo(): void {
    this.gameSummaryState = !this.gameSummaryState;
    if (this.gameSummaryState) {
      this.questionEngineService.trackEventGA('View Game Summary', 'Expand');
    } else {
      this.questionEngineService.trackEventGA('View Game Summary', 'Collapse');
    }
  }

  public get showHomeTeamScore(): boolean {
    return this.homeTeamScore >= 0 && this.homeTeamScore !== null;
  }
  public set showHomeTeamScore(value:boolean){}
  public get showAwayTeamScore(): boolean {
    return this.awayTeamScore >= 0 && this.awayTeamScore !== null;
  }
  public set showAwayTeamScore(value:boolean){}
  private prizeIndicator(correctAnswersPrizes: ICorrectAnswersPrizesModel[], correctAnswers: number ): string {
    correctAnswersPrizes.forEach( correctAnswersPrize => {
      if (correctAnswers >= correctAnswersPrize.requiredCorrectAnswers) {
        this.prize = correctAnswersPrize.amount;
        this.prizeResult = `${correctAnswersPrize.currency}${this.prize}`;
        this.prizeType = correctAnswersPrize.prizeType;
      }
    });
    return this.prizeResult;
  }

  private questionSummaryHandler(questionsList): void {
    questionsList.map((question: Question) => {
      question.answers.forEach((answer: IAnswerModel) => {
        if (answer.userChoice) {
         answer.correctAnswer && this.correctAnswerCounter++;
          this.quizSummary.push({
            question: question.text,
            selectedAnswer: answer.text,
            correctAnswer: answer.correctAnswer
          });
        }
      });
    });
    this.prizeIndicator(this.quiz.correctAnswersPrizes, this.correctAnswerCounter);
    this.checkCorrectAnswerResult(questionsList);
  }

  /*
  * Check all dependencies when user can lose a quiz
  * */
  private get isLose(): boolean {
     return this.prize === 0 || isNaN(this.prize) || this.prizeType === 'NONE';
  }
  private set isLose(value:boolean){}
  private checkCorrectAnswerResult(questionsList): void {
    if (this.isLose && this.correctAnswerCounter < questionsList.length) {
      this.correctAnswerResult = 'lose';
      return;
    }
    if(this.correctAnswerCounter && questionsList.length) {
      this.correctAnswerResult = 'won';
    }
    else {
      this.correctAnswerResult = '';
    }
  }

}
