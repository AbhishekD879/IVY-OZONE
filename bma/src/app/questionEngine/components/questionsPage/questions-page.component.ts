import { Component, ComponentFactoryResolver, OnInit } from '@angular/core';

import { Router } from '@angular/router';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';

import { InfoDialogComponent } from '@app/questionEngine/components/shared/infoDialog/info-dialog.component';
import {
  LATEST_TAB_ID, LATEST_TAB_PAGE_ROUTE, PREVIOUS_TAB_PAGE_ROUTE,
  QE_COMPONENT_MISSED_DATA, SURVEY_END_ROUTE
} from '@app/questionEngine/constants/question-engine.constant';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { IInfoDialogParams } from '@app/questionEngine/models/infoDialogParams.model';

@Component({
  selector: 'questions-page',
  templateUrl: './questions-page.component.html',
  styleUrls: ['./questions-page.component.scss'],
})
export class QuestionsPageComponent implements OnInit {
  qeData: QuestionEngineQuizModel;
  private exitPopupTitle: string = this.localeService.getString('qe.exitPopupTitle');

  constructor(
    public router: Router,
    private questionEngineService: QuestionEngineService,
    private pubSubService: PubSubService,
    protected dialogService: DialogService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    private localeService: LocaleService
  ) {
  }

  ngOnInit(): void {
    if (this.questionEngineService.checkIfShouldRedirectGuest()) {
      return;
    }

    if (this.questionEngineService.qeData && this.questionEngineService.qeData.baseQuiz) {
      this.qeData = this.questionEngineService.qeData.baseQuiz;
      this.checkIfShowQuestionPage();
    } else {
      this.pubSubService.publish(this.pubSubService.API.QE_FATAL_ERROR, [QE_COMPONENT_MISSED_DATA]);
    }
  }

  public get useBackButtonToExitAndHideXButton(): boolean {
    return this.qeData && this.qeData.quizConfiguration && this.qeData.quizConfiguration.useBackButtonToExitAndHideXButton;
  }
  public set useBackButtonToExitAndHideXButton(value:boolean){}

  handleBackArrow(): void {
    if (this.useBackButtonToExitAndHideXButton) {
      this.openCloseAppDialog();
    } else {
      this.openGoToSplashOrContinueDialog();
    }
  }

  openGoToSplashOrContinueDialog(): void {
    if (this.qeData && this.qeData.quizConfiguration && this.qeData.quizConfiguration.showExitPopup) {
      this.dialogHandler(this.goToSplash.bind(this));
      return;
    }
    this.goToSplash();
  }

  openCloseAppDialog(): void {
    if (this.qeData && this.qeData.quizConfiguration && this.qeData.quizConfiguration.showExitPopup) {
      this.dialogHandler(this.closeApp.bind(this));
      return;
    }
    this.closeApp();
  }

  protected dialogHandler(callbackFn: Function): void {
    const params = {
      dialogClass: 'confirm-exit-dialog',
      src: this.qeData.exitPopup.iconSvgPath,
      caption: this.qeData.exitPopup.header,
      text: this.qeData.exitPopup.description,
      buttons: [
        {
          caption: this.qeData.exitPopup.submitCTAText,
          cssClass: 'btn-continue',
          handler: this.keepPlay.bind(this)
        },
        {
          caption: this.qeData.exitPopup.closeCTAText,
          cssClass: 'btn-handle',
          handler: callbackFn
        }
      ],
    };

    this.openInfoDialog(params);
}

  protected openInfoDialog(params: IInfoDialogParams): void {
    this.dialogService.openDialog(DialogService.API.qe.infoDialog,
      this.componentFactoryResolver.resolveComponentFactory(InfoDialogComponent), true, params);
  }

  private keepPlay(): void {
    this.dialogService.closeDialog(DialogService.API.qe.infoDialog);
    this.questionEngineService.trackEventGA(this.exitPopupTitle, 'Keep Playing');
  }

  private checkIfShowQuestionPage(): void {
    if (this.qeData.firstAnsweredQuestion || new Date(this.qeData.entryDeadline).getTime() < new Date().getTime()) {
      if (this.qeData.quizConfiguration && !this.qeData.quizConfiguration.showPreviousAndLatestTabs) {
        this.router.navigateByUrl(`${this.questionEngineService.resolvePath(this.qeData.sourceId)}/${SURVEY_END_ROUTE}`);
      } else {
        const { redirectToTab } = this.questionEngineService;
        const path = (redirectToTab === LATEST_TAB_ID ? LATEST_TAB_PAGE_ROUTE : PREVIOUS_TAB_PAGE_ROUTE);
        this.router.navigateByUrl(`${this.questionEngineService.resolvePath(this.qeData.sourceId)}/${path}`);
      }
    }
  }

  private goToSplash(): void {
    if (this.qeData && this.qeData.quizConfiguration && (!this.qeData.quizConfiguration.showSplashPage || !this.qeData.splashPage)) {
      this.closeApp();
    } else {
      this.router.navigateByUrl(this.questionEngineService.resolvePath(this.qeData.sourceId));
      this.dialogService.closeDialog(DialogService.API.qe.infoDialog);
      this.questionEngineService.trackEventGA(this.exitPopupTitle, 'Exit Game');
    }
  }

  private closeApp(): void {
    this.router.navigateByUrl(this.questionEngineService.checkPreviousPage() || '/');
    this.dialogService.closeDialog(DialogService.API.qe.infoDialog);
    this.questionEngineService.trackEventGA('Exit');
  }
}
