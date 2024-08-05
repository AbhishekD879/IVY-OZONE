import { Injectable, OnDestroy } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpResponse } from '@angular/common/http';

import { catchError, flatMap, map, timeout, filter, pairwise } from 'rxjs/operators';
import { from as observableFrom, Observable, of as observableOf, Subscription, throwError } from 'rxjs';

import environment from '@environment/oxygenEnvConfig';
import { UserService } from '@core/services/user/user.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { MapQuizModelService } from '@app/questionEngine/services/question-engine/mapQuizModel.service';
import { GtmService } from '@core/services/gtm/gtm.service';

import { IUserAnswersModel } from '@app/questionEngine/models/userAnswers.model';
import { IQuizHistoryModel } from '@app/questionEngine/models/quizHistory.model';
import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { INoGamesContentModel } from '@app/questionEngine/models/noGamesContent.model';

import {
  LATEST_TAB_ID,
  LOGIN_RULE, PREVIOUS_TAB_ID,
  QE_INIT_DATA_FAILURE,
  QUIZZES_PAGE_SIZE,
  QE_PATH_VARIABLE,
  CORRECT4_SOURCE_ID, BACKEND_RESPONSE_TIMEOUT_LIMIT, QUESTION_PAGE_ROUTE
} from '@app/questionEngine/constants/question-engine.constant';
import { IPrevQuizModel } from '@app/questionEngine/models/qePrevQuizModel.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { IQuizModel } from '@app/questionEngine/models/quiz.model';
import { Location } from '@angular/common';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable({
  providedIn: 'root'
})
export class QuestionEngineService implements OnDestroy {

  isLoginPopupShown: boolean;
  brand: string = environment.brand;
  public redirectToTab: string = '';
  public showSubmitNotification: boolean = false;
  public quizHistoryModel: IQuizHistoryModel;
  public qeData: QuestionEngineModel;
  public qeSubmittedThisSession: boolean = false;
  public dataIsUpToDate: boolean = true;
  public checkForAnonymousData: boolean = false;
  private previousRoute: string;
  private routerSubscription: Subscription;

  constructor(
    private pubSubService: PubSubService,
    private http: HttpClient,
    private userService: UserService,
    protected bppService: BppService,
    private routingState: RoutingState,
    private mapQuizModelService: MapQuizModelService,
    private commandService: CommandService,
    private gtmService: GtmService,
    protected awsService: AWSFirehoseService,
    private router: Router,
    protected route: ActivatedRoute,
    private location: Location
  ) {
    this.init();
  }

  public init(): void {
    this.routerSubscription = this.router.events
      .pipe(filter(event => event instanceof NavigationEnd), pairwise())
      .subscribe((e) => {
        this.handleAdditionalNavigatingForSplashAndQuestionPages(e);
      });
  }

  public ngOnDestroy(): void {
    this.routerSubscription.unsubscribe();
  }

  public get hideSplashPageConfig(): boolean {
    return this.qeData && this.qeData.baseQuiz
      && this.qeData.baseQuiz.quizConfiguration && this.qeData.baseQuiz.quizConfiguration.showSplashPage === false;
  }
  public set hideSplashPageConfig(value:boolean){}
  public get quizAlreadyTaken() {
    return this.qeData && this.qeData.baseQuiz && this.qeData.baseQuiz.firstAnsweredQuestion;
  }
  public set quizAlreadyTaken(value:any){}
  public get sourceIdFromParams(): string {
    if (this.router.url.match(CORRECT4_SOURCE_ID)) {
      return CORRECT4_SOURCE_ID.slice(1); // delete "/" before text
    } else {
      return this.routingState.getRouteParam('sourceId', this.route.snapshot);
    }
  }
  public set sourceIdFromParams(value:string){}

  /**
   * Map BackEnd response to data model used on FrontEnd
   * @param {IQuizHistoryModel} quizHistoryModel
   * @return {QuestionEngineModel}
   */
  public mapResponseOnComponentModel(quizHistoryModel: IQuizHistoryModel): QuestionEngineModel {
    if (!quizHistoryModel || (!quizHistoryModel.live && !(quizHistoryModel.previous && quizHistoryModel.previous.length > 0))) {
      this.triggerFatalError('No base quiz data');
      return null; // no data at all
    }

    this.quizHistoryModel = quizHistoryModel;
    this.qeData = new QuestionEngineModel();
    this.qeData.previousCount = quizHistoryModel.previousCount;

    if (quizHistoryModel.live) {
      this.qeData.baseQuiz = this.mapQuizModelService.mapQuizModel(quizHistoryModel.live);
      this.qeData.baseQuiz.isLive = true;
    } else {
      this.qeData.baseQuiz = this.mapQuizModelService.mapQuizModel(quizHistoryModel.previous[0]);
    }

    this.qeData.previous = quizHistoryModel.previous.map(quiz => this.mapQuizModelService.mapQuizModel(quiz));
    if (this.qeData.baseQuiz.splashPage) {
      this.resolveCtaButtonText();
    }
    return this.qeData;
  }

