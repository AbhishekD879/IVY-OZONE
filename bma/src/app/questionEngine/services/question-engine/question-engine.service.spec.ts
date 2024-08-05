import { from, of, of as observableOf, throwError as observableThrowError, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { QuestionEngineService } from './question-engine.service';
import environment from '@environment/oxygenEnvConfig';
import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { QuestionEngineSplashPageModel } from '@app/questionEngine/models/questionEngineSplashPage.model';
import { QuestionEngineResultsPageModel } from '@app/questionEngine/models/questionEngineResultsPage.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { Question } from '@app/questionEngine/models/question.model';
import { LinksModel } from '@app/questionEngine/models/links.model';
import { HttpErrorResponse, HttpHeaders, HttpResponse } from '@angular/common/http';
import { QuestionEngineQuestionDetailsModel } from '@app/questionEngine/models/questionEngineQuestionDetails.model';
import { QuizPopupModel } from '@app/questionEngine/models/quizPopup.model';
import { prevQuizModel, QEData } from '@app/questionEngine/services/qe-mock-data.mock';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { QE_INIT_DATA_FAILURE } from '@questionEngine/constants/question-engine.constant';
import { NavigationEnd } from '@angular/router';

describe('QuestionEngineService', () => {
  let service: QuestionEngineService;
  let customServiceForSubmitErrors: QuestionEngineService;

  const mockQEData = new QEData();

  let http,
    userService,
    mapQuizModelService,
    bppService,
    pubSubService,
    routingState,
    commandService,
    gtmService,
    awsService,
    router,
    route,
    routeSnapshot,
    getRequestParams,
    locationService;

  const sourceId = '/correct4';
  const userAnswers = {
    username: 'dmytro-aug-28',
    customerId: '12345678',
    quizId: '5d56cc2f591ed2714181187d',
    brand: 'ladbrokes',
    sourceId: '/upsell/aug-16',
    questionIdToAnswerId: {
      '7ec5e0e7-2214-416d-9134-fd0042d7d43f': ['4264b8d1-35cf-46f4-b79d-5b7d390f5eb3'],
      '9b1260d7-634a-4157-a824-87bb6db2f580': ['962661f2-78fb-4582-9f70-ac604e68d90f'],
      '2f656c04-5b3b-4024-831e-b00f74c5df08': ['1f73d900-d678-4842-92df-ae81e7c1d922']
    }
  };

  const quizHistoryModel = {
    'previousCount': 0,
    'live': {
      'quizConfiguration': {
        showSubmitPopup: true,
        showExitPopup: true,
        showSplashPage: true,
        showEventDetails: true,
        showProgressBar: true,
        showQuestionNumbering: true,
        showSwipeTutorial: true,
        useBackButtonToExitAndHideXButton: true,
        showPreviousAndLatestTabs: true
      },
      'id': '5d765a55c9e77c000100245b',
      'sourceId': '/correct4',
      'displayFrom': '',
      'displayTo': '',
      'entryDeadline': '',
      'title': 'devq1',
      'splashPage': {
        'title': 'dev-hellen',
        'strapLine': 'Lorem ipsum dolor sit amet, consectetur adipis elit, sed do eiusmod tempor incididunt.',
        'paragraphText1': 'pT1',
        'paragraphText2': 'pT2',
        'paragraphText3': 'pT3',
        'playForFreeCTAText': 'Play now for free',
        'seeYourSelectionsCTAText': 'See your selections',
        'seePreviousSelectionsCTAText': 'See previous games',
        'loginToViewCTAText': 'Login to view',
        'backgroundSvgFilePath': '',
        'backgroundSvgFilename': null,
        'logoSvgFilePath': 'logo.svg',
        'logoSvgFilename': 'fantastic.svg',
        'footerSvgFilePath': 'footer.svg',
        'footerSvgFilename': 'group-4.svg',
        'footerText': '18+. UK+IRE Online & Mobile Coral customers only. T&Cs apply.',
        'active': false,
        'showPreviousGamesButton': false
      },
      endPage: {
        backgroundSvgImagePath: 'string',
        gameDescription: 'string',
        noLatestRoundMessage: 'Latest title.subtitle',
        noPreviousRoundMessage: 'Previous title.subtitle',
        showAnswersSummary: false,
        showPrizes: false,
        showResults: false,
        showUpsell: false,
        submitMessage: 'string',
        title: 'string',
        upsellAddToBetslipCtaText: 'string',
        upsellBetInPlayCtaText: 'string',
        submitCta: 'Let`s go!',
      },
      'qeQuickLinks': {
        'title': 'hellen_test',
        'links': [{
          'title': 'Prizes',
          'relativePath': 'prizes',
          'description': '<h2>Prizes</h2>'
        }, {
          'title': 'Frequently Asked Questions',
          'relativePath': 'faq',
          'description': '<h2>FAQ</h2>'
        }, {
          'title': 'Terms & Conditions',
          'relativePath': 'terms-and-conditions',
          'description': '<h2>Terms and conditions</h2>'
        }]
      },
      'quizLoginRule': 'START',
      'firstQuestion': null,
      'firstAnsweredQuestion': null,
      'defaultQuestionsDetails': {
        'awayTeamName': 'Man Utd',
        'awayTeamSvgFilePath': 'f.svg',
        'channelSvgFilePath': 'd.svg',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
        'homeTeamName': 'Tottenham',
        'homeTeamSvgFilePath': 'img.svg',
        'middleHeader': '12:30',
        'signposting': '',
        'topLeftHeader': 'Champions League',
        'topRightHeader': 'FRI AUG 23'
      },
      'quizBackgroundSvgFilePath': 'images.svg',
      'quizLogoSvgFilePath': 'questionDetails.svg',
      'exitPopup': {
        'iconSvgPath': '3d3ce10c2aa2.svg',
        'closeCTAText': 'EXIT GAME',
        'description': 'Your selections will not be saved if you exit  without submitting them',
        'header': 'Are you sure?',
        'submitCTAText': 'KEEP PLAYING',
      },
      'submitPopup': {
        'iconSvgPath': '3d3ce10c2aa2.svg',
        'closeCTAText': 'EXIT GAME',
        'description': 'Your selections will not be saved if you exit  without submitting them',
        'header': 'Are you sure?',
        'submitCTAText': 'KEEP PLAYING',
      },
      'eventDetails': {
        'eventId': '10050712',
        'eventName': 'Man Unt vs Lviv',
        'startTime': '2019-10-16T13:18:00Z',
        'actualScores': [
          1,
          2
        ],
        'liveNow': false
      },
      'correctAnswersPrizes': [
        {
          'requiredCorrectAnswers': 1,
          'amount': 1,
          'currency': '$',
          'prizeType': ''
        },
        {
          'requiredCorrectAnswers': 2,
          'amount': 2,
          'currency': '£',
          'prizeType': ''
        },
        {
          'requiredCorrectAnswers': 3,
          'amount': 3,
          'currency': 'E',
          'prizeType': ''
        },
        {
          'requiredCorrectAnswers': 4,
          'amount': 50,
          'currency': '£',
          'prizeType': ''
        }],
    },
    'previous': [],
  };

  const qeData = new QuestionEngineModel();

  const pageNumber = 0;
  const pageSize = 3;

  beforeEach(() => {
    qeData.baseQuiz = new QuestionEngineQuizModel();
    qeData.baseQuiz.splashPage = new QuestionEngineSplashPageModel(
      'testStrapLine',
      'paragraphText1',
      'paragraphText2',
      'paragraphText3',
      'footertext',
      'logoSvgPath',
      'logoSvgUrl',
      'footerSvgPath',
      'footerSvgUrl',
      null,
      'loginToViewCTAText',
      'playForFreeCTAText',
      'seePreviousSelectionsCTAText',
      'seeYourSelectionsCTAText',
      'backgroundSvgFilePath',
      false
    );

    qeData.baseQuiz.resultsPage = new QuestionEngineResultsPageModel({
      backgroundSvgImagePath: 'string',
      gameDescription: 'string',
      noLatestRoundMessage: 'Latest title.subtitle',
      noPreviousRoundMessage: 'Previous title.subtitle',
      showAnswersSummary: false,
      showPrizes: false,
      showResults: false,
      showUpsell: false,
      submitMessage: 'string',
      title: 'string',
      upsellAddToBetslipCtaText: 'string',
      upsellBetInPlayCtaText: 'string',
      submitCta: 'Let`s go!',
    });

    qeData.baseQuiz.quickLinks = [new LinksModel()];
    qeData.baseQuiz.entryDeadline = new Date();
    qeData.baseQuiz.firstAnsweredQuestion = null;
    qeData.baseQuiz.firstQuestion = null;
    qeData.baseQuiz.id = 'testId';
    qeData.baseQuiz.sourceId = '/cash_v3';
    qeData.baseQuiz.quizLoginRule = 'START';

    qeData.baseQuiz.defaultQuestionsDetails = new QuestionEngineQuestionDetailsModel(
      'awayTeamName',
      'awayTeamSvgFilePath',
      'channelSvgFilePath',
      'description',
      'homeTeamName',
      'homeTeamSvgFilePath',
      'middleHeader',
      'signposting',
      'topLeftHeader',
      'topRightHeader'
    );

    qeData.baseQuiz.quizBackgroundSvgFilePath = 'quizBackgroundSvgFilePath';
    qeData.baseQuiz.quizLogoSvgFilePath = 'quizLogoSvgFilePath';
    qeData.baseQuiz.exitPopup = new QuizPopupModel(
      'iconSvgPath',
      'header',
      'description',
      'submitCTAText',
      'closeCTAText'
    );
    qeData.baseQuiz.submitPopup = new QuizPopupModel(
      'submitPopupIconSvgPath',
      'submitPopupHeader',
      'submitPopupDescription',
      'submitPopupSubmitCTAText',
      'submitPopupCloseCTAText'
    );

    qeData.baseQuiz.correctAnswersPrizes = [{
      requiredCorrectAnswers: 1,
      amount: 1,
      currency: '$',
      prizeType: ''
    }];

    qeData.baseQuiz.sourceId = '/correct4';

    pubSubService = {
      API: {
        TOGGLE_MOBILE_HEADER_FOOTER: 'TOGGLE_MOBILE_HEADER_FOOTER',
        QE_FATAL_ERROR: 'QE_FATAL_ERROR'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      url: '/qe/cash_v3',
      events: of({})
    };

    route = {
      params: observableOf({
        id: '1',
        sport: 'tennis'
      }),
      snapshot: routeSnapshot
    } as any;

    routeSnapshot = {
      data: {},
      url: [{ path: 'sport' }],
      paramMap: {
        get: jasmine.createSpy('get').and.returnValue(observableOf({}))
      },
      params: {
        sport: 'football'
      }
    } as any;

    bppService = jasmine.createSpyObj('bppService', ['send']);
    http = {
      get: jasmine.createSpy('get').and.returnValue(observableOf({
        body: {}
      })),
      post: jasmine.createSpy('post').and.returnValue(observableOf({
        body: {}
      }))
    };

    userService = {
      status: false,
      username: 'Sofofika1',
      bppToken: 'qwerty'
    };

    mapQuizModelService = {
      mapQuizModel: jasmine.createSpy('mapQuizModel').and.returnValue(mockQEData.qeData.baseQuiz)
    };

    routingState = {
      getPreviousUrl: jasmine.createSpy('getPreviousUrl').and.returnValue('/correct4-page'),
      getRouteParam: jasmine.createSpy('getRouteParam').and.returnValue('correct4')
    };

    commandService = {
      API: commandApi,
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({
        result: true
      }))
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };

    awsService = {
      errorLog: jasmine.createSpy('errorLog').and.returnValue(observableOf()),
      addAction: jasmine.createSpy('addAction').and.returnValue(observableOf())
    };

    locationService = {
      back: jasmine.createSpy('back').and.callThrough()
    };

    service = new QuestionEngineService(
      pubSubService,
      http,
      userService,
      bppService,
      routingState,
      mapQuizModelService,
      commandService,
      gtmService,
      awsService,
      router,
      route,
      locationService
    );

    customServiceForSubmitErrors = new QuestionEngineService(
      pubSubService,
      http,
      userService,
      bppService,
      routingState,
      mapQuizModelService,
      commandService,
      gtmService,
      awsService,
      router,
      route,
      locationService
    );

    customServiceForSubmitErrors.qeData = {
      ...qeData,
      baseQuiz: {
        ...qeData.baseQuiz,
        sourceId: 'correct4'
      }
    };

    getRequestParams = [
      `${environment.QUESTION_ENGINE_ENDPOINT}/v1/quiz/history/${userService.username}/?source-id=${sourceId}&previous-limit=3`, {
      observe: 'response',
      responseType: 'json',
      headers: jasmine.any(HttpHeaders)
    }];
  });

  describe('Testing QuestionEngineService ', () => {
    it('init should call processGoingToSplashPage', fakeAsync(() => {
      const navInfo1 = new NavigationEnd(null, 'stub1', 'stub1');
      const navInfo2 = new NavigationEnd(null, 'stub2', 'stub2');
      router.events = from([navInfo1, navInfo2]);
      const service2 = new QuestionEngineService(
        pubSubService,
        http,
        userService,
        bppService,
        routingState,
        mapQuizModelService,
        commandService,
        gtmService,
        awsService,
        router,
        route,
        locationService
      );
      service2['handleAdditionalNavigatingForSplashAndQuestionPages'] =
        jasmine.createSpy('handleAdditionalNavigatingForSplashAndQuestionPages');

      service2.init();
      tick(5000);

      expect(service2['handleAdditionalNavigatingForSplashAndQuestionPages']).toHaveBeenCalledTimes(1);
    }));

    it('should init component', () => {
      expect(service).toBeTruthy();
    });

    it('should call unsubscribe', () => {
      service['routerSubscription'].unsubscribe = jasmine.createSpy('routerSubscription').and.callThrough();
      service.ngOnDestroy();

      expect(service['routerSubscription'].unsubscribe).toHaveBeenCalled();
    });

    it('should redirect from splash if configured to not show splash page', () => {
      const navigationInfo = [{url: '/qe/questions', urlAfterRedirects: '/qe/questions'}, {url: '/qe/splash'}];
      (<any>service).qeData = {baseQuiz: {quizConfiguration: {showSplashPage: false}, firstAnsweredQuestion: <any>{success: true}}};

      service['handleAdditionalNavigatingForSplashAndQuestionPages'](navigationInfo);

      expect(locationService.back).toHaveBeenCalledTimes(1);
    });

    it('should not redirect from splash page if it is configured', () => {
      const navigationInfo = [{url: '/qe/questions', urlAfterRedirects: '/qe/questions'}, {url: '/qe/splash'}];
      (<any>service).qeData = {baseQuiz: {quizConfiguration: {showSplashPage: true}, firstAnsweredQuestion: <any>{success: true}}};

      service['handleAdditionalNavigatingForSplashAndQuestionPages'](navigationInfo);

      expect(locationService.back).toHaveBeenCalledTimes(0);
    });

    it('shouldn\'t redirect if from questions page to other', () => {
      const navigationInfo = [{url: '/qe/questions', urlAfterRedirects: '/qe/questions'}, {url: '/qe/other'}];
      (<any>service).qeData = {baseQuiz: {quizConfiguration: {showSplashPage: false}, firstAnsweredQuestion: <any>{success: true}}};

      service['handleAdditionalNavigatingForSplashAndQuestionPages'](navigationInfo);

      expect(locationService.back).toHaveBeenCalledTimes(0);
    });

    it('should redirect from questions if quiz already taken', () => {
      const navigationInfo = [{url: '/qe/other', urlAfterRedirects: '/qe/other'}, {url: '/qe/questions'}];
      (<any>service).qeData = {baseQuiz: {quizConfiguration: {showSplashPage: false}, firstAnsweredQuestion: <any>{success: true}}};

      service['handleAdditionalNavigatingForSplashAndQuestionPages'](navigationInfo);

      expect(locationService.back).toHaveBeenCalledTimes(1);
    });

    it('should redirect from questions if came from splash', () => {
      const navigationInfo = [{url: '/qe/splash', urlAfterRedirects: '/qe/splash'}, {url: '/qe/questions'}];
      (<any>service).qeData = {baseQuiz: {quizConfiguration: {showSplashPage: false}, firstAnsweredQuestion: <any>{success: false}}};

      service['handleAdditionalNavigatingForSplashAndQuestionPages'](navigationInfo);

      expect(locationService.back).toHaveBeenCalledTimes(0);
    });

    it('should call http "get" for getQuizHistory from backend', () => {

      quizHistoryModel.live.firstAnsweredQuestion = {
        'id': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
        'text': 'Who will win?',
        'answers': [{
          'id': 'f4a391cb-0dc4-4279-828d-84a78273c4b9',
          'text': '1',
          'correctAnswer': false,
          'questionAskedId': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
          'nextQuestionId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
          'userChoice': false
        }, {
          'id': 'b2d5b7b9-9c6f-45c9-8aeb-a3cb550d6ba9',
          'text': '2',
          'correctAnswer': false,
          'questionAskedId': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
          'nextQuestionId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
          'userChoice': true
        }],
        'questionType': 'SINGLE',
        'nextQuestions': {
          '1fa2682c-937b-4972-90cd-5161e6e83dc6': {
            'id': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
            'text': '447i ',
            'answers': [
              {
                'id': '7b2bb73c-04d9-42b2-be11-e2a723308fe8',
                'text': '2+2',
                'correctAnswer': false,
                'questionAskedId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
                'nextQuestionId': '772ccffc-d07c-4f8d-b7a8-dc4692eae6e4',
                'userChoice': true
              }, {
                'id': '277dc091-21ad-406e-9b6a-39eeae8158b3',
                'text': '4',
                'correctAnswer': false,
                'questionAskedId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
                'nextQuestionId': '772ccffc-d07c-4f8d-b7a8-dc4692eae6e4',
                'userChoice': false
              }],
            'questionType': 'SINGLE',
            'nextQuestions': {},
            'questionDetails': {}
          }
        },
        'questionDetails': {
          'awayTeamName': 'Man Utd',
          'awayTeamSvgFilePath': 'f.svg',
          'channelSvgFilePath': 'd.svg',
          'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
          'homeTeamName': 'Tottenham',
          'homeTeamSvgFilePath': 'img.svg',
          'middleHeader': '12:30',
          'signposting': '',
          'topLeftHeader': 'Champions League',
          'topRightHeader': 'FRI AUG 23'
        }
      };
      service.mapResponseOnComponentModel(quizHistoryModel);

      service.getQuizHistory().subscribe();

      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);

      const noEndPage = {
        ...quizHistoryModel,
        live: {
          ...quizHistoryModel.live,
          endPage: null
        }
      };

      service.mapResponseOnComponentModel(noEndPage);

      expect(noEndPage).toBeDefined();
      expect(service.resolveCtaButtonText).toBeDefined();
    });

    it('should call mapResponseOnComponentModel and return undefined qeData', () => {
      const quizHistoryModelNull = null;
      service.getQuizHistory().subscribe();

      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);
      service.mapResponseOnComponentModel(quizHistoryModelNull);
      expect(pubSubService.publish).toHaveBeenCalled();
      expect(service.qeData).not.toBeDefined();
    });

    it('should map qeData', () => {
      const quizHistoryModelNoLive = {
        ...quizHistoryModel,
        live: null,
        previous: [quizHistoryModel.live, quizHistoryModel.live]
      };
      service.getQuizHistory().subscribe();

      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);
      service.mapResponseOnComponentModel(quizHistoryModelNoLive);

      expect(service.qeData).toBeDefined();
      expect(service.qeData.baseQuiz).toBeDefined();
      expect(service.quizHistoryModel).toBeDefined();

      const quizHistoryModelFull = {
        ...quizHistoryModel,
        previous: [quizHistoryModel.live, quizHistoryModel.live]
      };
      service.getQuizHistory().subscribe();

      expect(http.get).toHaveBeenCalledTimes(2);
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);
      service.mapResponseOnComponentModel(quizHistoryModelFull);

      expect(service.qeData).toBeDefined();
      expect(service.qeData.baseQuiz).toBeDefined();
      expect(service.qeData.previous.length).toEqual(2);
    });

    it('should call mapResponseOnComponentModel and check if firstAnsweredQuestion present', () => {
      service.getQuizHistory().subscribe();

      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);
      quizHistoryModel.live.firstAnsweredQuestion = null;
      quizHistoryModel.live.firstQuestion = {
        'id': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
        'text': 'Who will win?',
        'answers': [
          {
            'id': 'f4a391cb-0dc4-4279-828d-84a78273c4b9',
            'text': '1',
            'correctAnswer': false,
            'questionAskedId': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
            'nextQuestionId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
            'userChoice': false
          }, {
            'id': 'b2d5b7b9-9c6f-45c9-8aeb-a3cb550d6ba9',
            'text': '2',
            'correctAnswer': false,
            'questionAskedId': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
            'nextQuestionId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
            'userChoice': true
          }],
        'questionType': 'SINGLE',
        'nextQuestions': {
          '1fa2682c-937b-4972-90cd-5161e6e83dc6': {
            'id': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
            'text': '447i ',
            'answers': [
              {
                'id': '7b2bb73c-04d9-42b2-be11-e2a723308fe8',
                'text': '2+2',
                'correctAnswer': false,
                'questionAskedId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
                'nextQuestionId': '772ccffc-d07c-4f8d-b7a8-dc4692eae6e4',
                'userChoice': true
              }, {
                'id': '277dc091-21ad-406e-9b6a-39eeae8158b3',
                'text': '4',
                'correctAnswer': false,
                'questionAskedId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
                'nextQuestionId': '772ccffc-d07c-4f8d-b7a8-dc4692eae6e4',
                'userChoice': false
              }],
            'questionType': 'SINGLE',
            'nextQuestions': {},
            'questionDetails': {}
          }
        },
        'questionDetails': {
          'awayTeamName': 'Man Utd',
          'awayTeamSvgFilePath': 'f.svg',
          'channelSvgFilePath': 'd.svg',
          'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
          'homeTeamName': 'Tottenham',
          'homeTeamSvgFilePath': 'img.svg',
          'middleHeader': '12:30',
          'signposting': '',
          'topLeftHeader': 'Champions League',
          'topRightHeader': 'FRI AUG 23'
        }
      };
      service.mapResponseOnComponentModel(quizHistoryModel);
      expect(qeData.baseQuiz.questionsList).toBeDefined();
    });

    it('should call mapResponseOnComponentModel and check if qeQuickLinks present', () => {
      service.getQuizHistory().subscribe();

      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);
      quizHistoryModel.live.qeQuickLinks = null;
      service.mapResponseOnComponentModel(quizHistoryModel);
      expect(qeData.baseQuiz.quickLinks).toBeTruthy();
    });

    it('should call mapResponseOnComponentModel and check if logoSvgFilePath present', () => {
      service.getQuizHistory().subscribe();
      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);
      service.mapResponseOnComponentModel(quizHistoryModel);

      expect(service.qeData.baseQuiz.splashPage.logoSvgUrl).toBeTruthy();
    });

    it('should call mapResponseOnComponentModel and check if footerSvgFilePath present', () => {
      service.getQuizHistory().subscribe();

      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);
      service.mapResponseOnComponentModel(quizHistoryModel);

      expect(service.qeData.baseQuiz.splashPage.footerSvgUrl).toBeTruthy();
    });

    it('should call mapResponseOnComponentModel and check if Splash Page present', () => {
      const myMockQEData = mockQEData;
      myMockQEData.qeData.baseQuiz.splashPage = null;

      service['mapQuizModelService'] = {
        ...mapQuizModelService,
        mapQuizModel: jasmine.createSpy('mapQuizModel').and.returnValue(myMockQEData.qeData.baseQuiz)
      };
      service.resolveCtaButtonText = jasmine.createSpy('resolveCtaButtonText');
      service.mapResponseOnComponentModel(quizHistoryModel);

      expect(service.resolveCtaButtonText).not.toHaveBeenCalled();
    });

    it('should call http "get" for getQuizHistory from backend', () => {
      quizHistoryModel.live.firstQuestion = {
        'id': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
        'text': 'Who will win?',
        'answers': [{
          'id': 'f4a391cb-0dc4-4279-828d-84a78273c4b9',
          'text': '1',
          'correctAnswer': false,
          'questionAskedId': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
          'nextQuestionId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
          'userChoice': false
        }, {
          'id': 'b2d5b7b9-9c6f-45c9-8aeb-a3cb550d6ba9',
          'text': '2',
          'correctAnswer': false,
          'questionAskedId': '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
          'nextQuestionId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
          'userChoice': true
        }],
        'questionType': 'SINGLE',
        'nextQuestions': {
          '1fa2682c-937b-4972-90cd-5161e6e83dc6': {
            'id': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
            'text': '447i ',
            'answers': [{
              'id': '7b2bb73c-04d9-42b2-be11-e2a723308fe8',
              'text': '2+2',
              'correctAnswer': false,
              'questionAskedId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
              'nextQuestionId': '772ccffc-d07c-4f8d-b7a8-dc4692eae6e4',
              'userChoice': true
            }, {
              'id': '277dc091-21ad-406e-9b6a-39eeae8158b3',
              'text': '4',
              'correctAnswer': false,
              'questionAskedId': '1fa2682c-937b-4972-90cd-5161e6e83dc6',
              'nextQuestionId': '772ccffc-d07c-4f8d-b7a8-dc4692eae6e4',
              'userChoice': false
            }],
            'questionType': 'SINGLE',
            'nextQuestions': {},
            'questionDetails': {
              'awayTeamName': 'Man Utd',
              'awayTeamSvgFilePath': 'f.svg',
              'channelSvgFilePath': 'd.svg',
              'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
              'homeTeamName': 'Tottenham',
              'homeTeamSvgFilePath': 'img.svg',
              'middleHeader': '12:30',
              'signposting': '',
              'topLeftHeader': 'Champions League',
              'topRightHeader': 'FRI AUG 23'
            }
          }
        }
      };
      service.mapResponseOnComponentModel(quizHistoryModel);

      service.getQuizHistory().subscribe();
      expect(http.get).toHaveBeenCalledWith(...getRequestParams);
    });

    it('should call getQuizHistory with true param', () => {
      const expected =
        'https://question-engine-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/quiz/history/?source-id=/correct4&previous-limit=3';
      service['doHistoryBackendCall'] = jasmine.createSpy('doHistoryBackendCall');

      service.getQuizHistory(true);

      expect(service['doHistoryBackendCall']).toHaveBeenCalled();
      expect(service['doHistoryBackendCall']).toHaveBeenCalledWith(expected);
    });

    it('should call http "get" for getQuizHistory from backend and return error', fakeAsync(() => {
      http.get.and.returnValue(throwError('error'));
      service.getQuizHistory().subscribe();
      expect(pubSubService.publish).toHaveBeenCalled();
    }));

    it('should call getQuizHistory with `initial=true`', () => {
      service.getQuizHistory().subscribe();
      expect(http.get).toHaveBeenCalled();
    });

    it('should call resetCheckForAnonymousDataValue', () => {
      service.checkForAnonymousData = true;
      service.resetCheckForAnonymousDataValue();
      expect(service.checkForAnonymousData).toBeFalsy();
    });

    it('should call do authentication call to BPP', () => {
      userService.bppToken = null;
      service['userService'] = {
        ...userService,
        bppToken: null
      };

      service.qeData = {
        ...qeData,
        baseQuiz: {
          ...qeData.baseQuiz,
          sourceId: 'correct4'
        }
      };
      service.getQuizHistory().subscribe();
      expect(http.get).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should call do authentication call to BPP and process error', () => {
      userService.bppToken = null;
      http.get.and.returnValue(throwError('error'));
      service['userService'] = {
        ...userService,
        bppToken: null
      };

      service.qeData = {
        ...qeData,
        baseQuiz: {
          ...qeData.baseQuiz,
          sourceId: 'correct4'
        }
      };
      service.getQuizHistory().subscribe();
      expect(http.get).not.toHaveBeenCalled();
    });

    it('should call http "post" for submitting user\'s answer', () => {
      service.submitUserAnswer(userAnswers, true).subscribe();
      expect(http.post).toHaveBeenCalledTimes(1);
      expect(http.post).toHaveBeenCalledWith(
        `${environment.QUESTION_ENGINE_ENDPOINT}/v1/user-answer/`, userAnswers, {
          headers: jasmine.any(HttpHeaders),
        });
    });

    it('should resolve CTA text', () => {
      service.qeData = qeData;
      qeData.baseQuiz.quizLoginRule = 'SUBMIT';
      service.resolveCtaButtonText();
      expect(service.qeData.baseQuiz.splashPage.ctaButtonText).toBeNull();

      qeData.baseQuiz.quizLoginRule = 'START';
      service.resolveCtaButtonText();
      expect(service.qeData.baseQuiz.splashPage.ctaButtonText).toEqual(qeData.baseQuiz.splashPage.loginToViewCTAText);

      userService.status = true;
      qeData.baseQuiz.firstAnsweredQuestion = new class extends Question {};
      service.resolveCtaButtonText();
      expect(service.redirectToTab).toEqual('latest');
      expect(service.qeData.baseQuiz.splashPage.ctaButtonText).toEqual(qeData.baseQuiz.splashPage.seeYourSelectionsCTAText);

      qeData.baseQuiz.firstAnsweredQuestion = null;
      service.resolveCtaButtonText();
      expect(service.redirectToTab).toEqual('previous');
      expect(service.qeData.baseQuiz.splashPage.ctaButtonText).toEqual(qeData.baseQuiz.splashPage.seePreviousSelectionsCTAText);

      const entryDeadlineDate = new Date();
      entryDeadlineDate.setDate(new Date().getDate() + 3);
      qeData.baseQuiz.entryDeadline = entryDeadlineDate;
      service.resolveCtaButtonText();
      //expect(service.qeData.baseQuiz.splashPage.ctaButtonText).toEqual('seePreviousSelectionsCTAText');
      expect(qeData.baseQuiz.splashPage.seePreviousSelectionsCTAText).toEqual('seePreviousSelectionsCTAText')
    });

    describe('Testing `handleNoPrevGamesContent` method', () => {
      it('should return `No Content` message for `Latest tab`', () => {
        service.qeData = qeData;
        expect(service.handleNoPrevGamesContent('latest')).toEqual({
          title: 'Latest title',
          subtitle: 'subtitle'
        });
      });

      it('should return `No Content` message for `Previous tab`', () => {
        service.qeData = qeData;
        expect(service.handleNoPrevGamesContent('previous')).toEqual({
          title: 'Previous title',
          subtitle: 'subtitle'
        });
      });

      it('should return default `No Content` message for `Latest tab`', () => {
        service.qeData = {
          ...qeData,
          baseQuiz: {
            ...qeData.baseQuiz,
            resultsPage: {
              ...qeData.baseQuiz.resultsPage,
              noLatestRoundMessage: ''
            }
          }
        };
        expect(service.handleNoPrevGamesContent('latest')).toEqual({
          title: 'No content',
          subtitle: 'No content'
        });
      });
    });

    it('should update `qeSubmited` value', () => {
      service.setQESubmitStatus(true);
      expect(service.qeSubmittedThisSession).toEqual(true);
    });
  });

  describe('Testing `checkPreviousPage` method', () => {
    it('should return updated value', () => {
      service.qeData = {
        ...qeData,
        baseQuiz: {
          ...qeData.baseQuiz,
          sourceId: 'hello'
        }
      };
      service['previousRoute'] = 'url1';
      service.checkPreviousPage();

      expect(service['previousRoute']).toEqual('/correct4-page');
    });

    it('should return previously defined value', () => {
      service.qeData = {
        ...qeData,
        baseQuiz: {
          ...qeData.baseQuiz,
          sourceId: 'correct4'
        }
      };
      service['previousRoute'] = 'url1';
      service.checkPreviousPage();

      expect(service['previousRoute']).toEqual('url1');
    });

    it('should return previously defined value, source id default', () => {
      service.qeData = {
        ...qeData,
        baseQuiz: {
          ...qeData.baseQuiz,
          sourceId: null
        }
      };

      service['previousRoute'] = '/root-football';
      service.checkPreviousPage();
      expect(service['previousRoute']).toEqual('/root-football');
    });
  });

  describe('Testing `setQEDataUptodateStatus` method', () => {
    it('should change class property value', () => {
      expect(service.dataIsUpToDate).toEqual(true);
      service.setQEDataUptodateStatus(false);
      expect(service.dataIsUpToDate).toEqual(false);
    });
  });

  describe('Testing `checkGameData` method', () => {
    const spyCB = jasmine.createSpy('spyCB');
    it('should DO call callback, live=null, previous=[]', () => {
      const data = {
        previousCount: 3,
        live: null,
        previous: []
      };
      service.checkGameData(data, spyCB);
      expect(spyCB).toHaveBeenCalledTimes(1);
    });

    it('should NOT call callback, live={quiz}, previous=[{quiz}]', () => {
      const spyCB1 = jasmine.createSpy('spyCB1');
      service.checkGameData(quizHistoryModel, spyCB1);
      expect(spyCB1).toHaveBeenCalledTimes(0);
    });

    it('should call triggerFatalError', () => {
      const spyCB2 = jasmine.createSpy('spyCB2');
      const data = {
        previousCount: 0,
        live: null,
        previous: []
      };
      service.triggerFatalError = jasmine.createSpy('triggerFatalError').and.returnValue(QE_INIT_DATA_FAILURE);
      service['checkForAnonymousData'] = true;
      service.checkGameData(data, spyCB2);

      expect(service.triggerFatalError).toHaveBeenCalled();
    });
  });

  it('addToSlipHandler', () => {
    service.addToSlipHandler('1');
    expect(commandService.executeAsync).toHaveBeenCalledWith(commandApi.ADD_TO_BETSLIP_BY_OUTCOME_IDS, ['1']);
  });

  describe('Testing `getPrevQuizes` method', () => {
    it('should call http get getUserPrevQuizBackendURL method', () => {
      service.getPrevQuizes(pageNumber, pageSize);

      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(
        `${environment.QUESTION_ENGINE_ENDPOINT}/v1/quiz/previous/${userService.username}/?source-id=${sourceId}` +
        `&page-number=${pageNumber}&page-size=${pageSize}`, {
          observe: 'response',
          responseType: 'json',
          headers: jasmine.any(HttpHeaders),
        });
    });

    it('should not call http get getUserPrevQuizBackendURL method when params are undefined ', () => {
      service['getUserPrevQuizBackendURL'](undefined, undefined);

      expect(http.get).not.toHaveBeenCalled();
    });

    it('should Not call http get getUserPrevQuizBackendURL method', () => {
      service['userService'] = {
        ...userService,
        username: null
      };
      service.getPrevQuizes(0, pageSize);

      expect(http.get).not.toHaveBeenCalled();
    });
  });

  describe('Testing `mapPrevQuizzesResponseOnComponentModel` method', () => {
    it('should not call method when no prevQuizModel', () => {
      const qePrevQuizData = null;
      service.getPrevQuizes(pageNumber, pageSize);

      expect(service.mapPrevQuizzesResponseOnComponentModel(qePrevQuizData)).toEqual(qePrevQuizData);
    });

    it('should not call method when there are no quizzes', () => {
      const qePrevQuizData = {
        totalRecords: 0,
        quizzes: []
      };
      service.getPrevQuizes(pageNumber, pageSize);

      expect(service.mapPrevQuizzesResponseOnComponentModel(qePrevQuizData)).toEqual(null);
    });

    it('should call method for prevQuizzes', () => {
      const prevQuizzes = {
        totalRecords: 2,
        quizzes: prevQuizModel.quizzes
      };
      service.getPrevQuizes(pageNumber, pageSize);
      expect((service.mapPrevQuizzesResponseOnComponentModel(prevQuizzes) as any).length).toEqual(2);
    });
  });

  describe('Test functions for Google Analytics', () => {
    it('should call for trackPageViewGA() function', () => {
      const pageURL = '/correct4/url';
      service['trackPageViewGA'](pageURL);

      expect(gtmService.push).toHaveBeenCalledWith('trackPageview', {
        virtualUrl: pageURL
      });
    });

    it('should call for trackEventGA() function with all params', () => {
      service.qeData = qeData;
      service['trackEventGA']('eventAction', 'eventLabel');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: service.titleFormatForGA(qeData.baseQuiz.sourceId),
        eventAction: 'eventAction',
        eventLabel: 'eventLabel'
      });
    });

    it('should call for trackEvent() function without eventLabel param', () => {
      service.qeData = qeData;
      service['trackEventGA']('eventAction');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: service.titleFormatForGA(qeData.baseQuiz.sourceId),
        eventAction: 'eventAction',
        eventLabel: 'none'
      });
    });

    it('should call for trackEvent() function when titleFormatForGA() return empty string ', () => {
      service.qeData = qeData;
      service.qeData.baseQuiz.sourceId = null;
      service['trackEventGA']('eventAction');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: '',
        eventAction: 'eventAction',
        eventLabel: 'none'
      });
    });
  });

  describe('Testing authenticate', () => {
    it('should re-throw err', fakeAsync(() => {
      service['commandService'] = {
        ...commandService,
        API: commandApi,
        executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.reject({
          error: 'err msg'
        }))
      };
      service['authenticate']().subscribe(
        () => {},
        (error) => {}
      );
      tick();
      expect(service['authenticate']).toThrow();
    }));

    it('submitUserAnswer should retry if 401 response status', fakeAsync(() => {
      const unauthorizedError = new HttpErrorResponse({
        error: {
          reason: 'UNAUTHORIZED'
        },
        status: 401,
        statusText: 'UNAUTHORIZED'
      });

      http.post = jasmine.createSpy('post').and
        .returnValues(
          observableThrowError(unauthorizedError),
          observableOf({
            body: userAnswers
          })
        );

      customServiceForSubmitErrors['authenticate'] = jasmine.createSpy('authenticate')
        .and
        .returnValue(observableOf(new HttpHeaders({token: 'super-secret'})));

      customServiceForSubmitErrors
        .submitUserAnswer(userAnswers, false)
        .subscribe(response => expect(response.body).toEqual(userAnswers));

      expect(http.post).toHaveBeenCalledTimes(2);
      expect(http.post).toHaveBeenCalledWith(
        `${environment.QUESTION_ENGINE_ENDPOINT}/v1/user-answer/`, userAnswers, {
          headers: jasmine.any(HttpHeaders),
        });
      tick();
    }));

    it('isUserAnswerExist should retry if 401 response status', fakeAsync(() => {
      const unauthorizedError = new HttpErrorResponse({
        error: {
          reason: 'UNAUTHORIZED'
        },
        status: 401,
        statusText: 'UNAUTHORIZED'
      });

      http.get = jasmine.createSpy('get').and
        .returnValues(
          observableThrowError(unauthorizedError),
          observableOf({
            body: false
          })
        );

      customServiceForSubmitErrors['authenticate'] = jasmine.createSpy('authenticate')
        .and
        .returnValue(observableOf(new HttpHeaders({token: 'super-secret'})));

      customServiceForSubmitErrors['isUserAnswerExist']('url')
        .subscribe(response => expect(response).toBeFalsy());

      expect(http.get).toHaveBeenCalledTimes(2);
      expect(http.get).toHaveBeenCalledWith(
        'url', {
          headers: jasmine.any(HttpHeaders),
          observe: 'response'
        });
      tick();
    }));

    it('doHistoryBackendCall should retry if 401 response status', fakeAsync(() => {
      const unauthorizedError = new HttpErrorResponse({
        error: {
          reason: 'UNAUTHORIZED'
        },
        status: 401,
        statusText: 'UNAUTHORIZED'
      });

      http.get = jasmine.createSpy('get').and
        .returnValues(
          observableThrowError(unauthorizedError),
          observableOf({
            body: quizHistoryModel
          })
        );

      customServiceForSubmitErrors['authenticate'] = jasmine.createSpy('authenticate')
        .and
        .returnValue(observableOf(new HttpHeaders({token: 'super-secret'})));

      customServiceForSubmitErrors['doHistoryBackendCall']('url')
        .subscribe(data => expect(data).toBe(quizHistoryModel));

      expect(http.get).toHaveBeenCalledTimes(2);
      expect(http.get).toHaveBeenCalledWith(
        'url', {
          headers: jasmine.any(HttpHeaders),
          observe: 'response',
          responseType: 'json',
        });
      tick();
    }));
  });

  describe('Testing `checkIfShouldRedirectGuest` method', () => {
    it('should redirect GUEST to splash page', () => {
      service['userService'] = {
        ...userService,
        status: false
      };

      service.mapResponseOnComponentModel(quizHistoryModel);
      service.checkIfShouldRedirectGuest();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/qe/correct4');
    });
    it('should redirect GUEST to app root', () => {
        service['userService'] = {
        ...userService,
        status: false
      };
        service.checkIfShouldRedirectGuest();
        expect(router.navigateByUrl).toHaveBeenCalledWith('/');
      });
    it('should NOT redirect InShop USER to splash page', () => {
        service['userService'] = {
        ...userService,
        status: true
      };
        service.checkIfShouldRedirectGuest();
        expect(router.navigateByUrl).not.toHaveBeenCalled();
        expect(service.checkIfShouldRedirectGuest()).not.toBeTruthy();
      });
  });

  describe('Testing `resolvePath()` method', () => {
    it('should work for`correct4`', () => {
      service['router'] = {
        ...router,
        navigateByUrl: jasmine.createSpy(),
        url: '/footballsuperseries'
      };

      expect(service.resolvePath('/footballsuperseries')).toEqual('/footballsuperseries');
      expect(service.sourceIdFromParams).toEqual('footballsuperseries');
    });

    it('should work for`cashv3`', () => {
      service['router'] = {
        ...router,
        navigateByUrl: jasmine.createSpy(),
        url: 'qe/cash_v3/splash'
      };

      expect(service.resolvePath('/cash_v3')).toEqual('/qe/cash_v3');
    });
  });

  describe('Testing toggleSubmitNotification', () => {
    it('should set up value to showSubmitNotification', () => {
      service.toggleSubmitNotification(true);

      expect(service.showSubmitNotification).toBeTruthy();

      service.toggleSubmitNotification(false);

      expect(service.showSubmitNotification).toBeFalsy();
    });
  });

  describe('isUserAnswerExist', () => {
    const url = 'url';

    beforeEach(() => {
      service['getAuthenticationHeader'] = jasmine.createSpy('getAuthenticationHeader')
        .and.returnValue(new HttpHeaders({
          token: service['userService'].bppToken
        }));
    });

    it('should send get http query to check if is user answer', () => {
      service['getAuthenticationHeader'] = jasmine.createSpy('getAuthenticationHeader').and.returnValue(new HttpHeaders({
        token: service['userService'].bppToken
      }));
      service['http'].get = jasmine.createSpy('get').and.returnValue(of(false));
      service['isUserAnswerExist'](url).subscribe();

      expect(service['http'].get).toHaveBeenCalled();
      expect(service['getAuthenticationHeader']).toHaveBeenCalled();

      expect(service['http'].get).toHaveBeenCalledWith(url, {
        headers: service['getAuthenticationHeader'](),
        observe: 'response' as any
      });
    });

    it('should send get http query to check if is user answer', () => {
      const response = new HttpResponse({body: true});

      service['http'].get = jasmine.createSpy('get').and.returnValue(of(response));

      service['isUserAnswerExist'](url).subscribe();

      expect(service['http'].get).toHaveBeenCalled();
      expect(service['getAuthenticationHeader']).toHaveBeenCalled();
    });

    it('should send get http query to check if is user answer', () => {
      const errorResponse = new HttpErrorResponse({status: 500});
      customServiceForSubmitErrors['http'].get = jasmine.createSpy('get').and.returnValue(observableThrowError(errorResponse));

      customServiceForSubmitErrors['isUserAnswerExist'](url).subscribe(() => {}, (error) => {});

      expect(customServiceForSubmitErrors['http'].get).toHaveBeenCalled();
      expect(customServiceForSubmitErrors['isUserAnswerExist']).toThrow();
    });
  });

  describe('userAnswersExist', () => {
    it('should call isUserAnswerExist is user is logged in', () => {
      service['isUserAnswerExist'] = jasmine.createSpy('isUserAnswerExist').and.returnValue(of(true));
      service['getAuthenticationHeader'] = jasmine.createSpy('getAuthenticationHeader').and.returnValue(new HttpHeaders({
        token: service['userService'].bppToken
      }));

      service['userAnswersExist']('username', 'quizId').subscribe();

      expect(service['isUserAnswerExist']).toHaveBeenCalled();
    });

    it('should not call isUserAnswerExist if user is not logged in', () => {
      service['getAuthenticationHeader'] = jasmine.createSpy('getAuthenticationHeader').and.returnValue(null);
      service['isUserAnswerExist'] = jasmine.createSpy('isUserAnswerExist').and.returnValue(of(true));

      service['userAnswersExist']('username', 'quizId').subscribe();

      expect(service['isUserAnswerExist']).not.toHaveBeenCalled();
    });

    it('should check isUserAnswerExist if commandService return response', fakeAsync( () => {
      const quizId = 'quizId';
      const url = `${`${environment.QUESTION_ENGINE_ENDPOINT}/v2/user-answer/`}${userService.username}/${quizId}/exists`;
      service['isUserAnswerExist'] = jasmine.createSpy('isUserAnswerExist').and.returnValue(of({}));
      service['getAuthenticationHeader'] = jasmine.createSpy('getAuthenticationHeader').and.returnValue(null);
      service['commandService'].executeAsync = jasmine.createSpy('executeAsync')
        .and.returnValue(Promise.resolve(true));

      service['userAnswersExist'](userService.username, quizId).subscribe(() => {
        expect(service['isUserAnswerExist']).toHaveBeenCalled();
        expect(service['isUserAnswerExist']).toHaveBeenCalledWith(url);
      });

      tick();
    }));

    it('should catch err if commandService return error', fakeAsync( () => {
      service['isUserAnswerExist'] = jasmine.createSpy('isUserAnswerExist').and.returnValue(of({}));
      service['getAuthenticationHeader'] = jasmine.createSpy('getAuthenticationHeader').and.returnValue(null);
      service['commandService'].executeAsync = jasmine.createSpy('executeAsync')
        .and.returnValue(Promise.reject({ error: 'err msg' }));

      service['userAnswersExist'](userService.username, 'quizId').subscribe(() => {}, () => {
        expect(service['isUserAnswerExist']).not.toHaveBeenCalled();
      });

      tick();
    }));
  });
});
