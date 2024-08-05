import { ProfitLossLinkComponent } from './profit-loss-link.component';

describe('VanillaProfitLossLinkComponent', () => {
  let rtsLinkService,
      productHomepagesConfig,
      coralSportsConfig,
      component: ProfitLossLinkComponent,
      link,
      casinoMyBetsIntegratedService,
      windowRef;

  beforeEach(() => {
    productHomepagesConfig = {
      portal: jasmine.createSpy()
    };
    coralSportsConfig = {
      rtsLink: jasmine.createSpy()
    };

    rtsLinkService = {
      getRtsLink: {
        coralSportsConfig,
        productHomepagesConfig,
      },
    };

    windowRef = {
      nativeWindow: {
        location: {
         href:  jasmine.createSpy()
        }
      }
    };

    casinoMyBetsIntegratedService = {
      goToSportsCTABtnClick: jasmine.createSpy(),
      confirmationPopUpClick: jasmine.createSpy()
    };

    component = new ProfitLossLinkComponent(rtsLinkService, casinoMyBetsIntegratedService, windowRef);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should gnerate RTS link', () => {
    component['generateRtsLink'] = jasmine.createSpy();
    rtsLinkService['getRtsLink'] = jasmine.createSpy();
    component.ngOnInit();
    expect(component['generateRtsLink']).toHaveBeenCalled();
  });

  it('should add link to rtsLink variable', () => {
    link = 'http://test.com';
    rtsLinkService['getRtsLink'] = jasmine.createSpy('getRtsLink').and.returnValue(link);
    component.ngOnInit();
    expect(component['rtsLink']).toBe(link);
    expect(component['generateRtsLink']()).toEqual(link);
  });

  describe('#profitLossClick', () => {
    it('isMyBetsInCasino is true and showLeavingCasinoDialog is false', () => {
      component.isMyBetsInCasino = true;
      component.showLeavingCasinoDialog = false;
      component.profitLossClick();
      expect(component['casinoMyBetsIntegratedService'].goToSportsCTABtnClick).toHaveBeenCalled();
    });

    it('isMyBetsInCasino false and showLeavingCasinoDialog false to location.href',() => {
      component.isMyBetsInCasino = false;
      component.showLeavingCasinoDialog = false;
      component.rtsLink = 'http://test.com';
      component.profitLossClick();
      expect(component.rtsLink).not.toBeNull();
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
