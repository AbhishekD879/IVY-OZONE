import { CouponsListSportTabComponent } from '@sbModule/components/couponsListSportTab/coupons-list-sport-tab.component';
import { of as observableOf, throwError } from 'rxjs';
import { tick, fakeAsync } from '@angular/core/testing';

describe('CouponsListSportTabComponent', () => {
  let component: CouponsListSportTabComponent,
    sportsConfigService,
    activatedRoute,
    routingState;

  beforeEach(() => {
    activatedRoute = {};

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf('sport'))
    };
    routingState = {
      getRouteParam: jasmine.createSpy('getRouteParam').and.returnValue('football')
    };

    component = new CouponsListSportTabComponent(sportsConfigService, activatedRoute, routingState);

    component.sport = {
      coupons: jasmine.createSpy('coupons').and.returnValue(Promise.resolve([{
        name: 'name',
        id: '12345'
      }]))
    };
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component['loadCouponsData'] = jasmine.createSpy('loadCouponsDataSpy');
    });

    it('should sync to Connect RELOAD_COUPONS and RELOAD_COMPONENTS events', () => {
      component.ngOnInit();
    });

    it('should loadCouponsData when executed and on connect events', () => {
      component.ngOnInit();
      expect(component['loadCouponsData']).toHaveBeenCalledTimes(1);
    });
  });

  it('ngOnDestroy should unsubscribe', () => {
    component['sportsConfigSubscription'] = {
      unsubscribe: jasmine.createSpy('sportsConfigSubscription.unsubscribe')
    } as any;

    component.ngOnDestroy();

    expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
  });

  describe('@loadCoupons', () => {
    it('should set couponList', fakeAsync(() => {
      const couponsList = ['testCoupon'];
      component.isLoaded = false;
      component.isResponseError = true;
      component.sport = {
        coupons: jasmine.createSpy('jackpot').and.returnValue(Promise.resolve(couponsList))
      };
      component['loadCoupons']();
      tick();
      expect(component.couponsList as any).toEqual(couponsList);
      expect(component.isResponseError).toBe(false);
      expect(component.isLoaded).toBe(true);
    }));

    it('should call loadDefaultData if error', fakeAsync(() => {
      component.sport = {
        coupons: jasmine.createSpy('jackpot').and.returnValue(Promise.reject('error'))
      };
      spyOn(component as any, 'loadDefaultData').and.callThrough();
      component['loadCoupons']();
      tick();
      expect(component['loadDefaultData']).toHaveBeenCalled();
    }));
  });

  describe('@loadCouponsData', () => {
    it('should call loadCoupons', () => {
      spyOn(component as any, 'loadCoupons').and.callThrough();
      component.sport = {
        coupons: jasmine.createSpy('jackpot').and.returnValue(Promise.resolve())
      };
      component['loadCouponsData']();
      expect(component['loadCoupons']).toHaveBeenCalled();
    });

    it('should call loadDefaultData', () => {
      spyOn(component as any, 'loadDefaultData').and.callThrough();
      routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue(null);
      component.sport = null;
      component['loadCouponsData']();
      expect(component['loadDefaultData']).toHaveBeenCalled();
    });

    it('should call loadCoupons', () => {
      const sportObj = {
        coupons: jasmine.createSpy('jackpot')
      };
      component['loadCoupons'] = jasmine.createSpy('coupons');
      routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue('routResult');
      sportsConfigService.getSport = jasmine.createSpy('getSport').and.returnValue(observableOf(sportObj));
      component.sport = null;
      component['loadCouponsData']();
      expect(component['loadCoupons']).toHaveBeenCalled();
      expect(component.sport).toBe(sportObj);
    });

    it('should call loadDefaultData', () => {
      spyOn(component as any, 'loadDefaultData').and.callThrough();
      spyOn(console, 'warn');
      routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue('routResult');
      sportsConfigService.getSport = jasmine.createSpy('getSport').and.returnValue(throwError({}));
      component.sport = null;

      component['loadCouponsData']();
      expect(component['loadDefaultData']).toHaveBeenCalled();
      expect(console.warn).toHaveBeenCalledWith('SportMain', {});

      sportsConfigService.getSport = jasmine.createSpy('getSport').and.returnValue(throwError({ error: 'error' }));
      component['loadCouponsData']();
      expect(component['loadDefaultData']).toHaveBeenCalled();
      expect(console.warn).toHaveBeenCalledWith('SportMain', 'error');
    });
  });
});
