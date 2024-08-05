import { QuestionsCarouselComponent } from '@app/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';
import { of, throwError } from 'rxjs';
import { discardPeriodicTasks, fakeAsync, tick } from '@angular/core/testing';

import { Carousel } from '@sharedModule/directives/ng-carousel/carousel.class';

import {
  LOGIN_RULE,
  NO_AUTHORIZATION,
  TIMEOUT_FOR_USER_ANSWER_CAROUSEL,
  ERROR_CODE
} from '@app/questionEngine/constants/question-engine.constant';

describe('QuestionsCarouselComponent', () => {
  let component: QuestionsCarouselComponent;
  let domToolsService,
    carouselService,
    userService,
    questionEngineService,
    pubSubService,
    windowRefService,
    dialogService,
    componentFactoryResolver,
    localeService,
    routerService,
    awsService,
    cdr,
    vnUserService;

  const userAnswers = {
    username: 'dmytro-aug-28',
    quizId: '5d56cc2f591ed2714181187d',
    brand: 'ladbrokes',
    sourceId: '/upsell/aug-16',
    questionIdToAnswerId: {
      '7ec5e0e7-2214-416d-9134-fd0042d7d43f': ['4264b8d1-35cf-46f4-b79d-5b7d390f5eb3'],
      '9b1260d7-634a-4157-a824-87bb6db2f580': ['962661f2-78fb-4582-9f70-ac604e68d90f'],
      '2f656c04-5b3b-4024-831e-b00f74c5df08': ['1f73d900-d678-4842-92df-ae81e7c1d922']
    }
  };

  const response = {
    latestQuiz: {
      id: 'id',
      sourceId: 'sourceId',
      firstQuestion: {},
      firstAnsweredQuestion: {},
    },
  };

  const backButtonService = {
    redirectToPreviousPage: jasmine.createSpy('redirectToPreviousPage')
  } as any;

  beforeEach(() => {
    cdr = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    carouselService = {
      carousel: {
        currentSlide: 1,
        slidesCount: 2,
        carouselLoop: false,
        next: jasmine.createSpy('next'),
        previous: jasmine.createSpy('previous'),
        toIndex: jasmine.createSpy('toIndex'),
        onSlideChange: (func) => func(),
        onSlideChangeCallbacks: (func) => func(),
      },
      remove: jasmine.createSpy('remove'),
      get: (name: string): Carousel => carouselService.carousel as Carousel
    };

    domToolsService = {
      getWidth: (w) => w
    };

    userService = {
      username: 'test'
    };

    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((cb) => cb()),
        clearTimeout: jasmine.createSpy('clearTimeout'),
        scrollTo: jasmine.createSpy('scrollTo')
      }
    };
    routerService = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    vnUserService = {
      claims: {
        get: jasmine.createSpy('get').and.returnValue('123')
      }
    };
    awsService = {
      errorLog: jasmine.createSpy('errorLog')
       };

    questionEngineService = {
      qeData: {
        baseQuiz: {
          quizLoginRule: LOGIN_RULE.START,
          latestQuiz: {
            id: jasmine.createSpy('id'),
          },
          questionsList: [{
            answers: [
              {
                id: 'f4a391cb-0dc4-4279-828d-84a78273c4b9',
                text: 1,
                correctAnswer: false,
                questionAskedId: '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
                nextQuestionId: '1fa2682c-937b-4972-90cd-5161e6e83dc6',
                userChoice: false
              },
              {
                id: 'f4a391cb-0dc4-4279-828d-84a78273c4b5',
                text: 1,
                correctAnswer: false,
                questionAskedId: '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
                nextQuestionId: '1fa2682c-937b-4972-90cd-5161e6e83dc6',
                userChoice: false
              },
            ],
            id: '7571a150-d10c-4994-86c8-c0cd5f01a5ca',
            nextQuestions: {},
            questionType: 'SINGLE',
            text: 'Who will win?',
            questionDetails: {
              awayTeamName: 'Man Utd',
              awayTeamSvgFilePath: 'f.svg',
              channelSvgFilePath: 'd.svg',
              description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
              homeTeamName: 'Tottenham',
              homeTeamSvgFilePath: 'img.svg',
              middleHeader: '12:30',
              signposting: '',
              topLeftHeader: 'Champions League',
              topRightHeader: 'FRI AUG 23'
            }
          }],
          submitPopup: {
            iconSvgPath: '3d3ce10c2aa2.svg',
            closeCTAText: 'EXIT GAME',
            description: 'Your selections will not be saved if you exit  without submitting them',
            header: 'Are you sure?',
            submitCTAText: 'KEEP PLAYING'
          },
          defaultQuestionsDetails: {
            awayTeamName: 'Man Utd',
            awayTeamSvgFilePath: 'f.svg',
            channelSvgFilePath: 'd.svg',
            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.',
            homeTeamName: 'Tottenham',
            homeTeamSvgFilePath: 'img.svg',
            middleHeader: '12:30',
            signposting: '',
            topLeftHeader: 'Champions League',
            topRightHeader: 'FRI AUG 23'
          },
          quizConfiguration: {
            showSubmitPopup: true,
            showSwipeTutorial: true,
            showPreviousAndLatestTabs: true,
            showEventDetails: true,
            showExitPopup: true,
            showProgressBar: true,
            showQuestionNumbering: true,
            showSplashPage: true,
            useBackButtonToExitAndHideXButton: false,
          }
        },
      },
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(response)),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel'),
      setQEDataUptodateStatus: jasmine.createSpy('setQEDataUptodateStatus'),
      submitUserAnswer: jasmine.createSpy('submitUserAnswer').and.returnValue(of(userAnswers)),
      setQESubmitStatus: jasmine.createSpy('setQESubmitStatus'),
      trackPageViewGA: jasmine.createSpy('trackPageViewGA'),
      resolvePath: jasmine.createSpy('resolvePath'),
      trackEventGA: jasmine.createSpy('trackEventGA'),
      toggleSubmitNotification: jasmine.createSpy('toggleSubmitNotification').and.returnValue(true)
    };

    pubSubService = {
      API: {
        QE_FATAL_ERROR: 'QE_FATAL_ERROR'
      },
      publish: jasmine.createSpy('publish')
    };

    dialogService = {
      openDialog: jasmine.createSpy('openDialog'),
      closeDialog: jasmine.createSpy('closeDialog'),
      openedPopups: () => {}
    };

    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue({ name: 'InfoDialogComponent' })
    };

    localeService = {
      getString: jasmine.createSpy('getString'),
    };

    component = new QuestionsCarouselComponent(
      carouselService,
      domToolsService,
      userService,
      questionEngineService,
      pubSubService,
      windowRefService,
      dialogService,
      componentFactoryResolver,
      localeService,
      routerService,
      awsService,
      backButtonService,
      cdr,
      vnUserService
    );
  });

  it('should create QuestionsCarouselComponent', () => {
    expect(component).toBeTruthy();
  });

  it('should call declareSwipeBehaviour when carousel was initialised', () => {
    component['declareSwipeBehaviour'] = jasmine.createSpy('declareSwipeBehaviour').and.callThrough();
    component.onCarouselInit(true);

    expect(component['declareSwipeBehaviour']).toHaveBeenCalledTimes(1);
  });

  it('should not call declareSwipeBehaviour when carousel wasnot initialised', () => {
    component['declareSwipeBehaviour'] = jasmine.createSpy('declareSwipeBehaviour').and.callThrough();
    component.onCarouselInit(false);

    expect(component['declareSwipeBehaviour']).toHaveBeenCalledTimes(0);
  });

  it('should save username when it is onInit', () => {
    component.ngOnInit();

    expect(component.userAnswers.username).toEqual(userService.username);
  });

  it('should publish error if no username and quiz login rule ON_LOGIN', () => {
    userService.username = null;
    component.ngOnInit();

    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QE_FATAL_ERROR, [NO_AUTHORIZATION]);
  });

  it('should not publish error if no username and quiz login rule not ON_LOGIN', () => {
    userService.username = null;

    component['questionEngineService'] = {
      ...questionEngineService,
      qeData: {
        baseQuiz: {
          id: jasmine.createSpy('id'),
          quizLoginRule: LOGIN_RULE.SUBMIT
        },
        quizConfiguration: {
          showPreviousAndLatestTabs: true
        },
      }
    };
    component.userService = {
      ...userService,
      username: null
    };
    component.ngOnInit();

    expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubService.API.QE_FATAL_ERROR, [NO_AUTHORIZATION]);
  });

  it('should  initBackendData', () => {
    response.latestQuiz.id = 'id';
    component.ngOnInit();

    expect(component.qeData).toEqual(questionEngineService.qeData.baseQuiz);
  });

  it('should call pubSubService.API.QE_FATAL_ERROR onInit', () => {
    component['questionEngineService'] = {
      ...questionEngineService,
      qeData: null,
      quizConfiguration: {
        showPreviousAndLatestTabs: true
      }
    };
    component.ngOnInit();

    expect(component.qeData).not.toBeDefined();
    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('should get progressBarStepWidth', () => {
    component.qeData = null;
    expect(component['progressBarStepWidth']).toBeFalsy();
  });

  it('should  initBackendData when firstAnsweredQuestion is not defined', () => {
    response.latestQuiz.firstAnsweredQuestion = null;
    component.ngOnInit();

    expect(component.qeData).toBeDefined();
  });

  it('should call currentCarouselStep', () => {
    component.ngOnInit();
    component.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', {test: 'test'});

    expect(component.currentAnswerId).toBeDefined();
  });

  it('should call `nextSlide()` without `nextQuestions`', () => {
    component.ngOnInit();
    component.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', null);

    expect(component.currentAnswerId).toBeDefined();
  });

  it('should call GA for questions path', () => {
    carouselService = {
      carousel: {
        currentSlide: 1,
        slidesCount: 4,
        carouselLoop: false,
        next: jasmine.createSpy('next'),
        previous: jasmine.createSpy('previous'),
        toIndex: jasmine.createSpy('toIndex'),
        onSlideChange: (func) => func(),
        onSlideChangeCallbacks: (func) => func(),
      },
      remove: jasmine.createSpy('remove'),
      get: (name: string): Carousel => carouselService.carousel as Carousel
    };

    const custComponent1 = new QuestionsCarouselComponent(
      carouselService,
      domToolsService,
      userService,
      questionEngineService,
      pubSubService,
      windowRefService,
      dialogService,
      componentFactoryResolver,
      localeService,
      routerService,
      awsService,
      backButtonService,
      cdr,
      vnUserService
    );

    custComponent1.ngOnInit();
    custComponent1.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', {test: 'test'});

    expect(questionEngineService.trackPageViewGA).toHaveBeenCalled();
  });

  it('should call clearTimeout for user answer', () => {
    component.ngOnInit();
    component.timeOutSlide = 1;
    component.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', {test: '1'});

    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledTimes(1);
    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(1);
  });

  it('should call progressBarStepWidth', () => {
    component.ngOnInit();
    component.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', {test: 'test'});

    expect(component.progressBarStepWidth).toBeDefined();
  });

  it('should call showSwipeTutorial and show only once', () => {
    component.ngOnInit();
    component.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', {test: 'test'});

    expect(component.currentCarouselStep).toEqual(carouselService.carousel.currentSlide);
  });

  it('should not showSwipeTutorial  but proceed with currentCarouselStep', () => {
    component['showSwipeTutorialDialog'] = false;
    component.ngOnInit();
    component.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', {test: 'test'});

    expect(component.currentCarouselStep).toEqual(carouselService.carousel.currentSlide);
  });

  it('should call submit popup when all questions passed', fakeAsync(() => {
    component.submitLoading = true;
    component.ngOnInit();

    component.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', {test: '1'});
    tick(TIMEOUT_FOR_USER_ANSWER_CAROUSEL);

    component.nextSlide('answerId', 'nextQuestionId', 'questionAskedId', {test: '2'});
    tick(TIMEOUT_FOR_USER_ANSWER_CAROUSEL);

    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
    expect(dialogService.openDialog).toHaveBeenCalled();
    discardPeriodicTasks();
  }));

  it('should call submit popup and call for redirectToEdit function', () => {
    component.ngOnInit();
    component['redirectToEdit']();

    expect(carouselService.carousel.toIndex).toHaveBeenCalled();
    expect(dialogService.closeDialog).toHaveBeenCalled();
  });

  it('should call submit popup and call for submitQuiz function', () => {
    component.ngOnInit();
    component['submitQuiz'](true);

    expect(component.submitLoading).toBeDefined();
    expect(questionEngineService.submitUserAnswer).toHaveBeenCalled();
    expect(component.onSubmitRewardNotAssigned).toBeFalsy();
  });

  it('should call submit popup and call for submitQuiz function for survey', () => {
    component.ngOnInit();
    component.qeData.quizConfiguration = {
      ...component.qeData.quizConfiguration,
      showPreviousAndLatestTabs: false };
    component['submitQuiz'](true, component.qeData.quizConfiguration.showPreviousAndLatestTabs);

    expect(component['submitButton']).toBeDefined();
    expect(component.submitLoading).toBeDefined();
    expect(questionEngineService.submitUserAnswer).toHaveBeenCalledWith({
      questionIdToAnswerId: Object({  }),
      quizId: undefined,
      username: 'test',
      customerId: '123',
      sourceId: '/undefined'
    }, false);
    expect(component.onSubmitRewardNotAssigned).toBeFalsy();
  });

  it('should call submit popup and call for submitQuiz function with false param', () => {
    component.ngOnInit();
    component['submitQuiz'](false);

    expect(component.submitLoading).toBeFalsy();
    expect(questionEngineService.submitUserAnswer).not.toHaveBeenCalled();
  });

  it('should call submit popup and call for submitQuiz function when error occur with `updateSubmitDialog`', () => {
    component['questionEngineService'] = questionEngineService;
    questionEngineService.submitUserAnswer = jasmine.createSpy('submitUserAnswer').and.returnValue(throwError({status: 404}));
    component['updateSubmitDialog'] = jasmine.createSpy('updateSubmitDialog');

    component.ngOnInit();
    component['submitQuiz'](true);

    expect(component.submitLoading).toBeFalsy();
    expect(component.errSubmit).toBeTruthy();
    expect(component.onSubmitRewardNotAssigned).toBeFalsy();
    expect(component['updateSubmitDialog']).toHaveBeenCalled();
  });

  it('should call submit popup and call for submitQuiz function when error occur NOT with `updateSubmitDialog`', () => {
    component['questionEngineService'] = questionEngineService;
    questionEngineService.submitUserAnswer = jasmine.createSpy('submitUserAnswer').and.returnValue(throwError({status: 404}));
    component['updateSubmitDialog'] = jasmine.createSpy('updateSubmitDialog');
    component.ngOnInit();
    component.qeData.quizConfiguration.showSubmitPopup = false;
    component['submitQuiz'](true);

    expect(component.submitLoading).toBeFalsy();
    expect(component.errSubmit).toBeTruthy();
    expect(component.onSubmitRewardNotAssigned).toBeFalsy();
    expect(component['updateSubmitDialog']).not.toHaveBeenCalled();
  });

  it('should show prevSlide', () => {
    component.ngOnInit();
    component.prevSlide();

    expect(carouselService.carousel.previous).toHaveBeenCalled();
  });

  it('should set onSubmitRewardNotAssigned to true if Backend returns the corresponding error code', () => {
    questionEngineService.submitUserAnswer = jasmine.createSpy('submitUserAnswer').and.returnValue(throwError({
      status: 500,
      error: {
        errorCode: ERROR_CODE.REWARD_NOT_ASSIGNED
      }
    }));
    component.ngOnInit();
    component['submitQuiz'](true);

    expect(backButtonService.redirectToPreviousPage).toHaveBeenCalled();
  });

  it('should open Info Dialog on updateSubmitDialog if showSubmitPopup === false', () => {
    component['openInfoDialog'] = jasmine.createSpy('openInfoDialog');

    component.ngOnInit();
    component['updateSubmitDialog']();

    expect(component['openInfoDialog']).toHaveBeenCalled();
  });

  it('should call submitQuiz on updateSubmitDialog if showSubmitPopup === false', () => {
    component['submitQuiz'] = jasmine.createSpy('submitQuiz');

    component.ngOnInit();

    component.qeData.quizConfiguration.showSubmitPopup = false;

    component['openSubmitDialog']();

    expect(component['submitQuiz']).toHaveBeenCalled();
  });

  it('should call submitQuiz on updateSubmitDialog if showSubmitPopup === false', () => {
    component['submitQuiz'] = jasmine.createSpy('submitQuiz');
    component['updateSubmitDialog'] = jasmine.createSpy('updateSubmitDialog');

    component.ngOnInit();

    component.qeData.quizConfiguration.showSubmitPopup = true;

    component['openSubmitDialog']();

    expect(component['submitQuiz']).toHaveBeenCalledTimes(0);
    expect(component['updateSubmitDialog']).toHaveBeenCalledTimes(1);
  });

  it('should call change question and don\'t show tutorial on swipeBehaviour if not all conditions are true', () => {
    component['questionEngineService'].trackPageViewGA = jasmine.createSpy('trackPageViewGA');

    component.ngOnInit();

    component['windowRefService'].nativeWindow.scrollTo = jasmine.createSpy('scrollTo');
    component['questionsCarousel'].onSlideChange = jasmine.createSpy('onSlideChange').and.callFake((cb) => {
      cb();
    });
    component['showSwipeTutorial'] = jasmine.createSpy('showSwipeTutorial').and.returnValue(true);
    component['toggleSwipeTutorialDialog'] = true;

    component['declareSwipeBehaviour']();

    expect(component['questionsCarousel'].onSlideChange).toHaveBeenCalled();
    expect(component['windowRefService'].nativeWindow.scrollTo).toHaveBeenCalled();
    expect(component['showSwipeTutorial']).toHaveBeenCalled();
    expect(component['showSwipeTutorialDialog']).toBeFalsy();
    expect(component['toggleSwipeTutorialDialog']).toBeFalsy();
  });

  it('should call change question and don\'t show tutorial on swipeBehaviour', () => {
    component.ngOnInit();

    component['windowRefService'].nativeWindow.scrollTo = jasmine.createSpy('scrollTo');
    component['questionsCarousel'].onSlideChange = jasmine.createSpy('onSlideChange').and.callFake((cb) => {
      cb();
    });
    component['showSwipeTutorial'] = jasmine.createSpy('showSwipeTutorial').and.returnValue(false);
    component['toggleSwipeTutorialDialog'] = false;
    component['declareSwipeBehaviour']();

    expect(component['toggleSwipeTutorialDialog']).toBeFalsy();
    expect(Object.keys(dialogService.openedPopups).length).toBe(0);
  });

  it('test GA tracking on onSlideChange', () => {
    dialogService.openedPopups.lenght = jasmine.createSpy('lenght').and.returnValue( 1);
    component.ngOnInit();
    component['declareSwipeBehaviour']();

    expect(questionEngineService.trackPageViewGA).toHaveBeenCalled();
  });

  describe('Testing `showSwipeTutorial` method', () => {
    it('should return true', () => {
      component.ngOnInit();
      component['showSwipeTutorial']();
      expect(component['showSwipeTutorial']()).toBeTruthy();
    });

    it('should NOT return true', () => {
      component.ngOnInit();
      component['questionsCarousel'].currentSlide = 2;
      component['showSwipeTutorial']();
      expect(component['showSwipeTutorial']()).toBeFalsy();
    });
  });
});
