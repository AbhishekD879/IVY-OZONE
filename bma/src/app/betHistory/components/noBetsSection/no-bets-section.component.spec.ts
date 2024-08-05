import { NoBetsSectionComponent } from './no-bets-section.component';
import { Subject } from 'rxjs';

describe('NoBetsSectionComponent', () => {
  let component: NoBetsSectionComponent;
  let casinoMyBetsIntegratedService, locale, windowRef;

  beforeEach(() => {
    casinoMyBetsIntegratedService = {
      noBetsMsgSubj: new Subject<string>(),
      goToSportsCTABtnClick: jasmine.createSpy('goToSportsCTABtnClick'),
      confirmationPopUpClick: jasmine.createSpy('confirmationPopUpClick')
    };

    locale = {
      getString: jasmine.createSpy().and.returnValue('Ladbrokes')
    }
    windowRef = {
      document: {
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue([{
          style: {},
          clientWidth: 274
        }]),
      }
    }
    component = new NoBetsSectionComponent(casinoMyBetsIntegratedService, locale, windowRef);
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should not call next with isMyBetsInCasino false', () => {
      component.isMyBetsInCasino = false;
      const spyOnNext = spyOn(component['casinoMyBetsIntegratedService'].noBetsMsgSubj as Subject<string>, 'next');
      component.ngOnInit();
      expect(spyOnNext).not.toHaveBeenCalled();
    });
  
    it('should call next with isMyBetsInCasino true', () => {
      component.isMyBetsInCasino = true;
      const spyOnNext = spyOn(component['casinoMyBetsIntegratedService'].noBetsMsgSubj as Subject<string>, 'next');
      component.ngOnInit();
      expect(spyOnNext).toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    it('should not call next with isMyBetsInCasino false', () => {
      component.isMyBetsInCasino = false;
      const spyOnNext = spyOn(component['casinoMyBetsIntegratedService'].noBetsMsgSubj as Subject<string>, 'next');
      component.ngOnDestroy();
      expect(spyOnNext).not.toHaveBeenCalled();
    });
  
    it('should call next with isMyBetsInCasino true', () => {
      component.isMyBetsInCasino = true;
      const spyOnNext = spyOn(component['casinoMyBetsIntegratedService'].noBetsMsgSubj as Subject<string>, 'next');
      component.ngOnDestroy();
      expect(spyOnNext).toHaveBeenCalled();
    });
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
  
  describe('#ngAfterViewInit', () => {
    it('lads ngAfterViewInit with clientwidth', () => {
      component.noBetsMessage = "No Open Bets in last 30 days";
      component.ngAfterViewInit();
      const dataElement = windowRef.document.querySelectorAll('.no-bets-msg.lads-text');
      expect(dataElement[0].style.padding).toBe('0 calc((100% - 245px) / 2)'); 
    });

    it('lads ngAfterViewInit with clientwidth 370 and date Range Message', () => {
      component.noBetsMessage = "No Open Bets in specified date range";
      windowRef.document.querySelectorAll.and.returnValue( [{ style: {},
            clientWidth: 360}])
      component.ngAfterViewInit();
      const dataElement = windowRef.document.querySelectorAll('.no-bets-msg.lads-text');
      expect(dataElement[0].style.padding).toBe('0 calc((100% - 240px) / 2)');  
    });

    it('lads ngAfterViewInit with clientwidth 370 and X days Message', () => {
      component.noBetsMessage = "No Open Bets in last 30 days";
      windowRef.document.querySelectorAll.and.returnValue( [{ style: {},
            clientWidth: 360}])
      component.ngAfterViewInit();
      const dataElement = windowRef.document.querySelectorAll('.no-bets-msg.lads-text');
      expect(dataElement[0].style.padding).toBe('0 calc((100% - 230px) / 2)'); 
    });

    it('coral ngAfterViewInit with clientwidth 370 and date Range Message', () => {
      component.noBetsMessage = "No Open Bets in specified date range";
      windowRef.document.querySelectorAll.and.callFake(x=>{
        if(x==='.no-bets-msg.lads-text')
        {
          return [];
        }else if(x==='.no-bets-msg') {
          return [{ style: {padding:0},
            clientWidth: 360}]
        }
      });
      const dataElement = windowRef.document.querySelectorAll('.no-bets-msg');
      component.ngAfterViewInit();
      expect(dataElement[0].style.padding).toBeDefined;
    });

    it('coral ngAfterViewInit with clientwidth 370 and X days Message', () => {
      component.noBetsMessage = "No Open Bets in last 30 days";
      windowRef.document.querySelectorAll.and.callFake(x=>{
        if(x==='.no-bets-msg.lads-text')
        {
          return [];
        }else if(x==='.no-bets-msg') {
          return [{ style: {padding:0},
            clientWidth: 360}]
        }
      });
      const dataElement = windowRef.document.querySelectorAll('.no-bets-msg');
      component.ngAfterViewInit();
      expect(dataElement[0].style.padding).toBeDefined;
    });

    it('coral ngAfterViewInit with clientwidth 300', () => {
      component.noBetsMessage = "No Open Bets in specified date range";
      windowRef.document.querySelectorAll.and.callFake(x=>{
        if(x==='.no-bets-msg.lads-text')
        {
          return [];
        }else if(x==='.no-bets-msg') {
          return [{ style: {padding:0},
            clientWidth: 274}]
        }
      });
      const dataElement = windowRef.document.querySelectorAll('.no-bets-msg');
      component.ngAfterViewInit();
      expect(dataElement[0].style.padding).toBeDefined; 
    });
  });

});
