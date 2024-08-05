import { QuestionEngineMainComponent } from './question-engine-main.component';
import { Observable, of, throwError, Subscription } from 'rxjs';
import { NavigationEnd } from '@angular/router';
import { quizItem } from '@app/questionEngine/services/qe-mock-data.mock';
import any = jasmine.any;

describe('QuestionMainComponent', () => {
  let component: QuestionEngineMainComponent;
  let pubSubService;
  let deviceService;
  let questionEngineService;
  let awsService;
  let localeService;
  let router;
  let bonusSuppressionService;
  let routeChangeListener: Subscription;
  let quizHistoryListener: Subscription;
  beforeEach(() => {
    const data = null;

    awsService = {
      API: {},
      addAction: jasmine.createSpy('addAction'),
      errorLog: jasmine.createSpy('errorLog')
    };

    pubSubService = {
      API: {
        TOGGLE_MOBILE_HEADER_FOOTER: 'TOGGLE_MOBILE_HEADER_FOOTER',
        QE_FATAL_ERROR: 'QE_FATAL_ERROR'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };

    questionEngineService = {
      qeData: null,
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(data)),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(data)),
      checkGameData: jasmine.createSpy('checkGameData'),
      pipe: jasmine.createSpy('pipe'),
      resetCheckForAnonymousDataValue: jasmine.createSpy('resetCheckForAnonymousDataValue'),
      setQEDataUptodateStatus: jasmine.createSpy('setQEDataUptodateStatus'),
      error: jasmine.createSpy('error').and.callThrough(),
    };

    deviceService = {
      isMobile: true
    };

    localeService = {
      getString: jasmine.createSpy('getString'),
    };
    bonusSuppressionService = {
      navigateAwayForRGYellowCustomer: jasmine.createSpy('navigateAwayForRGYellowCustomer'),
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    };
    const ne = new NavigationEnd(0, 'http://foo.bar/latest-quiz', 'http://foo.bar/c4');
    const events = new Observable(observer => {
        observer.next(ne);
        observer.complete();
      });

    router = {
      events,
    };
    routeChangeListener = new Subscription();
    quizHistoryListener = new Subscription();
    component = new QuestionEngineMainComponent(
      pubSubService as any,
      deviceService as any,
      questionEngineService as any,
      awsService as any,
      localeService as any,
      router as any,
      bonusSuppressionService as any
    );
    component['routeChangeListener'] = routeChangeListener;
    component['quizHistoryListener'] = quizHistoryListener;
  });

  it('should create component', () => {
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('should call initComponentData', () => {
    component['initComponentData'] = jasmine.createSpy();
    bonusSuppressionService.checkIfYellowFlagDisabled = jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false)
    pubSubService.subscribe = jasmine.createSpy().and.callFake((arg1, arg2, callback) => callback());
    component.ngOnInit();
    expect(component['initComponentData']).toHaveBeenCalledTimes(2);
  });

  it('should create component and `initComponentData` method', () => {
    quizItem.live = null;
    let checkForAnonymousData = false;
    const myQuestionEngineService = {
      ...questionEngineService,
      qeData: null,
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(quizItem)),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(quizItem)),
      checkGameData: (data, cb) => {
        if (data && !data.live && !data.previous.length) {
          if (checkForAnonymousData) {
            // eslint-disable-next-line
            console.log('call of mocked `triggerFatalError` method');
          } else {
            checkForAnonymousData = true;
            cb(true);
            return true;
          }
        }
      },
      pipe: jasmine.createSpy('pipe'),
      error: jasmine.createSpy('error').and.callThrough(),
    };
    component['questionEngineService'] = myQuestionEngineService;

    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(myQuestionEngineService.getQuizHistory).toHaveBeenCalledWith(true);
  });

  it('should publish error if failed to retrieve data', () => {
    const mockQuestionEngineService = {
      ...questionEngineService,
      checkGameData: jasmine.createSpy('checkGameData'),
      setQEDataUptodateStatus: jasmine.createSpy('setQEDataUptodateStatus'),
      getQuizHistory: () => {
        return of({data: 'any data'});
      }
    };

    spyOn(mockQuestionEngineService, 'getQuizHistory').and.callFake(() => {
      return throwError(new Error('Fake error'));
    });

    component['questionEngineService'] = mockQuestionEngineService;

    component.ngOnInit();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QE_FATAL_ERROR, any(Object));
  });

  it('should not call awsService on ngOnInit pubSubService.API.QE_FATAL_ERROR when error not defined', () => {
    const errorMessage = 'error';
    const error = null;

    component['pubSubService'].subscribe = jasmine.createSpy('subscribe').and.callFake((name, api, fn) => {
      if (api === pubSubService.API.QE_FATAL_ERROR) {
        fn(errorMessage, error);

        expect(component.errorMessage).toEqual(errorMessage);
        expect(awsService.errorLog).not.toHaveBeenCalled();
      }
    });

    component.ngOnInit();
  });

  it('should call on ngOnInit pubSubService.API.QE_FATAL_ERROR, call awsService ', () => {

    const errorMessage = 'error';
    const error = {error: 'error'};

    component['pubSubService'].subscribe = jasmine.createSpy('subscribe').and.callFake((name, api, fn) => {
      if (api === pubSubService.API.QE_FATAL_ERROR) {
        fn(errorMessage, error);
        expect(component.errorMessage).toEqual(errorMessage);
        expect(awsService.errorLog).toHaveBeenCalled();
        expect(awsService.addAction).toHaveBeenCalled();
      }
    });

    component.ngOnInit();
  });

  it('should hide footer & header for mobile', () => {
    component.ngOnInit();

    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, false);
  });

  it('should show footer & header for mobile when ngOnDestroy()', () => {
    component.ngOnDestroy();

    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, true);
  });

});
