
import { of as observableOf } from 'rxjs';
import { tick, fakeAsync } from '@angular/core/testing';
import { ChildActivationStart, ChildActivationEnd } from '@angular/router';

import { BetFilterComponent } from '@app/retail/components/betFilter/bet-filter.component';

describe('BetFilterComponent ', () => {
  let component: BetFilterComponent,
    windowRef,
    asyncLoad,
    betFilterParams,
    router,
    routingState,
    deviceService,
    commandService,
    backButtonService,
    userService, 
    recService

  beforeEach(() => {
    windowRef = {
      document: {
        dispatchEvent: jasmine.createSpy('dispatchEvent'),
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener')
      }
    };
    asyncLoad = {
      loadJsFile: jasmine.createSpy('loadJsFile').and.returnValue(observableOf(null)),
      loadCssFile: jasmine.createSpy('loadCssFile').and.returnValue(observableOf(null))
    };
    betFilterParams = {
      chooseMode: jasmine.createSpy('chooseMode').and.returnValue(observableOf({}))
    };
    router = {
      events: observableOf([]),
      navigate: jasmine.createSpy('navigate'),
      url:'test',
      getCurrentNavigation: jasmine.createSpy('getCurrentNavigation')
    };
    routingState = {
      getCurrentSegment: jasmine.createSpy('getCurrentSegment'),
      getPreviousSegment: jasmine.createSpy('getPreviousSegment')
    };
    deviceService = {};
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync'),
      API: {
        ADD_TO_BETSLIP_BY_OUTCOME_IDS: '@betslipModule/betslip.module#BetslipModule:addToBetSlip'
      }
    };
    backButtonService = {
      redirectToPreviousPage: jasmine.createSpy('redirectToPreviousPage')
    };
    userService = {
      currency: 'GBP'
    };
    recService = {
      addScript : jasmine.createSpy('addScript'),
    };

    component = new BetFilterComponent(
      windowRef,
      asyncLoad,
      betFilterParams,
      router,
      routingState,
      deviceService,
      commandService,
      backButtonService,
      userService,
      recService
    );
    component['tryBootstrapBetFilter']({ mode: 'online' });
  });

  describe('#tryBootstrapBetFilter', () => {
    it('and should use stickyElements true in NOT desktop mode', () => {
      component['deviceService'].isDesktop = false;
      component['tryBootstrapBetFilter']({ mode: 'online' });

      expect(windowRef.document.dispatchEvent)
        .toHaveBeenCalledWith(jasmine.objectContaining({
          detail: { mode: 'online', stickyElements: true, currencyType: userService.currency }
        }));
    });

    it('and should use stickyElements false in desktop mode', () => {
      component['deviceService'].isDesktop = true;
      component['tryBootstrapBetFilter']({ mode: 'online' });

      expect(windowRef.document.dispatchEvent)
        .toHaveBeenCalledWith(jasmine.objectContaining({
          detail: { mode: 'online', stickyElements: false , currencyType: userService.currency }
        }));
    });
  });

  describe('ngOnInit', () => {
        it('should call addScript method ',()=>{
      betFilterParams.params = {couponName:"test"};  
      router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ previousNavigation: { finalUrl:'/betslip/unavailable23' } } as any);  
      component.ngOnInit();
      expect(recService.addScript).toHaveBeenCalled();
    });
    it('should navigate to "/" from shoplocator (shoplocator on back errorpage)', fakeAsync(() => {
      betFilterParams.params = {};
      router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ previousNavigation: { finalUrl:'/shop-locator' } } as any);  
      router.url='/bet-filter?todaymatches';
      component.ngOnInit();
      expect(router.navigate).toHaveBeenCalledWith(['/sport/football/coupons']);
    }));    
    it('should navigate to "/" (shoplocator on back errorpage)', fakeAsync(() => {
      betFilterParams.params = {};
      router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ previousNavigation: { finalUrl:'/betslip/unavailable' } } as any);  
      router.url='/bet-filter?todaymatches';
      component.ngOnInit();
      expect(router.navigate).toHaveBeenCalledWith(['/sport/football/coupons']);
    }));    
    it('should navigate to "/" (hard refresh without coupon name)', fakeAsync(() => {
      betFilterParams.params = {};
      router.getCurrentNavigation = jasmine.createSpy('currentNavigation').and.returnValue({ previousNavigation: { finalUrl:'/betslip/unavailable' } } as any);  
      router.url='/bet-filter';
      component.ngOnInit();
      expect(router.navigate).toHaveBeenCalledWith(['/sport/football/coupons']);
    }));    
    it('should navigate to "/" (canceled)', fakeAsync(() => {
      betFilterParams.params = {couponName:"test"};
      betFilterParams.chooseMode.and.returnValue(observableOf({ cancelled: true }));
      component.ngOnInit();
      tick();
      expect(betFilterParams.chooseMode).toHaveBeenCalledTimes(1);
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    }));

    it('should navigate to "/" (cannot bootstrap params)', fakeAsync(() => {
      betFilterParams.params = {couponName:"test"};
      component.ngOnInit();
      tick();
      expect(betFilterParams.chooseMode).toHaveBeenCalledTimes(1);
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    }));

    it('should not subscribe to choose mode', () => {
      betFilterParams.params = { mode: 'online' };
      component.ngOnInit();
      expect(betFilterParams.chooseMode).not.toHaveBeenCalled();
    });

    it('should not navigate to "/"', fakeAsync(() => {
      betFilterParams.chooseMode.and.returnValue(observableOf({ mode: 'online' }));
      router.url='bet-filter?abc';
      betFilterParams.params = {couponName:"test"};
      component.ngOnInit();
      tick();
      expect(betFilterParams.chooseMode).toHaveBeenCalledTimes(1);
      expect(router.navigate).not.toHaveBeenCalled();
    }));

    it('should listen to "BF_ADD_TO_BETSLIP"', () => {
      betFilterParams.params = {couponName:"test"};      
      component.ngOnInit();
      betFilterParams.params = {couponName:"test"};
      expect(windowRef.document.addEventListener).toHaveBeenCalledWith('BF_ADD_TO_BETSLIP', jasmine.any(Function));
    });

    it('should listen to "REDIRECT_TO_PREV_PAGE_BET_FILTER"', () => {
      betFilterParams.params = {couponName:"test"};      
      component.ngOnInit();
      expect(windowRef.document.addEventListener).toHaveBeenCalledWith('REDIRECT_TO_PREV_PAGE_BET_FILTER', jasmine.any(Function));
    });
  });

  describe('ngOnInit (DESTROY_BET_FILTER)', () => {
    beforeEach(() => {
      windowRef.document.dispatchEvent.calls.reset();
    });

    it('should dispatch event', fakeAsync(() => {
      router.events = observableOf(new ChildActivationStart({} as any));
      routingState.getCurrentSegment.and.returnValue('');
      routingState.getPreviousSegment.and.returnValue('betFilter');

      betFilterParams.params = {couponName:"test"};
      component.ngOnInit();
      tick();

      expect(windowRef.document.dispatchEvent).toHaveBeenCalledWith(
        jasmine.objectContaining({ type: 'DESTROY_BET_FILTER' })
      );
    }));

    it('should not dispatch event (event instance mismatch)', fakeAsync(() => {
      router.events = observableOf(new ChildActivationEnd({} as any));
      betFilterParams.params = {couponName:"test"};
      component.ngOnInit();
      tick();
      expect(windowRef.document.dispatchEvent).not.toHaveBeenCalled();
    }));

    it('should not dispatch event (segments the same)', fakeAsync(() => {
      router.events = observableOf(new ChildActivationStart({} as any));
      routingState.getCurrentSegment.and.returnValue('');
      routingState.getPreviousSegment.and.returnValue('');
      betFilterParams.params = {couponName:"test"};      
      component.ngOnInit();
      tick();
      expect(windowRef.document.dispatchEvent).not.toHaveBeenCalled();
    }));

    it('should not dispatch event (prev segment is not "betFilter")', fakeAsync(() => {
      router.events = observableOf(new ChildActivationStart({} as any));
      routingState.getCurrentSegment.and.returnValue('');
      routingState.getPreviousSegment.and.returnValue('home');
      betFilterParams.params = {couponName:"test"};      
      component.ngOnInit();
      tick();
      expect(windowRef.document.dispatchEvent).not.toHaveBeenCalled();
    }));
  });

  describe('#ngOnDestroy', () => {
    it('should unsubscribe', () => {
      component['routeChangeStartHandler'] = { unsubscribe: jasmine.createSpy() } as any;
      component.ngOnDestroy();
      expect(windowRef.document.removeEventListener).toHaveBeenCalledWith('BF_ADD_TO_BETSLIP', jasmine.any(Function));
      expect(component['routeChangeStartHandler'].unsubscribe).toHaveBeenCalled();
    });
  });

  it('@handleAddToBetslip', () => {
    const event = { detail: { ids: ['123', '123'] } } as any;
    component['handleAddToBetslip'](event);
    expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS,
      [event.detail.ids, true, true, false]);
  });

  it('@redirectToPreviousPage', () => {
    component['redirectToPreviousPage']();
    expect(backButtonService.redirectToPreviousPage).toHaveBeenCalled();
  });
});
