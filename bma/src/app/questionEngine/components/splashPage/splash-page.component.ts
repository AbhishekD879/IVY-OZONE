import { Component, OnDestroy, OnInit } from '@angular/core';
import { timeout } from 'rxjs/operators';
import { Router } from '@angular/router';

import { UserService } from '@core/services/user/user.service';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { IQuizHistoryModel } from '@app/questionEngine/models/quizHistory.model';
import {
  BACKEND_RESPONSE_TIMEOUT_LIMIT,
  LOGIN_RULE,
  QUESTION_PAGE_ROUTE,
  QE_INIT_DATA_FAILURE,
  LATEST_TAB_ID,
  LATEST_TAB_PAGE_ROUTE,
  PREVIOUS_TAB_PAGE_ROUTE
} from '@app/questionEngine/constants/question-engine.constant';
import { HttpErrorResponse } from '@angular/common/http';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
@Component({
  selector: 'splash-page',
  templateUrl: './splash-page.component.html',
  styleUrls: ['./splash-page.component.scss'],
})

export class SplashPageComponent implements OnInit, OnDestroy{

  qeData: QuestionEngineQuizModel;
  isUserLoggedIn: boolean;
  previousRoute: string;
  loginProcessing: boolean = false;
  btnProcessingMsg: string = this.localeService.getString('qe.btnProcessingMsg');
  previousResults: boolean;
  private tag: string = 'QeSplashPage';
  f2pErrMsg:string;
  isDesktop = false;

  constructor(
    public userService: UserService,
    public questionEngineService: QuestionEngineService,
    public pubSubService: PubSubService,
    public router: Router,
    public localeService: LocaleService,
    private cmsService:CmsService,
    public serviceClosureService: ServiceClosureService
  ) {
  }



  ngOnInit(): void {
   /* FSS F2P check flag */
    this.cmsService.getSystemConfig().subscribe((config: any) => {
      this.f2pErrMsg=  config.F2PERRORS['F2PError']|| '';
    });
    this.initData();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.tag);
    this.pubSubService.unsubscribe(this.pubSubService.API.USER_CLOSURE_PLAY_BREAK);
  }

  onCtaButtonClick(): void {
    if (this.loginProcessing) {
      return;
    }
    if (!this.isUserLoggedIn && this.qeData.quizLoginRule === LOGIN_RULE.START) {
      this.openLoginDialog();
    } else {
      this.goToQuestionsPage();
    }
  }

  closeApp(): void {
    this.router.navigateByUrl(this.previousRoute || '/');
    this.questionEngineService.trackEventGA('Exit');
  }

  private initData(): void {
    this.isUserLoggedIn = this.userService.status;
    const { qeData } = this.questionEngineService;
    this.qeData = qeData && qeData.baseQuiz;
    this.previousRoute = this.questionEngineService.checkPreviousPage();
    if (this.qeData) {
      // redirect if needed
      this.previousResults = !!qeData.previous.length;
      const hideSplashPage = (this.qeData.quizConfiguration) && (this.qeData.quizConfiguration.showSplashPage === false);
      if (hideSplashPage || !(this.qeData.splashPage)) {
        if (this.isUserLoggedIn) {
          this.goToQuestionsPage();
        } else {
          this.router.navigate(['/']);
        }
        return;
      }

      // else proceed to splash page
      if (this.questionEngineService.qeSubmittedThisSession) {
        this.getComponentData();
        return;
      }
      this.isUserLoggedIn ? this.handleQEData() : !this.questionEngineService.isLoginPopupShown && this.openLoginDialog();
    } else {
      this.router.navigate(['/']);
      return;
    }
  }

  private goToQuestionsPage(): void {
    const { redirectToTab } = this.questionEngineService;
    let path;
    if((redirectToTab === QUESTION_PAGE_ROUTE) || !redirectToTab ) {
      path = QUESTION_PAGE_ROUTE;
    } else if(redirectToTab === LATEST_TAB_ID) {
      path = LATEST_TAB_PAGE_ROUTE;
    } else {
      path = PREVIOUS_TAB_PAGE_ROUTE;
    }
    const redirectUrl: string = `${this.questionEngineService.resolvePath(this.qeData.sourceId)}/${path}`;
    if (this.qeData && this.qeData.splashPage && this.qeData.splashPage.ctaButtonText) {
      this.questionEngineService.trackEventGA(this.qeData.splashPage.ctaButtonText);
    }
    this.router.navigateByUrl(redirectUrl);
  
  }

  private openLoginDialog(): void {
    if (this.qeData.quizLoginRule === LOGIN_RULE.START) {
      this.questionEngineService.isLoginPopupShown = true;

      this.pubSubService.subscribe(this.tag, this.pubSubService.API.QE_HISTORY_DATA_RECEIVED, () => {
        this.loginProcessing = true;
        this.initData();
        this.handleQEData();
       /*  this.disableCtaBtnF2P =  this.closureService.userServiceClosureOrPlayBreakCheck() &&
        this.closureService.userServiceClosureOrPlayBreak; */
        this.isUserLoggedIn = true;
      });
      this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, {moduleName: 'header'});
    }
  }

  private getComponentData(): void {
      this.questionEngineService.getQuizHistory()
      .pipe(timeout(BACKEND_RESPONSE_TIMEOUT_LIMIT))
      .subscribe((data: IQuizHistoryModel) => {
        this.handleQEData(data);
      },
      (error: Error | HttpErrorResponse) => {
        this.loginProcessing = false;
        this.questionEngineService.triggerFatalError(QE_INIT_DATA_FAILURE, error);
      });
  }

  private handleQEData(data: IQuizHistoryModel = this.questionEngineService.quizHistoryModel): void {
    // if no quiz live or previous game data from BE - perform default data fetch
    if (this.questionEngineService.checkGameData(data, this.getComponentData.bind(this))) {
      return;
    }
    this.questionEngineService.setQESubmitStatus(false);

    const quizHistoryData: QuestionEngineModel = this.questionEngineService.mapResponseOnComponentModel(data);
    this.qeData = quizHistoryData && quizHistoryData.baseQuiz;
    this.previousRoute = this.questionEngineService.checkPreviousPage();
    this.loginProcessing = false;
  }
}
