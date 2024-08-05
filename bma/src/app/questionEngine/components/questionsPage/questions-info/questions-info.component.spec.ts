import { QuestionsInfoComponent } from './questions-info.component';
import any = jasmine.any;

describe('QuestionInfoComponent', () => {
  let component: QuestionsInfoComponent;
  let questionEngineService;
  let pubSubService;

  beforeEach(() => {
    questionEngineService = {
      getQuizHistory: jasmine.createSpy('getQuizHistory'),
      qeData: {baseQuiz: jasmine.createSpy('qeData')}
    };

    pubSubService = {
      API: {
        QE_FATAL_ERROR: 'QE_FATAL_ERROR'
      },
      publish: jasmine.createSpy('publish')
    };

    component = new QuestionsInfoComponent(
      questionEngineService as any,
      pubSubService as any
    );
  });

  it('should create QuestionInfoComponent with data', () => {
    component.ngOnInit();
    expect(component.qeData).toBeDefined();
  });

  it('should publish fatal error if no data', () => {
    delete component['questionEngineService'].qeData;

    component.ngOnInit();
    expect(component.qeData).not.toBeDefined();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.QE_FATAL_ERROR, any(Object));
  });
});
