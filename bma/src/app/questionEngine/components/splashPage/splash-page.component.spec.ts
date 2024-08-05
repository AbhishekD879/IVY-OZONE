import { SplashPageComponent } from './splash-page.component';
import { of, throwError } from 'rxjs';
import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import { QuestionEngineSplashPageModel } from '@app/questionEngine/models/questionEngineSplashPage.model';
import { QeQuickLinkModel } from '@app/questionEngine/models/qeQuickLink.model';
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';
import { LOGIN_RULE } from '@app/questionEngine/constants/question-engine.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('SplashPageComponent', () => {
  let component: SplashPageComponent;

  let userService,
    questionEngineService,
    pubSubService,
    router,
    localeService,
    cmsService,
    serviceClosureService;

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
      'textBtn',
      'loginToViewCTAText',
      'playForFreeCTAText',
      'seePreviousSelectionsCTAText',
      'seeYourSelectionsCTAText',
      'backgroundSvgFilePath',
      false
    );
    qeData.baseQuiz.quickLinks = [new QeQuickLinkModel()];
    // qeData.latestQuiz = new QuestionEngineQuizModel();
    qeData.baseQuiz.entryDeadline = new Date();
    qeData.baseQuiz.firstAnsweredQuestion = null;
    qeData.baseQuiz.firstQuestion = null;
    qeData.baseQuiz.id = 'testId';
    qeData.baseQuiz.splashPage.backgroundSvgFilePath = 'backgroundSvgUrl';
    qeData.baseQuiz.quizLoginRule = LOGIN_RULE.START;
    qeData.baseQuiz.sourceId = '/correct4';
    qeData.baseQuiz.quizConfiguration = {
      showSplashPage: true
    };
    qeData.previous = [];

    pubSubService = {
      publish: jasmine.createSpy(
        
      ),
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };

    userService = {
      status: true,
      username: 'bla',
      isInShopUser: () => {
        return false;
      }
    };

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('Processing..'),
    };

    questionEngineService = {
      qeData: qeData,
      isLoginPopupShown: false,
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeData.baseQuiz)),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(qeData)),
      resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
      pipe: jasmine.createSpy('pipe'),
      triggerFatalError: jasmine.createSpy('triggerFatalError'),
      checkPreviousPage: jasmine.createSpy('checkPreviousPage'),
      setQESubmitStatus: jasmine.createSpy('setQESubmitStatus'),
      checkGameData: jasmine.createSpy('checkGameData'),
      error: jasmine.createSpy('error').and.callThrough(),
      subscribe: jasmine.createSpy('subscribe').and.returnValue(of(qeData)),
      resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3'),
      redirectToTab: '',
      trackEventGA: jasmine.createSpy('trackEventGA'),
      trackPageViewGA: () => { }
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        F2PERRORS: {
        }
      }))
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue('/correct4/questions'),
    };

    component = new SplashPageComponent(
      userService as any,
      questionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,
      serviceClosureService as any
    );

  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should create component and call `getComponentData` method', () => {

    component.ngOnInit();
    component['getComponentData']();
    expect(component).toBeTruthy();
  });

  it('should call `getComponentData` method with param', () => {
    let called = false;
    const myQuestionEngineService = {
      ...questionEngineService,
      checkGameData: (data, cb) => {
        if (!called) {
          called = true;
          cb(true);
          return true;
        }
      }
    };

    const myComponent = new SplashPageComponent(
      userService as any,
      myQuestionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );

    myComponent.ngOnInit();
    myComponent['getComponentData']();
    expect(myComponent).toBeTruthy();
    expect(myQuestionEngineService.getQuizHistory).toHaveBeenCalledTimes(2);
  });

  it(`should not call 'getQuizHistory'`, () => {
    const myQuestionEngineService = {
      ...questionEngineService,
      quizHistoryModel: {}
    };

    const myComponent = new SplashPageComponent(
      userService as any,
      myQuestionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );

    myComponent.ngOnInit();
    expect(myQuestionEngineService.getQuizHistory).not.toHaveBeenCalled();
  });

  it('should call customQuestionEngineService.triggerFatalError', () => {
    const customQuestionEngineService = {
      qeData: null,
      resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(null),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(null),
      pipe: jasmine.createSpy('pipe'),
      checkPreviousPage: jasmine.createSpy('checkPreviousPage'),
      checkGameData: jasmine.createSpy('checkGameData'),
      triggerFatalError: jasmine.createSpy('triggerFatalError'),
      error: jasmine.createSpy('error').and.callThrough(),
      subscribe: jasmine.createSpy('subscribe').and.returnValue(of(qeData)),
      redirectToTab: '',
      trackEventGA: jasmine.createSpy('trackEventGA'),
      trackPageViewGA: () => { }
    };

    const customComponent = new SplashPageComponent(
      userService as any,
      customQuestionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );

    customComponent.ngOnInit();

    expect(component.qeData).not.toBeDefined();
    expect(router.navigate).toHaveBeenCalled();
  });

  

  it('should NOT call `redirectLink` or `openLoginDialog` on loginProcessing', () => {
    component.ngOnInit();
    component.loginProcessing = true;
    component.onCtaButtonClick();
    component['openLoginDialog'] = jasmine.createSpy();

    expect(router.navigateByUrl).not.toHaveBeenCalled();
    expect(component['openLoginDialog']).not.toHaveBeenCalled();
  });

  it('should NOT call `redirectLink` or `openLoginDialog` on loginProcessing', () => {
    component.ngOnInit();
    component.loginProcessing = true;
    component.onCtaButtonClick();
    component['openLoginDialog'] = jasmine.createSpy('openLoginDialog');

    expect(router.navigateByUrl).not.toHaveBeenCalled();
    expect(component['openLoginDialog']).not.toHaveBeenCalled();
  });
 
  it('should update CTA after login', () => {
    let methodCb = () => {
    };
    pubSubService.subscribe.and.callFake((name, method, cb) => {
      methodCb = cb;
    });
    methodCb();
    userService.status = false;
    const customComponent = new SplashPageComponent(
      userService as any,
      questionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );

    customComponent.ngOnInit();
    customComponent.onCtaButtonClick();

    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('should call removeEventListener onDestroy component', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('QeSplashPage');
  });

  it('should call checkUserStatus', () => {
    (questionEngineService.getQuizHistory as jasmine.Spy).and.returnValue(of(qeData));

    const customUserService = {
      status: false,
      username: 'zzz',
      isInShopUser: () => {
        return true;
      }
    };

    const customComponent = new SplashPageComponent(
      customUserService as any,
      questionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );

    customComponent.ngOnInit();

    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('should call checkUserStatus with qeData when isUserLoggedIn is false', () => {

    let methodCb = () => { };
    pubSubService.subscribe.and.callFake((name, method, cb) => {
      methodCb = cb;
    });

    const customQuestionEngineService = {
      qeData: {
        baseQuiz: {
          latestQuiz: {
            id: jasmine.createSpy('id'),
          },
          quizLoginRule: LOGIN_RULE.START,
          splashPage: { foo: 'bar' }
        },
        previous: []
      },
      setQESubmitStatus: jasmine.createSpy(),
      checkGameData: jasmine.createSpy(),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(null),
      checkPreviousPage: () => {
        return false;
      },
      triggerFatalError: jasmine.createSpy('triggerFatalError'),
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeData)),
      isLoginPopupShown: jasmine.createSpy('isLoginPopupShown').and.returnValue(true),
      trackEventGA: jasmine.createSpy('trackEventGA'),
      trackPageViewGA: () => { },
      resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3'),
    };

    const customUserService1 = {
      status: false,
      username: 'zzz',
      isInShopUser: () => {
        return false;
      }
    };

    const customComponent1 = new SplashPageComponent(
      customUserService1 as any,
      customQuestionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );

    customComponent1.ngOnInit();
    customComponent1.onCtaButtonClick();
    methodCb();

    expect(customQuestionEngineService.mapResponseOnComponentModel).toHaveBeenCalled();
  });

  it('should NOT call checkUserStatus with qeData when isUserLoggedIn is true', () => {
    component.qeData = qeData.baseQuiz;
    const customQuestionEngineService = {
      qeData: {
        baseQuiz: {
          latestQuiz: {
            id: jasmine.createSpy('id')
          },
          quizLoginRule: LOGIN_RULE.START,
          splashPage: { foo: 'bar' }
        },
        previous: []
      },
      setQESubmitStatus: jasmine.createSpy('setQESubmitStatus'),
      checkGameData: jasmine.createSpy('checkGameData'),
      checkPreviousPage: () => {
        return false;
      },
      resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3'),
      triggerFatalError: jasmine.createSpy('triggerFatalError'),
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeData)),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel'),
      resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
      trackEventGA: jasmine.createSpy('trackEventGA'),
      trackPageViewGA: () => { }
    };

    const customUserService1 = {
      status: false,
      username: 'zzz',
      isInShopUser: () => {
        return false;
      }
    };

    const customComponent1 = new SplashPageComponent(
      customUserService1 as any,
      customQuestionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );
    customComponent1.qeData = qeData.baseQuiz;
    let methodCb = () => { };
    pubSubService.subscribe.and.callFake((name, method, cb) => {
      customComponent1['isUserLoggedIn'] = true;
      methodCb = cb;
    });
    console.log(customComponent1.qeData.sourceId);
    customComponent1.ngOnInit();
    //customComponent1.onCtaButtonClick();
    methodCb();
    expect(customComponent1.isUserLoggedIn).toEqual(true);
  });

  it('should NOT call checkUserStatus with qeData when isUserLoggedIn is true', () => {
    component.qeData = qeData.baseQuiz;
    const customQuestionEngineService = {
      qeData: {
        baseQuiz: {
          latestQuiz: {
            id: jasmine.createSpy('id')
          },
          quizLoginRule: LOGIN_RULE.START,
          splashPage: { foo: 'bar' }
        },
        previous: []
      },
      setQESubmitStatus: jasmine.createSpy('setQESubmitStatus'),
      checkGameData: jasmine.createSpy('checkGameData'),
      checkPreviousPage: () => {
        return false;
      },
      triggerFatalError: jasmine.createSpy('triggerFatalError'),
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeData)),
      resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3'),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel'),
      resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
      trackEventGA: jasmine.createSpy('trackEventGA'),
      trackPageViewGA: () => { }
    };

    const customUserService1 = {
      status: false,
      username: 'zzz',
      isInShopUser: () => {
        return false;
      }
    };

    const customComponent1 = new SplashPageComponent(
      customUserService1 as any,
      questionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );

    customComponent1.qeData = qeData.baseQuiz;
    let methodCb;
    pubSubService.subscribe.and.callFake((name, method, cb) => {
      customComponent1['isUserLoggedIn'] = true;
      methodCb = cb;
    });

    customComponent1.ngOnInit();
  //  customComponent1.onCtaButtonClick();
    methodCb();

    expect(customComponent1.isUserLoggedIn).toEqual(true);
  });

  it('should call checkUserStatus with error', () => {
    pubSubService.subscribe.and.callFake((name, method, cb) => { });

    const mockQuestionEngineService2 = {
      qeData: {
        baseQuiz: {
          latestQuiz: {
            id: jasmine.createSpy('id'),
          },
          quizLoginRule: LOGIN_RULE.START,
          splashPage: { foo: 'bar' }
        },
        previous: []
      },
      triggerFatalError: jasmine.createSpy('triggerFatalError'),
      checkPreviousPage: () => {
        return false;
      },
      getQuizHistory: () => {
        return of({ data: null });
      },
      trackEventGA: jasmine.createSpy('trackEventGA'),
      trackPageViewGA: () => { },
      qeSubmittedThisSession: true
    };

    spyOn(mockQuestionEngineService2, 'getQuizHistory').and.callFake(() => {
      return throwError(new Error('Fake error'));
    });

    const customUserService2 = {
      status: false,
      username: 'zzz',
      isInShopUser: () => {
        return false;
      }
    };

    const customComponent2 = new SplashPageComponent(
      customUserService2 as any,
      mockQuestionEngineService2 as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );

    customComponent2.ngOnInit();

    expect(mockQuestionEngineService2.triggerFatalError).toHaveBeenCalled();
  });

  describe('Testing `goToQuestionsPage` method', () => {

    it('should navigate to previous quizes page', () => {

      const customComponent1 = new SplashPageComponent(
        userService as any,
        questionEngineService as any,
        pubSubService as any,
        router as any,
        localeService as any,
        cmsService as any,serviceClosureService as any
      );

      customComponent1.ngOnInit();
      customComponent1.qeData = qeData.baseQuiz;
      customComponent1.onCtaButtonClick();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/qe/cash_v3/questions');
    });

    it('should navigate to latest quiz page', () => {
      const customQuestionEngineService = {
        ...questionEngineService,
        redirectToTab: 'latest',
        resolvePath: jasmine.createSpy().and.returnValue('/correct4'),
      };

      const customComponent1 = new SplashPageComponent(
        userService as any,
        customQuestionEngineService as any,
        pubSubService as any,
        router as any,
        localeService as any,
        cmsService as any,serviceClosureService as any

      );

      customComponent1.ngOnInit();
      customComponent1.qeData = qeData.baseQuiz;
      customComponent1.onCtaButtonClick();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/correct4/after/latest-quiz');
    });

    it('should navigate to previous tab on results page', () => {
      const customQuestionEngineService = {
        ...questionEngineService,
        redirectToTab: 'previous',
        resolvePath: jasmine.createSpy().and.returnValue('/correct4'),
      };

      const customComponent1 = new SplashPageComponent(
        userService as any,
        customQuestionEngineService as any,
        pubSubService as any,
        router as any,
        localeService as any,
        cmsService as any,serviceClosureService as any

      );

      customComponent1.ngOnInit();
      customComponent1.qeData = qeData.baseQuiz;
      customComponent1.onCtaButtonClick();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/correct4/after/previous-quizes');
    });

    it('should navigate to questions page', () => {
      const customQuestionEngineService = {
        ...questionEngineService,
        redirectToTab: 'questions',
        resolvePath: jasmine.createSpy().and.returnValue('/correct4'),
      };

      const customComponent1 = new SplashPageComponent(
        userService as any,
        customQuestionEngineService as any,
        pubSubService as any,
        router as any,
        localeService as any,
        cmsService as any,serviceClosureService as any

      );

      customComponent1.ngOnInit();
      customComponent1.qeData = qeData.baseQuiz;
      customComponent1.onCtaButtonClick();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/correct4/questions');
    });

    it('should navigate to questions page if redirectToTab is emptyString', () => {
      const customQuestionEngineService = {
        ...questionEngineService,
        redirectToTab: '',
        resolvePath: jasmine.createSpy().and.returnValue('/correct4'),
      };

      const customComponent1 = new SplashPageComponent(
        userService as any,
        customQuestionEngineService as any,
        pubSubService as any,
        router as any,
        localeService as any,
        cmsService as any,serviceClosureService as any

      );

      customComponent1.ngOnInit();
      customComponent1.qeData = qeData.baseQuiz;
      customComponent1.onCtaButtonClick();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/correct4/questions');
    });
  });

  it('should call close app', () => {
    component.closeApp();
    expect(router.navigateByUrl).toHaveBeenCalled();
  });

  describe('Testing `refreshQEData` method', () => {
    it('should be triggered', () => {
      component['questionEngineService'].qeSubmittedThisSession = true;
      component.ngOnInit();

      expect(questionEngineService['getQuizHistory']).toHaveBeenCalled();
    });

    it('should be triggered with response errors', () => {
      component['questionEngineService'].qeSubmittedThisSession = true;
      component['questionEngineService'].triggerFatalError = jasmine.createSpy('triggerFatalError');
      component['questionEngineService'].getQuizHistory = jasmine.createSpy('getQuizHistory').and.returnValue(throwError('error'));

      component.ngOnInit();

      expect(component['questionEngineService'].getQuizHistory).toHaveBeenCalled();
      expect(component['questionEngineService'].triggerFatalError).toHaveBeenCalled();
    });

    it('should be navigate to QuestionsPage if showSplashPage is false', () => {
      userService.status = true;
      component['goToQuestionsPage'] = jasmine.createSpy();
      component['questionEngineService'].qeData.baseQuiz.quizConfiguration.showSplashPage = false;

      component.ngOnInit();

      expect(component['goToQuestionsPage']).toHaveBeenCalled();
    });

    it('should navigate to root if showSplashPage is false and user is not logged in', () => {
      userService.status = false;
      component['goToQuestionsPage'] = jasmine.createSpy();
      component['questionEngineService'].qeData.baseQuiz.quizConfiguration.showSplashPage = false;

      component.ngOnInit();

      expect(component['goToQuestionsPage']).toHaveBeenCalledTimes(0);
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });
  });

  it('should navigate to questions page if showSplashPage enabled, but null splash page came', () => {
    userService.status = true;
    component['goToQuestionsPage'] = jasmine.createSpy();
    component['questionEngineService'].qeData.baseQuiz.quizConfiguration.showSplashPage = true;
    component['questionEngineService'].qeData.baseQuiz.splashPage = null;

    component.ngOnInit();

    expect(component['goToQuestionsPage']).toHaveBeenCalledTimes(1);
  });

  it('should NOT have f2p error mesage', fakeAsync(() => {
    const myComponent = new SplashPageComponent(
      userService as any,
      questionEngineService as any,
      pubSubService as any,
      router as any,
      localeService as any,
      cmsService as any,serviceClosureService as any
    );
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of())
    };
    myComponent.ngOnInit();
    tick();
    expect(myComponent.f2pErrMsg).toBe('');
  }));

  
  it('should set f2p flag on init', () => {
    component.ngOnInit();
    component['initData']();
    pubSubService.subscribe.and.callFake((name, method, cb) => {
      expect(component['disableCtaBtnF2P']).toBe(cb);
    });
  });
});
