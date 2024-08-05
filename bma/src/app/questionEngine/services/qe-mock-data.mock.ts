import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { QuestionEngineSplashPageModel } from '@app/questionEngine/models/questionEngineSplashPage.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { QuestionEngineResultsPageModel } from '@app/questionEngine/models/questionEngineResultsPage.model';

export const upsellItemDynamic = {
  fallbackImagePath: undefined,
  marketName: 'Match Betting',
  price: 2,
  priceDen: 1,
  priceNum: 1,
  selectionId: 546121881,
  selectionName: 'some dynamic upsell',
};

export const upsellItemDefault = {
  fallbackImagePath: '/src/some/image.png',
  imageUrl: 'www.google.com',
  marketName: 'Match Betting',
  price: 2,
  priceDen: 1,
  priceNum: 1,
  selectionId: 546121881,
  selectionName: 'some generic upsell',
};

export class QEData {
  public qeData = new QuestionEngineModel();

  constructor() {
    this.qeData.baseQuiz = new QuestionEngineQuizModel();
    this.qeData.baseQuiz.splashPage = new QuestionEngineSplashPageModel(
      'testStrapLine',
      'paragraphText1',
      'paragraphText2',
      'paragraphText3',
      'footertext',
      'logoSvgPath',
      'logoSvgUrl',
      'footerSvgPath',
      'footerSvgUrl',
      'textBtn',
      'loginToViewCTAText',
      'playForFreeCTAText',
      'seePreviousSelectionsCTAText',
      'seeYourSelectionsCTAText',
      'backgroundSvgFilePath',
      false
    );
    this.qeData.baseQuiz.resultsPage = new QuestionEngineResultsPageModel({
      backgroundSvgImagePath: 'string',
      gameDescription: 'string',
      noLatestRoundMessage: 'title.subtitle',
      noPreviousRoundMessage: 'string',
      showAnswersSummary: true,
      showPrizes: false,
      showResults: true,
      showUpsell: false,
      submitMessage: 'string',
      title: 'string',
      upsellAddToBetslipCtaText: 'string',
      upsellBetInPlayCtaText: 'string',
      submitCta: 'Let`s go!',
    }, upsellItemDynamic);
    this.qeData.baseQuiz.quizConfiguration = {
      showSubmitPopup: true,
      showExitPopup: true,
      showSplashPage: true,
      showEventDetails: true,
      showProgressBar: true,
      showQuestionNumbering: true,
      showSwipeTutorial: true,
      useBackButtonToExitAndHideXButton: true,
      showPreviousAndLatestTabs: true
    };
    this.qeData.baseQuiz.quickLinks = [];
    this.qeData.baseQuiz.questionsList = [];
    this.qeData.baseQuiz.entryDeadline = new Date();
    this.qeData.baseQuiz.firstAnsweredQuestion = null;
    this.qeData.baseQuiz.defaultQuestionsDetails = {
      awayTeamName: 'Man Utd',
      awayTeamSvgFilePath: 'f.svg',
      channelSvgFilePath: 'd.svg',
      description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
      homeTeamName: 'Tottenham',
      homeTeamSvgFilePath: 'img.svg',
      middleHeader: '12:30',
      signposting: '',
      topLeftHeader: 'FRI AUG 231',
      topRightHeader: 'FRI AUG 23'
    };
    this.qeData.baseQuiz.firstQuestion = null;
    this.qeData.baseQuiz.id = 'testId';

    this.qeData.baseQuiz.sourceId = '/correct4';

    this.qeData.baseQuiz.quizLoginRule = 'START';

    this.qeData.baseQuiz.correctAnswersPrizes = [{
      requiredCorrectAnswers: 1,
      amount: 1,
      currency: '$',
      prizeType: 'type'
    }];
    this.qeData.baseQuiz.eventDetails = {
      eventId: '10050712',
      eventName: 'Man Unt vs Lviv',
      startTime: '2019-10-16T13:18:00Z',
      actualScores: [
        1,
        2
      ],
      liveNow: false
    };

    this.qeData.previous = [new QuestionEngineQuizModel()];
    this.qeData.previousCount = 13;
  }
}


