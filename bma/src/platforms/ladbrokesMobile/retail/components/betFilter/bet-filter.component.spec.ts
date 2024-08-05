
import { of as observableOf } from 'rxjs';

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
    recService;

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


});