  public resolvePath(sourceId: string): string {
    return this.router.url.match(CORRECT4_SOURCE_ID) ? CORRECT4_SOURCE_ID : `${QE_PATH_VARIABLE}${sourceId}`;
  }

  public checkIfShouldRedirectGuest(): boolean {
    if (!this.userService.status) {
      const path = this.qeData ? `${this.resolvePath(this.qeData.baseQuiz.sourceId)}` : '/';
      this.router.navigateByUrl(path);
      return true;
    }
    return false;
  }

  /**
   * Map BackEnd response to data model used on FrontEnd
   * @param {prevQuizModel} IPrevQuizModel
   * @return {QuestionEngineQuizModel[]}
   */
  public mapPrevQuizzesResponseOnComponentModel(prevQuizModel: IPrevQuizModel): QuestionEngineQuizModel[] {
    if (!prevQuizModel || !(prevQuizModel.quizzes && prevQuizModel.quizzes.length > 0)) {
      return null; // no data at all
    }
    return prevQuizModel.quizzes.map((quiz: IQuizModel) => this.mapQuizModelService.mapQuizModel(quiz));
  }

  /**
   * Determines CTA text and updates in FE data model
   */
  public resolveCtaButtonText(): void {
    const {
      splashPage: {
        loginToViewCTAText, playForFreeCTAText, seePreviousSelectionsCTAText, seeYourSelectionsCTAText
      }
    } = this.qeData.baseQuiz;
    let ctaButtonText = null;

    if (this.qeData.baseQuiz.quizLoginRule === LOGIN_RULE.START) {
      if (!this.userService.status) {
        this.qeData.baseQuiz.splashPage.ctaButtonText = loginToViewCTAText; // please login
        return;
      }

      if (this.qeData.baseQuiz.firstAnsweredQuestion) {
        this.redirectToTab = LATEST_TAB_ID;
        ctaButtonText = seeYourSelectionsCTAText; // See your selections
      } else {
        if (this.qeData.baseQuiz.entryDeadline > new Date()) {
          this.redirectToTab = QUESTION_PAGE_ROUTE;
          ctaButtonText = playForFreeCTAText; // Play Game
        } else {
          this.redirectToTab = PREVIOUS_TAB_ID;
          ctaButtonText = seePreviousSelectionsCTAText; // See previous games
        }
      }
    }
    this.qeData.baseQuiz.splashPage.ctaButtonText = ctaButtonText;
  }

  public titleFormatForGA(str: string): string {
    const st: string = str ? str.slice(1) : '';
    return st ? st.charAt(0).toUpperCase() + st.substr(1).toLowerCase() : '';
  }

  /**
   * GA: Send tracking data to GTM
   *
   * @param eventAction, eventLabel
   */
  public trackEventGA(eventAction: string, eventLabel: string = 'none'): void {
    this.gtmService.push('trackEvent', {
      eventCategory: this.titleFormatForGA(this.qeData.baseQuiz.sourceId),
      eventAction: eventAction,
      eventLabel: eventLabel
    });
  }

  /**
   * GA: Send tracking pageURL data to GTM
   *
   * @param pageURL
   */
  public trackPageViewGA(pageURL: string): void {
    this.gtmService.push('trackPageview', {
      virtualUrl: pageURL
    });
  }

  public handleNoPrevGamesContent(tabType: string): INoGamesContentModel {
    const { noLatestRoundMessage, noPreviousRoundMessage } = this.qeData.baseQuiz.resultsPage;

    const content = tabType === LATEST_TAB_ID ? noLatestRoundMessage : noPreviousRoundMessage;
    return {
      title: content ? content.split('.')[0] : 'No content',
      subtitle: content ? content.split('.')[1] : 'No content'
    };
  }

  toggleSubmitNotification(value: boolean): void {
    this.showSubmitNotification = value;
  }