export const questionItem = {
  id: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
  text: 'Who will win?',
  questionType: 'SINGLE',
  questionDetails: {
    topLeftHeader: 'City1',
    topRightHeader: 'United2',
    middleHeader: 'middle3',
    homeTeamName: '87678678',
    homeTeamSvgFilePath: '/images/uploads/questionDetails/6fb0129f-7342-40ae-9d13-fc7f5f134150.svg',
    awayTeamName: '8767878678',
    channelSvgFilePath: '/images/uploads/questionDetails/604b8624-01bf-4281-8854-6cbb5db93a41.svg',
    awayTeamSvgFilePath: '/images/uploads/questionDetails/b4a16940-8976-405e-8e5d-632a345ba88e.svg',
    signposting: 'QUESTION 11 OF 44',
    description: 'new'
  },
  answers: [
    {
      id: 'f48f1116-d00e-4559-ae54-82315b66a2ee',
      text: 'Tottenham',
      correctAnswer: false,
      questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
      nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
      userChoice: false
    },
    {
      id: '898a2af1-eaae-4c41-9718-54b6c0e28a32',
      text: 'Draw',
      correctAnswer: true,
      questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
      nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
      userChoice: true
    },
    {
      id: '633cca3c-69cd-404d-8c17-ef95eb5416c0',
      text: 'Man Utd',
      correctAnswer: false,
      questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
      nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78',
      userChoice: false
    }
  ],
  nextQuestions: null
};

