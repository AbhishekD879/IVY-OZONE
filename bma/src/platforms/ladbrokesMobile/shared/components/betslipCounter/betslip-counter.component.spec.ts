import { commandApi } from '@core/services/communication/command/command-api.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';
import { LadbrokesBetslipCounterComponent } from '@ladbrokesMobile/shared/components/betslipCounter/betslip-counter.component';

describe('LadbrokesBetslipCounterComponent', () => {
  let component: LadbrokesBetslipCounterComponent;
  let pubsubService;
  let commandService;
  let storageService;
  let changeDetectorRef;

  beforeEach(() => {
    pubsubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.returnValue((param1, param2, callback) => {
        callback(0);
      }),
      unsubscribe: jasmine.createSpy()
    };
    commandService = {
      API: commandApi,
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve({
        betsCount: 0
      }))
    };
    storageService = {
      get: jasmine.createSpy().and.returnValue(1)
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    component = new LadbrokesBetslipCounterComponent(pubsubService, commandService, storageService, changeDetectorRef);
    spyOn(window, 'clearTimeout');
  });

  describe('@setCounter', () => {
    it('should set counter animation if animateBetCounter !== betCounter', fakeAsync(() => {
      component.bsBetCounter = 1;
      component.dsBetCounter = 1;
      component.setCounter();
      expect(clearTimeout).toHaveBeenCalled();
      expect(component.animateBetCounter).toBe(2);
      expect(component.animate).toBe(true);
      tick(component.duration);
      expect(component.animate).toBe(false);
    }));

    it('should not set counter animation if animateBetCounter === betCounter', () => {
      component.bsBetCounter = 0;
      component.dsBetCounter = 0;
      component.setCounter();
      expect(clearTimeout).not.toHaveBeenCalled();
      expect(component.animate).toBe(false);
    });
    it('should not set counter animation during initialization of component', () => {
      component.bsBetCounter = 1;
      component.dsBetCounter = 1;
      component.setCounter(true);
      expect(clearTimeout).not.toHaveBeenCalled();
      expect(component.animate).toBe(false);
    });
  });

  it('@ngOnDestroy: should clear timeout', () => {
    component.ngOnDestroy();
    expect(clearTimeout).toHaveBeenCalledWith(component.animation);
  });
});
