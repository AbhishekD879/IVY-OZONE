import { of } from 'rxjs';

import { QuestionEngineMainComponent } from './question-engine-main.component';

describe('Desktop QuestionEngine Main Component', () => {
  let bonusSuppressionService;

  const data = null;
  const userService = {} as any;
  const router = {
    url: 'qe/correct4/splash',
    events: of({})
  } as any;

  const awsService = {
    API: {},
    addAction: jasmine.createSpy('addAction'),
    errorLog: jasmine.createSpy('errorLog')
  } as any;

  const pubSubService = {
    API: {
      TOGGLE_MOBILE_HEADER_FOOTER: 'TOGGLE_MOBILE_HEADER_FOOTER',
      QE_FATAL_ERROR: 'QE_FATAL_ERROR'
    },
    subscribe: jasmine.createSpy('subscribe'),
    unsubscribe: jasmine.createSpy('unsubscribe'),
    publish: jasmine.createSpy('publish')
  } as any;

  const questionEngineService = {
    qeData: null,
    getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(data)),
    mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(data)),
    checkGameData: jasmine.createSpy('checkGameData'),
    setQEDataUptodateStatus: jasmine.createSpy('setQEDataUptodateStatus'),
    pipe: jasmine.createSpy('pipe'),
    error: jasmine.createSpy('error').and.callThrough(),
  } as any;

  const deviceService = {
    isMobile: true
  } as any;

  const localeService = {
    getString: jasmine.createSpy('getString'),
  }as any;

   const component: QuestionEngineMainComponent= new QuestionEngineMainComponent(
    pubSubService,
    deviceService,
    questionEngineService,
    awsService,
    localeService,
    router,
    bonusSuppressionService
  );

  describe('Testing `getQuizName` method', () => {
    it('should create component and return correct4 if url `qe/correct4/splash`', () => {
      component.ngOnInit();
      expect(component).toBeTruthy();

      component.getQuizName();
      expect(component.quizName).toEqual('correct4');
    });

    it('should return `` if url `/`', () => {
      component['router'] = {
        ...router,
        url: '/',
        events: of({})
      };
      expect(component.getQuizName()).toEqual('');
    });

    it('should return `` if url `/question-engine/smart-money`', () => {
      component['router'] = {
        ...router,
        url: '/question-engine/smart-money',
        events: of({})
      };
      expect(component.getQuizName()).toEqual('smart-money');
    });
  });
});
