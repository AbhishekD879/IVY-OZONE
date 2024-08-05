import { LatestTabComponent } from './latest-tab.component';
import { of } from 'rxjs';
import { QEData, questionItem, upsellItemDynamic, upsellItemDefault } from '../../../../services/qe-mock-data.mock';
import { UpsellItemModel } from '@app/questionEngine/models/upsell.model';
import { QuestionEngineModel } from '@questionEngine/models/questionEngineModel.model';
import { QuestionEngineQuizModel } from '@questionEngine/models/questionEngineQuiz.model';
import { QuestionEngineSplashPageModel } from '@questionEngine/models/questionEngineSplashPage.model';
import { QuestionEngineResultsPageModel } from '@questionEngine/models/questionEngineResultsPage.model';
import { LinksModel } from '@questionEngine/models/links.model';
import { QuestionEngineQuestionDetailsModel } from '@questionEngine/models/questionEngineQuestionDetails.model';
import { QuizPopupModel } from '@questionEngine/models/quizPopup.model';

describe('LatestTabComponent', () => {
  let component: LatestTabComponent;
  let questionEngineService,
    router;
  let qeData;
  beforeEach(() => {
    qeData = new QuestionEngineModel();
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
      submitCta: 'string',
    });

    qeData.baseQuiz.quickLinks = [new LinksModel()];
    qeData.baseQuiz.entryDeadline = new Date();
    qeData.baseQuiz.firstAnsweredQuestion = null;
    qeData.baseQuiz.firstQuestion = null;
    qeData.baseQuiz.id = 'testId';
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
    qeData.baseQuiz.questionsList = [questionItem];
    qeData.baseQuiz.questionsList[0].answers[0] = {
      id: 'f48f1116-d00e-4559-ae54-82315b66a2ee',
      userChoice: false,
      text: 'Tottenham',
      correctAnswer: false,
      questionAskedId: '637f1a4d-fe05-4f5d-9083-d678f4ca8fc1',
      nextQuestionId: '265d6eeb-6cf5-41e2-a5fd-2820f27d6a78'
    };

    questionEngineService = {
      qeData,
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(qeData)),
      resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
      pipe: jasmine.createSpy('pipe'),
      error: jasmine.createSpy('error').and.callThrough(),
      subscribe: jasmine.createSpy('subscribe').and.returnValue(of(qeData)),
      handleNoPrevGamesContent: jasmine.createSpy('handleNoPrevGamesContent').and.returnValue({
        title: 'title',
        subtitle: 'subtitle'
      }),
      trackPageViewGA: () => {}
    };

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue('/correct4/'),
    };

    component = new LatestTabComponent(
      questionEngineService as any, router as any);
    component.qeData = qeData;
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should show `No Previous Game` message', () => {
    const noLatestRoundDataText = {
      title: 'title',
      subtitle: 'subtitle'
    };

    component.ngOnInit();
    expect(component.showNoResultsWarning).toBeTruthy();
    expect(component.noLatestRoundTxt).toEqual(noLatestRoundDataText);
  });

  it('should NOT show `No Previous Game` message', () => {
    component.qeData = {
      ...qeData,
      baseQuiz: {
        ...qeData.baseQuiz,
        firstAnsweredQuestion: {
          ...qeData.baseQuiz.firstAnsweredQuestion,
          id: 'bar'
        }
      }
    };
    component.ngOnInit();
    expect(component.showNoResultsWarning).not.toBeTruthy();
  });

  describe('Testing `questionSummaryHandler` method', () => {
    it('should NOT be called', () => {
      component.qeData = { ...qeData,
        baseQuiz: {
          ...qeData.baseQuiz,
          questionsList: null
        }
      };

      component.ngOnInit();
      expect(component.quizSummary).toEqual([]);
    });

    it('should BE called and render `showSummary`', () => {
      component.qeData = qeData;
      component.qeData.baseQuiz.firstAnsweredQuestion = questionItem;
      delete component.qeData.baseQuiz.questionsList[0].answers[1];
      component.qeData.baseQuiz.questionsList[0].answers[0].userChoice = true;
      component.qeData.baseQuiz.resultsPage.showResults = false;
      component.qeData.baseQuiz.resultsPage.showAnswersSummary = true;
      component.ngOnInit();

      expect(component.quizSummary.length).toEqual(1);
      expect(component.showSummary).toEqual(true);
      expect(component.showResults).toEqual(false);
    });

    it('should BE called and NOT render anything', () => {
      component.qeData.baseQuiz.firstAnsweredQuestion = questionItem;
      component.qeData.baseQuiz.questionsList = [];
      component.ngOnInit();

      expect(component.quizSummary.length).toEqual(0);
      expect(component.showSummary).toEqual(false);
      expect(component.showResults).toEqual(false);
    });

    it('should BE called and render `showResults`', () => {
      component.qeData.baseQuiz.firstAnsweredQuestion = questionItem;
      component.qeData.baseQuiz.questionsList = [questionItem];
      component.qeData.baseQuiz.questionsList[0].answers[0].userChoice = true;
      component.qeData.baseQuiz.questionsList[0].answers[0].correctAnswer = true;
      component.qeData.baseQuiz.resultsPage.showResults = true;
      component.qeData.baseQuiz.resultsPage.showAnswersSummary = false;
      component.ngOnInit();
      expect(component.quizSummary.length).toEqual(1);
      expect(component.showSummary).toEqual(false);
      expect(component.showResults).toEqual(true);
    });

    it('trackByFn', () => {
      const index = 5;
      const output = '5';
      expect(component.trackByFn(index)).toBe(output);
    });
  });

  describe('Testing `upsellVisibilityHandler` method', () => {
    it('should be called and render dynamic/default upsell', () => {
      component.qeData.baseQuiz.firstAnsweredQuestion = questionItem;
      component.qeData.baseQuiz.resultsPage.showUpsell = true;
      component.qeData.baseQuiz.resultsPage.upsell = new UpsellItemModel(upsellItemDynamic);
      component.qeData.baseQuiz.questionsList[0].answers[0].correctAnswer = false;
      component.ngOnInit();

      expect(component.showUpsell).toBeTruthy();
      expect(component.showGenericUpsell).not.toBeTruthy();
    });

    it('should be called and render fallback upsell img', () => {
      delete component.qeData.baseQuiz.firstAnsweredQuestion;
      component.qeData.baseQuiz.resultsPage.showUpsell = true;
      component.qeData.baseQuiz.resultsPage.upsell = new UpsellItemModel({
        ...upsellItemDynamic,
        fallbackImagePath: 'some/url.png'
      });

      component.qeData.baseQuiz.questionsList[0].answers[0].correctAnswer = false;
      component.ngOnInit();
      expect(component.showUpsell).not.toBeTruthy();
      expect(component.showNoResultsWarning).toBeTruthy();
      expect(component.showGenericUpsell).toBeTruthy();
    });

    it('should be called and NOT render any upsell', () => {
      delete component.qeData.baseQuiz.resultsPage.upsell;
      component.qeData.baseQuiz.questionsList[0].answers[0].correctAnswer = false;
      component.ngOnInit();
      expect(component.showUpsell).not.toBeTruthy();
      expect(component.showGenericUpsell).not.toBeTruthy();
    });
  });

  describe('Testing `genericUpsellHandler` method', () => {
    let myComponent;
    let myRouter;

    beforeEach(() => {
      myRouter = {
        navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue('/correct4/'),
      };

      const myQuestionEngineService = {
        qeData,
        mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(qeData)),
        resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
        pipe: jasmine.createSpy('pipe'),
        error: jasmine.createSpy('error').and.callThrough(),
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(qeData)),
        handleNoPrevGamesContent: jasmine.createSpy('handleNoPrevGamesContent').and.returnValue({
          title: 'title',
          subtitle: 'subtitle'
        }),
        trackPageViewGA: () => {}
      };

      myComponent = new LatestTabComponent(
        myQuestionEngineService as any, myRouter as any);
      myComponent.qeData = new QEData().qeData;
      myComponent.qeData.baseQuiz.resultsPage.upsell = new UpsellItemModel(upsellItemDefault);
    });

    it('should redirect to provided url', () => {
      myComponent.ngOnInit();
      myComponent.genericUpsellHandler();

      expect(myRouter.navigateByUrl).toHaveBeenCalledWith(myComponent.qeData.baseQuiz.resultsPage.upsell.imageUrl);
    });

    it('should redirect to question engine root with sourceId property', () => {
      myComponent.qeData.baseQuiz.resultsPage.upsell.imageUrl = null;
      myComponent.ngOnInit();
      myComponent.genericUpsellHandler();

      expect(myRouter.navigateByUrl).toHaveBeenCalledWith('/correct4');
    });

    it('should redirect to app root', () => {
      myComponent.qeData.baseQuiz.sourceId = null;
      myComponent.qeData.baseQuiz.resultsPage.upsell.imageUrl = null;
      myComponent.ngOnInit();
      myComponent.genericUpsellHandler();

      expect(myRouter.navigateByUrl).toHaveBeenCalledWith('/');
    });
  });
});
