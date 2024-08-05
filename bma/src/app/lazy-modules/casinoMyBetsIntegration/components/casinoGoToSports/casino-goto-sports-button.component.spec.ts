import { Subject } from 'rxjs';
import { CasinoGoToSportsComponent } from './casino-goto-sports-button.component';

describe('CasinoGoToSportsComponent', () => {
  let component: CasinoGoToSportsComponent;
  let casinoMyBetsIntegratedService;

  beforeEach(() => {
    casinoMyBetsIntegratedService = {
      goToSportsCTABtnClick: jasmine.createSpy('goToSportsCTABtnClick'),
      confirmationPopUpClick: jasmine.createSpy('confirmationPopUpClick'),
      noBetsMsgSubj: new Subject<string>()
    };
    component = new CasinoGoToSportsComponent(casinoMyBetsIntegratedService);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should be called and should subscribe to noBetsMsgSubj', () => {
    component.ngOnInit();
    component['casinoMyBetsIntegratedService'].noBetsMsgSubj.next('you have no open bets');
    expect(component.noBetsMessage).toBe('you have no open bets');
  });

  describe('#goToSportsClick', () => {
    it('goToSportsClick, with showLeavingCasinoDialog as true', () => {
      component.showLeavingCasinoDialog = true;
      component.goToSportsClick();
      expect(component['casinoMyBetsIntegratedService'].goToSportsCTABtnClick).not.toHaveBeenCalled();  
    });

    it('goToSportsClick, with showLeavingCasinoDialog as false', () => {
      component.showLeavingCasinoDialog = false;
      component.goToSportsClick();
      expect(component['casinoMyBetsIntegratedService'].goToSportsCTABtnClick).toHaveBeenCalled();  
    });
  });

  describe('#confirmationDialogClick', () => {
    it('confirmationDialogClick, with event data', () => {
      const event = {
          checkboxValue: true, 
          btnClicked: 'no thanks'
      };
      component.confirmationDialogClick(event);
      expect(component['casinoMyBetsIntegratedService'].confirmationPopUpClick).toHaveBeenCalled();  
    });
  });
});
