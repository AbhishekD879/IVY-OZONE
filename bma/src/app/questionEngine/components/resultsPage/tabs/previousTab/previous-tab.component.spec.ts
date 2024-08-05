import { PreviousTabComponent } from './previous-tab.component';
import { of, Subscription, throwError } from 'rxjs';
import { prevQuizModel, QEData } from '../../../../services/qe-mock-data.mock';
import { QuestionEngineService } from '@app/questionEngine/services/question-engine/question-engine.service';

describe('PreviousTabComponent', () => {
  const { qeData } = new QEData();
  let component: PreviousTabComponent;
  let questionEngineService;

  questionEngineService = {
    qeData,
    pipe: jasmine.createSpy('pipe'),
    error: jasmine.createSpy('error').and.callThrough(),
    subscribe: jasmine.createSpy('subscribe').and.returnValue(of(prevQuizModel)),
    triggerFatalError: jasmine.createSpy('triggerFatalError'),
    handleNoPrevGamesContent: jasmine.createSpy('handleNoPrevGamesContent').and.returnValue({
      title: 'title',
      subtitle: 'subtitle'
    }),
    getPrevQuizes: jasmine.createSpy('getPrevQuizes').and.returnValue(of(prevQuizModel)),
    mapPrevQuizzesResponseOnComponentModel: jasmine.createSpy('mapPrevQuizzesResponseOnComponentModel').and.returnValue(of(prevQuizModel)),
    trackEventGA: jasmine.createSpy('trackEventGA'),
    trackPageViewGA: () => {}
  };

  const subscription: Subscription = new Subscription();

  beforeEach(() => {
    component = new PreviousTabComponent(
      questionEngineService as QuestionEngineService
    );
    component['subscription'] = subscription;
    component.qeData = qeData;
    component['getPrevQuizesData'] = jasmine.createSpy('getPrevQuizesData');
  });

  describe('Should init PreviousTabComponent', () => {
    it('Should create a component', () => {
      component.ngOnInit();
      expect(component).toBeTruthy();
    });

    it('should create component & DO NOT show no previous Results message', () => {
      component.ngOnInit();

      expect(component).toBeTruthy();
      expect(component.showNoResultsWarning).toEqual(false);
    });

    it('should create component & show no previous Results message', () => {
      component.qeData = {
        ...qeData,
        previous: []
      };
      component.ngOnInit();
      expect(component).toBeTruthy();
      expect(component.loading).toEqual(false);
      expect(component.showNoResultsWarning).toEqual(true);
    });

    it('Should call for triggerFatalError when response is failed', () => {
      const customQEData = {
        baseQuiz: null,
        previous: null,
        previousCount: 0
      };
      questionEngineService = {
        ...questionEngineService,
        getPrevQuizes: jasmine.createSpy('getPrevQuizes').and.returnValue(throwError('error'))
      };
      const myComponent = new PreviousTabComponent(
        questionEngineService as QuestionEngineService,
      );

      myComponent.ngOnInit();
      myComponent.qeData = customQEData;
      myComponent['getPrevQuizesData'](5, 3);

      expect(myComponent['questionEngineService'].triggerFatalError).toHaveBeenCalled();
    });
  });

  describe('Should call for onShowMoreClick function', () => {
    it('should show more prevQuizzes', () => {
      component.ngOnInit();
      component.onShowMoreClick();

      expect(component['getPrevQuizesData']).toHaveBeenCalled();
      expect(component.showMoreBtn).toEqual(true);
    });

    it('should not Show more prevQuizzes', () => {
      const customQEData = {
          ...qeData,
          previous: [],
          previousCount: 0
      };
      const prevQuizzes = {
        totalRecords: 0,
        quizzes: []
      };

      questionEngineService = {
        ...questionEngineService,
        customQEData,
        getPrevQuizes: jasmine.createSpy('getPrevQuizes').and.returnValue(of(prevQuizzes))
      };
      const componentCustom = new PreviousTabComponent(
        questionEngineService as QuestionEngineService
      );
      componentCustom.qeData = customQEData;
      componentCustom['previousCount'] = 0;
      componentCustom.ngOnInit();
      componentCustom.onShowMoreClick();

      expect(component['getPrevQuizesData']).not.toHaveBeenCalled();
    });

    describe('Test for `Show More `button', () => {
      it('should show `Show More` button', () => {
        component.ngOnInit();
        expect(component.showMoreBtn).toEqual(true);
      });

      it('should NOT show `Show More` button', () => {
        const prevQuizzes = {
          totalRecords: 0,
          quizzes: []
        };
        component['questionEngineService'] = {
        ...questionEngineService,
            getPrevQuizes: jasmine.createSpy('getPrevQuizes').and.returnValue(of(prevQuizzes))
        };
        component.qeData = qeData;
        component.qeData.previousCount = 3;
        component.ngOnInit();
        component.onShowMoreClick();

        expect(component.showMoreBtn).toBeFalsy();
      });
    });

    it('should hide `Show More` button', () => {
      component['previousCount'] = 3;
      component.pageNumber = 4;
      component.ngOnInit();
      component.hasNextPage();
      expect(component.showMoreBtn).toEqual(false);
    });
  });

  it('should call ngOnDestroy', () => {
    component['subscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();

    expect(component['subscription']['unsubscribe']).toHaveBeenCalled();
  });

  it('test for trackByFn', () => {
    const index = 5;
    const output = '5';
    expect(component.trackByFn(index)).toBe(output);
  });
});
