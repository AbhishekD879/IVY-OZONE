import { DesktopQuestionsPageComponent } from './questions-page.component';
import { of } from 'rxjs';

describe('Desktop QuestionsEngine Page Component', () => {
  let component: DesktopQuestionsPageComponent;

  let router;
  let questionEngineService;
  let pubSubService;
  let dialogService;
  let componentFactoryResolver;
  let localeService;

  beforeEach(() => {

    router = {
      navigateByUrl: jasmine.createSpy(),
      events: of({})
    };

    pubSubService = {
      API: {
        QE_FATAL_ERROR: 'QE_FATAL_ERROR'
      },
      publish: jasmine.createSpy()
    };

    dialogService = {
      API: jasmine.createSpy(),
      openDialog: jasmine.createSpy(),
      closeDialog: jasmine.createSpy(),
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy().and.returnValue({ name: 'InfoDialogComponent' })
    };

    questionEngineService = {
      qeData: {
        baseQuiz: {
          exitPopup: {
            iconSvgPath: '3d3ce10c2aa2.svg',
            closeCTAText: 'EXIT GAME',
            description: 'Your selections will not be saved if you exit  without submitting them',
            header: 'Are you sure?',
            submitCTAText: 'KEEP PLAYING',
          }
        }
      },
      trackPageViewGA: () => {},
      trackEventGA: () => {},
      toggleSubmitNotification: jasmine.createSpy(),
      checkPreviousPage: jasmine.createSpy(),
      checkIfShouldRedirectGuest: jasmine.createSpy().and.returnValue(false)
    };

    localeService = {
      getString: jasmine.createSpy()
    };

    component = new DesktopQuestionsPageComponent(
      router as any,
      questionEngineService as any,
      pubSubService as any,
      dialogService as any,
      componentFactoryResolver as any,
      localeService as any
    );
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