  public submitUserAnswer(userAnswers: IUserAnswersModel, isSurvey: boolean = false): Observable<any> {
    return this.http.post(`${environment.QUESTION_ENGINE_ENDPOINT}/v1/user-answer/`, userAnswers, {
      headers: this.getAuthenticationHeader()
    }).pipe(
      map((res: any) => {
        this.toggleSubmitNotification(!isSurvey); // used for displaying submit notification on results page
        return res;
      }),
      catchError((err: Error | HttpErrorResponse) => {
        this.awsService.addAction(`${this.qeData.baseQuiz.sourceId}=>Submit_Quizzes_Error`,
          { error: err });
        if (err instanceof HttpErrorResponse) {
          if (err.status === 400 && err.error && err.error.reason && err.error.reason.indexOf('already been submitted') !== -1) {
            return observableOf(true); // return success
          } else if (err.status === 401) {
            return this.authenticate().pipe(
              flatMap(bppToken => this.submitUserAnswer(userAnswers, isSurvey))
            );
          } else {
            return throwError(err);
          }
        }
      }));
  }

  /**
   * set flag that QA has been submitted so if user go back to Splash Screen system perform
   * call to update app QE Data
   */
  public setQESubmitStatus(value: boolean): void { // TODO move this into submitUserAnswer method
    this.qeSubmittedThisSession = value;
  }

  /**
   * Tell app that QE data should be updated after Quiz submission
   * @param value
   */
  public setQEDataUptodateStatus(value: boolean): void {
    this.dataIsUpToDate = value;
  }

  /**
   * check if no quiz live or previous game data
   * from BE - proceed with default data fetch
   * @param data
   * @param cb
   */
  public checkGameData(data: IQuizHistoryModel, cb: Function): boolean {
    if (data && !data.live && data.previous && !data.previous.length) {
      if (this.checkForAnonymousData) {
        this.triggerFatalError(QE_INIT_DATA_FAILURE);
      } else {
        this.checkForAnonymousData = true;
        cb(true);
        return true;
      }
    }
    return false;
  }

  /**
   * reset flag value for anonymous call to BE used in `checkGameData()` method;
   */
  public resetCheckForAnonymousDataValue(): void {
    this.checkForAnonymousData = false;
  }

  public triggerFatalError(message: string, error?: Error): void {
    this.pubSubService.publish(this.pubSubService.API.QE_FATAL_ERROR, [message, error]);
  }

  /**
   * Do BackEnd call for Question Engine data depending on user login status
   * @return {QuestionEngineModel}
   */
  public getQuizHistory(initial: boolean = false): Observable<IQuizHistoryModel | unknown> {
    if (this.userService && this.userService.username && !initial) { // user is logged in
      const authenticationHeader = this.getAuthenticationHeader();

      if (authenticationHeader) {
        return this.doHistoryBackendCall<IQuizHistoryModel>(this.getUserHistoryBackendURL(), authenticationHeader);
      } else {
        return this.authenticate().pipe(
          flatMap(bppTokenHeader => this.doHistoryBackendCall<IQuizHistoryModel>(
            this.getUserHistoryBackendURL(),
            bppTokenHeader)
          )
        );
      }
    } else {
      return this.doHistoryBackendCall<IQuizHistoryModel>(this.anonymousBackendURL);
    }
  }

  /**
   * Do BackEnd call for checkQuizAvailability data depending on user login status
   * @return Observable<boolean>
   */
  public userAnswersExist(username: string, quizId: string): Observable<boolean> {
    const url = `${environment.QUESTION_ENGINE_ENDPOINT}/v2/user-answer/${username}/${quizId}/exists`;
    if (this.getAuthenticationHeader()) {
      return this.isUserAnswerExist(url);
    }
    return this.authenticate().pipe(
      flatMap(bppTokenHeader => this.isUserAnswerExist(url))
    );
  }

  /**
   * Do BackEnd call for Question Engine Previous Quizzes data depending on user login status
   * @return {IPrevQuizModel}
   */
  public getPrevQuizes(pageNumber: number, pageSize: number): Observable<IPrevQuizModel | unknown> {
    if (this.userService && this.userService.username) { // user is logged in
      return this.doHistoryBackendCall<IPrevQuizModel>(
        this.getUserPrevQuizBackendURL(pageNumber, pageSize),
        this.getAuthenticationHeader()
      );
    }
  }

