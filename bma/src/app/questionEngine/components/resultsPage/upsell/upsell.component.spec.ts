import { UpsellComponent } from './upsell.component';
import { of, throwError } from 'rxjs';
import { QEData } from '@app/questionEngine/services/qe-mock-data.mock';

describe('UpsellComponent', () => {
  const { qeData } = new QEData();
  let component: UpsellComponent;

  const questionEngineService = {
    qeData: qeData,
    isLoginPopupShown: false,
    getQuizHistory: jasmine.createSpy('getQuizHistory').and.returnValue(of(qeData)),
    mapResponseOnComponentModel: jasmine.createSpy('mapResponseOnComponentModel').and.returnValue(of(qeData)),
    resolveCtaButtonText: jasmine.createSpy('resolveCtaButtonText'),
    pipe: jasmine.createSpy('pipe'),
    triggerFatalError: jasmine.createSpy('triggerFatalError'),
    checkPreviousPage: jasmine.createSpy('checkPreviousPage'),
    setQESubmitStatus: jasmine.createSpy('setQESubmitStatus'),
    checkGameData: jasmine.createSpy('checkGameData'),
    error: jasmine.createSpy('error').and.callThrough(),
    subscribe: jasmine.createSpy('subscribe').and.returnValue(of(qeData)),
    addToSlipHandler: jasmine.createSpy('addToSlipHandler').and.returnValue(of()),
    redirectToTab: ''
  } as any;

  const router = {
    navigate: jasmine.createSpy('navigate'),
    navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue(''),
  };

  const localeService = {
    getString: jasmine.createSpy('getString').and.returnValue('upsellTryAgain'),
  };

  const gtmService = {
    push: jasmine.createSpy('push').and.returnValue('')
  };

  beforeEach(() => {
    component = new UpsellComponent(
      questionEngineService as any,
      router as any,
      localeService as any,
      gtmService as any
    );
    component.qeData = qeData;
  });

  it('should create component', () => {
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('should set upsell title to `Event Name`', () => {
    component.ngOnInit();
    expect(component.upsellTitle).toEqual('Man Unt vs Lviv');
  });

  it('should Format upsell title without Pipes', () => {
    qeData.baseQuiz.eventDetails.eventName = '|East Jay| |vs| |Lake Mark|';
    component.ngOnInit();
    expect(component.upsellTitle).toEqual('East Jay vs Lake Mark');
  });

  it('should NOT fail if NO Event Name value passed to Format upsell title without Pipes', () => {
    qeData.baseQuiz.eventDetails.eventName = null;
    component.ngOnInit();
    expect(component.upsellTitle).toEqual(null);
  });

  it('should set upsell title to `Selection Name`', () => {
    const today = new Date();
    const tomorrow = new Date();
    tomorrow.setDate(today.getDate() + 1);
    qeData.baseQuiz.eventDetails.startTime = tomorrow;
    component.ngOnInit();
    expect(component.upsellTitle).toEqual('some dynamic upsell');
  });

  it('should process `betInPlayHandler` method', () => {
    component.ngOnInit();
    component.betInPlayHandler();
    expect(router.navigateByUrl).toHaveBeenCalledWith('/event/10050712');
  });

  it('should process `addToSlip` method', () => {
    component['questionEngineService'] = {
      ...questionEngineService,
      addToSlipHandler: jasmine.createSpy('addToSlipHandler').and.returnValue(of({data: 'data'})),
    };

    component.qeData = qeData;
    expect(component.processingAddToSlip).toEqual(false);
    component.ngOnInit();
    component.addToSlip();
    expect(component['questionEngineService'].addToSlipHandler).toHaveBeenCalledWith('546121881');
    expect(component.upsellData.betNowCTA).toEqual('string');
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('should process `addToSlip` method and fail', () => {
    component['questionEngineService'] = {
      ...questionEngineService,
      addToSlipHandler: jasmine.createSpy('addToSlipHandler').and.returnValue(throwError('error'))
    };
    component.qeData = qeData;

    expect(component.processingAddToSlip).toEqual(false);
    component.ngOnInit();
    component.addToSlip();
    expect(component.upsellData.betNowCTA).toEqual('upsellTryAgain');
  });

  describe('Testing `ngOnDestroy`', () => {
    it('should call `addToSlipHandler` unsubscribe', () => {
      component['addToSlipHandler'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();
      expect(component['addToSlipHandler']['unsubscribe']).toHaveBeenCalled();
    });

    it('should NOT call `addToSlipHandler` unsubscribe', () => {
      component['addToSlipHandler'] = null as any;
      component.ngOnDestroy();
    });
  });

  describe('Testing `calculateReturns`', () => {
    it('should calc in proper way', () => {
      component['calculateReturns'](1.4523423);
      expect(component.upsellReturn).toEqual('upsellTryAgain14.52');

      component['calculateReturns'](1.43);
      expect(component.upsellReturn).toEqual('upsellTryAgain14.30');

      component['calculateReturns'](1.00026);
      expect(component.upsellReturn).toEqual('upsellTryAgain10');
    });
  });
});
