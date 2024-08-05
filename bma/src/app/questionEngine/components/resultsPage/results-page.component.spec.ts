import { ResultsPageComponent } from './results-page.component';
import { of, throwError } from 'rxjs';
import { QEData, questionItem } from '../../services/qe-mock-data.mock';

describe('ResultsPageComponent', () => {
  const { qeData } = new QEData();
  let component: ResultsPageComponent;

  const questionEngineService = {
    qeData,
    checkPreviousPage: jasmine.createSpy('checkPreviousPage').and.returnValue('/prev-route'),
    trackEventGA: jasmine.createSpy('trackEventGA'),
    getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeData)),
    mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(qeData)),
    resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
    pipe: jasmine.createSpy('pipe'),
    triggerFatalError: jasmine.createSpy('triggerFatalError'),
    toggleSubmitNotification: jasmine.createSpy('toggleSubmitNotification'),
    setQEDataUptodateStatus: jasmine.createSpy('setQEDataUptodateStatus'),
    error: jasmine.createSpy('error').and.callThrough(),
    subscribe: jasmine.createSpy('subscribe').and.returnValue(of(qeData)),
    resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/correct4'),
    checkIfShouldRedirectGuest: jasmine.createSpy('checkIfShouldRedirectGuest').and.returnValue(true),
    dataIsUpToDate: true,
  };

  const activatedRoute = {
    snapshot: {
      data: {
        segment: 'latest'
      }
    }
  };

  const router = {
    navigate: jasmine.createSpy('navigate'),
    navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue('/correct4/questions'),
  };

  const windowRefService = {
    nativeWindow: {
      setTimeout: (cb) => cb(),
    }
  };


  beforeEach(() => {
    component = new ResultsPageComponent(
      questionEngineService as any,
      activatedRoute as any,
      router as any,
      windowRefService as any
    );
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should call app closing when back arrow pressing when config', () => {
    (<any>component.qeData) = {baseQuiz: {quizConfiguration: {useBackButtonToExitAndHideXButton: true}}};
    component['closeApp'] = jasmine.createSpy('closeApp');

    component.handleBackArrow();

    expect(component['closeApp']).toHaveBeenCalled();
  });

  it('should call app closing when back arrow pressing and splash page disabled', () => {
    (<any>component.qeData) = {baseQuiz: {quizConfiguration: {useBackButtonToExitAndHideXButton: false, showSplashPage: false}}};
    component['closeApp'] = jasmine.createSpy('closeApp');

    component.handleBackArrow();

    expect(component['closeApp']).toHaveBeenCalled();
  });

  it('should call back action when back arrow pressing when config', () => {
    (<any>component.qeData) = {baseQuiz: {quizConfiguration: {useBackButtonToExitAndHideXButton: false}}};
    (<any>component.qeData) = {baseQuiz: {splashPage: {}}};
    component['backToSplash'] = jasmine.createSpy('openGoToSplashOrContinueDialog');

    component.handleBackArrow();

    expect(component['backToSplash']).toHaveBeenCalled();
  });

  it('should call close action when back arrow pressing when config', () => {
    (<any>component.qeData) = {baseQuiz: {quizConfiguration: {useBackButtonToExitAndHideXButton: false}}};
    (<any>component.qeData) = {baseQuiz: {splashPage: null}};
    component['closeApp'] = jasmine.createSpy('openGoToSplashOrContinueDialog');

    component.handleBackArrow();

    expect(component['closeApp']).toHaveBeenCalled();
  });

  describe('testing ngOnInit', () => {

    it('should stop executing if Guest', () => {
      component['questionEngineService'].checkIfShouldRedirectGuest
        = jasmine.createSpy('checkIfShouldRedirectGuest').and.returnValue(true);
      component['initConfig'] = jasmine.createSpy('initConfig');
      component.ngOnInit();
      expect(component['initConfig']).not.toHaveBeenCalled();
    });

    it('should set `this.resultPageBg` to `none`', () => {
      component['questionEngineService'].qeData.baseQuiz.resultsPage.backgroundSvgImagePath = '';
      component.ngOnInit();

      expect(component.resultPageBg).toEqual('none');
    });

    it('should set `this.resultPageBg` to `value`', () => {
      component['questionEngineService'].qeData.baseQuiz.resultsPage.backgroundSvgImagePath = '/some_file.svg';
      component['questionEngineService'].checkIfShouldRedirectGuest = () => false;
      component.ngOnInit();

      expect(component.resultPageBg).toEqual('url(/some_file.svg)');
    });

    it('should NOT set `this.resultPageBg` because it`s null', () => {
      delete component['questionEngineService'].qeData.baseQuiz.resultsPage.backgroundSvgImagePath;
      component['questionEngineService'].checkIfShouldRedirectGuest = () => false;
      component.ngOnInit();

      expect(component.resultPageBg).toEqual('none');
    });

    it('should call `refreshQEData` on init', () => {
      component['questionEngineService'].dataIsUpToDate = false;
      component['questionEngineService'].checkIfShouldRedirectGuest = () => false;
      component['dataIsUpToDate'] = false;
      component.ngOnInit();

      expect(component['questionEngineService'].setQEDataUptodateStatus).toHaveBeenCalledWith(true);
    });

    it('should call `refreshQEData` on init with failed response', () => {
      component['questionEngineService'].getQuizHistory = jasmine.createSpy('getQuizHistory').and.returnValue(throwError('error')),
      component['questionEngineService'].checkIfShouldRedirectGuest = () => false;
      component['dataIsUpToDate'] = false;
      component.ngOnInit();

      expect(component['questionEngineService'].triggerFatalError).toHaveBeenCalled();
    });

    it('should trigger FATAL ERROR if data is broken', () => {
      delete component['questionEngineService'].qeData.baseQuiz.resultsPage.backgroundSvgImagePath;
      component['questionEngineService'].checkIfShouldRedirectGuest = () => false;
      component.ngOnInit();

      expect(component['questionEngineService'].triggerFatalError).toHaveBeenCalled();
    });

    it('should set `activeTab` to previous', () => {
      const customActivatedRoute = {
        snapshot: {
          data: {
            segment: 'previous'
          }
        }
      };

      const component2 = new ResultsPageComponent(
        questionEngineService as any,
        customActivatedRoute as any,
        router as any,
        windowRefService as any
      );
      component2.activeTab = 'previous';
      component2.ngOnInit();
      expect(component2.activeTab).toEqual('previous');
      component2.changeTab('last');
      expect(component2.activeTab).toEqual('last');
    });

  });

  describe('Testing `notifierHandler` method', () => {
    beforeEach(() => {});
    it('should `show` submit notification', () => {
      const myQuestionEngineService = {
        qeData,
        checkPreviousPage: jasmine.createSpy('checkPreviousPage').and.returnValue('/prev-route'),
        trackEventGA: jasmine.createSpy('trackEventGA'),
        getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeData)),
        mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(qeData)),
        resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
        pipe: jasmine.createSpy('pipe'),
        triggerFatalError: jasmine.createSpy('triggerFatalError'),
        toggleSubmitNotification: jasmine.createSpy('toggleSubmitNotification'),
        setQEDataUptodateStatus: jasmine.createSpy('setQEDataUptodateStatus'),
        error: jasmine.createSpy('error').and.callThrough(),
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(qeData)),
        resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/correct4'),
        checkIfShouldRedirectGuest: jasmine.createSpy('checkIfShouldRedirectGuest').and.returnValue(false),
        dataIsUpToDate: true,
        showSubmitNotification: true
      };

      const myComponent = new ResultsPageComponent(
        myQuestionEngineService as any,
        activatedRoute as any,
        router as any,
        windowRefService as any
      );

      myComponent.ngOnInit();
      expect(myComponent.showSubmitNotification).toEqual(true);
    });

    it('should NOT `show` submit notification', () => {
      component['questionEngineService'].showSubmitNotification = false;

      expect(component.showSubmitNotification).toEqual(false);
    });
  });

  describe('Testing navigating from QE', () => {
    it('should navigate to previous page and track GA on closing', () => {
      component.closeApp();

      expect(router.navigateByUrl).toHaveBeenCalledWith('/prev-route');
      expect(questionEngineService.trackEventGA).toHaveBeenCalledWith('Exit');
    });

    it('should navigate to app root', () => {
      component['questionEngineService'].checkPreviousPage
        = jasmine.createSpy('checkPreviousPage').and.returnValue('');
      component.closeApp();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/');
    });
  });

  describe('Testing `backToSplash` method', () => {
    it('should redirect to sourceId', () => {
      component.backToSplash();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/correct4');
    });

    it('should redirect to root', () => {
      delete component['questionEngineService'].qeData;

      component.backToSplash();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/');
    });
  });

  describe('Testing case if `showPreviousAndLatestTabs` is set to false', () => {
    let myComponent;
    beforeEach(() => {
      const myQeData = new QEData();
      const myQuestionEngineService1 = {
        qeData: myQeData.qeData,
        checkPreviousPage: jasmine.createSpy('checkPreviousPage').and.returnValue('/prev-route'),
        trackEventGA: jasmine.createSpy('trackEventGA'),
        getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeData)),
        mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(qeData)),
        resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
        pipe: jasmine.createSpy('pipe'),
        triggerFatalError: jasmine.createSpy('triggerFatalError'),
        toggleSubmitNotification: jasmine.createSpy('toggleSubmitNotification'),
        setQEDataUptodateStatus: jasmine.createSpy('setQEDataUptodateStatus'),
        error: jasmine.createSpy('error').and.callThrough(),
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(qeData)),
        resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/correct4'),
        checkIfShouldRedirectGuest: jasmine.createSpy('checkIfShouldRedirectGuest').and.returnValue(false),
        dataIsUpToDate: true,
        showSubmitNotification: true
      };
      myQuestionEngineService1.qeData.baseQuiz.quizConfiguration.showPreviousAndLatestTabs = false;

      myComponent = new ResultsPageComponent(
        myQuestionEngineService1 as any,
        activatedRoute as any,
        router as any,
        windowRefService as any
      );
      myComponent['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion = questionItem;
    });

    it('should redirect to questions', () => {
      myComponent['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion = null;
      const entryDate = new Date();
      entryDate.setHours(new Date().getHours() + 1); // set entry date to `Be In Future`(eg +1 hour)
      myComponent['questionEngineService'].qeData.baseQuiz.entryDeadline = entryDate;
      myComponent.ngOnInit();

      expect(router.navigateByUrl).toHaveBeenCalledWith('/qe/correct4/questions');
    });

    it('should redirect to previous page. Entry deadline in the past', () => {
      myComponent['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion = null;
      myComponent['questionEngineService'].checkPreviousPage
        = jasmine.createSpy('checkPreviousPage').and.returnValue('/prev-route');
      const entryDate = new Date();
      entryDate.setHours(new Date().getHours() - 1); // set entry date to `Be In Past`(eg -1 hour)
      myComponent['questionEngineService'].qeData.baseQuiz.entryDeadline = entryDate;
      myComponent.ngOnInit();

      expect(router.navigateByUrl).toHaveBeenCalledWith('/prev-route');
    });

    it('should redirect to `home`. Entry deadline in the past', () => {
      myComponent['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion = null;
      myComponent['questionEngineService'].checkPreviousPage
        = jasmine.createSpy('checkPreviousPage').and.returnValue(null);
      const entryDate = new Date();
      entryDate.setHours(new Date().getHours() - 1); // set entry date to `Be In Past`(eg -1 hour)
      myComponent['questionEngineService'].qeData.baseQuiz.entryDeadline = entryDate;
      myComponent.ngOnInit();

      expect(router.navigateByUrl).toHaveBeenCalledWith('/');
    });

    it('should define endPage', () => {
      myComponent['questionEngineService'].qeData.baseQuiz.questionsList = [questionItem, questionItem];
      myComponent['questionEngineService'].qeData.baseQuiz.resultsPage.submitMessage = 'old title';
      myComponent['questionEngineService'].qeData.baseQuiz.questionsList[1].answers[1].endPage
        = myComponent['questionEngineService'].qeData.baseQuiz.resultsPage;

      myComponent['questionEngineService'].qeData.baseQuiz.questionsList[1].answers[1].endPage = {
        ...myComponent['questionEngineService'].qeData.baseQuiz.questionsList[1].answers[1].endPage,
        submitMessage: 'updated title'
      };

      myComponent.ngOnInit();

      expect(myComponent.qeData.baseQuiz.resultsPage.submitMessage).toEqual('updated title');
    });

    it('should use default endPage', () => {
      myComponent['questionEngineService'].qeData.baseQuiz.questionsList = [questionItem, questionItem];
      myComponent['questionEngineService'].qeData.baseQuiz.resultsPage.title = 'old title';
      delete myComponent['questionEngineService'].qeData.baseQuiz.questionsList[1].answers[1].endPage;
      myComponent['questionEngineService'].qeData.baseQuiz.quizConfiguration.showPreviousAndLatestTabs = false;
      myComponent.ngOnInit();

      expect(myComponent.qeData.baseQuiz.resultsPage.title).toEqual('old title');
    });

    it('should `triggerFatalError`', () => {
      myComponent['questionEngineService'].qeData.baseQuiz.resultsPage.title = 'old title';
      myComponent['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion = questionItem;
      myComponent['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion.answers = [];
      myComponent['questionEngineService'].qeData.baseQuiz.quizConfiguration.showPreviousAndLatestTabs = false;
      myComponent.ngOnInit();

      expect(questionEngineService.triggerFatalError).toHaveBeenCalled();
    });
  });
});