  public checkPreviousPage(): string {
    const path = this.qeData.baseQuiz.sourceId || `/${this.sourceIdFromParams}`;
    if (!this.routingState.getPreviousUrl().match(path)) {
      this.previousRoute = this.routingState.getPreviousUrl();
    }
    return this.previousRoute;
  }

  public addToSlipHandler(selectionId: string): Observable<{}> {
    return observableFrom(
      this.commandService.executeAsync(this.commandService.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS, [selectionId])
    );
  }

  private get anonymousBackendURL(): string {
    return `${environment.QUESTION_ENGINE_ENDPOINT}/v1/quiz/history/?source-id=/${this.sourceIdFromParams}&previous-limit=3`;
  }
  private set anonymousBackendURL(value:string){}

  private handleAdditionalNavigatingForSplashAndQuestionPages(e): void {
    const navSourceInfo = e[0];
    const navSourcePath = navSourceInfo && navSourceInfo.urlAfterRedirects;
    const navTargetInfo = e[1];
    const navTargetPath = navTargetInfo && navTargetInfo.url;

    const preventNavigatingToSplash = navTargetPath && navTargetPath.endsWith('splash')
      && navTargetPath.includes(QE_PATH_VARIABLE) && this.hideSplashPageConfig;
    const comingToQuestionsFromSplash = navSourcePath.endsWith('splash') && navSourcePath.includes(QE_PATH_VARIABLE);
    const preventNavigatingToQuestions = navTargetPath && navTargetPath.endsWith(QUESTION_PAGE_ROUTE)
      && navTargetPath.includes(QE_PATH_VARIABLE) && !comingToQuestionsFromSplash && this.quizAlreadyTaken;

    if (preventNavigatingToSplash || preventNavigatingToQuestions) {
      this.location.back();
    }
  }

  private isUserAnswerExist(url: string): Observable<boolean> {
    return this.http.get(url, { headers: this.getAuthenticationHeader(), observe: 'response' })
      .pipe(timeout(BACKEND_RESPONSE_TIMEOUT_LIMIT),
        map((response: HttpResponse<any>) => response.body),
        catchError((err: Error | HttpErrorResponse) => {
          if (err instanceof HttpErrorResponse && err.status === 401) {
            return this.authenticate().pipe(
              flatMap(bppToken => this.isUserAnswerExist(url))
            );
          }
          return throwError(err);
        })
      );
  }

  private doHistoryBackendCall<T>(url: string, header?: HttpHeaders): Observable<T | unknown> {
    return this.getHistoryModel(url, header).pipe(
      map((data: HttpResponse<IQuizHistoryModel>) => data.body),
      catchError((error) => {
        if (error instanceof HttpErrorResponse && error.status === 401) {
          return this.authenticate().pipe(
            flatMap(bppToken => this.doHistoryBackendCall(url, bppToken))
          );
        }
        console.error(`Error loading QE data ${url}`, error);
        this.triggerFatalError(QE_INIT_DATA_FAILURE, error);
        return observableOf(null);
      })
    );
  }

  private authenticate(): Observable<HttpHeaders> {
    return observableFrom(this.commandService.executeAsync(this.commandService.API.BPP_AUTH_SEQUENCE))
      .pipe(
        map(() => this.getAuthenticationHeader()),
        catchError(error => {
          console.error('Failed to authenticate to BPP');
          return throwError(error);
        })
      );
  }

  private getAuthenticationHeader(): HttpHeaders {
    return !this.userService.bppToken ? undefined : new HttpHeaders({
      token: this.userService.bppToken
    });
  }

  private getHistoryModel(url: string, authenticationHeader): Observable<HttpResponse<IQuizHistoryModel>> {
    return this.http.get<IQuizHistoryModel | null>(url, {
      observe: 'response',
      responseType: 'json',
      headers: authenticationHeader
    });
  }

  private getUserHistoryBackendURL(): string {
    return `${environment.QUESTION_ENGINE_ENDPOINT}/v1/quiz/history/${this.userService.username}` +
      `/?source-id=/${this.sourceIdFromParams}&previous-limit=3`;
  }

  private getUserPrevQuizBackendURL(pageNumber: number, pageSize: number = QUIZZES_PAGE_SIZE): string {
    return `${environment.QUESTION_ENGINE_ENDPOINT}/v1/quiz/previous/${this.userService.username}` +
      `/?source-id=/${this.sourceIdFromParams}&page-number=${pageNumber}&page-size=${pageSize}`;
  }

}
