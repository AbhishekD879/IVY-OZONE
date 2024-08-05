import {Component, Inject, OnInit} from '@angular/core';
import {Quiz} from '@app/client/private/models/quiz.model';
import {DateRange} from '@app/client/private/models/dateRange.model';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '@app/client/private/services/brand.service';
import {LoginRule} from '@app/quiz/model/loginRule';
import {EMPTY_SP, SplashPage} from '@app/client/private/models/splash-page.model';
import {SplashPageApiService} from '@app/quiz/service/splash-page.api.service';
import * as _ from 'lodash';
import * as uuid from 'uuid';
import {Filename} from '@app/client/public/models/filename.model';
import {QuestionDetailsModel} from '@app/client/private/models/questionDetails.model';
import {QEQuickLinks} from '@app/client/private/models/qeQuickLinks.model';
import {QEQuickLinksApiService} from '@app/quiz/service/quick-links.api.service';
import {EndPageApiService} from '@app/quiz/service/end-page.api.service';
import {EndPage} from '@app/client/private/models/end-page.model';
import {QuizPopup} from '@app/client/private/models/quizPopup.model';
import {EventDetails} from '@app/client/private/models/eventDetails.model';
import {QuizConfiguration} from '@app/client/private/models/quizconfiguration.model';
import {Question} from '@app/client/private/models/question.model';

