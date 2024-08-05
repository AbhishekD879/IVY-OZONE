import { async } from '@angular/core/testing';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { CouponSegmentListComponent } from './coupon-segment-list.component';
import { Observable } from 'rxjs/Observable';
import { CouponSegmentExt, DayOfWeek, ScheduleType } from '@app/client/private/models/footballcoupon.model';
import * as _ from 'lodash';
import { AppConstants } from '@app/app.constants';
import { Order } from '@app/client/private/models/order.model';

describe('CouponSegmentListComponent', () => {
  let component: CouponSegmentListComponent;
  let couponList: CouponSegmentExt[];

  let apiClientService;
  let dialogService: Partial<DialogService>;
  let matSnackBar: Partial<MatSnackBar>;
  let router: Partial<Router>;
  let globalLoaderService: Partial<GlobalLoaderService>;

  const scheduleType = ScheduleType;

  beforeEach(async(() => {
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
        yesCallback();
      })
    };

    router = {
      navigate: jasmine.createSpy('navigate')
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hidLoader')
    };

    couponList = [{
      id: 4,
      title: 'Test 1 title',
      dayOfWeek: ['MONDAY']
    }, {
      id: 7,
      title: 'Test 2 title'
    }] as any;

    apiClientService = {
      footballCoupon: jasmine.createSpy('footballCoupon').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(Observable.of({ body: couponList })),
        remove: jasmine.createSpy('remove').and.returnValue(Observable.of({})),
        reorder: jasmine.createSpy('reorder').and.returnValue(Observable.of({}))
      })
    };

    matSnackBar = {
      open: jasmine.createSpy('open')
    };

    component = new CouponSegmentListComponent(
      apiClientService as any,
      dialogService as any,
      matSnackBar as any,
      router as any,
      globalLoaderService as any
    );
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should get coupons', () => {
    component['setCouponSegmentExt'] = jasmine.createSpy('setCouponSegmentExt');
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.footballCoupon().findAllByBrand).toHaveBeenCalled();
    expect(component.couponSegments).toEqual(couponList);
    expect(component['setCouponSegmentExt']).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#ngOnInit should handle error when get coupons', () => {
    apiClientService.footballCoupon().findAllByBrand.and.returnValue(Observable.throw({}));
    component['setCouponSegmentExt'] = jasmine.createSpy('setCouponSegmentExt');
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(component['setCouponSegmentExt']).not.toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#setCouponSegmentExt should set schedule type', () => {
    component['setDayOfWeekArr'] = jasmine.createSpy('setDayOfWeekArr');
    component['setCouponSegmentExt']();
    expect(component['setDayOfWeekArr']).not.toHaveBeenCalled();

    component.couponSegments = couponList;
    component['setCouponSegmentExt']();
    expect(component['setDayOfWeekArr']).toHaveBeenCalled();
    expect(component.couponSegments[0].scheduleType).toEqual(scheduleType.DaysOfWeek);
    expect(component.couponSegments[1].scheduleType).toEqual(scheduleType.DatesPeriod);
  });

  it('#setDayOfWeekArr should set dayOfWeekArr', () => {
    const coupon: CouponSegmentExt = {
      id: 4,
      dayOfWeek: ['MONDAY']
    } as any;
    component['setDayOfWeekArr'](coupon);

    const dayOfWeekArr = [
      { dayName: 'SUNDAY', checked: false },
      { dayName: 'MONDAY', checked: true },
      { dayName: 'TUESDAY', checked: false },
      { dayName: 'WEDNESDAY', checked: false },
      { dayName: 'THURSDAY', checked: false },
      { dayName: 'FRIDAY', checked: false },
      { dayName: 'SATURDAY', checked: false }
    ];

    const expected: CouponSegmentExt = {
      id: 4,
      dayOfWeek: ['MONDAY'],
      dayOfWeekArr: _.map(dayOfWeekArr, item => new DayOfWeek(item.dayName, item.checked))
    } as any;

    expect(coupon).toEqual(expected);
  });

  it('#data should return filtered coupons', () => {
    component.couponSegments = _.cloneDeep(couponList);
    component.searchField = '';
    expect(component.data).toEqual(couponList);

    component.searchField = 'test 2';
    expect(component.data).toEqual([couponList[1]]);
  });

  it('#removeCouponSegment should show dialog and remove coupon', () => {
    component.couponSegments = _.cloneDeep(couponList);
    const targetCoupon: CouponSegmentExt = couponList[1];

    component.removeCouponSegment(targetCoupon);
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: 'Remove Segment',
      message: `Are You Sure You Want to Remove ${targetCoupon.title} Segment`,
      yesCallback: jasmine.any(Function)
    });

    expect(apiClientService.footballCoupon().remove).toHaveBeenCalledWith(targetCoupon.id);
    expect(component.couponSegments).toEqual([couponList[0]]);
  });

  it('#addNewSegment should navigate to new page', () => {
    component.addNewSegment();
    expect(router.navigate).toHaveBeenCalledWith([`/football-coupon/coupon-segments/add`]);
  });

  it('#reorderHandler should save new coupon order', () => {
    const newOrder: Order = { order: ['123'], id: '321' };
    component.reorderHandler(newOrder);
    expect(apiClientService.footballCoupon().reorder).toHaveBeenCalledWith(newOrder);
    expect(matSnackBar.open).toHaveBeenCalledWith(
      `Segments order saved!`,
      'Ok!',
      {
        duration: AppConstants.HIDE_DURATION,
      }
    );
  });
});
