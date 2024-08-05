import { of as observableOf, of } from 'rxjs';
import { QuizDialogComponent } from './quiz-dialog.component';
import { fakeAsync } from '@angular/core/testing';
import { NavigationEnd } from '@angular/router';

describe('QuizDialogComponent', () => {
  let component;
  let infoDialogComponent;
  let storageService;
  let cmsService;
  let router;
  let questionEngineService;
  let username;
  let windowRef;

  const settings = {
    id: '123',
    popupTitle: 'Title',
    popupText: 'Text',
    quizId: '123',
    yesText: 'Yes',
    remindLaterText: 'Remind me later',
    dontShowAgainText: 'Not show again'
  };

  beforeEach(() => {
    username = 'TestUserName';
    cmsService = {
      getQuizPopupSettingDetails: jasmine.createSpy('getQuizPopupSettingDetails').and.returnValue(of(settings)),
      getQuizPopupSetting: jasmine.createSpy().and.returnValue(of({ id: '123',  enabled: true, pageUrls: '/' }))
    };
    infoDialogComponent = {
      openInfoDialog: jasmine.createSpy('openInfoDialog'),
      closePopUp: jasmine.createSpy('closePopUp')
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy().and.returnValue({})
    };
    router = {
      navigateByUrl: jasmine.createSpy(),
      events: {
        subscribe: jasmine.createSpy('subscribe')
      },
      url: '/'
    };

    questionEngineService = {
      userAnswersExist: jasmine.createSpy('userAnswersExist').and.returnValue(of(false)),
      submitUserAnswer: jasmine.createSpy('submitUserAnswer').and.returnValue(of({}))
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake((callback) => {
          callback && callback();
        }),
        clearTimeout: jasmine.createSpy(),
      }
    };

    component = new QuizDialogComponent(
      infoDialogComponent,
      storageService,
      cmsService,
      router,
      questionEngineService,
      windowRef
    );

    component.user = {
      status: true,
      username: username,
      bppToken: 'bppToken',
      playerCode: 'playerCode'
    };
    component.quizPopupSettings = {
      id: '0',
      pageUrls: 'aaaa, bbb, ccc',
      enabled: true,
      sourceId: '/source-id',
      quizId: 'quizId'
    };
  });

  it('should create QuizDialogComponent component', () => {
    expect(component).toBeDefined();
  });

  it('should subscribe to changes on ngOnInit ', () => {
    router.events = observableOf(new NavigationEnd(0, '', ''));
    spyOn(component, 'handleQuizPopupDisplay');

    component.ngOnInit();

    expect(component.cms.getQuizPopupSetting).toHaveBeenCalled();
    expect(component.handleQuizPopupDisplay).toHaveBeenCalledTimes(2);
  });

  it('should get QuizPopupSettings and display quiz dialog on renderQuizDialog', () => {
    spyOn(component, 'displayQuizDialog');

    component.renderQuizDialog();

    expect(component.cms.getQuizPopupSettingDetails).toHaveBeenCalled();
    expect(component.displayQuizDialog).toHaveBeenCalled();
    expect(component.displayQuizDialog).toHaveBeenCalledWith(settings);
  });

  it('should get QuizPopupSettings and do not display quiz dialog on renderQuizDialog if quizSettings are empty', () => {
    spyOn(component, 'displayQuizDialog');
    component.cms.getQuizPopupSettingDetails = jasmine.createSpy('getQuizPopupSettingDetails').and.returnValue(of(null));

    component.renderQuizDialog();

    expect(component.cms.getQuizPopupSettingDetails).toHaveBeenCalled();
    expect(component.displayQuizDialog).not.toHaveBeenCalled();
  });

  it('should open Dialog on displayQuizDialog', () => {
    component.displayQuizDialog(settings);

    expect(component.dialogService.openInfoDialog).toHaveBeenCalled();
  });

  it('should open Dialog on displayQuizDialog without defined settings', () => {
    delete settings.popupTitle;
    delete settings.popupText;
    delete settings.quizId;
    delete settings.remindLaterText;
    delete settings.yesText;
    delete settings.dontShowAgainText;
    component.displayQuizDialog(settings);

    expect(component.dialogService.openInfoDialog).toHaveBeenCalled();
  });

  it('should open quiz info dialog with 3 buttons on displayQuizDialog ', fakeAsync(() => {
    spyOn(component, 'destroy');

    component.dialogService.openInfoDialog.and.callFake((p1, p2, p3, p4, p5, btns) => {
      btns[0].handler();
      btns[1].handler();
      btns[2].handler();
    });

    component.displayQuizDialog(settings);

    expect(component.destroy).toHaveBeenCalledTimes(3);
    expect(component.destroy).toHaveBeenCalledWith(false);
    expect(component.destroy).toHaveBeenCalledWith(true);
    expect(component.destroy).toHaveBeenCalledWith(false);
  }));

  it('should navigate to Quiz page on openQuiz', () => {
    spyOn(component, 'destroy');

    component.openQuiz();

    expect(component.router.navigateByUrl).toHaveBeenCalled();
    expect(component.destroy).toHaveBeenCalled();

    expect(component.router.navigateByUrl).toHaveBeenCalledWith(`/qe${component.quizPopupSettings.sourceId}`);
    expect(component.destroy).toHaveBeenCalledWith(true);
  });

  it('should navigate to correct4 page on openQuiz', () => {
    spyOn(component, 'destroy');
    component.quizPopupSettings.sourceId = '/quiz/footballsuperseries';

    component.openQuiz();

    expect(component.router.navigateByUrl).toHaveBeenCalled();
    expect(component.destroy).toHaveBeenCalled();

    expect(component.router.navigateByUrl).toHaveBeenCalledWith(`/footballsuperseries`);
    expect(component.destroy).toHaveBeenCalledWith(true);
  });

  it('should destroy dialog and set value to storage if destroy method is called with parameter false', () => {
    component.destroy(false);

    expect(component.questionEngineService.submitUserAnswer).toHaveBeenCalled();
    expect(component.questionEngineService.submitUserAnswer).toHaveBeenCalledWith({
      username: component.user.username,
      customerId: component.user.playerCode,
      quizId: component.quizPopupSettings.quizId,
      sourceId: component.quizPopupSettings.sourceId,
      questionIdToAnswerId: {
        DO_NOT_SHOW_AGAIN: ['DO_NOT_SHOW_AGAIN']
      }
    });
    expect(component.dialogService.closePopUp).toHaveBeenCalled();
    expect(component.storageService.set).toHaveBeenCalled();
  });

  it('should destroy dialog if destroy method is called with true', () => {
    component.destroy(true);

    expect(component.dialogService.closePopUp).toHaveBeenCalled();
    expect(component.questionEngineService.submitUserAnswer).not.toHaveBeenCalled();
    expect(component.storageService.set).not.toHaveBeenCalled();
    expect(component.questionEngineService.submitUserAnswer).not.toHaveBeenCalled();
  });

  it('should destroy component if ngOnDestroy triggered', () => {
    spyOn(component, 'destroy');

    component.routeChangeSub = {unsubscribe: jasmine.createSpy('unsubscribe')};
    component.quizDetailsSub = {unsubscribe: jasmine.createSpy()};

    component.ngOnDestroy();

    expect(component.destroy).toHaveBeenCalled();
    expect(component.quizDetailsSub.unsubscribe).toHaveBeenCalled();
    expect(component.routeChangeSub.unsubscribe).toHaveBeenCalled();
  });

  describe('isQuizPopupAvailable', () => {
    it('should return true if quiz popup is available for route', () => {
      const routes = ['/', '/horse-racing/*', '/home/live-stream'];
      const url = '/horse-racing/';
      const result = component.isQuizPopupAvailable(routes, url);

      expect(result).toBeTruthy();
    });

    it('should return false if quiz popup is not available for route url', () => {
      const routes = ['/', '/horse-racing/*', '/sport/tennis/matches'];
      const url = '/live-stream/';
      const result = component['isQuizPopupAvailable'](routes, url);

      expect(result).toBeFalsy();
    });

    it('should check if current url is in availables pool', () => {
      const routes = ['/', '/horse-racing/*', '/sport/tennis/matches'];
      const url1 = '/';
      const url2 = '/horse-racing/features';
      const url3 = '/sport/tennis/matches';


      const url4 = '/live-stream/';
      const url5 = '/sport/football/matches/today/';
      const url6 = '/greyhound-racing/today/';

      expect(component['isQuizPopupAvailable'](routes, url1)).toBeTruthy();
      expect(component['isQuizPopupAvailable'](routes, url2)).toBeTruthy();
      expect(component['isQuizPopupAvailable'](routes, url3)).toBeTruthy();

      expect(component['isQuizPopupAvailable'](routes, url4)).toBeFalsy();
      expect(component['isQuizPopupAvailable'](routes, url5)).toBeFalsy();
      expect(component['isQuizPopupAvailable'](routes, url6)).toBeFalsy();
    });
  });

  describe('handleQuizPopupDisplay', () => {
    const quizId = 'quizId';
    beforeEach(() => {
      component.isQuizPopupAvailable = jasmine.createSpy().and.returnValue(true);
      component.user.status = true;
      component.renderQuizDialog = jasmine.createSpy();
      component.popupTimer = 100;
    });

    it('should display quiz dialog if user logged in, dialog is available and quiz is enabled', () => {
      component.handleQuizPopupDisplay();

      expect(component.storageService.set).not.toHaveBeenCalled();
      expect(component.isQuizPopupAvailable).toHaveBeenCalled();
      expect(component.renderQuizDialog).toHaveBeenCalled();
    });

    it('shouldn\'t quiz dialog if user not logged in', () => {
      component.user.status = false;

      component.handleQuizPopupDisplay();

      expect(component.isQuizPopupAvailable).not.toHaveBeenCalled();
      expect(component.questionEngineService.userAnswersExist).not.toHaveBeenCalled();
      expect(component.renderQuizDialog).not.toHaveBeenCalled();
    });

    it('shouldn\'t display quiz dialog if user choose don\'t show me again or finished quiz', () => {
      component.questionEngineService.userAnswersExist = jasmine.createSpy('userAnswersExist').and.returnValue(of(true));

      component.handleQuizPopupDisplay();

      expect(component.questionEngineService.userAnswersExist).toHaveBeenCalled();
      expect(component.storageService.set).toHaveBeenCalled();
      expect(component.renderQuizDialog).not.toHaveBeenCalled();
    });

    it('shouldn\'t display quiz dialog if quiz is set as don\'t showAgain', () => {
      component.storageService.get = jasmine.createSpy().and.returnValue({ quizId: quizId, showAgain: false, username : username});
      component.handleQuizPopupDisplay();

      expect(component.questionEngineService.userAnswersExist).not.toHaveBeenCalled();
      expect(component.isQuizPopupAvailable).toHaveBeenCalled();
      expect(component.renderQuizDialog).not.toHaveBeenCalled();
    });

    it('should display quiz dialog if new quiz is setted to popup', () => {
      component.quizPopupSettings.quizId = 'newQuiz';
      component.storageService.get = jasmine.createSpy().and.returnValue({ quizId: quizId, showAgain: false});

      component.handleQuizPopupDisplay();
      expect(component.questionEngineService.userAnswersExist).toHaveBeenCalled();
      expect(component.isQuizPopupAvailable).toHaveBeenCalled();
      expect(component.renderQuizDialog).toHaveBeenCalled();
    });

    it('shouldn\'t display quiz dialog if list of available pageUrls is empty', () => {
      component.quizPopupSettings.pageUrls = '';
      component.isQuizPopupAvailable = jasmine.createSpy('isQuizPopupAvailable').and.returnValue(false);

      component.handleQuizPopupDisplay();

      expect(component.questionEngineService.userAnswersExist).not.toHaveBeenCalled();
      expect(component.isQuizPopupAvailable).toHaveBeenCalled();
      expect(component.renderQuizDialog).not.toHaveBeenCalled();

      expect(component.isQuizPopupAvailable).toHaveBeenCalledWith(
        component.quizPopupSettings.pageUrls.split(','),
        component.router.url
      );
    });

    it('shouldn\'t display quiz dialog if list of available pageUrls not exist', () => {
      component.quizPopupSettings.pageUrls = null;
      component.isQuizPopupAvailable = jasmine.createSpy('isQuizPopupAvailable').and.returnValue(false);

      component.handleQuizPopupDisplay();

      expect(component.questionEngineService.userAnswersExist).not.toHaveBeenCalled();
      expect(component.isQuizPopupAvailable).toHaveBeenCalledWith(
        [''],
        component.router.url
      );
      expect(component.isQuizPopupAvailable).toHaveBeenCalled();
      expect(component.renderQuizDialog).not.toHaveBeenCalled();
    });

    it('should display quiz dialog if quiz is available and quiz is not passed', () => {
      component.handleQuizPopupDisplay();

      expect(component.questionEngineService.userAnswersExist).toHaveBeenCalled();
      expect(component.isQuizPopupAvailable).toHaveBeenCalled();
      expect(component.renderQuizDialog).toHaveBeenCalled();
    });

    it('shouldn\'t dislay quiz dialog if user is not logged in', () => {
      component.user.username = null;
      component.user.status = false;
      component.handleQuizPopupDisplay();

      expect(component.questionEngineService.userAnswersExist).not.toHaveBeenCalled();
    });

    it('shouldn\'t dislay quiz dialog if quizPopupSettings is empty', () => {
      component.quizPopupSettings = null;
      component.handleQuizPopupDisplay();

      expect(component.questionEngineService.userAnswersExist).not.toHaveBeenCalled();
    });

    it('should clearTimeout if popupTimer is not empty', () => {
      component.handleQuizPopupDisplay();

      expect(component.windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
    });

    it('shouldn\'t call clearTimeout if popupTimer is not empty', () => {
      component.popupTimer = null;
      component.handleQuizPopupDisplay();

      expect(component.windowRef.nativeWindow.clearTimeout).not.toHaveBeenCalled();
    });

    it('should display quiz dialog if user is logged in and has available quiz', () => {
      component.handleQuizPopupDisplay();

      expect(component.questionEngineService.userAnswersExist).toHaveBeenCalled();
      expect(component.renderQuizDialog).toHaveBeenCalled();
    });

    it('should set previous url', () => {
      router.url = '/home';
      component.handleQuizPopupDisplay();
      expect(component['previousUrl']).toBe(router.url);
    });
  });
});
