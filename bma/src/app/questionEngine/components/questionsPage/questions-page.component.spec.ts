import { QuestionsPageComponent } from './questions-page.component';
import { of } from 'rxjs';
import any = jasmine.any;

import { InfoDialogComponent } from '@app/questionEngine/components/shared/infoDialog/info-dialog.component';
import { questionItem } from '@app/questionEngine/services/qe-mock-data.mock';
import { CORRECT4_SOURCE_ID, QE_PATH_VARIABLE } from '@questionEngine/constants/question-engine.constant';

describe('QuestionsPageComponent', () => {
  let component: QuestionsPageComponent;

  let router;
  let questionEngineService;
  let pubSubService;
  let QEContent;
  let dialogService;
  let componentFactoryResolver;
  let localeService;

  beforeEach(() => {
    QEContent = {
      logoSvgFilePath: 'https://cdn.zeplin.io/5d4b121f8d5c26520b23a39a/assets/1329E03A-AF81-4613-A809-2E81D5E0190A.svg`',
    };

    router = {
      navigateByUrl: jasmine.createSpy('router'),
      url: '/qe/cashv3/questions'
    };

    questionEngineService = {
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(QEContent)),
      checkPreviousPage: jasmine.createSpy('checkPreviousPage').and.returnValue('/prev-route'),
      qeData: {
        baseQuiz: {
          sourceId: '/cashv3',
          exitPopup: {
            iconSvgPath: '3d3ce10c2aa2.svg',
            closeCTAText: 'EXIT GAME',
            description: 'Your selections will not be saved if you exit  without submitting them',
            header: 'Are you sure?',
            submitCTAText: 'KEEP PLAYING',
          },
          quizConfiguration: {
            showPreviousAndLatestTabs: true,
            showExitPopup: true
          },
          splashPage: {}
        }
      },
      resolvePath: () => {
        return router.url.match(CORRECT4_SOURCE_ID) ? CORRECT4_SOURCE_ID : `${QE_PATH_VARIABLE}/cashv3`;
      },
      trackPageViewGA: () => {},
      trackEventGA: jasmine.createSpy('trackEventGA'),
      checkIfShouldRedirectGuest: jasmine.createSpy('checkIfShouldRedirectGuest').and.returnValue(false)
    };

    pubSubService = {
      API: {
        QE_FATAL_ERROR: 'QE_FATAL_ERROR'
      },
      publish: jasmine.createSpy('publish')
    };

    dialogService = {
      API: jasmine.createSpy('API'),
      openDialog: jasmine.createSpy('openDialog'),
      closeDialog: jasmine.createSpy('closeDialog')
    };

    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue({ name: 'InfoDialogComponent' })
    };

    localeService = {
      getString: jasmine.createSpy('getString')
    };
    component = new QuestionsPageComponent(
      router as any,
      questionEngineService as any,
      pubSubService as any,
      dialogService as any,
      componentFactoryResolver as any,
      localeService as any
    );

  });

  it('should create QuestionsPageComponent with data', () => {
    component.ngOnInit();

    expect(questionEngineService.getQuizHistory).not.toHaveBeenCalled();
    expect(component.qeData).toBeDefined();
  });

  it('should stop executing if Guest', () => {
    component['questionEngineService'].checkIfShouldRedirectGuest
      = jasmine.createSpy('checkIfShouldRedirectGuest').and.returnValue(true);
    component.ngOnInit();

    expect(component.qeData).not.toBeDefined();
  });

  it('should redirect to QE V3 previous', () => {
    component['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion = questionItem;
    component.ngOnInit();

    expect(router.navigateByUrl).toHaveBeenCalledWith('/qe/cashv3/after/previous-quizes');
  });

  it('should redirect to QE V3 previous if `entry date` is in PAST', () => {
    component['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion = undefined;
    const entryDate = new Date();
    entryDate.setHours(new Date().getHours() - 1); // set entry date to `Be In Past`(eg -1 hour)
    component['questionEngineService'].qeData.baseQuiz.entryDeadline = entryDate;
    component.ngOnInit();

    expect(router.navigateByUrl).toHaveBeenCalledWith('/qe/cashv3/after/previous-quizes');
  });

  it('should redirect to ResultsPage if answered has been submitted previously and Survey mode on', () => {
    component['questionEngineService'].qeData.baseQuiz.firstAnsweredQuestion = questionItem;
    component['questionEngineService'].qeData.baseQuiz.quizConfiguration.showPreviousAndLatestTabs = false;
    component.ngOnInit();

    expect(router.navigateByUrl).toHaveBeenCalledWith('/qe/cashv3/survey-end');
  });


  it('should redirect to QE C4 latest', () => {
    const myRouter = {
      navigateByUrl: jasmine.createSpy(),
      url: '/footballsuperseries/questions'
    };
    const myQuestionEngineService = {
      redirectToTab: 'latest',
      getQuizHistory: jasmine.createSpy().and.returnValue(of(QEContent)),
      checkPreviousPage: jasmine.createSpy().and.returnValue('/prev-route'),
      qeData: {
        baseQuiz: {
          sourceId: '/footballsuperseries',
          exitPopup: {
            iconSvgPath: '3d3ce10c2aa2.svg',
            closeCTAText: 'EXIT GAME',
            description: 'Your selections will not be saved if you exit  without submitting them',
            header: 'Are you sure?',
            submitCTAText: 'KEEP PLAYING',
          },
          firstAnsweredQuestion: questionItem,
          quizConfiguration: {
            showPreviousAndLatestTabs: true
          }
        }
      },
      resolvePath: () => {
        return myRouter.url.match(CORRECT4_SOURCE_ID) ? CORRECT4_SOURCE_ID : `${QE_PATH_VARIABLE}/cashv3`;
      },
      trackPageViewGA: () => {},
      trackEventGA: jasmine.createSpy(),
      checkIfShouldRedirectGuest: jasmine.createSpy().and.returnValue(false)
    };

    const myComponent = new QuestionsPageComponent(
      myRouter as any,
      myQuestionEngineService as any,
      pubSubService as any,
      dialogService as any,
      componentFactoryResolver as any,
      localeService as any
    );

    myComponent.ngOnInit();

    expect(myRouter.navigateByUrl).toHaveBeenCalledWith('/footballsuperseries/after/latest-quiz');
  });

  it('should publish fatal error if no data', () => {
    delete component['questionEngineService'].qeData;
    component.ngOnInit();

    expect(component.qeData).not.toBeDefined();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QE_FATAL_ERROR, any(Object));
  });

  it('should call exit popup', () => {
    component.ngOnInit();
    component.openGoToSplashOrContinueDialog();

    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(InfoDialogComponent);
    expect(dialogService.openDialog).toHaveBeenCalled();
  });

  it('should call goToSplash on openExitDialog if showExitPopup === false', () => {
    component['goToSplash'] = jasmine.createSpy('closeApp');

    component.ngOnInit();

    component.qeData.quizConfiguration.showExitPopup = false;

    component.openGoToSplashOrContinueDialog();

    expect(dialogService.openDialog).not.toHaveBeenCalled();
    expect(component['goToSplash']).toHaveBeenCalled();
  });

  it('should call exit popup on openCloseAppDialog if showExitPopup === true', () => {
    component.ngOnInit();
    component.openCloseAppDialog();

    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(InfoDialogComponent);
    expect(dialogService.openDialog).toHaveBeenCalled();
  });

  it('should call closeApp on openCloseAppDialog if showExitPopup === false', () => {
    component['closeApp'] = jasmine.createSpy('closeApp');

    component.ngOnInit();

    component.qeData.quizConfiguration.showExitPopup = false;

    component.openCloseAppDialog();

    expect(dialogService.openDialog).not.toHaveBeenCalled();
    expect(component['closeApp']).toHaveBeenCalled();
  });

  it('should call exit popup and call for goToSplash() function', () => {
    (<any>questionEngineService.qeData.baseQuiz.quizConfiguration) = {showSplashPage: true};

    component.ngOnInit();
    component['goToSplash']();

    expect(router.navigateByUrl).toHaveBeenCalled();
    expect(dialogService.closeDialog).toHaveBeenCalled();
    expect(questionEngineService.trackEventGA).toHaveBeenCalledWith(component['exitPopupTitle'], 'Exit Game');
  });

  it('should call closeApp() when goToSplash if showSplashPage config is disabled', () => {
    component['closeApp'] = jasmine.createSpy('closeApp');
    (<any>questionEngineService.qeData.baseQuiz.quizConfiguration) = {showSplashPage: false};

    component.ngOnInit();
    component['goToSplash']();

    expect(component['closeApp']).toHaveBeenCalled();
  });

  it('should call exit popup and call for closeApp() function', () => {
    component.ngOnInit();
    component['closeApp']();

    expect(router.navigateByUrl).toHaveBeenCalledWith('/prev-route');
    expect(dialogService.closeDialog).toHaveBeenCalled();
    expect(questionEngineService.trackEventGA).toHaveBeenCalledWith('Exit');
  });

  it('should call exit popup, call for closeApp() function and route to / if no previous route', () => {
    component['questionEngineService'].checkPreviousPage = () => undefined;
    component.ngOnInit();
    component['closeApp']();

    expect(router.navigateByUrl).toHaveBeenCalledWith('/');
    expect(dialogService.closeDialog).toHaveBeenCalled();
    expect(questionEngineService.trackEventGA).toHaveBeenCalledWith('Exit');
  });

  it('should call exit popup and call for keepPlay() function', () => {
    component.ngOnInit();
    component['keepPlay']();

    expect(dialogService.closeDialog).toHaveBeenCalled();
    expect(questionEngineService.trackEventGA).toHaveBeenCalledWith(component['exitPopupTitle'], 'Keep Playing');
  });

  it('should call openCloseAppDialog when back arrow pressing', () => {
    (<any>questionEngineService.qeData.baseQuiz.quizConfiguration) = {useBackButtonToExitAndHideXButton: true};
    component['openCloseAppDialog'] = jasmine.createSpy('openCloseAppDialog');

    component.ngOnInit();
    component.handleBackArrow();

    expect(component['openCloseAppDialog']).toHaveBeenCalled();
  });

  it('should call openGoToSplashOrContinueDialog when back arrow pressing', () => {
    (<any>questionEngineService.qeData.baseQuiz.quizConfiguration) = {useBackButtonToExitAndHideXButton: false};
    component['openCloseAppDialog'] = jasmine.createSpy('openCloseAppDialog');
    component['openGoToSplashOrContinueDialog'] = jasmine.createSpy('openGoToSplashOrContinueDialog');

    component.ngOnInit();
    component.handleBackArrow();

    expect(component['openGoToSplashOrContinueDialog']).toHaveBeenCalled();
  });
});