export const quizItem = {
  sourceId: '/correct4',
  previousCount: 2,
  live: {
    id: '5daacf02c9e77c00014281a9',
    sourceId: '/correct4',
    displayFrom: '2019-10-16T20:15:00Z',
    displayTo: '2019-10-22T09:15:00Z',
    entryDeadline: '2019-10-21T11:15:00Z',
    title: 'DEMO_DUPLICATE_3',
    firstAnsweredQuestion: questionItem,
    splashPage: {
      title: 'DEMO_SP',
      strapLine: 'Win with Correct 4! Psum dolor sit amet, consectetur adipis elit, sed do eiusmod tempor incididunt!',
      paragraphText1: '<h2>bla bla</h2>',
      paragraphText2: '<h2>bla bla</h2>',
      paragraphText3: '<h2>bla bla</h2>',
      playForFreeCTAText: 'Play now for free',
      seePreviousSelectionsCTAText: 'See previous games',
      seeYourSelectionsCTAText: 'See your selections',
      loginToViewCTAText: 'Login to view',
      backgroundSvgFilePath: '',
      backgroundSvgFilename: '',
      logoSvgFilePath: '/images/uploads/quizSplashPage/d0c41af1-1af2-44b4-9dad-249a3ebc3036.svg',
      logoSvgFilename: 'fantastic.svg',
      footerSvgFilename: 'group-4.svg',
      footerSvgFilePath: '/images/uploads/quizSplashPage/0de9ddf3-aa43-4f97-bb29-63665631b2c8.svg',
      footerText: '18+. UK+IRE Online & Mobile Coral customers only. T&Cs apply.'
    },
    qeQuickLinks: {
      title: 'DEMO_QL',
      links: [
        {
          title: 'Prizes',
          relativePath: 'prizes',
          description: '<h2>bla bla</h2>'
        },
        {
          title: 'Frequently Asked Questions',
          relativePath: 'faq',
          description: '<h2>bla bla</h2>'
        },
        {
          title: 'Terms & Conditions',
          relativePath: 'terms',
          description: '<h2>bla bla</h2>'
        }
      ]
    },
    quizLoginRule: 'START',
    quizLogoSvgFilePath: '/images/uploads/questionDetails/75dc7300-c94a-4c61-a397-a51ea41298d4.svg',
    quizBackgroundSvgFilePath: '/images/uploads/questionDetails/dfaf7b28-3ba7-4390-bea7-d61922456bad.svg',
    defaultQuestionsDetails: {
      topLeftHeader: 'Champions League Dup3',
      topRightHeader: 'FRI AUG 23',
      middleHeader: '12:30',
      homeTeamName: 'Tottenham Dup3',
      homeTeamSvgFilePath: '/images/uploads/questionDetails/fd36d916-0f60-4870-a09e-2d11f5e899fa.svg',
      awayTeamName: 'Man Utd Dup3',
      channelSvgFilePath: '/images/uploads/questionDetails/1a333ce8-eab1-43d0-be06-54444a4f14ad.svg',
      awayTeamSvgFilePath: '/images/uploads/questionDetails/c5bd2fae-3538-44f7-8e44-4c6daf99174f.svg',
      signposting: 'Signposting DEFAULT',
      description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.'
    },
    endPage: {
      title: 'DEMO_EP',
      backgroundSvgImagePath: '/images/uploads/quizEndPage/df1b09ed-578f-47c1-83b4-1c3f457f8452.svg',
      gameDescription: 'Game descriptions',
      submitMessage: 'Thank you for completing our survey Sofia',
      upsellBetInPlayCtaText: 'Bet now!',
      noLatestRoundMessage: 'No latest rounds. Come back next week for the next round',
      noPreviousRoundMessage: 'No Previous games',
      upsellAddToBetslipCtaText: 'Add to Betslip!',
      showUpsell: true,
      showAnswersSummary: true,
      showResults: true,
      showPrizes: true,
      submitCta: 'Let`s go!'
    },
    submitPopup: {
      iconSvgPath: '/images/uploads/questionDetails/77f5ca6e-609a-4f19-a883-eceb1c8a03b6.svg',
      header: 'Confirm your selections!',
      description: 'Don’t forget your selections are final once  you hit submit',
      submitCTAText: 'SUBMIT',
      closeCTAText: 'Go back and edit'
    },
    exitPopup: {
      iconSvgPath: '/images/uploads/questionDetails/4c3b7bee-177d-463c-bfc3-43149622ff6b.svg',
      header: 'Are you sure?',
      description: 'Your selections will not be saved if you exit  without submitting them',
      submitCTAText: 'KEEP PLAYING',
      closeCTAText: 'EXIT GAME'
    },
    correctAnswersPrizes: [
      {
        requiredCorrectAnswers: 1,
        amount: 100,
        currency: '£',
        prizeType: ''
      },
      {
        requiredCorrectAnswers: 2,
        amount: 200,
        currency: '£',
        prizeType: ''
      }
    ],
    eventDetails: {
      eventId: '',
      eventName: '',
      startTime: '',
      actualScores: [
        200000000,
        200
      ],
      liveNow:  false
    },
    firstQuestion: {
      id: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
      text: 'Who will win?',
      questionType: 'SINGLE',
      questionDetails : {
        topLeftHeader: 'City1',
        topRightHeader: 'United2',
        middleHeader: 'middle3',
        homeTeamName: '87678678',
        homeTeamSvgFilePath: '/images/uploads/questionDetails/6fb0129f-7342-40ae-9d13-fc7f5f134150.svg',
        awayTeamName: '8767878678',
        channelSvgFilePath: '/images/uploads/questionDetails/604b8624-01bf-4281-8854-6cbb5db93a41.svg',
        awayTeamSvgFilePath: '/images/uploads/questionDetails/b4a16940-8976-405e-8e5d-632a345ba88e.svg',
        signposting: 'QUESTION 11 OF 44',
        description: 'new'
      },
      answers: [
        {
          id: 'f48f1116-d00e-4559-ae54-82315b66a2ee',
          userChoice: false,
          text: 'Tottenham',
          correctAnswer: false,
          questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
          nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
        },
        {
          id: '898a2af1-eaae-4c41-9718-54b6c0e28a32',
          userChoice: false,
          text: 'Draw',
          correctAnswer: false,
          questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
          nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
        },
        {
          id: '633cca3c-69cd-404d-8c17-ef95eb5416c0',
          userChoice: false,
          text: 'Man Utd',
          correctAnswer: true,
          questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
          nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
        }
      ],
      nextQuestions: null
    }
  },
  previous: []
};