@Component({
  selector: 'app-quiz-engine-create',
  templateUrl: './quiz-engine-create.component.html'
})
export class QuizEngineCreateComponent implements OnInit {
  newQuiz: Quiz;
  loginRules: Array<string> = Object.keys(LoginRule);
  defaultLoginRule = LoginRule.START;
  selectSplashPages: Array<SplashPage>;
  selectQuickLinks: Array<QEQuickLinks>;
  endPages: EndPage[];

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private splashPageApiService: SplashPageApiService,
    private quickLinksApiService: QEQuickLinksApiService,
    private endPageApiService: EndPageApiService) {
  }

  ngOnInit() {

    this.newQuiz = {
      sourceId: '',
      splashPage: undefined,
      qeQuickLinks: {} as QEQuickLinks,
      displayFrom: '',
      displayTo: '',
      entryDeadline: this.getInitialEntryDeadlineDate().toISOString(),
      firstQuestion: null,
      id: '',
      active: false,
      quizLoginRule: this.defaultLoginRule.toString(),
      title: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      notValid: false,
      brand: this.brandService.brand,
      updatedByUserName: '',
      createdByUserName: '',
      isChanged: false,
      upsell: null,
      endPage: null,
      quizLogoSvg: {} as Filename,
      quizBackgroundSvg: {} as Filename,
      defaultQuestionsDetails: {} as QuestionDetailsModel,
      submitPopup: {} as QuizPopup,
      exitPopup: {} as QuizPopup,
      correctAnswersPrizes: [],
      eventDetails: {} as EventDetails,
      highlighted: false,
      quizConfiguration: {} as QuizConfiguration
    };

    if (this.data['data'] && this.data['data'].quizToClone) {
      this.newQuiz.sourceId = this.data['data'].quizToClone.sourceId;
      this.newQuiz.title = this.data['data'].quizToClone.title;
      this.newQuiz.displayFrom = this.data['data'].quizToClone.displayFrom;
      this.newQuiz.displayTo = this.data['data'].quizToClone.displayTo;
      this.newQuiz.entryDeadline = this.data['data'].quizToClone.entryDeadline;
      this.defaultLoginRule = this.data['data'].quizToClone.quizLoginRule;
      this.newQuiz.quizLoginRule = this.data['data'].quizToClone.quizLoginRule;
      this.newQuiz.quizConfiguration = this.data['data'].quizToClone.quizConfiguration;

      if (this.data['data'].quizToClone.firstQuestion) {
        this.cloneQuestions();
      }

      this.newQuiz.upsell = null;
      this.newQuiz.quizLogoSvg = {} as Filename;
      this.newQuiz.quizBackgroundSvg = {} as Filename;
      this.newQuiz.defaultQuestionsDetails = {} as QuestionDetailsModel;
      this.newQuiz.submitPopup = {} as QuizPopup;
      this.newQuiz.exitPopup = {} as QuizPopup;
      this.newQuiz.correctAnswersPrizes = [];
      this.newQuiz.eventDetails = {} as EventDetails;
    }

    this.loadSplashPages();
    this.loadQuickLinksPages();
    this.loadEndPages();
  }

  private cloneQuestions() {
    const questions = Question.flatten(this.data['data'].quizToClone.firstQuestion);

    questions.forEach(question => {
      question.id = uuid.v4();
      question.answers.forEach(answer => answer.id = uuid.v4());
    });

    this.newQuiz.firstQuestion = Question.unflatten(questions);
  }

  private getInitialEntryDeadlineDate() {
    const date = new Date();
    date.setHours(date.getHours() + 2);
    return date;
  }

  private loadSplashPages(): void {
    this.splashPageApiService.getSplashPagesByBrand()
      .subscribe((data: any) => {
        this.selectSplashPages = data.body;
        this.selectSplashPages.unshift(EMPTY_SP);
        if (this.data['data'] && this.data['data'].quizToClone && this.data['data'].quizToClone.splashPage) {
          this.onChangeSelectedSplashPage(this.data['data'].quizToClone.splashPage.id);
        }
      });
  }

  private loadQuickLinksPages(): void {
    this.quickLinksApiService.getQEQuickLinksByBrand()
      .subscribe((data: any) => {
        this.selectQuickLinks = data.body;
        if (this.data['data'] && this.data['data'].quizToClone && this.data['data'].quizToClone.qeQuickLinks) {
          this.onChangeSelectedQuickLinks(this.data['data'].quizToClone.qeQuickLinks.id);
        }
      });
  }

  isValidModel(): boolean {
    return this.newQuiz.title.length > 0 &&
      this.newQuiz.sourceId.length > 0 &&
      this.isValidSourceId() &&
      this.isEntryDeadlineValid() &&
      !!this.newQuiz.endPage;
  }

  isEntryDeadlineValid(): boolean {
    const displayFromDate = new Date(this.newQuiz.displayFrom);
    const displayToDate = new Date(this.newQuiz.displayTo);
    const entryDeadline = new Date(this.newQuiz.entryDeadline);
    return entryDeadline > displayFromDate && entryDeadline < displayToDate;
  }

  isValidSourceId(): boolean {
    return this.newQuiz.sourceId.indexOf('/') === 0;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  handleVisibilityDateUpdate(data: DateRange): void {
    this.newQuiz.displayFrom = new Date(data.startDate).toISOString();
    this.newQuiz.displayTo = new Date(data.endDate).toISOString();
  }

  public handelEntryDeadline(date: string): void {
    this.newQuiz.entryDeadline = new Date(date).toISOString();
  }

  public onChangeLoginRule(value: string): void {
    this.newQuiz.quizLoginRule = value;
  }

  onChangeSelectedSplashPage(splashPageId: string): void {
    if (splashPageId === '-1') {
      this.newQuiz.splashPage = undefined;
    } else {
      this.newQuiz.splashPage = _.find(this.selectSplashPages, {id: splashPageId});
    }
  }

  onChangeSelectedQuickLinks(quickLinksId: string): void {
    this.newQuiz.qeQuickLinks = _.find(this.selectQuickLinks, {id: quickLinksId});
  }

  loadEndPages() {
    this.endPageApiService.getEndPagesByBrand()
      .subscribe((data: any) => {
        this.endPages = data.body;
        if (this.data['data'] && this.data['data'].quizToClone && this.data['data'].quizToClone.endPage) {
          this.onEndPageSelection(this.data['data'].quizToClone.endPage.id);
        }
      });
  }

  onEndPageSelection(endPageId: string) {
    this.newQuiz.endPage = _.find(this.endPages, {id: endPageId});
  }
}
