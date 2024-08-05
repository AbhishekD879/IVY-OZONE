import { Subscriber, of } from 'rxjs';

import { YourcallBetslipComponent } from '@yourcall/components/yourCallBetslip/yourcall-betslip.component';
import { DSBet } from '@yourcall/models/bet/ds-bet';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('YourcallBetlipComponent', () => {
  let component;
  let deviceService;
  let windowRefService;
  let elementRef;
  let rendererService;
  let localeService;
  let pubsubService;
  let userService;
  let fracToDecService;
  let domToolsService;
  let yourcallBetslipService;
  let yourCallNotificationService;
  let yourcallDashboardService;
  let yourcallMarketsService;
  let quickbetDataProviderService;
  let changeDetectorRef;
  let storageService;

  beforeEach(() => {
    deviceService = {};
    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval').and.callFake(fn => fn()),
        clearInterval: jasmine.createSpy('clearInterval'),
        setTimeout: jasmine.createSpy('setTimeout'),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({} as any),
        getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({
          left: 50
        } as any)
      } as any
    } as any;
    rendererService = {
      renderer: {
        hello: 111,
        listen: jasmine.createSpy('listen')
      }
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue( [{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}])
    };
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync'),
      API: pubSubApi
    };
    userService = {};
    fracToDecService = {};
    domToolsService = {
      getWidth: jasmine.createSpy('getWidth').and.returnValue(100),
      getHeight: jasmine.createSpy('getHeight').and.returnValue(50),
      getOffset: jasmine.createSpy('getOffset').and.returnValue({
        top: 10
      }),
      css: jasmine.createSpy('css')
    };
    yourcallBetslipService = {
      addSelection: jasmine.createSpy('addSelection'),
      removeSelection: jasmine.createSpy('removeSelection'),
      placeBet: jasmine.createSpy('placeBet').and.returnValue(of({}))
    };
    yourCallNotificationService = {
      clear: jasmine.createSpy('clear'),
      saveErrorMessage: jasmine.createSpy('saveErrorMessage')
    };
    yourcallDashboardService = {
      calculateOdds: jasmine.createSpy('calculateOdds'),
      clear: jasmine.createSpy('clear')
    };
    yourcallMarketsService = {
      removeSelectedValues: jasmine.createSpy('removeSelectedValues')
    };
    quickbetDataProviderService = {
      quickbetPlaceBetListener: of({}),
      quickbetReceiptListener: { next: jasmine.createSpy('next') }
    };
    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new YourcallBetslipComponent(deviceService, windowRefService, elementRef, rendererService, localeService, pubsubService,
      userService, fracToDecService, domToolsService, yourcallBetslipService, yourCallNotificationService, yourcallDashboardService,
      yourcallMarketsService, quickbetDataProviderService, changeDetectorRef,storageService);
  });

  describe('ngOnInit', () => {
    it('should call detach & detectChanges, call addSelection', () => {
      component.eventEntity = { classId: '41', categoryId: '55' };
      yourcallBetslipService.addSelection.and.returnValue(Promise.reject('Some error'));
      pubsubService.subscribe.and.callFake((subsriberName, channel, cb) => {
        if (channel === pubsubService.API.ADD_TO_YC_BETSLIP) {
          cb({ id: '9' });
        }
      });
      component.ngOnInit();
      expect(component.bodyClass).toEqual('yourcall-bs-opened');
      expect(component.ycOddsValue).toBeTruthy();
      expect(component.recalculatePositions).toBeTruthy();
      expect(changeDetectorRef.detach).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(yourcallBetslipService.addSelection).toHaveBeenCalledWith({
        id: '9',
        classId: '41',
        categoryId: '55'
      });
    });

    it('should call detach & detectChanges, call addSelection - and set event properties', fakeAsync(() => {
      const selectionData = { token: '123' } as DSBet;
      component.eventEntity = { classId: '41', categoryId: '55', typeName: 'test', categoryName: 'football' };
      yourcallBetslipService.addSelection.and.returnValue(Promise.resolve(selectionData));
      pubsubService.subscribe.and.callFake((subsriberName, channel, cb) => {
        if (channel === pubsubService.API.ADD_TO_YC_BETSLIP) {
          cb({ id: '9' });
        }
      });
      spyOn(component, 'placeBetListener');
      component.ngOnInit();
      tick();
      expect(component.selectionData.typeName).toEqual(component.eventEntity.typeName);
      expect(component.selectionData.categoryName).toEqual(component.eventEntity.categoryName);
    }));

    it('should sey ycOddsValue to undefined in case if it is 5-A side bet', () => {
      component.isFiveASideBet = true;
      component.ngOnInit();
      expect(component.ycOddsValue).toBeFalsy();
    });

    it('should subscribe for "scroll" and "resize" window events if ' +
      'device is not mobile origin', () => {
      deviceService.isMobileOrigin = false;
      deviceService.isTablet = false;

      component.ngOnInit();

      expect(rendererService.renderer.listen).toHaveBeenCalledTimes(2);
    });

    it('should subscribe for "scroll" and "resize" window events if device is tablet', () => {
      deviceService.isMobileOrigin = true;
      deviceService.isTablet = true;

      component.ngOnInit();

      expect(rendererService.renderer.listen).toHaveBeenCalledTimes(2);
    });

    it('should not subscribe for "scroll" and "resize" window events if device is desktop', () => {
      deviceService.isMobileOrigin = true;
      deviceService.isTablet = false;
      deviceService.isDesktop = true;

      component.ngOnInit();

      expect(rendererService.renderer.listen).not.toHaveBeenCalled();
    });

    it('should handle resize event', () => {
      const timer = 123;
      const newTimer = 124;

      component['resizeTimer'] = timer;
      rendererService.renderer.listen.and.callFake((windowRef, eventName, cb) => {
        if ('resize' === eventName) {
          cb();
        }
      });
      windowRefService.nativeWindow.setTimeout.and.returnValue(newTimer);
      deviceService.isTablet = true;
      component['isFixed'] = true;

      component.ngOnInit();

      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(timer);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(component.relocate, component['resizeTimeout']);
      expect(component['resizeTimer']).toEqual(newTimer);
      expect(component['isFixed']).toBeFalsy();
    });
  });

  describe('ngOnDestroy', () => {
    it('should clear listeners', () => {
      component.ngOnDestroy();

      expect(windowRefService.nativeWindow.clearInterval);
      expect(pubsubService.unsubscribe).toHaveBeenCalledWith('YourCallBetslip');
    });

    it('should clear listeners when onInit was not initiated', () => {
      component.ngOnInit();
      component.ngOnDestroy();

      expect(pubsubService.unsubscribe).toHaveBeenCalledWith('YourCallBetslip');
    });

    it('should clear resize timer', () => {
      const timer = 123;
      component['resizeTimer'] = timer;
      component.ngOnDestroy();

      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(timer);
    });
  });

  describe('onQuickbetEvent', () => {
    it('should handle reuse selection event', () => {
      component.selectionData = { token: '123' } as DSBet;
      component['closeQuickBet'] = { emit: jasmine.createSpy('closeQuickBet') };
      component['removeEdpBybTabs'] = true;
      component.onQuickbetEvent({ output: 'reuseSelectionFn' });

      expect(yourcallDashboardService.calculateOdds).toHaveBeenCalled();
      expect(yourcallBetslipService.removeSelection).toHaveBeenCalled();
      expect(component.selectionData).toBeNull();
      expect(component.closeQuickBet.emit).toHaveBeenCalled();
      expect(pubsubService.publish).toHaveBeenCalledWith('YC_DASHBOARD_DISPLAYING_CHANGED', true);
      expect(pubsubService.publish).toHaveBeenCalledWith('REMOVE_EDP_BYB_TABS');
    });

    it('should handle close panel event', () => {
      component.selectionData = { token: '123' } as DSBet;
      component.ngOnInit();
      component.onQuickbetEvent({ output: 'closePanelFn' });

      expect(yourcallDashboardService.clear).toHaveBeenCalled();
      expect(yourcallBetslipService.removeSelection).toHaveBeenCalled();
      expect(yourcallMarketsService.removeSelectedValues).toHaveBeenCalled();
      expect(component.selectionData).toBeNull();
      expect(pubsubService.publish).toHaveBeenCalledWith('YC_DASHBOARD_DISPLAYING_CHANGED', false);
    });

    it('should handle place bet event and store old odds', () => {
      component.selectionData = {
        token: '123',
        newOddsValue: '2/1',
        price: null
      } as DSBet;
      component.ngOnInit();
      component.onQuickbetEvent({ output: 'placeBetFn' });

      expect(yourCallNotificationService.clear).toHaveBeenCalled();
      expect(component.selectionData.price).toEqual(jasmine.objectContaining({
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false
      }));
      expect(component.selectionData.newOddsValue).toBeNull();
      expect(component.selectionData.oldOddsValue).toEqual('2/1');
    });

    it('should handle place bet event and not store old odds if new odds not available', () => {
      component.selectionData = {
        token: '123',
        newOddsValue: '',
        price: null
      } as DSBet;
      component.ngOnInit();
      component.onQuickbetEvent({ output: 'placeBetFn' });

      expect(yourCallNotificationService.clear).toHaveBeenCalled();
      expect(component.selectionData.price).toEqual(jasmine.objectContaining({
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false
      }));
      expect(component.selectionData.newOddsValue).toBeFalsy();
      expect(component.selectionData.oldOddsValue).toBeUndefined();
    });

    it('should not trigger any reuseSelection, closePanel or placeBet handlers if output not covered', () => {
      component.ngOnInit();
      component.onQuickbetEvent({ output: 'notHandled' });

      expect(yourCallNotificationService.clear).not.toHaveBeenCalled();
    });
  });

  describe('closePanel', () => {
    it('should call emit if there if called from receipt', () => {
      component['closeBetReceipt'] = { emit: jasmine.createSpy('closePanel') };
      component.closePanel(true);
      expect(component.closeBetReceipt.emit).toHaveBeenCalled();
    });
    it('should`t call emit if there if called not from receipt', () => {
      component['closeBetReceipt'] = { emit: jasmine.createSpy('closePanel') };
      component.closePanel(false);
      expect(component.closeBetReceipt.emit).not.toHaveBeenCalled();
    });
    it('should`t fail in edge case when no event emitter', () => {
      component.closePanel(true);
    });
  });

  it('should return odds stored in yourcallDashboardService', () => {
    const odds = {
      dec: '1',
      frac: '2'
    };
    yourcallDashboardService.odds = odds;

    expect(component.ycOddsValue()).toEqual(odds);
  });

  describe('handlePanelRender', () => {
    beforeEach(() => {
      deviceService.isMobileOrigin = true;
      deviceService.isTablet = false;
    });

    it('should reset fixed position flag', () => {
      component.isFixed = true;

      component['handlePanelRender']();

      expect(component.isFixed).toBeFalsy();
    });

    it('should set placeBet listener', () => {
      component['quickbetPlaceBetSubscriber'] = null;

      component['handlePanelRender']();

      expect(component['quickbetPlaceBetSubscriber']).toEqual(jasmine.any(Subscriber));
    });

    it('should unsubscribe from previous placeBet listener and set new one', () => {
      const quickbetPlaceBetSubscriber = jasmine.createSpyObj('quickbetPlaceBetSubscriber',
        ['unsubscribe']);

      component['quickbetPlaceBetSubscriber'] = quickbetPlaceBetSubscriber;
      component['handlePanelRender']();

      expect(quickbetPlaceBetSubscriber.unsubscribe).toHaveBeenCalled();
      expect(component['quickbetPlaceBetSubscriber']).toEqual(jasmine.any(Subscriber));
    });

    it('should call relocateAfter', () => {
      spyOn(component as any, 'relocateAfter');
      component['handlePanelRender']();
      expect((component as any).relocateAfter).toHaveBeenCalledWith();
    });

    it('#placeBetListener', () => {
      component['isBetReceipt'].emit = jasmine.createSpy('isBetReceipt.emit');
      component['removeSubscribers'] = jasmine.createSpy('removeSubscribers');
      component.selectionData = { eventId: 1 };
      component.eventEntity = { classId: '41', categoryId: '55' };
      const receiptDetailsModel = {data: {isquickbet: false, betId: '12345'}};
      yourcallBetslipService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of(receiptDetailsModel));
      component['placeBetListener']();

      expect(pubsubService.publish).toHaveBeenCalledWith('BETS_COUNTER_PLACEBET');
      expect(pubsubService.publishSync).toHaveBeenCalledWith('MY_BET_PLACED', receiptDetailsModel.data);
      expect(pubsubService.publish).toHaveBeenCalledWith('STORE_FREEBETS');
      expect(component['isBetReceipt'].emit).toHaveBeenCalled();
    });

    it('should call if local storage is empty', () => {
      component['isBetReceipt'].emit = jasmine.createSpy('isBetReceipt.emit');
      component['removeSubscribers'] = jasmine.createSpy('removeSubscribers');
      component.selectionData = { eventId: 1 };
      component.eventEntity = { classId: '41', categoryId: '55',id: 11};
      const receiptDetailsModel = {data: {isquickbet: false, betId: 3}};
      yourcallBetslipService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of(receiptDetailsModel));
      storageService.get = jasmine.createSpy().and.returnValue([]);
      component['placeBetListener']();
      expect(pubsubService.publish).toHaveBeenCalledWith('STORE_FREEBETS');
      expect(component['isBetReceipt'].emit).toHaveBeenCalled();
    });

    it('should call if local storage event id and bet id is present', () => {
      component['isBetReceipt'].emit = jasmine.createSpy('isBetReceipt.emit');
      component['removeSubscribers'] = jasmine.createSpy('removeSubscribers');
      component.selectionData = { eventId: 1 };
      component.eventEntity = { classId: '41', categoryId: '55',id: 11};
      const receiptDetailsModel = {data: {isquickbet: false, betId: 3}};
      yourcallBetslipService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of(receiptDetailsModel));
      storageService.get = jasmine.createSpy().and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
      component['placeBetListener']();
      expect(pubsubService.publish).toHaveBeenCalledWith('STORE_FREEBETS');
      expect(component['isBetReceipt'].emit).toHaveBeenCalled();
    });

    it('should call if local storage event id present and bet id is not present', () => {
      component['isBetReceipt'].emit = jasmine.createSpy('isBetReceipt.emit');
      component['removeSubscribers'] = jasmine.createSpy('removeSubscribers');
      component.selectionData = { eventId: 1 };
      component.eventEntity = { classId: '41', categoryId: '55',id: 11};
      const receiptDetailsModel = {data: {isquickbet: false, betId: 5}};
      yourcallBetslipService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of(receiptDetailsModel));
      storageService.get = jasmine.createSpy().and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"22","betIds":[4]}]);
      component['placeBetListener']();
      expect(pubsubService.publish).toHaveBeenCalledWith('STORE_FREEBETS');
      expect(component['isBetReceipt'].emit).toHaveBeenCalled();
    });

    it('should call if local storage is null', () => {
      component['isBetReceipt'].emit = jasmine.createSpy('isBetReceipt.emit');
      component['removeSubscribers'] = jasmine.createSpy('removeSubscribers');
      component.selectionData = { eventId: 1 };
      component.eventEntity = { classId: '41', categoryId: '55' };
      const receiptDetailsModel = {data: {isquickbet: false, betId: '12345'}};
      yourcallBetslipService.placeBet = jasmine.createSpy('placeBet').and.returnValue(of(receiptDetailsModel));
      storageService.get = jasmine.createSpy().and.returnValue(null);
      component['placeBetListener']();
      expect(pubsubService.publish).toHaveBeenCalledWith('STORE_FREEBETS');
      expect(component['isBetReceipt'].emit).toHaveBeenCalled();
    });
  });
  describe('relocate', () => {
    beforeEach(() => {
      deviceService.isMobileOrigin = true;
      deviceService.isTablet = true;
      deviceService.isDesktop = false;
      deviceService.isFixed = false;
    });
    it('should relocate quickbet panel if recalculatePositions is true (by default)', () => {
      component['relocate']();
      expect(domToolsService.css).toHaveBeenCalledWith(jasmine.anything(), {
        position: 'fixed',
        left: 50,
        bottom: 52,
        width: 100
      } as any);
    });
    it('should`t relocate quickbet panel if recalculatePositions is false', () => {
      component.recalculatePositions = false;
      component['relocate']();
      expect(domToolsService.css).toHaveBeenCalledWith(jasmine.anything(), {
        position: 'fixed',
        left: 0,
        bottom: 0,
        width: 100
      } as any);
    });
  });

  describe('handleBybLiveEvent', () => {
    beforeEach(() => {
      component.selectionData = { eventId: 1 };
    });

    it('should disable selection', () => {
      component.handleBybLiveEvent({ id: 1 });
      expect(component.selectionData.disabled).toBeTruthy();
      expect(component.removeEdpBybTabs).toBeTruthy();
      expect(yourCallNotificationService.saveErrorMessage).toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledWith('quickbet.betPlacementErrors.EVENT_SUSPENDED');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalledWith();
    });

    it('should not disable selection', () => {
      component.handleBybLiveEvent({ id: 2 });
      expect(component.selectionData.disabled).toBeFalsy();
    });
  });
});