export const prevQuizModel = {
  totalRecords: 2,
  quizzes: [
    {
      id: '5daacf02c9e77c00014281a9',
      sourceId: '/correct4',
      displayFrom: '2019-10-16T20:15:00Z',
      displayTo: '2019-10-22T09:15:00Z',
      entryDeadline: '2019-10-21T11:15:00Z',
      title: 'DEMO_DUPLICATE_3',
      firstAnsweredQuestion: questionItem,
      splashPage: {
        title: 'DEMO_SP',
        strapLine: 'Win with Correct 4! Psum dolor sit amet, consectetur adipis elit, sed do eiusmod tempor incididunt!',
        paragraphText1: '<h2>bla bla</h2>',
        paragraphText2: '<h2>bla bla</h2>',
        paragraphText3: '<h2>bla bla</h2>',
        playForFreeCTAText: 'Play now for free',
        seePreviousSelectionsCTAText: 'See previous games',
        seeYourSelectionsCTAText: 'See your selections',
        loginToViewCTAText: 'Login to view',
        backgroundSvgFilePath: '',
        backgroundSvgFilename: '',
        logoSvgFilePath: '/images/uploads/quizSplashPage/d0c41af1-1af2-44b4-9dad-249a3ebc3036.svg',
        logoSvgFilename: 'fantastic.svg',
        footerSvgFilename: 'group-4.svg',
        footerSvgFilePath: '/images/uploads/quizSplashPage/0de9ddf3-aa43-4f97-bb29-63665631b2c8.svg',
        footerText: '18+. UK+IRE Online & Mobile Coral customers only. T&Cs apply.',
        showPreviousGamesButton: false
      },
      qeQuickLinks: {
        title: 'DEMO_QL',
        links: [
          {
            title: 'Prizes',
            relativePath: 'prizes',
            description: '<h2>bla bla</h2>'
          },
          {
            title: 'Frequently Asked Questions',
            relativePath: 'faq',
            description: '<h2>bla bla</h2>'
          },
          {
            title: 'Terms & Conditions',
            relativePath: 'terms',
            description: '<h2>bla bla</h2>'
          }
        ]
      },
      quizLoginRule: 'START',
      quizLogoSvgFilePath: '/images/uploads/questionDetails/75dc7300-c94a-4c61-a397-a51ea41298d4.svg',
      quizBackgroundSvgFilePath: '/images/uploads/questionDetails/dfaf7b28-3ba7-4390-bea7-d61922456bad.svg',
      defaultQuestionsDetails: {
        topLeftHeader: 'Champions League Dup3',
        topRightHeader: 'FRI AUG 23',
        middleHeader: '12:30',
        homeTeamName: 'Tottenham Dup3',
        homeTeamSvgFilePath: '/images/uploads/questionDetails/fd36d916-0f60-4870-a09e-2d11f5e899fa.svg',
        awayTeamName: 'Man Utd Dup3',
        channelSvgFilePath: '/images/uploads/questionDetails/1a333ce8-eab1-43d0-be06-54444a4f14ad.svg',
        awayTeamSvgFilePath: '/images/uploads/questionDetails/c5bd2fae-3538-44f7-8e44-4c6daf99174f.svg',
        signposting: 'Signposting DEFAULT',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.'
      },
      endPage: {
        title: 'DEMO_EP',
        backgroundSvgImagePath: '/images/uploads/quizEndPage/df1b09ed-578f-47c1-83b4-1c3f457f8452.svg',
        gameDescription: 'Game descriptions',
        submitMessage: 'Thank you for completing our survey Sofia',
        upsellBetInPlayCtaText: 'Bet now!',
        noLatestRoundMessage: 'No latest rounds. Come back next week for the next round',
        noPreviousRoundMessage: 'No Previous games',
        upsellAddToBetslipCtaText: 'Add to Betslip!',
        showUpsell: true,
        showAnswersSummary: true,
        showResults: true,
        showPrizes: true,
        submitCta: 'Let`s go!'
      },
      submitPopup: {
        iconSvgPath: '/images/uploads/questionDetails/77f5ca6e-609a-4f19-a883-eceb1c8a03b6.svg',
        header: 'Confirm your selections!',
        description: 'Don’t forget your selections are final once  you hit submit',
        submitCTAText: 'SUBMIT',
        closeCTAText: 'Go back and edit'
      },
      exitPopup: {
        iconSvgPath: '/images/uploads/questionDetails/4c3b7bee-177d-463c-bfc3-43149622ff6b.svg',
        header: 'Are you sure?',
        description: 'Your selections will not be saved if you exit  without submitting them',
        submitCTAText: 'KEEP PLAYING',
        closeCTAText: 'EXIT GAME'
      },
      quizConfiguration: {
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
      correctAnswersPrizes: [
        {
          requiredCorrectAnswers: 1,
          amount: 100,
          currency: '£',
          prizeType: ''
        }
      ],
      eventDetails: {
        eventId: '',
        eventName: '',
        startTime: '',
        actualScores: [
          200000000,
          200
        ],
        liveNow:  false
      },
      firstQuestion: {
        id: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
        text: 'Who will win?',
        questionType: 'SINGLE',
        questionDetails : {
          topLeftHeader: 'City1',
          topRightHeader: 'United2',
          middleHeader: 'middle3',
          homeTeamName: '87678678',
          homeTeamSvgFilePath: '/images/uploads/questionDetails/6fb0129f-7342-40ae-9d13-fc7f5f134150.svg',
          awayTeamName: '8767878678',
          channelSvgFilePath: '/images/uploads/questionDetails/604b8624-01bf-4281-8854-6cbb5db93a41.svg',
          awayTeamSvgFilePath: '/images/uploads/questionDetails/b4a16940-8976-405e-8e5d-632a345ba88e.svg',
          signposting: 'QUESTION 11 OF 44',
          description: 'new'
        },
        answers: [
          {
            id: 'f48f1116-d00e-4559-ae54-82315b66a2ee',
            userChoice: false,
            text: 'Tottenham',
            correctAnswer: false,
            questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
            nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
          },
          {
            id: '898a2af1-eaae-4c41-9718-54b6c0e28a32',
            userChoice: false,
            text: 'Draw',
            correctAnswer: false,
            questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
            nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
          },
          {
            id: '633cca3c-69cd-404d-8c17-ef95eb5416c0',
            userChoice: false,
            text: 'Man Utd',
            correctAnswer: true,
            questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
            nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
          }
        ],
        nextQuestions: null
      }
    },
    {
      id: '5daacf02c9e77c00014281a8',
      sourceId: '/correct4',
      displayFrom: '2019-10-16T20:15:00Z',
      displayTo: '2019-10-22T09:15:00Z',
      entryDeadline: '2019-10-21T11:15:00Z',
      title: 'DEMO_DUPLICATE_3',
      firstAnsweredQuestion: questionItem,
      splashPage: {
        title: 'DEMO_SP',
        strapLine: 'Win with Correct 4! Psum dolor sit amet, consectetur adipis elit, sed do eiusmod tempor incididunt!',
        paragraphText1: '<h2>bla bla</h2>',
        paragraphText2: '<h2>bla bla</h2>',
        paragraphText3: '<h2>bla bla</h2>',
        playForFreeCTAText: 'Play now for free',
        seePreviousSelectionsCTAText: 'See previous games',
        seeYourSelectionsCTAText: 'See your selections',
        loginToViewCTAText: 'Login to view',
        backgroundSvgFilePath: '',
        backgroundSvgFilename: '',
        logoSvgFilePath: '/images/uploads/quizSplashPage/d0c41af1-1af2-44b4-9dad-249a3ebc3036.svg',
        logoSvgFilename: 'fantastic.svg',
        footerSvgFilename: 'group-4.svg',
        footerSvgFilePath: '/images/uploads/quizSplashPage/0de9ddf3-aa43-4f97-bb29-63665631b2c8.svg',
        footerText: '18+. UK+IRE Online & Mobile Coral customers only. T&Cs apply.',
        showPreviousGamesButton: false
      },
      qeQuickLinks: {
        title: 'DEMO_QL',
        links: [
          {
            title: 'Prizes',
            relativePath: 'prizes',
            description: '<h2>bla bla</h2>'
          },
          {
            title: 'Frequently Asked Questions',
            relativePath: 'faq',
            description: '<h2>bla bla</h2>'
          },
          {
            title: 'Terms & Conditions',
            relativePath: 'terms',
            description: '<h2>bla bla</h2>'
          }
        ]
      },
      quizLoginRule: 'START',
      quizLogoSvgFilePath: '/images/uploads/questionDetails/75dc7300-c94a-4c61-a397-a51ea41298d4.svg',
      quizBackgroundSvgFilePath: '/images/uploads/questionDetails/dfaf7b28-3ba7-4390-bea7-d61922456bad.svg',
      defaultQuestionsDetails: {
        topLeftHeader: 'Champions League Dup3',
        topRightHeader: 'FRI AUG 23',
        middleHeader: '12:30',
        homeTeamName: 'Tottenham Dup3',
        homeTeamSvgFilePath: '/images/uploads/questionDetails/fd36d916-0f60-4870-a09e-2d11f5e899fa.svg',
        awayTeamName: 'Man Utd Dup3',
        channelSvgFilePath: '/images/uploads/questionDetails/1a333ce8-eab1-43d0-be06-54444a4f14ad.svg',
        awayTeamSvgFilePath: '/images/uploads/questionDetails/c5bd2fae-3538-44f7-8e44-4c6daf99174f.svg',
        signposting: 'Signposting DEFAULT',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.'
      },
      endPage: {
        title: 'DEMO_EP',
        backgroundSvgImagePath: '/images/uploads/quizEndPage/df1b09ed-578f-47c1-83b4-1c3f457f8452.svg',
        gameDescription: 'Game descriptions',
        submitMessage: 'Thank you for completing our survey Sofia',
        upsellBetInPlayCtaText: 'Bet now!',
        noLatestRoundMessage: 'No latest rounds. Come back next week for the next round',
        noPreviousRoundMessage: 'No Previous games',
        upsellAddToBetslipCtaText: 'Add to Betslip!',
        showUpsell: true,
        showAnswersSummary: true,
        showResults: true,
        showPrizes: true,
        submitCta: 'Let`s go!'
      },
      submitPopup: {
        iconSvgPath: '/images/uploads/questionDetails/77f5ca6e-609a-4f19-a883-eceb1c8a03b6.svg',
        header: 'Confirm your selections!',
        description: 'Don’t forget your selections are final once  you hit submit',
        submitCTAText: 'SUBMIT',
        closeCTAText: 'Go back and edit'
      },
      exitPopup: {
        iconSvgPath: '/images/uploads/questionDetails/4c3b7bee-177d-463c-bfc3-43149622ff6b.svg',
        header: 'Are you sure?',
        description: 'Your selections will not be saved if you exit  without submitting them',
        submitCTAText: 'KEEP PLAYING',
        closeCTAText: 'EXIT GAME'
      },
      correctAnswersPrizes: [
        {
          requiredCorrectAnswers: 1,
          amount: 100,
          currency: '£',
          prizeType: ''
        }
      ],
      quizConfiguration: {
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
      eventDetails: {
        eventId: '',
        eventName: '',
        startTime: '',
        actualScores: [
          200000000,
          200
        ],
        liveNow:  false
      },
      firstQuestion: {
        id: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
        text: 'Who will win?',
        questionType: 'SINGLE',
        questionDetails : {
          topLeftHeader: 'City1',
          topRightHeader: 'United2',
          middleHeader: 'middle3',
          homeTeamName: '87678678',
          homeTeamSvgFilePath: '/images/uploads/questionDetails/6fb0129f-7342-40ae-9d13-fc7f5f134150.svg',
          awayTeamName: '8767878678',
          channelSvgFilePath: '/images/uploads/questionDetails/604b8624-01bf-4281-8854-6cbb5db93a41.svg',
          awayTeamSvgFilePath: '/images/uploads/questionDetails/b4a16940-8976-405e-8e5d-632a345ba88e.svg',
          signposting: 'QUESTION 11 OF 44',
          description: 'new'
        },
        answers: [
          {
            id: 'f48f1116-d00e-4559-ae54-82315b66a2ee',
            userChoice: false,
            text: 'Tottenham',
            correctAnswer: false,
            questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
            nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
          },
          {
            id: '898a2af1-eaae-4c41-9718-54b6c0e28a32',
            userChoice: false,
            text: 'Draw',
            correctAnswer: false,
            questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
            nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
          },
          {
            id: '633cca3c-69cd-404d-8c17-ef95eb5416c0',
            userChoice: false,
            text: 'Man Utd',
            correctAnswer: true,
            questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
            nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
          }
        ],
        nextQuestions: null
      }
    },
  ]
};
