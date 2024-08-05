import { TermsConditionsComponent } from './terms-conditions.component';
import { of } from 'rxjs';

describe('TermsConditionsComponent', () => {
  let component: TermsConditionsComponent;
  let cmsService;
  let domTools;
  let router;
  let casinoMyBetsIntegratedService;

  const elementRef = {
    nativeElement: {}
  };

  beforeEach(() => {
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        CashOut: {
          terms: true
        },
        Connect: {
          shopBetHistory: true
        }
      }))
    };
    domTools = {
      closest: jasmine.createSpy()
    };
    router = {
      navigateByUrl: jasmine.createSpy()
    };
    casinoMyBetsIntegratedService = {
      goToSportsCTABtnClick: jasmine.createSpy(),
      confirmationPopUpClick: jasmine.createSpy()
    };

    component = new TermsConditionsComponent(
      cmsService,
      domTools,
      elementRef,
      casinoMyBetsIntegratedService,
      router
    );

    component['elementRef'] = <any>elementRef;
    component.ngOnInit();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(cmsService.getSystemConfig).toHaveBeenCalled();
    expect(domTools.closest).toHaveBeenCalledTimes(1);
    expect(domTools.closest).toHaveBeenCalledWith(elementRef.nativeElement, '#home-betslip-tabs');
  });

  describe('#termsAndConditionsUrlClick', () => {
    it('isMyBetsInCasino is true and showLeavingCasinoDialog is false', () => {
      component.isMyBetsInCasino = true;
      component.showLeavingCasinoDialog = false;
      component.termsAndConditionsUrlClick('/static/ema-terms-conditions');
      expect(component['casinoMyBetsIntegratedService'].goToSportsCTABtnClick).toHaveBeenCalled();
    });

    it('isMyBetsInCasino is false and showLeavingCasinoDialog is false', () => {
      component.isMyBetsInCasino = false;
      component.showLeavingCasinoDialog = false;
      component.termsAndConditionsUrlClick('/static/ema-terms-conditions');
      expect(component['router'].navigateByUrl).toHaveBeenCalled();
    });
  });

  describe('#confirmationDialogClick', () => {
    it('should call confirmationPopUpClick()', () => {
      const event = {
        output: 'userAction',
        value: {
          checkboxValue: true, 
          btnClicked: 'no thanks'
        }
      };
      component.confirmationDialogClick(event);
      expect(component['casinoMyBetsIntegratedService'].confirmationPopUpClick).toHaveBeenCalled();
    });
  });
});
