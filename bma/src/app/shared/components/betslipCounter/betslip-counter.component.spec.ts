import { BetslipCounterComponent } from './betslip-counter.component';

import { commandApi } from '@core/services/communication/command/command-api.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('BetslipCounterComponent', () => {
  let component: BetslipCounterComponent;
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
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({
        betsCount: 0
      }))
    };
    storageService = {
      get: jasmine.createSpy('get').and.callFake(key => {
        return key === 'betSelections' ? ['bet1', 'bet2'] :
          key === 'dsBetslip' ? 'dsbet' : null;
      })
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    component = new BetslipCounterComponent(pubsubService, commandService, storageService, changeDetectorRef);
  });

  it('should create', () => {
    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(commandService.executeAsync).toHaveBeenCalledTimes(1);
    expect(commandService.executeAsync).toHaveBeenCalledWith(commandApi.DS_READY, undefined, 0);

    expect(pubsubService.subscribe).toHaveBeenCalledTimes(2);
    expect(pubsubService.subscribe).toHaveBeenCalledWith('betSlipCounter', pubSubApi.BETSLIP_COUNTER_UPDATE, jasmine.anything());

    expect(storageService.get).toHaveBeenCalledTimes(3);
    expect(storageService.get).toHaveBeenCalledWith('dsBetslip');

    expect(component.bsBetCounter).toEqual(2);
  });

  it('should set counter on ini', () => {
    spyOn(component as any, 'setCounter').and.callThrough();
    component.ngOnInit();

    expect(component['setCounter']).toHaveBeenCalled();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    expect(component.betCounter).toBe(2);
  });

  it('should properly count if bet array is empty', () => {
    component['storageService'].get = jasmine.createSpy('get').and.callFake(key => {
      return key === 'betSelections' ? [] : null;
    }) as any;
    component.ngOnInit();
    expect(component.betCounter).toBe(0);
  });

  it('betsLength', () => {
    const amount = component.betsLength;
    expect(amount).toEqual(2);
    expect(storageService.get).toHaveBeenCalledWith('betSelections');
    expect(storageService.get).toHaveBeenCalledWith('toteBet');
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('betSlipCounter');
  });

  describe('toteBet', () => {
    it('should count toteBet is present', () => {
      component['storageService'].get = jasmine.createSpy('get').and.callFake(key => {
        return key === 'betSelections' ? [] :
          key === 'toteBet' ? { toteBet: true } : null;
      }) as any;
      component.ngOnInit();
      expect(component.betCounter).toBe(1);
    });

    it('should count toteBet is not present', () => {
      component['storageService'].get = jasmine.createSpy('get').and.callFake(key => {
        return key === 'betSelections' ? [] :
          key === 'toteBet' ? null : null;
      }) as any;
      component.ngOnInit();
      expect(component.betCounter).toBe(0);
    });
  });
});
