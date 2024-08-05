import { fakeAsync, tick } from '@angular/core/testing';
import { CouponsContentSportTabComponent } from '@sb/components/couponsContentSportTab/coupons-content-sport-tab.component';
import { throwError, of as observableOf } from 'rxjs';

describe('CouponsContentSportTabComponent', () => {
  let component;
  let events;
  let slpSpinnerStateService;
  let coupons: any;
  let pubSubService;
  let changeDetectorRef;

  beforeEach(() => {
    coupons = [{}, { id: '1', events: [{ id: '123' }] }];

    slpSpinnerStateService = {
      handleSpinnerState: jasmine.createSpy('handleSpinnerState')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb('2123')),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        DELETE_EVENT_FROM_CACHE: 'DELETE_EVENT_FROM_CACHE'
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    component = new CouponsContentSportTabComponent(
      slpSpinnerStateService,
      pubSubService,
      changeDetectorRef
    );
    events = [{}];
    component.sport = {
      extendRequestConfig: jasmine.createSpy('extendRequestConfig'),
      coupons: jasmine.createSpy('coupons').and.returnValue(observableOf(coupons)),
      unSubscribeCouponsForUpdates: jasmine.createSpy('unSubscribeCouponsForUpdates'),
      couponEventsRequestParams: jasmine.createSpy('couponEventsRequestParams').and.returnValue({ params: 'params' }),
      couponEventsByCouponId: jasmine.createSpy('couponEventsByCouponId').and.returnValue(events),
      subscribeCouponsForUpdates: jasmine.createSpy('subscribeCouponsForUpdates')
    };
  });

  describe('@ngOnInit', () => {
    it('should call methods & loadCouponsData happy flow', fakeAsync(() => {
      component.ngOnInit();
      tick();

      expect(component.sport.extendRequestConfig).toHaveBeenCalledWith('coupons');
      expect(component.coupons.length).toBe(2);
      expect(component.isLoaded).toBe(true);
      expect(component.isResponseError).toBe(false);
      expect(pubSubService.subscribe).toHaveBeenCalledWith('CouponsContentTab', 'DELETE_EVENT_FROM_CACHE', jasmine.any(Function));
    }));

    it('loadCouponsData failed flow', fakeAsync(() => {
      component.sport.coupons.and.returnValue(Promise.reject({ error: 'error' }));
      component.ngOnInit();
      tick();

      expect(component.coupons.length).toBe(0);
      expect(component.isLoaded).toBe(true);
      expect(component.isResponseError).toBe(true);
    }));
  });

  describe('@ngOnDestroy', () => {
    it(`should complete unsubscribe$ subject`, () => {
      spyOn(component['unsubscribe$'], 'next');
      spyOn(component['unsubscribe$'], 'complete');

      component.ngOnDestroy();

      expect(component['unsubscribe$'].next).toHaveBeenCalled();
      expect(component['unsubscribe$'].complete).toHaveBeenCalled();
    });

    it('should call unSubscribeCouponsForUpdates', () => {
      component.subscribedCoupons = { id: 'id' };
      component.ngOnDestroy();

      expect(component.sport.unSubscribeCouponsForUpdates).toHaveBeenCalledWith('id');
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('CouponsContentTab');
    });
  });

  describe('@getCouponContent', () => {
    it('should run happy flow without events', () => {
      const coupon = { isExpanded: false, id: 'id', isEventsLoaded: null, isEventsAvailable: null };
      component.subscribedCoupons = { id: true };
      component.getCouponContent(coupon as any);

      expect(component.subscribedCoupons['id']).toBe(false);
      expect(component.sport.unSubscribeCouponsForUpdates).toHaveBeenCalledWith('id');
      expect(coupon.isExpanded).toBe(true);
      expect(coupon.isEventsLoaded).toBe(true);
      expect(coupon.isEventsAvailable).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should run happy flow with events', () => {
      const coupon = { isExpanded: false, id: 'id', events: null };

      component.subscribedCoupons = { id: true };
      events.push([{ typeDisplayOrder: -2, id: 1 }, { typeDisplayOrder: -1, id: 2 }]);
      component.getCouponContent(coupon as any);

      expect(coupon.events[0].id).toBe(1);
      expect(component.sport.subscribeCouponsForUpdates).toHaveBeenCalledWith(jasmine.any(Array), 'id');
      expect(component.subscribedCoupons['id']).toBe(true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should run fail flow', () => {
      const coupon = { isEventsLoaded: null, isEventsAvailable: null };
      component.sport.couponEventsByCouponId.and.returnValue(throwError({ error: 'error' }));
      component.getCouponContent(coupon as any);

      expect(coupon.isEventsLoaded).toBe(true);
      expect(coupon.isEventsAvailable).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should set coupon.isExpanded to false and unsubscribeForUpdates', () => {
      const coupon = { isExpanded: true, id: '1' };
      spyOn(component, 'unsubscribeForUpdates');

      component.getCouponContent(coupon as any);

      expect(component['unsubscribeForUpdates']).toHaveBeenCalledWith(coupon.id);
      expect(coupon.isExpanded).toBe(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it(`should takeUntil unsubscribe$`, () => {
      const coupon = { isExpanded: false, id: '1' };

      component.getCouponContent(coupon as any);
      expect(coupon.isExpanded).toBe(true);

      coupon.isExpanded = false;
      component['unsubscribe$'].next();
      component['unsubscribe$'].complete();

      component.getCouponContent(coupon as any);
      expect(coupon.isExpanded).toBe(true);
      expect(component.sport.subscribeCouponsForUpdates).not.toHaveBeenCalled();
    });
  });

  it('should return coupon id', () => {
    expect(component.trackById(1, { id: 1 })).toBe(1);
  });

  it('should call reloadComponent', () => {
    component.subscribedCoupons = { id: 'id' };
    component.reloadComponent();

    expect(component.sport.unSubscribeCouponsForUpdates).toHaveBeenCalledWith('id');
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('CouponsContentTab');

    expect(component.sport.extendRequestConfig).toHaveBeenCalledWith('coupons');
    expect(component.coupons.length).toBe(2);
    expect(component.isLoaded).toBe(true);
    expect(component.isResponseError).toBe(false);
    expect(pubSubService.subscribe).toHaveBeenCalledWith('CouponsContentTab', 'DELETE_EVENT_FROM_CACHE', jasmine.any(Function));
  });

  describe('#loadCouponsData', () => {
    it('should successfully load Coupons Data', () => {
      component['loadCouponsData']();

      expect(component.coupons).toEqual(coupons);
      expect(component.isResponseError).toEqual(false);
      expect(component.isLoaded).toEqual(true);
      expect(slpSpinnerStateService.handleSpinnerState).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(2);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should handle error load Coupons Data', () => {
      component.sport.coupons.and.returnValue(throwError({ error: 'error' }));
      component['loadCouponsData']();

      expect(component.coupons).toEqual([]);
      expect(component.isResponseError).toEqual(true);
      expect(component.isLoaded).toEqual(true);
      expect(slpSpinnerStateService.handleSpinnerState).toHaveBeenCalled();
    });

    it(`should takeUntil unsubscribe$`, () => {
      component['loadCouponsData']();

      expect(component.coupons).toEqual(coupons);

      component.coupons = undefined;
      component['unsubscribe$'].next();
      component['unsubscribe$'].complete();
      component['loadCouponsData']();
      expect(component.coupons).toEqual(coupons);
    });
  });

  describe('unsubscribeForUpdates', () => {
    const id = '1';
    it(`should Not unSubscribeCouponsForUpdates if subscribedCoupons not contain id`, () => {
      component.subscribedCoupons[id] = false;

      component['unsubscribeForUpdates'](id);

      expect(component.sport.unSubscribeCouponsForUpdates).not.toHaveBeenCalled();
    });

    it(`should unSubscribeCouponsForUpdates`, () => {
      component.subscribedCoupons[id] = true;

      component['unsubscribeForUpdates'](id);

      expect(component.subscribedCoupons[id]).toBeFalsy();
      expect(component.sport.unSubscribeCouponsForUpdates).toHaveBeenCalledWith(id);
    });
  });

  describe('#deleteEvent', () => {
    it('should deleteEvent', () => {
      component['loadCouponsData']();
      expect(component.coupons).toEqual(coupons);

      component['deleteEvent']('123');

      expect(component.coupons).toEqual([{}]);
    });
  });
});
