import { ChangeDetectorRef, Component, ComponentFactoryResolver, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { timeout } from 'rxjs/operators';

import { CarouselService } from '@sharedModule/directives/ng-carousel/carousel.service';
import { Carousel } from '@sharedModule/directives/ng-carousel/carousel.class';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { BackButtonService } from '@core/services/backButton/back-button.service';

import { IUserAnswersModel } from '@app/questionEngine/models/userAnswers.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { InfoDialogComponent } from '@questionEngine/components/shared/infoDialog/info-dialog.component';
import {
  LOGIN_RULE,
  NO_AUTHORIZATION,
  QE_COMPONENT_MISSED_DATA,
  LATEST_TAB_PAGE_ROUTE,
  TIMEOUT_FOR_USER_ANSWER_CAROUSEL,
  TIMEOUT_SWIPE_TUTORIAL,
  BACKEND_RESPONSE_TIMEOUT_LIMIT,
  ERROR_CODE
} from '@app/questionEngine/constants/question-engine.constant';
import { IInfoDialogParams } from '@questionEngine/models/infoDialogParams.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { UserService as VanillaUserService } from '@frontend/vanilla/core';

@Component({
  selector: 'questions-carousel',
  templateUrl: './questions-carousel.component.html',
  styleUrls: ['./questions-carousel.component.scss'],
})
export class QuestionsCarouselComponent implements OnInit {

  carouselName: string = 'questions-carousel';
  timeOutSlide: number;
  toggleSwipeTutorialDialog: boolean = false;
  qeData: QuestionEngineQuizModel;
  userAnswers = {questionIdToAnswerId: {}} as IUserAnswersModel;
  ngCarouselDisableRightSwipe: boolean = true;  // for Swipe toggle
  swipeTutorialMsg: string = this.localeService.getString('qe.swipeTutorialMsg');
  ngCarouselMoveThresholdPercentage: string | number = '10'; // distance to swipe %

  submitLoading: boolean = false;
  errSubmit: boolean = false;
  submitLoadingBtn: string = this.localeService.getString('qe.submitLoading');
  submitTryAgainBtn: string = this.localeService.getString('qe.submitTryAgain');
  onSubmitRewardNotAssigned: boolean = false;
  protected submitPopupTitle: string = this.localeService.getString('qe.submitPopupTitle');
  protected showSwipeTutorialDialog: boolean = true;
  protected questionNumberGA: string; // track question's number for GA
  public userAction: Array<string> = [];

  private isSurvey: boolean = false;

  get currentAnswerId(): string | number {
    return this.questionsCarousel && this.userAction[this.currentCarouselStep];
  }
set currentAnswerId(value:string | number){}
  get currentCarouselStep(): number {
    return this.questionsCarousel ? this.questionsCarousel.currentSlide : 0;
  }
set currentCarouselStep(value:number){}
  get progressBarStepWidth(): string {
    if (this.qeData?.questionsList?.length) {
      return `${(this.currentCarouselStep + 1) * (100 / this.qeData.questionsList.length)}%`;
    }
    return null;
  }
set progressBarStepWidth(value:string){}
  protected get questionsCarousel(): Carousel {
    return this.carouselService.get(this.carouselName);
  }
protected set questionsCarousel(value:Carousel){}


  constructor(
    private carouselService: CarouselService,
    public domToolsService: DomToolsService,
    public userService: UserService,
    protected questionEngineService: QuestionEngineService,
    private pubSubService: PubSubService,
    protected windowRefService: WindowRefService,
    protected dialogService: DialogService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    private localeService: LocaleService,
    private router: Router,
    private awsService: AWSFirehoseService,
    private backButtonService: BackButtonService,
    protected cdr: ChangeDetectorRef,
    protected vnUserService: VanillaUserService
  ) { }

  ngOnInit(): void {
    this.initBackendData();
    if (this.userService.username) {
      this.userAnswers.username = this.userService.username;
      this.userAnswers.customerId = this.vnUserService.claims.get('http://api.bwin.com/v3/user/pg/nameidentifier');
    } else if (this.questionEngineService.qeData.baseQuiz.quizLoginRule === LOGIN_RULE.START) { // todo use qeData from class?
      this.pubSubService.publish(this.pubSubService.API.QE_FATAL_ERROR, [NO_AUTHORIZATION]);
    }

    this.userAnswers.sourceId = `/${this.questionEngineService.sourceIdFromParams}`;
    this.questionEngineService.trackPageViewGA(`/${this.questionEngineService.sourceIdFromParams}/question1`);
  }

  nextSlide(answerId: string, nextQuestionId: string, questionAskedId: string, nextQuestions: {}): void {
    this.userAction[this.currentCarouselStep] = answerId;  // SAVE answerId for stepBack
    this.userAnswers.questionIdToAnswerId[questionAskedId] = [answerId]; // need to send to backend

    if (nextQuestions) {
      nextQuestions[this.currentCarouselStep] = nextQuestions;

      this.timeOutSlide && this.windowRefService.nativeWindow.clearTimeout(this.timeOutSlide);
      this.timeOutSlide = this.windowRefService.nativeWindow.setTimeout(() =>
        this.userAction[this.currentCarouselStep] && this.questionsCarousel && this.questionsCarousel.next(),
          TIMEOUT_FOR_USER_ANSWER_CAROUSEL
      );
    }
    if ((this.currentCarouselStep + 1) === this.questionsCarousel.slidesCount) {
      this.openSubmitDialog();
    }
  }

  prevSlide(): void {
    this.questionsCarousel.previous();
    this.trackQuizArrowNavGA(0); // GA: Send data `Previous question` to GTM
  }

  openSubmitDialog(): void {
    if (this.qeData.quizConfiguration && this.qeData.quizConfiguration.showSubmitPopup) {
      this.updateSubmitDialog();
    } else {
      this.submitQuiz(!this.submitLoading);
    }
  }

  navigateToSlide(index: number): void {
    this.questionsCarousel.currentSlide !== index && this.questionsCarousel.toIndex(index);
  }

  onCarouselInit(isInit: boolean): void {
    if (isInit) {
      this.declareSwipeBehaviour();
    }
  }

  protected openInfoDialog(params: IInfoDialogParams): void {
    this.dialogService.openDialog(DialogService.API.qe.infoSubmitDialog,
      this.componentFactoryResolver.resolveComponentFactory(InfoDialogComponent), true, params);
  }

  protected declareSwipeBehaviour(): void {
    this.questionsCarousel.onSlideChange(() => {
      this.cdr.detectChanges();
      this.windowRefService.nativeWindow.scrollTo({ top: 0, left: 0, behavior: 'smooth'});
      if (this.showSwipeTutorial && this.showSwipeTutorial() && this.showSwipeTutorialDialog) {
        this.toggleSwipeTutorialDialog = true;
        this.showSwipeTutorialDialog = false;
        this.windowRefService.nativeWindow.setTimeout(() => {
          this.toggleSwipeTutorialDialog = false;
        }, TIMEOUT_SWIPE_TUTORIAL);
      }
      this.ngCarouselDisableRightSwipe = !(this.currentCarouselStep >= 0 && (this.userAction[this.currentCarouselStep]));

      if (!Object.keys(this.dialogService.openedPopups).length) {
        this.questionNumberGA = `/${this.questionEngineService.sourceIdFromParams}/question${this.currentCarouselStep + 1}`;
        this.questionEngineService.trackPageViewGA(this.questionNumberGA);
      }
    });
  }

  protected showSwipeTutorial(): boolean {
    return this.currentCarouselStep === 1 && !this.userAction[this.currentCarouselStep] && !this.toggleSwipeTutorialDialog;
  }

  protected redirectToEdit(): void {
    this.windowRefService.nativeWindow.clearTimeout(this.timeOutSlide);
    this.dialogService.closeDialog(DialogService.API.qe.infoSubmitDialog);
    this.questionEngineService.trackEventGA(this.submitPopupTitle, 'Go Back & Edit');
    this.navigateToSlide(0);
  }

  /**
   * GA: Send tracking data to GTM
   */
  private trackQuizArrowNavGA(directionNumber: number): void {
    const currentQuestion = this.questionsCarousel.currentSlide + 1;
    this.questionNumberGA = `/${this.questionEngineService.sourceIdFromParams}/question${currentQuestion + directionNumber}`;
    this.questionEngineService.trackPageViewGA(this.questionNumberGA);
  }

  private goToResultPage(): void {
    this.router.navigateByUrl(`${this.questionEngineService.resolvePath(this.qeData.sourceId)}/${LATEST_TAB_PAGE_ROUTE}`);
  }

  private get submitButton(): { caption: string; cssClass: string, handler: Function } {
    const caption = this.submitLoading ? this.submitLoadingBtn : this.errSubmit
      ? this.submitTryAgainBtn : this.qeData.submitPopup.submitCTAText;
    const cssClass = this.submitLoading ? 'btn-submit-processing' : 'btn-submit';
    const handler = this.submitQuiz.bind(this, !this.submitLoading);

    return { caption, cssClass, handler };
  }
  private set submitButton(value: { caption: string; cssClass: string, handler: Function }){}
  private updateSubmitDialog(): void {
    const params = {
      dialogClass: 'confirm-exit-dialog',
      src: this.qeData.submitPopup.iconSvgPath,
      caption: this.qeData.submitPopup.header,
      text: this.qeData.submitPopup.description,
      buttons: [
        this.submitButton,
        {
          caption: this.qeData.submitPopup.closeCTAText,
          cssClass: 'btn-handle',
          handler: this.redirectToEdit.bind(this)
        }
      ],
    };

    this.openInfoDialog(params);
  }

  private submitQuiz(execute?: boolean, isSurvey: boolean = false): void {
    if (!execute) {
      return;
    }
    this.submitLoading = true;

    this.questionEngineService.submitUserAnswer(this.userAnswers, this.isSurvey)
      .pipe(timeout(BACKEND_RESPONSE_TIMEOUT_LIMIT))
      .subscribe(
        () => {
          this.submitSuccess();
        },
        (err: HttpErrorResponse) => {
          this.awsService.errorLog(err);

          if (err.error && err.error.errorCode === ERROR_CODE.REWARD_NOT_ASSIGNED) {
            this.submitLoading = false;
            this.dialogService.closeDialog(DialogService.API.qe.infoSubmitDialog);
            this.backButtonService.redirectToPreviousPage();
          } else {
            this.submitLoading = false;
            this.errSubmit = true;
            if (this.qeData.quizConfiguration && this.qeData.quizConfiguration.showSubmitPopup) {
              this.updateSubmitDialog(); // update dialog params
            }
          }
        }
      );
  }

  private initBackendData(): void {
    if (this.questionEngineService.qeData && this.questionEngineService.qeData.baseQuiz) {
      this.qeData = this.questionEngineService.qeData.baseQuiz;
      this.isSurvey = this.qeData.quizConfiguration && !this.qeData.quizConfiguration.showPreviousAndLatestTabs;
      this.userAnswers.quizId = this.qeData.id;
    } else {
      this.pubSubService.publish(this.pubSubService.API.QE_FATAL_ERROR, [QE_COMPONENT_MISSED_DATA]);
    }
  }

  private submitSuccess(): void {
    this.submitLoading = false;
    this.goToResultPage();
    this.questionEngineService.setQESubmitStatus(true);
    this.questionEngineService.setQEDataUptodateStatus(false);
    this.dialogService.closeDialog(DialogService.API.qe.infoSubmitDialog);
    this.questionEngineService.trackEventGA(this.submitPopupTitle, 'Submit');
    this.questionEngineService.toggleSubmitNotification(!this.isSurvey); // used for displaying submit notification on results page
  }
}
