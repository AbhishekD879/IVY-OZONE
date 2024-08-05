import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { timeout } from 'rxjs/operators';

import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';

import { IResultPageContent } from '@app/questionEngine/models/resultpageContent.model';
import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { IQuizHistoryModel } from '@app/questionEngine/models/quizHistory.model';
import {
  BACKEND_RESPONSE_TIMEOUT_LIMIT,
  QE_COMPONENT_MISSED_DATA, QE_INIT_DATA_FAILURE,
  TIMEOUT_FOR_SUBMIT_NOTIFICATION
} from '@app/questionEngine/constants/question-engine.constant';

@Component({
  selector: 'results-page',
  templateUrl: './results-page.component.html',
  styleUrls: ['./results-page.component.scss'],
})

export class ResultsPageComponent implements OnInit {

  qeData: QuestionEngineModel; // this is parent so it taken from here
  activeTab: string = this.activatedRoute.snapshot.data.segment.match('latest') ? 'latest' : 'previous';
  showSubmitNotification: boolean = false;
  hideNotifier: boolean = false;
  hideSwitchers = this.activatedRoute.snapshot.data.segment.match('previous-results');
  isQuizResultPage: boolean = true;
  resultPageContent: IResultPageContent;
  resultPageBg: string = 'none';
  private dataIsUpToDate: boolean = this.questionEngineService.dataIsUpToDate;

  constructor(
    private questionEngineService: QuestionEngineService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private windowRefService: WindowRefService
  ) {
  }

  ngOnInit(): void {
    if (this.questionEngineService.checkIfShouldRedirectGuest()) {
      return;
    }

    if (this.dataIsUpToDate) {
      this.initConfig(this.questionEngineService.qeData);
    } else {
      this.refreshQEData(); // if quiz has been submitted recently - fetch updated data
    }
  }

  changeTab(tab: string): void {
    this.activeTab = tab;
    const tabTitle: string = tab.charAt(0).toUpperCase() + tab.substr(1).toLowerCase();
    this.questionEngineService.trackEventGA(tabTitle);
  }

  public get useBackButtonToExitAndHideXButton(): boolean {
    return this.qeData && this.qeData.baseQuiz && this.qeData.baseQuiz.quizConfiguration &&
      this.qeData.baseQuiz.quizConfiguration.useBackButtonToExitAndHideXButton;
  }
public set useBackButtonToExitAndHideXButton(value:boolean){}
  public get splashPageDisabled(): boolean {
    return this.qeData && this.qeData.baseQuiz
      && this.qeData.baseQuiz.quizConfiguration
      && !this.qeData.baseQuiz.quizConfiguration.showSplashPage;
  }
public set splashPageDisabled(value:boolean){}
  handleBackArrow(): void {
    if (this.useBackButtonToExitAndHideXButton || !this.qeData.baseQuiz.splashPage) {
      this.closeApp();
    } else {
      this.backToSplash();
    }
  }

  backToSplash(): void {
    if (this.splashPageDisabled) {
      this.closeApp();
    } else {
      const {qeData} = this.questionEngineService;
      const path = qeData ? `${this.questionEngineService.resolvePath(qeData.baseQuiz.sourceId)}` : '/';
      this.router.navigateByUrl(path);
    }
  }

  closeApp(): void {
    this.router.navigateByUrl(this.questionEngineService.checkPreviousPage() || '/');
    this.questionEngineService.trackEventGA('Exit');
  }

  /**
   * Perform initial component check & setup
   * @param qeData
   */
  private initConfig(qeData: QuestionEngineModel): void {
    if (qeData && qeData.baseQuiz && qeData.baseQuiz.resultsPage) {
      this.qeData = qeData;
    } else {
      this.questionEngineService.triggerFatalError(QE_COMPONENT_MISSED_DATA);
      return;
    }

    if (this.qeData.baseQuiz.resultsPage.backgroundSvgImagePath) {
      this.resultPageBg = `url(${qeData.baseQuiz.resultsPage.backgroundSvgImagePath})`;
    }
    if (qeData.baseQuiz.quizConfiguration && !qeData.baseQuiz.quizConfiguration.showPreviousAndLatestTabs) {
     this.quizEndPageHandler();
    }

    this.resolveContent(this.qeData.baseQuiz);
    this.notifierHandler(this.qeData.baseQuiz, this.questionEngineService.showSubmitNotification);
  }

  private quizEndPageHandler(): void {
    this.isQuizResultPage = false;

    if (!this.qeData.baseQuiz.firstAnsweredQuestion || !this.qeData.baseQuiz.questionsList) {
      if (new Date(this.qeData.baseQuiz.entryDeadline).getTime() > new Date().getTime()) {
        this.router.navigateByUrl(`${this.questionEngineService.resolvePath(this.qeData.baseQuiz.sourceId)}/questions`);
      } else {
        this.router.navigateByUrl(this.questionEngineService.checkPreviousPage() || '/');
      }
      return;
    }

    if (this.qeData.baseQuiz.questionsList.length) {
      const answerItem = this.qeData.baseQuiz.questionsList[this.qeData.baseQuiz.questionsList.length - 1].answers
        .find(el => el.userChoice);

      // if user answer specific endpage exist - update resultpage data for endpage
      if (answerItem && answerItem.endPage) {
        const { gameDescription, noLatestRoundMessage, submitMessage, submitCta } = answerItem.endPage;
        this.qeData.baseQuiz.resultsPage = {
          ...this.qeData.baseQuiz.resultsPage,
          gameDescription,
          noLatestRoundMessage,
          submitMessage,
          submitCta
        };
      }
    } else {
      this.questionEngineService.triggerFatalError(QE_INIT_DATA_FAILURE);
      console.error(`Error loading QE survey data; No Survey answer endpage data available`);
    }
  }

  private resolveContent(baseQuiz: QuestionEngineQuizModel): void {
    const { resultsPage } = baseQuiz;
    this.resultPageContent = {
      gameDescription: resultsPage.gameDescription,
      noLatestRoundMessage: resultsPage.noLatestRoundMessage,
      noPreviousRoundMessage: resultsPage.noPreviousRoundMessage,
      submitMessage: resultsPage.submitMessage,
      title: resultsPage.title,
      upsellAddToBetslipCtaText: resultsPage.upsellAddToBetslipCtaText,
      upsellBetInPlayCtaText: resultsPage.upsellBetInPlayCtaText,
    };
  }

  private notifierHandler(baseQuiz: QuestionEngineQuizModel, showSubmitNotification: boolean): void {
    if (baseQuiz && showSubmitNotification ) {
      this.showSubmitNotification = true;
      this.questionEngineService.toggleSubmitNotification(false);
      this.windowRefService.nativeWindow.setTimeout(() => this.hideNotifier = true, TIMEOUT_FOR_SUBMIT_NOTIFICATION);
    }
  }

  private refreshQEData(): void {
    this.questionEngineService.getQuizHistory()
      .pipe(timeout(BACKEND_RESPONSE_TIMEOUT_LIMIT))
      .subscribe((data: IQuizHistoryModel) => {
          this.questionEngineService.setQEDataUptodateStatus(true);
          this.initConfig(this.questionEngineService.mapResponseOnComponentModel(data));
        },
        (error) => {
          this.questionEngineService.triggerFatalError(QE_INIT_DATA_FAILURE, error);
        }
      );
  }
}
