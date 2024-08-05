import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { timeout } from 'rxjs/operators';

import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { INoGamesContentModel } from '@app/questionEngine/models/noGamesContent.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { IPrevQuizModel } from '@app/questionEngine/models/qePrevQuizModel.model';
import {
  BACKEND_RESPONSE_TIMEOUT_LIMIT,
  QE_INIT_DATA_FAILURE,
  QUIZZES_PAGE_SIZE
} from '@app/questionEngine/constants/question-engine.constant';

@Component({
  selector: 'previous-tab',
  templateUrl: './previous-tab.component.html',
  styleUrls: ['./previous-tab.component.scss'],
})

export class PreviousTabComponent implements OnInit, OnDestroy {

  public qeData: QuestionEngineModel = this.questionEngineService.qeData;
  public loading: boolean = false;
  public noPreviousRoundTxt: INoGamesContentModel;
  public showNoResultsWarning: boolean = false;
  public prevQuizes: QuestionEngineQuizModel[] = [];
  public pageCounter: number;
  public pageNumber: number = 1;
  public showMoreBtn: boolean;
  private subscription: Subscription;
  private previousCount: number = this.qeData.previousCount;

  constructor(
    private questionEngineService: QuestionEngineService
  ) {
  }

  ngOnInit(): void {
    const { previous, previousCount } = this.qeData;

    if (this.checkIfNoResults(previous)) {
      this.loading = false;
      this.showNoResultsWarning = true;
      this.noPreviousRoundTxt = this.questionEngineService.handleNoPrevGamesContent('previous');
    } else {
      this.prevQuizes = previous;
      this.showMoreBtn = (previousCount > QUIZZES_PAGE_SIZE);
      this.pageCounter = Math.ceil(this.previousCount / QUIZZES_PAGE_SIZE);
    }

    this.questionEngineService.trackPageViewGA(`/${this.questionEngineService.sourceIdFromParams}/previous-quiz`);
  }
  ngOnDestroy(): void {
    this.subscription && this.subscription.unsubscribe();
  }

  public hasNextPage(): void {
    if (this.pageNumber >= this.pageCounter) {
      this.showMoreBtn = false;
    }
  }

  public onShowMoreClick(): void {
    this.loading = true;
    this.questionEngineService.trackEventGA('View Historic Games', 'Show More');
    this.previousCount = this.previousCount - QUIZZES_PAGE_SIZE;
    this.getPrevQuizesData(this.pageNumber, QUIZZES_PAGE_SIZE);
    this.pageNumber++;
  }

  public trackByFn(index: number): string {
    return `${index}`;
  }

  private checkIfNoResults(previous: QuestionEngineQuizModel[]): boolean {
    return (!previous || !previous.length) || this.questionEngineService.checkForAnonymousData;
  }

  private getPrevQuizesData(pageNumber: number, pageSize: number): void {
    this.subscription = this.questionEngineService.getPrevQuizes(pageNumber, pageSize)
      .pipe(timeout(BACKEND_RESPONSE_TIMEOUT_LIMIT))
      .subscribe((data: IPrevQuizModel) => {
          this.loading = false;
          const mapPrevQuizzesResponseOnComponentModel: any = this.questionEngineService.mapPrevQuizzesResponseOnComponentModel(data);
          this.prevQuizes = [
            ...this.prevQuizes,
            ...[mapPrevQuizzesResponseOnComponentModel]
          ];
          this.hasNextPage();
        },
        (error) => {
          this.questionEngineService.triggerFatalError(QE_INIT_DATA_FAILURE, error);
        }
      );
  }
}
