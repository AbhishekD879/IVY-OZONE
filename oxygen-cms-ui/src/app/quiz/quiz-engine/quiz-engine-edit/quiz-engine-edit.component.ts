import {Component, OnInit, ViewChild} from '@angular/core';
import {Quiz} from '@app/client/private/models/quiz.model';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {DateRange} from '@app/client/private/models/dateRange.model';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';
import {ActivatedRoute, Router} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {AppConstants, Brand} from '@app/app.constants';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {LoginRule} from '@app/quiz/model/loginRule';
import {SplashPageApiService} from '@app/quiz/service/splash-page.api.service';
import {EMPTY_SP, SplashPage} from '@app/client/private/models/splash-page.model';
import {Answer, Question} from '@app/client/private/models/question.model';
import * as _ from 'lodash';
import {UpsellComponent} from '@app/quiz/quiz-engine/upsell/upsell.component';
import {ErrorService} from '@app/client/private/services/error.service';
import {QEQuickLinks} from '@app/client/private/models/qeQuickLinks.model';
import {QEQuickLinksApiService} from '@app/quiz/service/quick-links.api.service';
import * as uuid from 'uuid';
import {EndPageApiService} from '@app/quiz/service/end-page.api.service';
import {EndPage} from '@app/client/private/models/end-page.model';
import {QuestionDetailsModel} from '@app/client/private/models/questionDetails.model';
import {QuestionDetailsImages} from '@app/quiz/model/questionImages';
import {Filename} from '@app/client/public/models/filename.model';
import {Prize} from '@app/client/private/models/prize.model';
import {QuizEngineCreateComponent} from '@app/quiz/quiz-engine/quiz-engine-create/quiz-engine-create.component';
import { FssRewardsDialogComponent } from '@app/quiz/fss-rewards-dialog/fss-rewards-dialog.component';
import { FssRewards } from '@app/client/private/models/coins-rewards.model';
import { BrandService } from '@app/client/private/services/brand.service';


