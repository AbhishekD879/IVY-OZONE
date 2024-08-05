import { commandApi } from '@core/services/communication/command/command-api.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { SlideOutBetslipComponent } from './slide-out-betslip.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('SlideOutBetslipComponent', () => {
  let component: SlideOutBetslipComponent;
  let freeBetsService,
    pubSubService,
    commandService,
    userService,
    betslipService,
    router,
    localeService,
    nativeBridgeService,
    deviceService;

  beforeEach(() => {
    freeBetsService = {
      getFreeBetsState: jasmine.createSpy()
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    commandService = {
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve({
        betsCount: 1
      })),
      API: commandApi
    };
    userService = {};
    betslipService = {
      count: jasmine.createSpy()
    };
    router = {
      navigate: jasmine.createSpy()
    };
    deviceService = {
      isWrapper: false
    };

    nativeBridgeService = {
      syncPlayerBetSlip: jasmine.createSpy('syncPlayerBetSlip'),
      onCloseBetSlip: jasmine.createSpy('onCloseBetSlip'),
      accaNotificationChanged: jasmine.createSpy('accaNotificationChanged'),
      syncWithNative: jasmine.createSpy('syncWithNative'),
      onRightMenuClick: jasmine.createSpy('onRightMenuClick'),
    };

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('Balance')
    };
    component = new SlideOutBetslipComponent(
      freeBetsService,
      nativeBridgeService,
      pubSubService,
      commandService,
      userService,
      betslipService,
      router,
      localeService,
      deviceService
    );
    component.onReceipt = true;
  });

  it('ngOnInit', fakeAsync(() => {
    pubSubService.subscribe.and.callFake((componentName: string, command: string, callback: Function) => {
      callback();
    });
    component.ngOnInit();
    tick();
    expect(component.onReceipt).toBe(false);
    expect(nativeBridgeService.onCloseBetSlip).toHaveBeenCalled();
    expect(component.betslipLabel).toBe('bs.betReceipt');
    expect(component.betslipStatus).toBe(true);
    expect(component.isDropDownMenuHidden).toBe(true);
    expect(component.balanceText).toBe('Balance');
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(6);
    expect(commandService.executeAsync).toHaveBeenCalled();
  }));

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('slideOutBetslip');
  });

  describe('#quickDeposit', () => {
    it('betslipStatus = true & onReceipt = true', () => {
      component.quickDeposit();

      expect(component.isDropDownMenuHidden).toBe(true);
      expect(router.navigate).toHaveBeenCalledWith(['/deposit']);
      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
    });
  });

  it('#hideSidebar', () => {
    component['hideSidebar']();
    expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
  });

  it('#toggleDropDownMenu', () => {
    component.isDropDownMenuHidden = false;
    component.toggleDropDownMenu();
    expect(component.isDropDownMenuHidden).toBe(true);

    component.toggleDropDownMenu();
    expect(component.isDropDownMenuHidden).toBe(false);
    expect(nativeBridgeService.onRightMenuClick).not.toHaveBeenCalled();
  });

  it('#toggleDropDownMenu: should call native bridge onRightMenuClick method', () => {
    component.isDropDownMenuHidden = true;
    deviceService.isWrapper = true;

    component.toggleDropDownMenu();

    expect(nativeBridgeService.onRightMenuClick).toHaveBeenCalled();
    expect(component.isDropDownMenuHidden).toBeFalsy();
  });

  it('#toggleBalance', () => {
    component.isDropDownMenuHidden = false;
    component.toggleBalance(true);
    expect(component.isBalanceHidden).toBe(true);
    expect(component.isDropDownMenuHidden).toBe(true);
    expect(pubSubService.publish).toHaveBeenCalledWith('USER_BALANCE_SHOW', true);

    component.toggleBalance(false);
    expect(component.isDropDownMenuHidden).toBe(true);
    expect(pubSubService.publish).toHaveBeenCalledWith('USER_BALANCE_SHOW', false);
  });

  describe('#onClick', () => {
    it('target null', () => {
      const event = {} as any,
        target = null;
      component.isDropDownMenuHidden = false;
      component.onClick(event, target);
      expect(component.isDropDownMenuHidden).toBe(false);
    });

    it('target is btnBalance text in the button', () => {
      const event = {} as any,
        target = { name: 'btnBalance' } as any;
      component.isDropDownMenuHidden = false;
      component.onClick(event, target);
      expect(component.isDropDownMenuHidden).toBe(false);
    });

    it('target is btnBalance box', () => {
      const event = {} as any,
        target = { parentElement: { name: 'btnBalance' }, name: 'other' } as any;
      component.isDropDownMenuHidden = false;
      component.onClick(event, target);
      expect(component.isDropDownMenuHidden).toBe(false);
    });

    it('target is any', () => {
      const event = {} as any,
        target = { parentElement: { name: 'other' }, name: 'other' } as any;
      component.isDropDownMenuHidden = false;
      component.onClick(event, target);
      expect(component.isDropDownMenuHidden).toBe(true);
    });
  });

  it('should set show-slide-out-betslip-false', () => {
    component.onReceipt = true;
    pubSubService.subscribe = jasmine.createSpy('subscribe');
    pubSubService.subscribe.and.callFake((componentName: string, command: string, callback: Function) => {
      if (command === 'show-slide-out-betslip-false') {
        callback('!prevent');
      }
    });
    component.ngOnInit();
    expect(component.onReceipt).toEqual(false);
  });

  it('should set BETSLIP_LABEL', () => {
    pubSubService.subscribe.and.callFake((componentName: string, command: string, callback: Function) => {
      if (command === 'BETSLIP_LABEL') {
        callback('Bet Slip');
      }
    });
    component.ngOnInit();
    expect(component.betslipLabel).toEqual('bs.betslipBtn');
  });

  it('should set show-slide-out-betslip-false', () => {
    commandService.executeAsync.and.returnValue(Promise.resolve());
    component.ngOnInit();
    expect(component.betslipStatus).toEqual(false);
  });
});
