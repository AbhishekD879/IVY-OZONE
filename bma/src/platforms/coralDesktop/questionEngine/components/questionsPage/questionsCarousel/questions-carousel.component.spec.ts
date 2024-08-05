import { of } from 'rxjs';
import { ChangeDetectorRef, ComponentFactoryResolver } from '@angular/core';
import { Router } from '@angular/router';

import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { UserService } from '@core/services/user/user.service';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import {
  DesktopQuestionsCarouselComponent
} from '@coralDesktop/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';

import { LOGIN_RULE } from '@app/questionEngine/constants/question-engine.constant';
import { BackButtonService } from '@core/services/backButton/back-button.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

describe('Desktop QuestionEngine Carousel Component', () => {
  let component: DesktopQuestionsCarouselComponent;
  let domToolsService,
      carouselService,
      userService,
      questionEngineService,
      response,
      pubSubService,
      windowRefService,
      dialogService,
      componentFactoryResolver,
      localeService,
      routerService,
      awsService,
      backButtonService,
      cdr,
      vnUserService;

  beforeEach(() => {

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

    response = {
      latestQuiz: {
        id: 'id',
        sourceId: 'sourceId',
        firstQuestion: {},
        firstAnsweredQuestion: {},
      },
    };

    carouselService = {
      carousel: {
        currentSlide: 1,
        slidesCount: 2,
        carouselLoop: false,
        next: jasmine.createSpy('next'),
        previous: jasmine.createSpy('previous'),
        toIndex: jasmine.createSpy(),
        onSlideChange: (func) => func(),
        onSlideChangeCallbacks: (func) => func(),
      },
      remove: jasmine.createSpy('remove'),
      get: (name: string): Carousel => carouselService.carousel as Carousel
    };

    domToolsService = {
      getWidth: (w) => w
    };

    vnUserService = {
      claims : {
         get : jasmine.createSpy('get').and.returnValue('123')
         }
      };

    userService = {
      username: 'test'
    };

    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((cb) => cb()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    routerService = {
      navigateByUrl: jasmine.createSpy()
    };

    questionEngineService = {
      qeData: {
        baseQuiz: {
          quizLoginRule: LOGIN_RULE.START,
          latestQuiz: {
            id: jasmine.createSpy(),
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
        }
      },
      getQuizHistory: jasmine.createSpy().and.returnValue(of(response)),
      mapResponseOnComponentModel: jasmine.createSpy(),
      toggleSubmitNotification: jasmine.createSpy(),
      checkPreviousPage: jasmine.createSpy(),
      submitUserAnswer: jasmine.createSpy().and.returnValue(of(userAnswers)),
      setQESubmitStatus: jasmine.createSpy(),
      setQEDataUptodateStatus: jasmine.createSpy(),
      trackPageViewGA: () => {},
      trackEventGA: () => {},
      resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3')
    };

    pubSubService = {
      API: {
        QE_FATAL_ERROR: 'QE_FATAL_ERROR'
      },
      publish: jasmine.createSpy('publish')
    };

    dialogService = {
      openDialog: jasmine.createSpy(),
      closeDialog: jasmine.createSpy()
    };

    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy().and.returnValue({ name: 'InfoDialogComponent' })
    };

    localeService = {
      getString: jasmine.createSpy(),
    };

    awsService = {
        errorLog: jasmine.createSpy('errorLog')
          };

    backButtonService = {
      redirectToPreviousPage: jasmine.createSpy('redirectToPreviousPage')
    };

    cdr = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new DesktopQuestionsCarouselComponent(
      carouselService as CarouselService,
      domToolsService as DomToolsService,
      userService as UserService,
      questionEngineService as QuestionEngineService,
      pubSubService as PubSubService,
      windowRefService as WindowRefService,
      dialogService as DialogService,
      componentFactoryResolver as ComponentFactoryResolver,
      localeService as LocaleService,
      routerService as Router,
      awsService as AWSFirehoseService,
      backButtonService as BackButtonService,
      cdr as ChangeDetectorRef,
      vnUserService
    );

  });

  it('should call submit popup and call for submitQuiz function', () => {
    component.ngOnInit();
    component['submitQuiz'](true);

    expect(component.submitLoading).toBeDefined();
    expect(questionEngineService.submitUserAnswer).toHaveBeenCalled();
  });

  it('go to next slide', () => {
    carouselService = {
      carousel: {
        currentSlide: 0,
        slidesCount: 2,
        carouselLoop: false,
        next: jasmine.createSpy('next'),
        previous: jasmine.createSpy('previous'),
        toIndex: jasmine.createSpy(),
        onSlideChange: (func) => func(),
        onSlideChangeCallbacks: (func) => func(),
      },
      remove: jasmine.createSpy('remove'),
      get: (name: string): Carousel => carouselService.carousel as Carousel
    };

    questionEngineService = {
      qeData: {
        baseQuiz: {
          quizLoginRule: LOGIN_RULE.START,
          latestQuiz: {
            id: jasmine.createSpy(),
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
          },
            {
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
        },
      },
      getQuizHistory: jasmine.createSpy().and.returnValue(of(response)),
      mapResponseOnComponentModel: jasmine.createSpy(),
      toggleSubmitNotification: jasmine.createSpy(),
      setQESubmitStatus: jasmine.createSpy(),
      setQEDataUptodateStatus: jasmine.createSpy(),
      trackPageViewGA: () => {},
      trackEventGA: () => {},
      resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3')
    };
    const customComponent = new DesktopQuestionsCarouselComponent(
      carouselService as CarouselService,
      domToolsService as DomToolsService,
      userService as UserService,
      questionEngineService as QuestionEngineService,
      pubSubService as PubSubService,
      windowRefService as WindowRefService,
      dialogService as DialogService,
      componentFactoryResolver as ComponentFactoryResolver,
      localeService as LocaleService,
      routerService as Router,
      awsService as AWSFirehoseService,
      backButtonService as BackButtonService,
      cdr as ChangeDetectorRef,
      vnUserService
    );

    customComponent.ngOnInit();
    customComponent['userAction'] = ['true', '2', '3', '4'];
    customComponent.goToNextSlide();

    expect(carouselService.carousel.toIndex).toHaveBeenCalled();
  });

  it('Test redirectToEdit() function', () => {
    component['redirectToEdit']();

    expect(component['dialogService'].closeDialog).toHaveBeenCalled();
  });

  it('should open new dialog on openInfoDialog', () => {
    const params = {
      dialogClass: '',
      src: '',
      caption: '',
      text: '',
      buttons: []
    };
    component['openInfoDialog'](params);

    expect(component['dialogService'].openDialog).toHaveBeenCalled();
  });
});