@Component({
  selector: 'app-quiz-engine-edit',
  templateUrl: './quiz-engine-edit.component.html',
  styleUrls: ['./quiz-engine-edit.component.scss']
})
export class QuizEngineEditComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;

  getDataError: string;
  id: string;
  loginRules: Array<string> = Object.keys(LoginRule);
  questionsList: Array<Question> = [];
  questionTitleLengthLimit: number = 200;
  questionTextMissing: boolean = false;
  quiz: Quiz;
  selectSplashPages: Array<SplashPage>;
  selectQuickLinks: Array<QEQuickLinks>;
  endPages: EndPage[] = [];

  questionDetailsImages: Array<QuestionDetailsImages> = [];

  displayedCheckboxDisabled: boolean;

  public breadcrumbsData: Breadcrumb[];
  public saveQuizErrorMsg: string = 'Cannot save quiz. ' +
    'For an active quiz all questions must have "text" and "option" fields filled';

  public saveEmptyQuizQuestionsErrorMsg: string = 'Cannot save quiz. ' +
    'Active quiz has to have at least one question';

  public activeQuizWarningMsg: string = 'Quiz is already active and live. This action may have negative impact on customers. ' +
    'Are you sure?';

  public prizeTypes = new Map<string, string>();

  showAccordionBool: boolean;
  quizEditingWarning: boolean;
  answerEndPages: EndPage[] = [];
  fssRewards: FssRewards;
  isBrandLads: boolean;
  prevPrizeType: string;

  constructor(private quizApiService: QuizApiService,
              private splashPageApiServcie: SplashPageApiService,
              private quickLinksApiService: QEQuickLinksApiService,
              private route: ActivatedRoute,
              private router: Router,
              private dialogService: DialogService,
              private snackBar: MatSnackBar,
              private dialog: MatDialog,
              private errorService: ErrorService,
              private endPageApiService: EndPageApiService,
              private brandService: BrandService) {

    this.isValidModel = this.isValidModel.bind(this);
    this.isBrandLads = this.brandService.brand === Brand.LADBROKES;
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.prizeTypes.set('CREDIT', 'Monetary');
    this.prizeTypes.set('FREE_BETS', 'Token');
    this.prizeTypes.set('NONE', 'No prize');
    this.loadInitialData();
  }

  loadInitialData(): void {
    this.quizEditingWarning = false;
    this.quizApiService.getQuiz(this.id)
      .subscribe(({body}: any) => {
        this.enrichQuizFromBackend(body);
        if (this.actionButtons) {
          this.actionButtons.extendCollection(this.quiz);
        }

        this.loadSplashPages();
        this.loadQuickLinksPages();
        this.loadEndPages();
        this.displayedCheckboxDisabled = this.isQuizActiveAndStarted();

        this.breadcrumbsData = [{
          label: `Quiz`,
          url: `/question-engine/quiz`
        }, {
          label: this.quiz.title,
          url: `/question-engine/quiz/${this.quiz.id}`
        }];
      }, error => {
        this.getDataError = error.message;
      });
  }

  isValidModel(quiz): boolean {
    return quiz
      && quiz.id
      && quiz.id.length > 0
      && quiz.sourceId.indexOf('/') === 0
      && !quiz.notValid
      && !this.questionTextMissing
      && this.validEventDetailsStartTime()
      && this.isEntryDeadlineValid()
      && this.isActiveQuizQuestionsValid()
      && !!quiz.endPage;
  }

  private enrichQuizFromBackend(quizFromBe) {
    quizFromBe.isChanged = false;
    this.quiz = quizFromBe;
    this.quizEditingWarning = this.isQuizActiveAndStarted();
    if (quizFromBe.firstQuestion) {
      this.questionsList = Question.flatten(this.quiz.firstQuestion);
      this.questionsList.forEach(question => {
        question.titleLength = {
          isValid: true
        };
      });
    }
  }

  private isActiveQuizQuestionsValid(): boolean {
    return this.quizEditingWarning ? this.questionsList.length > 0 : true;
  }

  private isEntryDeadlineValid(): boolean {
    const displayFromDate = new Date(this.quiz.displayFrom);
    const displayToDate = new Date(this.quiz.displayTo);
    const entryDeadline = new Date(this.quiz.entryDeadline);
    return entryDeadline > displayFromDate && entryDeadline < displayToDate;
  }

  isValidSourceId(): boolean {
    return this.quiz.sourceId.indexOf('/') === 0;
  }

  handleVisibilityDateUpdate(data: DateRange): void {
    this.quiz.displayFrom = new Date(data.startDate).toISOString();
    this.quiz.displayTo = new Date(data.endDate).toISOString();
  }

  /*
      by changing Qs order or data per answer, we are not changing original data object,
      so we need manually update object Quiz by transforming Qs list into origin Qs tree
     */
  public updateQuestions(): void {
    this.quiz.firstQuestion = this.questionListToTree();
  }

  public addQuestion() {

    if (this.quizEditingWarning) {
      this.dialogService.showConfirmDialog({
        title: 'Add Question Warning',
        message: this.activeQuizWarningMsg,
        yesCallback: () => {
          proceedWithAddQuestion.call(this);
        }
      });
    } else {
      proceedWithAddQuestion.call(this);
    }

    function proceedWithAddQuestion() {
      const question = {
        id: uuid.v4(),
        answers: [],
        titleLength: {
          isValid: true,
        },
        questionType: 'SINGLE',
        text: '',
        hint: '',
        questionDetails: {
          awayTeamSvg: {
            originalname: ''
          },
          homeTeamSvg: {
            originalname: ''
          },
          channelSvg: {
            originalname: ''
          }
        } as QuestionDetailsModel,
        nextQuestions: {}
      };
      this.questionsList.push(question);
      this.addAnswerWithoutWarning(question);
      this.loadPrizes();
      this.mutateQuiz();
    }
  }

  public checkQuestionDescInput(e, {text, titleLength}) {
    titleLength.isValid = text.length <= this.questionTitleLengthLimit;
    this.quiz.notValid = !titleLength.isValid;
    this.checkQuestionTextPresence();
  }

  private checkQuestionTextPresence(): void {
    this.questionTextMissing = !!this.questionsList.find((question) => {
      return question.text ? question.text.length === 0 || question.answers.length === 0 ||
        (!!question.answers.find((answer) => {
          return answer.text ? answer.text.length === 0 : true;
        })) : true;
    }) && this.quiz.active;
  }

  public handleQuizActivation(): void {
    this.quiz.active = !this.quiz.active;
    this.quiz.isChanged = true;
    this.checkQuestionTextPresence();
  }

  public removeQuestion(qIndex) {
    const doRemoveQuestion = () => {

      if (qIndex !== 0 && qIndex === (this.questionsList.length - 1)) {
        this.questionsList[qIndex - 1].nextQuestions = {};
      } else if (qIndex > 0) {
        this.questionsList[qIndex - 1].nextQuestions = this.questionsList[qIndex].nextQuestions;
      }

      this.questionsList = (this.questionsList.slice(0, qIndex))
        .concat(this.questionsList.slice(qIndex + 1));
      this.loadPrizes();
      this.mutateQuiz();
    };

    if (this.quizEditingWarning) {
      this.dialogService.showConfirmDialog({
        title: 'Remove Warning',
        message: this.activeQuizWarningMsg,
        yesCallback: () => {
          proceedWithRemove.call(this);
        }
      });
    } else {
      proceedWithRemove.call(this);
    }

    function proceedWithRemove() {
      if (this.quiz.upsell && this.existsInDynamicUpsell(this.questionsList[qIndex])) {
        this.dialogService.showConfirmDialog({
          title: 'Confirm deletion',
          message: 'This question is used in Dynamic Upsell configuration. It will be lost if you remove it. Are you sure?',
          yesCallback: () => {
            doRemoveQuestion();
            this.quiz.upsell.options = {};
          }
        });
      } else {
        doRemoveQuestion();
      }
    }
  }

  public existsInDynamicUpsell(question: Question): boolean {
    const firstQuestionAnswerId = Object.keys(this.quiz.upsell.options).length > 0
      ? Object.keys(this.quiz.upsell.options)[0].split(';')[0]
      : '';

    const secondQuestionAnswerId = Object.keys(this.quiz.upsell.options).length > 0
      ? Object.keys(this.quiz.upsell.options)[0].split(';')[1]
      : '';

    return question.answers.some(answer => answer.id === firstQuestionAnswerId || answer.id === secondQuestionAnswerId);
  }

  public checkAnswerInput(answer) {
    if (answer && !answer.text.length) {
      answer.correctAnswer = false;
    }
    this.mutateQuiz();
  }

  public mutateQuiz() {
    this.quiz.isChanged = true;
    this.checkQuestionTextPresence();
  }

  public handleCorrectAnswer(question, answer) {
    let previousCorrectAnswer = '';
    question.answers.map((value) => {
      if (value.correctAnswer) {
        previousCorrectAnswer = value.text;
      }
      value.correctAnswer = false;
    });

    answer.correctAnswer = previousCorrectAnswer !== answer.text;
    this.mutateQuiz();
  }

  public addAnswer(question) {
    if (this.quizEditingWarning) {
      this.dialogService.showConfirmDialog({
        title: 'Add Answer Warning',
        message: this.activeQuizWarningMsg,
        yesCallback: () => {
          proceedWithAnswerAdding.call(this);
        }
      });
    } else {
      proceedWithAnswerAdding.call(this);
    }

    function proceedWithAnswerAdding() {
      question.answers.push({
        id: uuid.v4(),
        text: '',
        questionAskedId: question.id,
        nextQuestionId: null,
        correctAnswer: false
      });
      this.mutateQuiz();
    }
  }

  public addAnswerWithoutWarning(question) {
    question.answers.push({
      id: uuid.v4(),
      text: '',
      questionAskedId: question.id,
      nextQuestionId: null,
      correctAnswer: false
    });
    this.mutateQuiz();
  }

  public removeAnswer(qIndex, aIndex) {
    const doRemoveAnswer = () => {
      this.questionsList[qIndex].answers = (this.questionsList[qIndex].answers.slice(0, aIndex))
        .concat(this.questionsList[qIndex].answers.slice(aIndex + 1));
      this.mutateQuiz();
    };

    if (this.quizEditingWarning) {
      this.dialogService.showConfirmDialog({
        title: 'Remove Warning',
        message: this.activeQuizWarningMsg,
        yesCallback: () => {
          procceedWithAnswerRemove.call(this);
        }
      });
    } else {
      procceedWithAnswerRemove.call(this);
    }

    function procceedWithAnswerRemove() {
      if (this.quiz.upsell && this.existsInDynamicUpsell(this.questionsList[qIndex])) {
        this.dialogService.showConfirmDialog({
          title: 'Confirm deletion',
          message: 'The question of this answer is used in Dynamic Upsell configuration. It will be lost if you remove it. Are you sure?',
          yesCallback: () => {
            doRemoveAnswer();
            this.quiz.upsell.options = {};
          }
        });
      } else {
        doRemoveAnswer();
      }
    }
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        if (this.isQuizActiveAndStarted()) {
          this.errorService.emitError('You are not allowed to delete the Quiz that has already been started and shown to customers. ' +
            'If you want to deactivate this Quiz please change Display From date to any date in the past');
        } else {
          this.removeQuiz();
        }
        break;
      case 'save':
        this.saveQuizChanges();
        break;
      case 'revert':
        this.revertQuizChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private removeQuiz(): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Quiz',
      message: 'This will permanently remove the quiz. Are you sure?',
      yesCallback: () => {
        this.quizApiService.deleteQuiz(this.quiz.id)
          .subscribe((data: any) => {
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'Quiz is Removed.'
            });
            this.router.navigate(['/question-engine/quiz/']);
          });
      }
    });
  }

  private questionListToTree() {
    // deep clone question list obj not to amend original one
    const questionsListCopy = JSON.parse(JSON.stringify(this.questionsList));
    const firstQuestion: Question = questionsListCopy.length ? questionsListCopy[0] : null;

    for (let i = 1; i < questionsListCopy.length; i++) {
      const currentQuestion = questionsListCopy[i - 1];
      const nextQuestion = questionsListCopy[i];

      if (!currentQuestion.nextQuestions) {
        currentQuestion.nextQuestions = {};
      }
      currentQuestion.nextQuestions[nextQuestion.id] = nextQuestion;

      if (currentQuestion.answers && currentQuestion.answers.length) {
        currentQuestion.answers.forEach(value => {
          value.questionAskedId = currentQuestion.id;
          value.nextQuestionId = nextQuestion.id;
        });
      }
    }
    return firstQuestion;
  }

  private saveQuizChanges(): void {
    this.updateQuestions();

    if (this.quiz.active && (!this.quiz.firstQuestion || !this.quiz.firstQuestion.answers || !this.quiz.firstQuestion.answers.length)) {
      this.errorService.emitError('You cannot make a Quiz active without any Question with Answers');
    } else {
      if (this.quiz.upsell && this.quiz.upsell.fallbackImageToUpload) {
        this.quizApiService.updateQuiz(this.quiz)
          .subscribe((quiz: Quiz) => {
            this.quizApiService.uploadFallbackImage(this.quiz.id, this.quiz.upsell.fallbackImageToUpload)
              .map((response: HttpResponse<Quiz>) => {
                this.quiz.upsell.fallbackImageToUpload = null;
                return response.body;
              })
              .subscribe(body => {
                  this.quiz = body;
                  this.quizEditingWarning = this.isQuizActiveAndStarted();
                  this.actionButtons.extendCollection(this.quiz);
                  this.showNotification('Quiz Changes are Saved.');
                  this.displayedCheckboxDisabled = this.isQuizActiveAndStarted();
                },
                (error: HttpErrorResponse) => {
                  this.errorService.emitError('Quiz changes are saved but Images are not uploaded. Error: ' + error.error.message);
                });
          });
      } else {
        this.quizApiService.updateQuiz(this.quiz)
          .map((response: HttpResponse<Quiz>) => {
            return response.body;
          })
          .subscribe((data: Quiz) => {
            this.quiz = data;
            this.actionButtons.extendCollection(this.quiz);
            this.quizEditingWarning = this.isQuizActiveAndStarted();
            this.showNotification('Quiz Changes are Saved.');
            this.uploadQuestionDetailsImages(0, this.quiz);
            this.displayedCheckboxDisabled = this.isQuizActiveAndStarted();
          });
      }
    }
  }

  private uploadQuestionDetailsImages(index, result: Quiz): void {
    if (this.questionDetailsImages.length !== index) {
      const imageToUpload = this.questionDetailsImages[index];
      index++;
      this.quizApiService.uploadQuestionDetailsImages(this.quiz.id, imageToUpload.questionId, imageToUpload.homeSvg,
        imageToUpload.awaySvg, imageToUpload.channel)
        .map((response: HttpResponse<Quiz>) => {
          return response.body;
        })
        .subscribe((data: Quiz) => {
          this.uploadQuestionDetailsImages(index, data);
        }, (error) => {
          this.revertQuizChanges();
        });
    } else if (this.questionDetailsImages.length !== 0) {
      this.questionDetailsImages = [];

      const flatten = Question.flatten(result.firstQuestion);

      _.forEach(this.questionsList, (question: Question) => {
        const foundQuestion = _.find(flatten, {id: question.id});
        question.questionDetails.homeTeamSvg = foundQuestion.questionDetails.homeTeamSvg;
        question.questionDetails.awayTeamSvg = foundQuestion.questionDetails.awayTeamSvg;
        question.questionDetails.channelSvg = foundQuestion.questionDetails.channelSvg;
      });

      this.showNotification('Images are uploaded');
    }
  }

  showNotification(message): void {
    this.snackBar.open(message, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  private revertQuizChanges(): void {
    this.questionsList = [];
    this.questionDetailsImages = [];
    this.loadInitialData();
  }

  public onChangeLoginRule(value: string): void {
    this.quiz.quizLoginRule = value;
  }

  private loadSplashPages(): void {
    this.splashPageApiServcie.getSplashPagesByBrand()
      .subscribe((data: any) => {
        this.selectSplashPages = data.body;
        this.selectSplashPages.unshift(EMPTY_SP);
      });
  }

  private loadQuickLinksPages(): void {
    this.quickLinksApiService.getQEQuickLinksByBrand()
      .subscribe((data: any) => {
        this.selectQuickLinks = data.body;
        const emptyQuickLink: QEQuickLinks = {
          brand: '',
          createdAt: '',
          createdBy: '',
          createdByUserName: '',
          id: '',
          links: [],
          title: '',
          updatedAt: '',
          updatedBy: '',
          updatedByUserName: ''

        };
        this.selectQuickLinks.unshift(emptyQuickLink);
      });
  }

  onChangeSelectedSplashPage(splashPageId: string): void {
    if (splashPageId === '-1') {
      this.quiz.splashPage = undefined;
    } else {
      this.quiz.splashPage = _.find(this.selectSplashPages, {id: splashPageId});
    }
  }

  onChangeSelectedQuickLinks(quickLinksId: string): void {
    this.quiz.qeQuickLinks = _.find(this.selectQuickLinks, {id: quickLinksId});
  }

  public handelEntryDeadline(date: string): void {
    this.quiz.entryDeadline = new Date(date).toISOString();
  }

  openUpsellConfig() {
    this.dialog.open(UpsellComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {quiz: this.quiz, flattenQuestions: this.questionsList}
    });
  }

  prepareToUploadQuestionDetailsImages(event, question: Question, imageType: string): void {
    const file = event.target.files[0];
    const supportedTypes = ['image/svg', 'image/svg+xml'];
    if (supportedTypes.indexOf(file.type) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"svg\".'
      });

      return;
    }
    let imageToUpload = _.find(this.questionDetailsImages, {questionId: question.id});

    if (!imageToUpload) {
      imageToUpload = new QuestionDetailsImages(question.id, undefined, undefined, undefined);
      this.questionDetailsImages.push(imageToUpload);
    }

    if (imageType === 'home') {
      imageToUpload.homeSvg = file;
    } else if (imageType === 'away') {
      imageToUpload.awaySvg = file;
    } else if (imageType === 'channel') {
      imageToUpload.channel = file;
    }
    this.quiz.isChanged = true;
  }

  getImageToUploadValue(question: Question, imageType: string): string {
    const homeTeam = imageType === 'home';
    const awayTeam = imageType === 'away';
    const channelTeam = imageType === 'channel';

    const imageToUpload = _.find(this.questionDetailsImages, {questionId: question.id});
    if (imageToUpload) {
      if (homeTeam) {
        return imageToUpload.homeSvg ? imageToUpload.homeSvg.name : question.questionDetails.homeTeamSvg.originalname;
      } else if (awayTeam) {
        return imageToUpload.awaySvg ? imageToUpload.awaySvg.name : question.questionDetails.awayTeamSvg.originalname;
      } else if (channelTeam) {
        return imageToUpload.channel ? imageToUpload.channel.name : question.questionDetails.channelSvg.originalname;
      }
    } else {
      if (homeTeam && question.questionDetails.homeTeamSvg) {
        return question.questionDetails.homeTeamSvg.originalname;
      } else if (awayTeam && question.questionDetails.awayTeamSvg) {
        return question.questionDetails.awayTeamSvg.originalname;
      } else if (channelTeam && question.questionDetails.channelSvg) {
        return question.questionDetails.channelSvg.originalname;
      }
    }
    return '';
  }

  removeQuestionDetailsImagesHandler(event, question: Question, imageType: string): void {
    const homeTeam = imageType === 'home';
    const awayTeam = imageType === 'away';
    const channelTeam = imageType === 'channel';

    if (homeTeam) {
      this.clearFilenameSvg(question.questionDetails.homeTeamSvg);
    } else if (awayTeam) {
      this.clearFilenameSvg(question.questionDetails.awayTeamSvg);
    } else if (channelTeam) {
      this.clearFilenameSvg(question.questionDetails.channelSvg);
    }

    if (this.questionDetailsImages.length > 0) {

      const imageToRemove = _.find(this.questionDetailsImages, {questionId: question.id});

      if (homeTeam) {
        imageToRemove.homeSvg = undefined;
      } else if (awayTeam) {
        imageToRemove.awaySvg = undefined;
      } else if (channelTeam) {
        imageToRemove.channel = undefined;
      }

      if (!imageToRemove.homeSvg && !imageToRemove.awaySvg && !imageToRemove.channel) {
        const index = this.questionDetailsImages.indexOf(imageToRemove, 0);
        if (index > -1) {
          this.questionDetailsImages.splice(index, 1);
        }
      }
    }

    this.quiz.isChanged = true;
  }

  private clearFilenameSvg(filename: Filename) {
    filename.originalname = '';
    filename.filename = '';
    filename.path = '';
    filename.filetype = '';
    filename.size = 0;
  }

  uploadSvgHandler(event) {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  getButtonName(fileName): string {
    return fileName && fileName.length > 0 ? 'Change File' : 'Upload File';
  }

  uploadQuizLogoSvgHandler(event) {
    const file = event.target.files[0];
    const supportedTypes = ['image/svg', 'image/svg+xml'];
    if (supportedTypes.indexOf(file.type) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"svg\".'
      });

      return;
    }

    this.quizApiService.uploadQuizLogoImage(this.quiz.id, file)
      .map((response: HttpResponse<Quiz>) => {
        return response.body;
      })
      .subscribe((quiz: Quiz) => {
        this.quiz.quizLogoSvg = quiz.quizLogoSvg;
        this.showNotification('Quiz Logo is uploaded');
      }, (error) => {
        this.actionButtons.extendCollection(this.quiz);
      });
  }

  uploadQuizBackgroundSvgHandler(event) {
    const file = event.target.files[0];
    const supportedTypes = ['image/svg', 'image/svg+xml'];
    if (supportedTypes.indexOf(file.type) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"svg\".'
      });

      return;
    }

    this.quizApiService.uploadQuizBackgroundImage(this.quiz.id, file)
      .map((response: HttpResponse<Quiz>) => {
        return response.body;
      })
      .subscribe((quiz: Quiz) => {
        this.quiz.quizBackgroundSvg = quiz.quizBackgroundSvg;
        this.showNotification('Quiz Background is uploaded');
      }, (error) => {
        this.actionButtons.extendCollection(this.quiz);
      });
  }

  removeQuizLogoSvgHandler() {

    this.quizApiService.deleteQuizLogoImage(this.quiz.id)
      .map((response: HttpResponse<Quiz>) => {
        return response.body;
      })
      .subscribe((quiz: Quiz) => {
        this.quiz.quizLogoSvg = quiz.quizLogoSvg;
        this.showNotification('Quiz Logo is Removed');
      });
  }

  removeQuizBackgroundSvgHandler() {
    this.quizApiService.deleteQuizBackgroundImage(this.quiz.id)
      .map((response: HttpResponse<Quiz>) => {
        return response.body;
      })
      .subscribe((quiz: Quiz) => {
        this.quiz.quizBackgroundSvg = quiz.quizBackgroundSvg;
        this.showNotification('Quiz Background is Removed');
      });
  }

  uploadDefaultQuestionDetailsSvgHandler(event, imageType) {
    const file = event.target.files[0];
    const supportedTypes = ['image/svg', 'image/svg+xml'];
    if (supportedTypes.indexOf(file.type) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"svg\".'
      });

      return;
    }

    this.quizApiService.uploadDefaultQuestionDetailsImage(this.quiz.id, file, imageType)
      .map((response: HttpResponse<Quiz>) => {
        return response.body;
      })
      .subscribe((quiz: Quiz) => {
        if (imageType === 'away') {
          this.quiz.defaultQuestionsDetails.awayTeamSvg = quiz.defaultQuestionsDetails.awayTeamSvg;
        } else if (imageType === 'home') {
          this.quiz.defaultQuestionsDetails.homeTeamSvg = quiz.defaultQuestionsDetails.homeTeamSvg;
        } else if (imageType === 'channel') {
          this.quiz.defaultQuestionsDetails.channelSvg = quiz.defaultQuestionsDetails.channelSvg;
        }
        this.showNotification('Image is uploaded');
      }, (error) => {
        this.actionButtons.extendCollection(this.quiz);
      });
  }

  removeDefaultQuestionDetailsSvgHandler(event, imageType) {
    this.quizApiService.deleteDefaultQuestionDetailsImage(this.quiz.id, imageType)
      .map((response: HttpResponse<Quiz>) => {
        return response.body;
      })
      .subscribe((quiz: Quiz) => {
        if (imageType === 'away') {
          this.quiz.defaultQuestionsDetails.awayTeamSvg = quiz.defaultQuestionsDetails.awayTeamSvg;
        } else if (imageType === 'home') {
          this.quiz.defaultQuestionsDetails.homeTeamSvg = quiz.defaultQuestionsDetails.homeTeamSvg;
        } else if (imageType === 'channel') {
          this.quiz.defaultQuestionsDetails.channelSvg = quiz.defaultQuestionsDetails.channelSvg;
        }
        this.showNotification('Image is Removed');
      });
  }

  loadEndPages() {
    const emptyEndPage: EndPage = {
      isChanged: false,
      showAnswersSummary: false,
      backgroundSvgImage: undefined,
      gameDescription: '',
      noLatestRoundMessage: '',
      noPreviousRoundMessage: '',
      showPrizes: false,
      showResults: false,
      submitMessage: '',
      showUpsell: false,
      id: '',
      title: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      brand: '',
      updatedByUserName: '',
      createdByUserName: '',
      upsellAddToBetslipCtaText: '',
      upsellBetInPlayCtaText: '',
      submitCta: '',
      successMessage: '',
      errorMessage: '',
      redirectionButtonLabel: '',
      redirectionButtonUrl: '',
      bannerSiteCoreId: ''
    };

    this.endPageApiService.getEndPagesByBrand()
      .subscribe((data: any) => {
        this.endPages = data.body;
        this.answerEndPages = [emptyEndPage, ...this.endPages];
      });
  }

  onEndPageSelection(endPageId: string) {
    this.quiz.endPage = _.find(this.endPages, {id: endPageId});
  }

  onAnswerEndPageSelection(endPageId: string, answer: Answer) {
    if (endPageId === '-1') {
      answer.endPage = undefined;
    } else {
      answer.endPage = _.find(this.endPages, {id: endPageId});
    }
    this.quiz.isChanged = true;
  }

  handleNeededChange(event) {
    if (event.index === 1) {
      setTimeout(() => {
        this.showAccordionBool = true;

      }, 100);
    } else {
      setTimeout(() => {
        this.showAccordionBool = false;
      }, 100);

    }
    this.handlePrizesTab(event);
  }

  private handlePrizesTab(event) {
    if (event.index === 2) {
      this.loadPrizes();
    }
  }

  uploadPopupIconSvgHandler(event, popupType: string) {
    const file = event.target.files[0];
    const supportedTypes = ['image/svg', 'image/svg+xml'];
    if (supportedTypes.indexOf(file.type) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"svg\".'
      });

      return;
    }

    this.quizApiService.uploadPopupIconImage(this.quiz.id, file, popupType)
      .map((response: HttpResponse<Quiz>) => {
        return response.body;
      })
      .subscribe((quiz: Quiz) => {
        if ('submit' === popupType) {
          this.quiz.submitPopup.icon = quiz.submitPopup.icon;
          this.showNotification('Submit Popup Icon is uploaded');
        } else if ('exit' === popupType) {
          this.quiz.exitPopup.icon = quiz.exitPopup.icon;
          this.showNotification('Exit Popup Icon is uploaded');
        }
      });
  }

  removePopupIconSvgHandler(event, popupType: string) {
    this.quizApiService.deletePopupIconImage(this.quiz.id, popupType)
      .map((response: HttpResponse<Quiz>) => {
        return response.body;
      })
      .subscribe((quiz: Quiz) => {
        if ('submit' === popupType) {
          this.quiz.submitPopup.icon = quiz.submitPopup.icon;
          this.showNotification('Submit Popup Icon is Removed');
        } else if ('exit' === popupType) {
          this.quiz.exitPopup.icon = quiz.exitPopup.icon;
          this.showNotification('Exit Popup Icon is Removed');
        }
      });
  }

  getLabel(prizeTypeKey: string): string {
    return this.prizeTypes.get(prizeTypeKey);
  }

  getKeys(): string[] {
    return Array.from(this.prizeTypes.keys());
  }

  private loadPrizes() {
    if (!this.quiz.correctAnswersPrizes) {
      this.quiz.correctAnswersPrizes = [];
    }
    if (this.quiz.correctAnswersPrizes.every(prize => prize.correctSelections !== 0)) {
      this.quiz.correctAnswersPrizes.push(new Prize(0, 'NONE', 0.0));
    }
    this.questionsList
      .map((question, index) => new Prize(index + 1, 'NONE', 0.0))
      .filter(prize => this.quiz.correctAnswersPrizes.every(existingPrize => existingPrize.correctSelections !== prize.correctSelections))
      .forEach(prize => this.quiz.correctAnswersPrizes.push(prize));
  }

  public clickUp(element) {

    this.validateAndMove(element, -1);
  }

  public clickDown(element) {

    this.validateAndMove(element, 1);
  }

  private validateAndMove(element, delta) {
    if (this.quiz.upsell && Object.keys(this.quiz.upsell.options).length) {
      this.dialogService.showConfirmDialog({
        title: 'Confirm reordering',
        message: 'Your entire Dynamic Upsell configuration will be lost due to Question order change. Are you sure?',
        yesCallback: () => {
          this.move(element, delta);
        }
      });
    } else {
      this.move(element, delta);
    }

  }

  private move(element, delta) {
    const oldIndex = this.questionsList.indexOf(element);
    const newIndex = oldIndex + delta;
    if (newIndex < 0 || newIndex === this.questionsList.length) {
      return; // Already at the top or bottom.
    }
    const indexes = [oldIndex, newIndex].sort(); // Sort the indixes
    this.questionsList.splice(indexes[0], 2, this.questionsList[indexes[1]], this.questionsList[indexes[0]]);

    this.endReordering(oldIndex, newIndex);
  }

  private endReordering(oldIndex, newIndex) {
    this.mutateQuiz();

    this.questionsList[oldIndex].nextQuestions = {};
    this.questionsList[newIndex].nextQuestions = {};

    if (this.questionsList[oldIndex].answers) {
      this.questionsList[oldIndex].answers.forEach(answer => {
        answer.nextQuestionId = null;
      });
    }
    if (this.questionsList[newIndex].answers) {
      this.questionsList[newIndex].answers.forEach(answer => {
        answer.nextQuestionId = null;
      });
    }
    if (this.quiz.upsell) {
      this.quiz.upsell.options = {};
    }
  }

  public eventIdChanged() {
    this.quiz.eventDetails.startTime = '';
    this.quiz.eventDetails.eventName = '';
    this.quiz.eventDetails.actualScores[0] = undefined;
    this.quiz.eventDetails.actualScores[1] = undefined;
  }

  private validEventDetailsStartTime(): boolean {
    const regExp = new RegExp('^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$');
    if (this.quiz.eventDetails.startTime) {
      return this.quiz.eventDetails.startTime.length === 0 ||
        (regExp.test(this.quiz.eventDetails.startTime) && !_.isNaN(Date.parse(this.quiz.eventDetails.startTime)));
    } else {
      return true;
    }
  }

  openCreateWindow() {
    const dialogRef = this.dialog.open(QuizEngineCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        data: {quizToClone: this.quiz}
      }
    });

    dialogRef.afterClosed().subscribe(newQuiz => {
      if (newQuiz) {
        this.quizApiService.createQuiz(newQuiz)
          .subscribe(response => {
            if (response) {
              this.router.routeReuseStrategy.shouldReuseRoute = function () {
                return false;
              };
              this.router.navigate([`/question-engine/quiz/${response.body.id}`]);
            }
          });
      }
    });
  }

  private isQuizActiveAndStarted(): boolean {
    const displayFromDate = new Date(this.quiz.displayFrom);
    const dateNow = new Date();
    return this.quiz.active && dateNow > displayFromDate;
  }

  openCoinRewardsPopup(prevPrizeType: string) {
    this.prevPrizeType = prevPrizeType;
    this.dialogService.showCustomDialog(FssRewardsDialogComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Coins Configuration',
      yesOption: 'Save',
      noOption: 'Cancel',
      data: _.cloneDeep(this.quiz.coin),
      yesCallback: (fssRewards: FssRewards) => {
        this.quiz.coin = fssRewards;
      },
      noCallback: () => {
        this.prevPrizeType!=='COIN' && (!this.quiz.coin?.value || this.quiz.coin?.value<1 || this.quiz.coin?.value>500) && this.quiz.correctAnswersPrizes.forEach((prize: Prize) => {
          if (prize.correctSelections === 0) {
            prize.prizeType = this.prevPrizeType;
          }
        });
      }
    });
  }
}
