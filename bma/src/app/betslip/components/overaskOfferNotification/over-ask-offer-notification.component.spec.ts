import { OveraskOfferNotificationComponent } from '@betslip/components/overaskOfferNotification/over-ask-offer-notification.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, Subscription } from 'rxjs';

describe('OveraskOfferNotificationComponent', () => {
  let component;
  let overAskService;
  let cmsService;

  beforeEach(() => {
    overAskService = {
      offerExpiresAt: ''
    };

    cmsService = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({
        traderOfferNotificationMessage: 'traderOfferNotificationMessage',
        traderOfferExpiresMessage: 'traderOfferExpiresMessage'
      }))
    };

    component = new OveraskOfferNotificationComponent(overAskService, cmsService);
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component['countdownTimer'] = jasmine.createSpy('countdownTimer');
    });

    it('should get cms config for notification message', () => {
      component.ngOnInit();

      expect(cmsService.getFeatureConfig).toHaveBeenCalledWith('Overask');
    });

    it('should no start flow for countdown if no expire time for offer', () => {
      component.ngOnInit();

      expect(component['countdownTimer']).not.toHaveBeenCalled();
      expect(component['intervalTimer']).toBeUndefined();
    });

    it('should no start flow for countdown if for expired offer', () => {
      overAskService.offerExpiresAt = new Date(Date.now() - 10000);
      component.ngOnInit();

      expect(component['countdownTimer']).not.toHaveBeenCalled();
      expect(component['intervalTimer']).toBeUndefined();
    });

    it('should call countdownTimer once', fakeAsync(() => {
      overAskService.offerExpiresAt = new Date();
      component.ngOnInit();

      tick(1000);

      expect(component['countdownTimer']).toHaveBeenCalledTimes(1);
      expect(component['intervalTimer']).toEqual(jasmine.any(Subscription));
    }));

    it('should call countdownTimer twice', fakeAsync(() => {
      overAskService.offerExpiresAt = new Date(Date.now() + 1500);
      component.ngOnInit();

      tick(5000);

      expect(component['countdownTimer']).toHaveBeenCalledTimes(2);
      expect(component['intervalTimer']).toEqual(jasmine.any(Subscription));
    }));
  });

  it('ngOnDestroy', () => {
    component['clearTimer'] = jasmine.createSpy('clearTimer');
    component['featureConfigSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    component.ngOnDestroy();

    expect(component['clearTimer']).toHaveBeenCalled();
    expect(component['featureConfigSubscription'].unsubscribe).toHaveBeenCalled();
  });

  it('should not unsubscribe from feature config', function () {
    component['featureConfigSubscription'] = undefined;
    component.ngOnDestroy();

    expect(component['featureConfigSubscription']).not.toBeDefined();
  });

  it('clearTimer', () => {
    const unsubscribe = jasmine.createSpy('unsubscribe');
    component['intervalTimer'] = {
      unsubscribe: unsubscribe
    };
    component['clearTimer']();

    expect(unsubscribe).toHaveBeenCalled();
  });

  it('formatTime', () => {
    expect(component['formatTime'](0)).toEqual('00');
    expect(component['formatTime'](11)).toEqual('11');
    expect(component['formatTime'](11)).toEqual('11');
  });

  describe('countdownTimer', () => {
    it('should clear timeout and do not calculate timer', () => {
      component['formatTime'] = jasmine.createSpy('formatTime').and.callFake(num => num);
      component['clearTimer'] = jasmine.createSpy('clearTimer');
      component['expiredTime'] = Date.now() - 500;
      component['countdownTimer']();

      expect(component['secondsToFinish']).toBe(-1);
      expect(component['clearTimer']).toHaveBeenCalled();
      expect(component['formatTime']).not.toHaveBeenCalled();
      expect(component['offerTimer']).toBe('');
    });

    it('should format timer value', () => {
      component['formatTime'] = jasmine.createSpy('formatTime').and.callFake(num => num);
      component['clearTimer'] = jasmine.createSpy('clearTimer');
      component['expiredTime'] = Date.now() + 500;
      component['countdownTimer']();

      expect(component['clearTimer']).not.toHaveBeenCalled();
      expect(component['formatTime']).toHaveBeenCalledTimes(2);
    });

    it('should define offerTimer', () => {
      component['expiredTime'] = Date.now() + 1500;
      component['countdownTimer']();

      expect(component['offerTimer']).toEqual('00:01');
    });
  });
});
