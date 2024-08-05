import { MapQuizModelService } from '@app/questionEngine/services/question-engine/mapQuizModel.service';
import { upsellItemDynamic, upsellItemDefault } from '@app/questionEngine/services/qe-mock-data.mock';

describe('MapQuizModelService', () => {
  let service: MapQuizModelService;

  let domSanitizer;
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
      'displayTo':  '',
      'entryDeadline':  '',
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
        'showPreviousGamesButton':false
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
      upsell: {
        dynamicUpsellOptions: {
          'b2d5b7b9-9c6f-45c9-8aeb-a3cb550d6ba9;7b2bb73c-04d9-42b2-be11-e2a723308fe8': upsellItemDynamic
        },
        defaultUpsellOption: upsellItemDefault,
        fallbackImagePath: 'some/source.png'
      }
    },
    'previous': [],
  };

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

  beforeEach(() => {
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue('htmlMarkup'),
      sanitize: jasmine.createSpy('sanitize').and.returnValue(''),
    };
    service = new MapQuizModelService(domSanitizer);
  });

  describe('', () => {

    it('should init component', () => {
      expect(service).toBeTruthy();
    });

    it('should transform data', () => {
      expect(service.mapQuizModel(quizHistoryModel.live).questionsList.length).toEqual(2);
    });

    it('should transform data with `Dynamic` upsell Data', () => {
      expect(service.mapQuizModel(quizHistoryModel.live).resultsPage.upsell.selectionName).toEqual('some dynamic upsell');
    });

    it('should transform data with `Generic` upsell Data', () => {
      const myQuizHistoryModel = {
        ...quizHistoryModel,
        live: {
          ...quizHistoryModel.live,
          upsell: {
            dynamicUpsellOptions: {
              'intentionally-wrong-id;7b2bb73c-04d9-42b2-be11-e2a723308fe8': upsellItemDynamic
            },
            defaultUpsellOption: upsellItemDefault,
            fallbackImagePath: 'some/source.png'
          }
        }
      };
      expect(service.mapQuizModel(myQuizHistoryModel.live).resultsPage.upsell.selectionName).toEqual('some generic upsell');
    });

    it('should transform data with `Generic` upsell Data', () => {
      const myQuizHistoryModel = {
        ...quizHistoryModel,
        live: {
          ...quizHistoryModel.live,
          upsell: {
            defaultUpsellOption: upsellItemDefault,
            fallbackImagePath: 'some/source.png'
          }
        }
      };
      expect(service.mapQuizModel(myQuizHistoryModel.live).resultsPage.upsell.selectionName).toEqual('some generic upsell');
    });

    it('should NOT transform data for upsell Data', () => {
      const myQuizHistoryModel = {
        ...quizHistoryModel,
        live: {
          ...quizHistoryModel.live,
          upsell: null
        }
      };
      expect(service.mapQuizModel(myQuizHistoryModel.live).resultsPage.upsell).not.toBeDefined();
    });

    it('should transform data with extra without upsell Data', () => {
      expect(service.mapQuizModel(quizHistoryModel.live).resultsPage.upsell.selectionName).toEqual('some dynamic upsell');
    });

    it('should transform data with extra conditions', () => {
      quizHistoryModel.live.splashPage.footerSvgFilePath = '';
      quizHistoryModel.live.splashPage.logoSvgFilePath = null;
      quizHistoryModel.live.endPage = null;
      quizHistoryModel.live.qeQuickLinks = null;
      expect(service.mapQuizModel(quizHistoryModel.live).resultsPage).toEqual(null);
      expect(service.mapQuizModel(quizHistoryModel.live).quickLinks).toEqual([]);
      expect(service.mapQuizModel(quizHistoryModel.live).splashPage.logoSvgFilePath).toEqual(null);
    });
  });

  describe('Testing Upsell transform methods', () => {
    it('should find all combination by `answersIdsCombineHandler` method', () => {
      const input = ['aa11', 'aa22', 'bb11', 'bb22'];
      const output = [ 'aa11;aa22', 'aa11;bb11', 'aa11;bb22', 'aa22;bb11', 'aa22;bb22', 'bb11;bb22' ];
      expect(service['answersIdsCombineHandler'](input)).toEqual(output);
    });
  });

  it('should set `splashPage` strapline to empty string', () => {
    quizHistoryModel.live.splashPage.strapLine = null;
    expect(service.mapQuizModel(quizHistoryModel.live).splashPage.strapLine).toEqual('');
  });

  it('should set bg image data', () => {
    quizHistoryModel.live.splashPage.backgroundSvgFilePath = '/some/url';
    service['cmsUrl'] = '/fake-cms';
    expect(service.mapQuizModel(quizHistoryModel.live).backgroundSvgUrl)
      .toEqual('/fake-cms/some/url');
  });

  it('should NOT set bg image data', () => {
    quizHistoryModel.live.splashPage.backgroundSvgFilePath = null;
    expect(service.mapQuizModel(quizHistoryModel.live).backgroundSvgUrl).toEqual(null);
  });

  it('should not traverse `splashPage` data', () => {
    const myQuizHistoryModel = {
      ...quizHistoryModel
    };
    myQuizHistoryModel.live.splashPage = null;
    expect(service.mapQuizModel(myQuizHistoryModel.live).splashPage).toEqual(undefined);
  });

  it('should not traverse `defaultQuestionsDetails` data', () => {
    const myQuizHistoryModel = {
      ...quizHistoryModel,
    };
    myQuizHistoryModel.live.defaultQuestionsDetails = null;
    expect(service.mapQuizModel(myQuizHistoryModel.live).defaultQuestionsDetails).toEqual(undefined);
  });
});
