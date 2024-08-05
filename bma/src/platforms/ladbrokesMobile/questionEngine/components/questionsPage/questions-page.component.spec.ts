import { QuestionsPageComponent } from './questions-page.component';
import { of } from 'rxjs';

describe('QuestionsEngine Page Component', () => {
   const router = {
    navigateByUrl: jasmine.createSpy('navigateByUrl'),
    events: of({})
  };

   const pubSubService = {
    API: {
      QE_FATAL_ERROR: 'QE_FATAL_ERROR'
    },
    publish: jasmine.createSpy('publish')
  };

   const dialogService = {
    API: jasmine.createSpy('API'),
    openDialog: jasmine.createSpy('openDialog'),
    closeDialog: jasmine.createSpy('closeDialog'),
  };
   const componentFactoryResolver = {
    resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue({ name: 'InfoDialogComponent' })
  };

   const questionEngineService = {
    qeData: {
      baseQuiz: {
        exitPopup: {
          iconSvgPath: '3d3ce10c2aa2.svg',
          closeCTAText: 'EXIT GAME',
          description: 'Your selections will not be saved if you exit  without submitting them',
          header: 'Are you sure?',
          submitCTAText: 'KEEP PLAYING',
        },
        quizConfiguration: {
          showExitPopup: true
        }
      }
    },
    trackPageViewGA: () => {},
    trackEventGA: () => {},
    checkIfShouldRedirectGuest: jasmine.createSpy('checkIfShouldRedirectGuest').and.returnValue(false)
  };

   const localeService = {
    getString: jasmine.createSpy('getString')
  };

  const component: QuestionsPageComponent = new QuestionsPageComponent(
    router as any,
    questionEngineService as any,
    pubSubService as any,
    dialogService as any,
    componentFactoryResolver as any,
    localeService as any
  );

  it('should call exit popup', () => {
    component.ngOnInit();
    component.openGoToSplashOrContinueDialog();

    expect(dialogService.openDialog).toHaveBeenCalled();

  });

});
