import { of } from 'rxjs';
import { BetslipTabsComponent } from './betslip-tabs.component';

describe('BetslipTabsComponent', () => {
  let component: BetslipTabsComponent;
  let betslipTabsService;
  let location;
  let userService;
  let betHistoryMainService;
  const tabs = [
    { title: 'Cash Out', name: 'Cash Out', id: 1, url: '/cashout' },
    { title: 'Open Bets', name: 'Open Bets', id: 2, url: '/open-bets' },
    { title: 'Bet History', name: 'Bet History', id: 3, url: '/bet-history' }
  ];
  const activeTab = { title: 'Cash Out', name: 'Cash Out', id: 1, url: '/cashout' };

  beforeEach(() => {
    betslipTabsService = {
      getTabsList: jasmine.createSpy().and.returnValue(of(tabs))
    };
    location = {
      path: jasmine.createSpy().and.returnValue('/cashout')
    } as any;
    userService = {
      status: true
    };

    betHistoryMainService = {
      showFirstBet: jasmine.createSpy('showFirstBet').and.returnValue({})
    };

    component = new BetslipTabsComponent(betslipTabsService, location, userService, betHistoryMainService);
  });


  describe('#mainInit', () => {
    it('should set component betslipTabs property', () => {
      component.ngOnInit();
      expect(component.betslipTabs).toEqual(tabs);
      expect(component.initialised).toBeTruthy();
      expect(component['getTabsSubscription']).toBeDefined();
    });

    it('should set active tab', () => {
      component.ngOnInit();
      expect(component.activeTab).toEqual(activeTab);
    });

    it('should set component isLoggedIn property to true', () => {
      component.ngOnInit();
      expect(component.isLoggedIn).toBeTruthy();
    });

    it('should destroy component and hide it before DOM will be updated', () => {
      component.ngOnInit();

      spyOn(component['getTabsSubscription'], 'unsubscribe');

      component.ngOnDestroy();

      expect(component.initialised).toBeFalsy();
      expect(component['getTabsSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });
});
