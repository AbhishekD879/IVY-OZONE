import { Subscription } from 'rxjs';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { StorageService } from '@core/services/storage/storage.service';
import { CmsService } from '@core/services/cms/cms.service';
import { IQuizSettings } from '@core/services/cms/models';
import { NavigationEnd, Router } from '@angular/router';
import { IQuizPopupSettings } from '@core/services/cms/models/quiz-settings.model';
import { UserService } from '@core/services/user/user.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { QuestionEngineService } from '@questionEngine/services/question-engine/question-engine.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import {
  QE_PATH_VARIABLE,
  QE_QUIZ_STORAGE_NAME,
  QE_QUIZ_POPUP_DELAY,
  CORRECT4_SOURCE_ID
} from '@questionEngine/constants/question-engine.constant';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'quiz-dialog',
  template: '',
  styleUrls: ['./quiz-dialog.component.scss']
})
export class QuizDialogComponent implements OnInit, OnDestroy {
  @Input() user: UserService;

  public quizPopupSettings: IQuizPopupSettings;
  private quizDetailsSub: Subscription;
  private routeChangeSub: Subscription;
  private popupTimer: number;
  private previousUrl: string;

  constructor(
    protected dialogService: InfoDialogService,
    protected storageService: StorageService,
    protected cms: CmsService,
    protected router: Router,
    protected questionEngineService: QuestionEngineService,
    private windowRef: WindowRefService,
  ) {
    this.handleQuizPopupDisplay = this.handleQuizPopupDisplay.bind(this);
  }

  ngOnInit(): void {
    // Quiz Popup settings
    this.cms.getQuizPopupSetting()
      .subscribe((settings: IQuizPopupSettings) => this.quizPopupSettings = settings);

    this.routeChangeSub = this.router.events
        .pipe(filter(event => event instanceof NavigationEnd))
        .subscribe(this.handleQuizPopupDisplay);

    this.handleQuizPopupDisplay();
  }

  /**
   * Render quiz dialog using actual cms settings
   */
  renderQuizDialog(): void {
    this.popupTimer = this.windowRef.nativeWindow.setTimeout(() => {
      this.quizDetailsSub = this.cms.getQuizPopupSettingDetails()
        .subscribe((quizSettings: IQuizSettings) => {
          if (quizSettings) {
            this.displayQuizDialog(quizSettings);
          }
        });
    }, QE_QUIZ_POPUP_DELAY);
  }

  ngOnDestroy(): void {
    this.destroy(true);
    this.quizDetailsSub && this.quizDetailsSub.unsubscribe();
    this.routeChangeSub && this.routeChangeSub.unsubscribe();
  }

  /**
   * Display info dialog with specific information
   * @param settings - Popup labels and properties
   */
  displayQuizDialog(settings: IQuizSettings): void {
    this.dialogService.openInfoDialog(
      settings.popupTitle || '',
      settings.popupText || '',
      settings.quizId ? `${settings.quizId} quiz-dialog` : 'quiz-dialog',
      'quizDialog',
      undefined,
        [{
            caption: settings.remindLaterText || '',
            cssClass: 'btn-style4',
            handler: () => this.destroy(true)
          },
          {
          caption: settings.yesText || '',
          cssClass: 'btn-style2 okButton',
          handler: () => this.openQuiz()
        },
        {
          caption: settings.dontShowAgainText || '',
          cssClass: 'btn-style-quiz',
          handler: () => this.destroy(false)
        }
      ]);
  }

  /**
   * Handle displaying of quiz dialog on current page
   * only if user is logged in, dialog is available and quiz is enabled - dialog might be displayed
   *
   * @param event  - Event
   */
  handleQuizPopupDisplay(): void {
    if (this.popupTimer) {
      this.windowRef.nativeWindow.clearTimeout(this.popupTimer);
    }

    if (!this.user || !this.user.username || !this.user.status || !this.quizPopupSettings || !this.quizPopupSettings.enabled) {
      return;
    }

    const availableRoutes = this.quizPopupSettings.pageUrls && this.quizPopupSettings.pageUrls.split(',') || [''];
    const isPopupAvailable = this.isQuizPopupAvailable(availableRoutes, this.router.url);
    const isChildUrl = this.parseMatchResult(this.router.url.match(this.previousUrl));

    if(this.router.url !== '/') {
      this.previousUrl = this.router.url;
    }

    if (!isPopupAvailable || isChildUrl) {
      return;
    }

    const qeQuiz = this.storageService.get(QE_QUIZ_STORAGE_NAME);

    if (qeQuiz && (qeQuiz.quizId === this.quizPopupSettings.quizId) && (qeQuiz.username === this.user.username)) {
      return;
    }

    this.questionEngineService.userAnswersExist(this.user.username, this.quizPopupSettings.quizId)
      .subscribe((userAnswersExist: boolean) => {
        if (userAnswersExist === true) {
          this.storageService.set(QE_QUIZ_STORAGE_NAME, {
            quizId: this.quizPopupSettings.quizId,
            showAgain: !userAnswersExist,
            username: this.user.username
          });
          return;
        }

        this.renderQuizDialog();
    });
  }

  /**
   * Navigate to available quiz
   */
  openQuiz(): void {
    const url = this.quizPopupSettings.sourceId.match(CORRECT4_SOURCE_ID)
      ? CORRECT4_SOURCE_ID
      : `${QE_PATH_VARIABLE}${this.quizPopupSettings.sourceId}`;
    this.router.navigateByUrl(url);
    this.destroy(true);
  }

  /**
   * Destroy dialog and save it status to Local storage
   * @param showAgainStatus {boolean} - permission to display quiz depends on user choice
   */
  destroy(showAgainStatus: boolean): void {
    if (showAgainStatus === false) {
      this.questionEngineService.submitUserAnswer({
        username: this.user.username,
        customerId: this.user.playerCode,
        quizId: this.quizPopupSettings.quizId,
        sourceId: this.quizPopupSettings.sourceId,
        questionIdToAnswerId: {
          DO_NOT_SHOW_AGAIN: ['DO_NOT_SHOW_AGAIN']
        }
      }).subscribe();

      this.storageService.set(QE_QUIZ_STORAGE_NAME, {
        quizId: this.quizPopupSettings.quizId,
        showAgain: showAgainStatus,
        username: this.user.username
      });
    }

    this.dialogService.closePopUp();
  }

  /**
   * Check if dialog is available for current url
   * @param availableRoutes {Array} - urls where popup is enabled
   * @param currentUrl {string} - current url
   *
   * Examples of page url rules:
   *  /, /horse-racing/, /live-stream - only for root page, /horse-racing/ page and /live-stream page
   *  /horse-racing/* - category horse-racing and all its child (for example /horse-racing/live-stream)
   */
  private isQuizPopupAvailable(availableRoutes: string[], currentUrl: string): boolean {
    return availableRoutes.some((url: string): boolean => {
      url = url.trim();
      let isEnabled = url === currentUrl;

      if (url[url.length - 1] === '*') {
        isEnabled = this.parseMatchResult(currentUrl.match(url));
      }

      return isEnabled;
    });
  }

  private parseMatchResult(matchResult: null | RegExpMatchArray): boolean {
    return !!(matchResult && (matchResult[0].length));
  }
}
