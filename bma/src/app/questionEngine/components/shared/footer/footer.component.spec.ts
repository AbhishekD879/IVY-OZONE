import { FooterComponent } from './footer.component';
import { of } from 'rxjs';
import { QuestionEngineModel } from '@app/questionEngine/models/questionEngineModel.model';
import any = jasmine.any;
import { QuestionEngineQuizModel } from '@app/questionEngine/models/questionEngineQuiz.model';

describe('FooterComponent', () => {
  let component: FooterComponent;
  const data = 'info';

  const pubSubService = {
    API: {
      TOGGLE_MOBILE_HEADER_FOOTER: 'TOGGLE_MOBILE_HEADER_FOOTER',
      QE_FATAL_ERROR: 'QE_FATAL_ERROR'
    },
    publish: jasmine.createSpy('publish')
  };

  const router = {
    navigateByUrl: jasmine.createSpy('navigateByUrl')
  };

  const questionEngineService = {
    qeData: {
      baseQuiz: {
        sourceId: '/v3'
      }
    },
    resolvePath: jasmine.createSpy('resolvePath').and.returnValue('/qe/cash_v3'),
    getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(data)),
    mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel')
      .and.returnValue(of(data)),
    trackEventGA: () => {}
  } as any;

  const windowRefService = {
    nativeWindow: {
      setTimeout: jasmine.createSpy('setTimeout').and.callFake((cb) => cb()),
    }
  };

  beforeEach(() => {
    component = new FooterComponent(
      questionEngineService as any,
      router as any,
      pubSubService as any,
      windowRefService as any
    );
  });

  it('should create component', () => {
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('should init component and set data if it`s not come', () => {
    component.ngOnInit();

    expect(component.qeData).toEqual(questionEngineService.qeData.baseQuiz);
  });

  it('should init component and set data which has been existed before', () => {
    const customData = 'test';

    const customQuestionEngineService = {
      geData: customData,
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(customData)),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(customData)),
    };

    const customComponent = new FooterComponent(
      customQuestionEngineService as any,
      router as any,
      pubSubService as any,
      windowRefService as any
    );
    customComponent.ngOnInit();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QE_FATAL_ERROR, any(Object));
  });

  it('should init component and publish error if no data', () => {
    const customData = 'test';

    const customQuestionEngineService = {
      geData: '',
      getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(customData)),
      mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(customData)),
    };

    const customComponent = new FooterComponent(
      customQuestionEngineService as any,
      router as any,
      pubSubService as any,
      windowRefService as any
    );
    customComponent.ngOnInit();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QE_FATAL_ERROR, any(Object));
  });

  it('should init component and init data', () => {
    const customData = new QuestionEngineModel();
    customData.baseQuiz = new QuestionEngineQuizModel();

    const customQuestionEngineService = {
      qeData: customData
    };

    const customComponent = new FooterComponent(
      customQuestionEngineService as any,
      router as any,
      pubSubService as any,
      windowRefService as any
    );
    customComponent.ngOnInit();
    expect(customComponent.qeData).toEqual(customData.baseQuiz);
  });

  it('should redirect link', () => {
    const link = {
      title: 'title',
      relativePath: 'faq',
      description: 'description',
    };
    const redirectUrl = '/qe/cash_v3/info/' + `${link.relativePath}`;

    component.ngOnInit();
    component.redirectLink(link, 1);

    expect(router.navigateByUrl).toHaveBeenCalledWith(redirectUrl);
    expect(component.clickedItem).toEqual(1);
  });

  it('trackByFn', () => {
    const index = 5;
    const output = '5';
    expect(component.trackByFn(index)).toBe(output);
  });

});
