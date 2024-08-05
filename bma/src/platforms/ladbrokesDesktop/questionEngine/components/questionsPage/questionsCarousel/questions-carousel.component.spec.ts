import { of } from 'rxjs';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import {
  QuestionsCarouselComponent
} from '@ladbrokesDesktop/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';

import { LOGIN_RULE } from '@app/questionEngine/constants/question-engine.constant';

describe('Desktop QuestionEngine Carousel Component', () => {
  let component: QuestionsCarouselComponent;

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

  const backButtonService = {
    redirectToPreviousPage: jasmine.createSpy('redirectToPreviousPage')
  } as any;

  const cdr = {
    detectChanges: jasmine.createSpy('detectChanges')
  } as any;

  const question = {
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
  } as any;

  const response = {
    latestQuiz: {
      id: 'id',
      sourceId: 'sourceId',
      firstQuestion: {},
      firstAnsweredQuestion: {},
    },
  };

  const carouselService = {
    carousel: {
      currentSlide: 1,
      slidesCount: 2,
      carouselLoop: false,
      next: jasmine.createSpy('next'),
      previous: jasmine.createSpy('previous'),
      toIndex: jasmine.createSpy('toIndex'),
      onSlideChange: (func) => func(),
      onSlideChangeCallbacks: (func) => func()
    },
    remove: jasmine.createSpy('remove'),
    get: (name: string): Carousel => carouselService.carousel as Carousel
  } as any;

  const domToolsService = {
    getWidth: (w) => w
  } as any;

  const userService = {
    username: 'test'
  } as any;

  const windowRefService = {
    nativeWindow: {
      setTimeout: jasmine.createSpy('setTimeout').and.callFake((cb) => cb()),
      clearTimeout: jasmine.createSpy('clearTimeout'),
      scrollTo: jasmine.createSpy('scrollTo')
    }
  } as any;
  const routerService = {
    navigateByUrl: jasmine.createSpy('navigateByUrl')
  } as any;
  const awsService = {
    errorLog: jasmine.createSpy('errorLog')
      } as any;

  const questionEngineService = {
    qeData: {
      baseQuiz: {
        quizConfiguration : {
          showSwipeTutorial: true
        },
        quizLoginRule: LOGIN_RULE.START,
        latestQuiz: {
          id: jasmine.createSpy('id'),
        },
        questionsList: [question, question, question],

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
      },
    },
    getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(response)),
    mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel'),
    setQESubmitStatus: jasmine.createSpy('setQESubmitStatus'),
    setQEDataUptodateStatus: jasmine.createSpy('setQEDataUptodateStatus'),
    resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3'),
    submitUserAnswer: jasmine.createSpy('submitUserAnswer').and.returnValue(of(userAnswers)),
    trackPageViewGA: () => {},
    trackEventGA: () => {},
    toggleSubmitNotification: jasmine.createSpy('toggleSubmitNotification').and.returnValue(true)
  } as any;

  const pubSubService = {
    API: {
      QE_FATAL_ERROR: 'QE_FATAL_ERROR'
    },
    publish: jasmine.createSpy('publish')
  } as any;

  const dialogService = {
    openDialog: jasmine.createSpy('openDialog'),
    closeDialog: jasmine.createSpy('closeDialog'),
    openedPopups: () => {}
  } as any;

  const componentFactoryResolver = {
    resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue({ name: 'InfoDialogComponent' })
  } as any;

  const localeService = {
    getString: jasmine.createSpy('getString'),
  } as any;

  const vnUserService = {
    claims : {
       get : jasmine.createSpy('get').and.returnValue('123')
       }
    } as any;
  


  beforeEach(() => {
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

    component['initBackendData']();
  });

  it('go to next slide', () => {
    component['navigateToSlide'] = jasmine.createSpy().and.returnValue(true);
    component['questionEngineService'].trackEventGA = jasmine.createSpy();
    component['questionEngineService'].trackPageViewGA = jasmine.createSpy();
    component['userAction'] = ['true', '2', '3', '4'];

    component.ngOnInit();
    component.goToNextSlide();

    expect(component['questionEngineService'].trackPageViewGA).toHaveBeenCalled();
    expect(component['navigateToSlide']).toHaveBeenCalled();
  });

  it('should open new dialog on openInfoDialog', () => {
    const params = {
      dialogClass: '',
      src: '',
      caption: '',
      text: '',
      buttons: [{
        caption: '',
        cssClass: '',
        handler: () => {},
      }]
    };

    component['openInfoDialog'](params);

    expect(component['dialogService'].openDialog).toHaveBeenCalled();
  });

  it('should call onSlideChange on swipeBehaviour', () => {
    component['questionsCarousel'].onSlideChange = jasmine.createSpy('onSlideChange');

    component['declareSwipeBehaviour']();

    expect(component['questionsCarousel'].onSlideChange).toHaveBeenCalled();
  });

  it('should call change question and show tutorial on swipeBehaviour if all conditions are true', () => {
    component['windowRefService'].nativeWindow.scrollTo = jasmine.createSpy('scrollTo');
    component['questionsCarousel'].onSlideChange = jasmine.createSpy('onSlideChange').and.callFake((cb) => {
      cb();
    });
    component['showSwipeTutorial'] = jasmine.createSpy('showSwipeTutorial').and.returnValue(true);
    component['showSwipeTutorialDialog'] = true;

    component['swipeBehaviour']();

    expect(component['questionsCarousel'].onSlideChange).toHaveBeenCalled();
    expect(component['windowRefService'].nativeWindow.scrollTo).toHaveBeenCalled();
    expect(component['showSwipeTutorial']).toHaveBeenCalled();
    expect(component['ngCarouselDisableRightSwipe']).toBeTruthy();
    expect(component['showSwipeTutorialDialog']).toBeFalsy();
    expect(component['toggleSwipeTutorialDialog']).toBeFalsy();
  });

  it('should call change question and don\'t show tutorial on swipeBehaviour if not all conditions are true', () => {
    component['windowRefService'].nativeWindow.scrollTo = jasmine.createSpy('scrollTo');
    component['questionsCarousel'].onSlideChange = jasmine.createSpy('onSlideChange').and.callFake((cb) => {
      cb();
    });
    component['showSwipeTutorial'] = jasmine.createSpy('showSwipeTutorial').and.returnValue(false);
    component['toggleSwipeTutorialDialog'] = true;

    component['swipeBehaviour']();

    expect(component['questionsCarousel'].onSlideChange).toHaveBeenCalled();
    expect(component['windowRefService'].nativeWindow.scrollTo).toHaveBeenCalled();
    expect(component['showSwipeTutorial']).toHaveBeenCalled();
    expect(component['ngCarouselDisableRightSwipe']).toBeTruthy();
    expect(component['showSwipeTutorialDialog']).toBeTruthy();
    expect(component['toggleSwipeTutorialDialog']).toBeTruthy();
  });

  it('should call dialogService.closeDialog()', () => {
    component['redirectToEdit']();

    expect(component['dialogService'].closeDialog).toHaveBeenCalled();
  });
});
