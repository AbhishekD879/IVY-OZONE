import { of, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { CouponsListComponent } from '@sbModule/components/couponsList/coupons-list.component';

describe('CouponsListSportTabComponent', () => {
  let component: CouponsListComponent,
    couponsListService,
    betFilterParamsService,
    routingHelperService,
    router;

  const couponSegment = [{ title: 'Coupons', couponKeys: '23, 56, 76'}];

  beforeEach(() => {
    couponsListService = {
      getCouponSegment: jasmine.createSpy().and.returnValue(of([])),
      groupCouponBySegment: jasmine.createSpy().and.returnValue([{}])
    };
    router = {
      navigate: jasmine.createSpy()
    };
    betFilterParamsService = {
      chooseMode: jasmine.createSpy().and.returnValue(of({}))
    };
    routingHelperService = {
      encodeUrlPart: jasmine.createSpy('encodeUrlPart').and.callFake((couponName: string) => couponName)
    };

    component = new CouponsListComponent(betFilterParamsService, couponsListService, routingHelperService, router);
  });

  describe('@ngOnInit', () => {
    it('should not create coupon segments if no data', fakeAsync(() => {
      component.couponsList = [];
      component.ngOnInit();
      expect(couponsListService.getCouponSegment).not.toHaveBeenCalled();
    }));

    it('should not create coupon segments if data are exist', fakeAsync(() => {
      couponsListService.getCouponSegment.and.returnValue(of(couponSegment));
      component.couponsList = [{ id: '243'}] as any;
      component.ngOnInit();
      tick(200);
      expect(couponsListService.getCouponSegment).toHaveBeenCalled();
      expect(couponsListService.groupCouponBySegment).toHaveBeenCalledWith(component.couponsList, couponSegment);
    }));

    it('should not create coupon segments if CMS data are not exist', () => {
      couponsListService.getCouponSegment.and.returnValue(throwError(null));
      component.couponsList = [{ id: '243'}] as any;
      component.ngOnInit();
      expect(couponsListService.groupCouponBySegment).toHaveBeenCalledWith(component.couponsList, []);
    });
  });

  describe('@trackById', () => {
    it('should track event by index', () => {
      expect(component.trackById(2, {} as any)).toEqual('2');
    });

    it('should track event by id', () => {
      expect(component.trackById(1, { id: 72124 } as any)).toEqual('172124');
    });
  });

  it('@couponUrl should form url with coupon name and ir', () => {
    expect(component.couponUrl({ name: 'coupon-name', id: 'coupon-id' } as any))
      .toEqual(`/coupons/football/coupon-name/coupon-id`);
    expect(routingHelperService.encodeUrlPart).toHaveBeenCalledWith('coupon-name');
  });

  describe('@goToBetFilter', () => {
    it('should navigate to third-party football filter app', () => {
      component.goToBetFilter();
      expect(router.navigate).toHaveBeenCalledWith(['bet-filter', 'filters', 'your-teams']);
    });

    it('should not navigate to third-party football filter app', () => {
      betFilterParamsService.chooseMode = jasmine.createSpy('chooseMode').and.returnValue(of({ cancelled: true }));

      component.goToBetFilter();
      expect(router.navigate).not.toHaveBeenCalledWith(['bet-filter', 'filters', 'your-teams']);
    });
  });
});
