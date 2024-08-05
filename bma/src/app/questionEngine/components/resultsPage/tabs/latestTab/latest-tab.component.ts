import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { INoGamesContentModel } from '@app/questionEngine/models/noGamesContent.model';
import { IQuizSummaryItemModel } from '@app/questionEngine/models/quiz-summary-item.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { Question, IAnswerModel } from '@app/questionEngine/models/question.model';
import { UpsellItemModel } from '@app/questionEngine/models/upsell.model';

@Component({
  selector: 'latest-tab',
  templateUrl: './latest-tab.component.html',
  styleUrls: ['./latest-tab.component.scss'],
})
export class LatestTabComponent implements OnInit {
  @Input() qeData: QuestionEngineModel;
  public noLatestRoundTxt: INoGamesContentModel;
  public showNoResultsWarning: boolean = false;
  public showResults: boolean = false;
  public showSummary: boolean = false;
  public showGenericUpsell: boolean = false;
  public quizSummary: IQuizSummaryItemModel[] = [];
  public showUpsell: boolean = false;
  private answerCounter: number = 0;
  private currentDay = new Date().getTime();

  constructor(
    private questionEngineService: QuestionEngineService,
    public router: Router,
  ) {
  }

  ngOnInit(): void {
    const { baseQuiz } = this.qeData;
    const { showUpsell, upsell } = baseQuiz.resultsPage;
    const quizDisplayTo = new Date(baseQuiz.displayTo).getTime();

    if (!baseQuiz.firstAnsweredQuestion || quizDisplayTo < this.currentDay) {
      this.showNoResultsWarning = true;
      this.noLatestRoundTxt = this.questionEngineService.handleNoPrevGamesContent('latest');
    } else if (baseQuiz.questionsList && baseQuiz.questionsList.length) {
      this.questionSummaryHandler(baseQuiz);
    }

    this.questionEngineService.trackPageViewGA(`/${this.questionEngineService.sourceIdFromParams}/latest-quiz`);
    this.upsellVisibilityHandler(showUpsell, upsell);
  }

  trackByFn(index: number): string {
    return `${index}`;
  }

  genericUpsellHandler(): void {
    const { imageUrl } = this.qeData.baseQuiz.resultsPage.upsell;
    this.router.navigateByUrl(imageUrl || this.qeData.baseQuiz.sourceId || '/');
  }

  private upsellVisibilityHandler(showUpsell: boolean, upsell: UpsellItemModel): void {
    if (!upsell || !showUpsell) {
      return;
    }
    this.showUpsell = !this.showResults && this.upsellValid(upsell) && !this.showNoResultsWarning;
    this.showGenericUpsell = !!upsell.fallbackImagePath && this.showNoResultsWarning;
  }

  private upsellValid(upsell: UpsellItemModel): boolean {
    return UpsellItemModel.isValid(upsell);
  }

  private questionSummaryHandler(baseQuiz: QuestionEngineQuizModel): void {
    const { questionsList, resultsPage } = baseQuiz;

    questionsList.forEach((question: Question ) => {
      question.answers.forEach((answer: IAnswerModel) => {
        if (answer.correctAnswer) {
          this.answerCounter++;
        }
        if (answer.userChoice) {
          this.quizSummary.push({
            question: question.text,
            selectedAnswer: answer.text
          });
        }
      });
    });

    this.showResults = resultsPage.showResults && questionsList.length === this.answerCounter;
    this.showSummary = resultsPage.showAnswersSummary && !this.showResults && !this.showNoResultsWarning;
  }
}
