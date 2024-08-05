import { async } from '@angular/core/testing';
import * as _ from 'lodash';
import { Router } from '@angular/router';
import { FormControl, FormGroup } from '@angular/forms';
import { Observable } from 'rxjs/Observable';

import { CouponSegmentComponent } from './coupon-segment.component';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { DialogService } from '../../shared/dialog/dialog.service';
import { BrandService } from '../../client/private/services/brand.service';
import { CouponSegment, CouponSegmentExt, DayOfWeek, ScheduleType } from '../../client/private/models/footballcoupon.model';

describe('CouponSegmentEditComponent', () => {
  let component: CouponSegmentComponent;
  let couponSegment: CouponSegmentExt;

  let activatedRoute;
  let apiClientService;
  let brandService: Partial<BrandService>;
  let router: Partial<Router>;
  let globalLoaderService: Partial<GlobalLoaderService>;
  let dialogService: Partial<DialogService>;

  const scheduleType = ScheduleType;

  beforeEach(async(() => {
    couponSegment = {
      title: 'Test Title',
      id: '5bd1bcdac9e77c00018d2ed6'
    } as any;

    brandService = {
      brand: 'ladbrokes'
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
        yesCallback();
      })
    };
    activatedRoute = {
      params: {
        subscribe: jasmine.createSpy('subscribe').and.callFake((cb) => cb({ id: '1' }))
      }
    };
    apiClientService = {
      footballCoupon: jasmine.createSpy('footballCoupon').and.returnValue({
        getById: jasmine.createSpy('getById').and.returnValue(Observable.of({ body: { id: '654' } })),
        edit: jasmine.createSpy('edit').and.returnValue(Observable.of({ body: couponSegment })),
        add: jasmine.createSpy('add').and.returnValue(Observable.of({ body: { id: 'testid' } })),
        remove: jasmine.createSpy('remove').and.returnValue(Observable.of({}))
      })
    };

    component = new CouponSegmentComponent(
      router as any,
      globalLoaderService as any,
      apiClientService as any,
      activatedRoute as any,
      dialogService as any,
      brandService as any
    );
  }));

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit: should create a form and call loadInitData', () => {
    spyOn<any>(component, 'loadInitData');
    component.ngOnInit();
    expect(component.form.get('couponName')).toBeTruthy();
    expect(component.form.get('couponKeys')).toBeTruthy();
    expect(component.form.get('couponSheduleType')).toBeTruthy();
    expect(Object.keys((component.form.get('daysWeek') as FormGroup).controls).length).toBe(7);
    expect(component['loadInitData']).toHaveBeenCalled();
  });

  it('#get couponKeys', () => {
    component.form = new FormGroup({
      couponKeys: new FormControl('')
    });
    expect(component.couponKeys).toBeTruthy();
  });

  it('#daysOfWeekValid should validate days of week', () => {
    component.couponSegment = {} as any;
    expect(component.daysOfWeekValid()).toBeFalsy();

    component.couponSegment.scheduleType = scheduleType.DatesPeriod;
    expect(component.daysOfWeekValid()).toBeTruthy();

    component.couponSegment.scheduleType = scheduleType.DaysOfWeek;
    expect(component.daysOfWeekValid()).toBeFalsy();

    component.couponSegment.dayOfWeekArr = [{ dayName: 'MONDAY', checked: true }];
    expect(component.daysOfWeekValid()).toBeTruthy();
  });

  it('#createEmptyCoupon: should create empty coupon segment', () => {
    component.createEmptySegment();
    expect(component.couponSegment.id).toBeNull();
    expect(component.couponSegment.createdAt).toBeNull();
    expect(component.couponSegment.createdBy).toBeNull();
    expect(component.couponSegment.updatedByUserName).toBeNull();
    expect(component.couponSegment.createdByUserName).toBeNull();
    expect(component.couponSegment.updatedAt).toBeNull();
    expect(component.couponSegment.updatedBy).toBeNull();
    expect(component.couponSegment.brand).toBe(brandService.brand);

    expect(component.couponSegment.title).toBe('');
    expect(component.couponSegment.couponKeys).toBe('');
    expect(component.couponSegment.scheduleType).toBe(ScheduleType.DaysOfWeek);
    expect(component.couponSegment.dayOfWeekArr.length).toBe(7);
    expect(component.couponSegment.dayOfWeek).toBeNull();
    expect(component.couponSegment.from).toBeNull();
    expect(component.couponSegment.to).toBeNull();
  });

  it('#loadInitData should get existing coupon', () => {
    component['setCouponSegmentExt'] = jasmine.createSpy('setCouponSegmentExt');
    component['setBreadcrumbsData'] = jasmine.createSpy('setBreadcrumbsData');

    component['loadInitData']();

    expect(apiClientService.footballCoupon().getById).toHaveBeenCalledWith('1');
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(component.pageType).toEqual('edit');
    expect(component['setCouponSegmentExt']).toHaveBeenCalledWith({ id: '654' } as CouponSegment);
    expect(component['setBreadcrumbsData']).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#loadInitData should handle request error on getById', () => {
    apiClientService.footballCoupon().getById.and.returnValue(Observable.throw(''));
    component['setCouponSegmentExt'] = jasmine.createSpy('setCouponSegmentExt');
    component['setBreadcrumbsData'] = jasmine.createSpy('setBreadcrumbsData');

    component['loadInitData']();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(component['setCouponSegmentExt']).not.toHaveBeenCalledWith({ id: '654' } as CouponSegment);
    expect(component['setBreadcrumbsData']).not.toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#loadInitData should handle error on get coupon', () => {
    component['loadInitData']();

    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(component.pageType).toEqual('edit');
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#loadInitData should create new coupon', () => {
    component['setBreadcrumbsData'] = jasmine.createSpy('setBreadcrumbsData');
    component['createEmptySegment'] = jasmine.createSpy('createEmptySegment');
    activatedRoute.params.subscribe.and.callFake((cb) => cb({}));
    component['loadInitData']();

    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(component.pageType).toEqual('add');
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component['setBreadcrumbsData']).toHaveBeenCalledWith(true);
    expect(component['createEmptySegment']).toHaveBeenCalled();
  });

  it('#setCouponSegmentExt should set coupon segment', () => {
    component['setDayOfWeekArr'] = jasmine.createSpy('setDayOfWeekArr');

    component['setCouponSegmentExt']({ dayOfWeek: ['someDay'] } as CouponSegment);
    expect(component.couponSegment.scheduleType).toEqual(scheduleType.DaysOfWeek);

    component['setCouponSegmentExt']({ dayOfWeek: null } as CouponSegment);
    expect(component.couponSegment.scheduleType).toEqual(scheduleType.DatesPeriod);

    expect(component['setDayOfWeekArr']).toHaveBeenCalledTimes(2);
  });

  it('#updateCouponSegment should update fields: from, to; call #updateDayOfWeek', () => {
    component['updateDayOfWeek'] = jasmine.createSpy('updateDayOfWeek');

    component.couponSegment = {
      scheduleType: scheduleType.DaysOfWeek,
      from: '123',
      to: '321'
    } as any;
    component['updateCouponSegment']();
    expect(component.couponSegment.from).toEqual(null);
    expect(component.couponSegment.to).toEqual(null);
    expect(component['updateDayOfWeek']).toHaveBeenCalled();

    component.couponSegment = {
      scheduleType: scheduleType.DatesPeriod,
      from: '2018-09-12T02:42:01+03:00',
      to: '2019-09-12T02:42:01+03:00',
      dayOfWeek: ['MONDAY', 'TUESDAY']
    } as any;
    component['updateCouponSegment']();
    expect(component.couponSegment.from).toEqual('2018-09-11T23:42:01.000Z');
    expect(component.couponSegment.to).toEqual('2019-09-11T23:42:01.000Z');
    expect(component.couponSegment.dayOfWeek).toBeNull();
  });

  it('#setDayOfWeekArr should set dayOfWeekArr', () => {
    component.couponSegment = {
      dayOfWeek: ['MONDAY', 'TUESDAY'],
      dayOfWeekArr: null
    } as any;

    component['setDayOfWeekArr']();

    let dayOfWeekArr: DayOfWeek[] = [
      { dayName: 'SUNDAY', checked: false },
      { dayName: 'MONDAY', checked: true },
      { dayName: 'TUESDAY', checked: true },
      { dayName: 'WEDNESDAY', checked: false },
      { dayName: 'THURSDAY', checked: false },
      { dayName: 'FRIDAY', checked: false },
      { dayName: 'SATURDAY', checked: false }
    ];
    dayOfWeekArr = _.map(dayOfWeekArr, item => new DayOfWeek(item.dayName, item.checked));
    expect(component.couponSegment.dayOfWeekArr).toEqual(dayOfWeekArr);
  });

  it('#updateDayOfWeek should set dayOfWeek from dayOfWeekArr', () => {
    const dayOfWeekArr: DayOfWeek[] = [
      { dayName: 'SUNDAY', checked: false },
      { dayName: 'MONDAY', checked: true },
      { dayName: 'TUESDAY', checked: true },
      { dayName: 'WEDNESDAY', checked: false },
      { dayName: 'THURSDAY', checked: false },
      { dayName: 'FRIDAY', checked: false },
      { dayName: 'SATURDAY', checked: false }
    ];

    const dayOfWeek: string[] = ['MONDAY', 'TUESDAY'];

    component.couponSegment = {
      dayOfWeekArr,
      dayOfWeek: null
    } as any;

    component['updateDayOfWeek']();
    expect(component.couponSegment.dayOfWeek).toEqual(dayOfWeek);
  });

  it('#setBreadcrumbsData should create breadcrumbs array', () => {
    component.couponSegment = couponSegment;
    component['setBreadcrumbsData']();
    const existingCoupRes = [
      { label: 'Coupon Segments', url: '/football-coupon/coupon-segments' },
      { label: 'Test Title', url: '/football-coupon/coupon-segments/5bd1bcdac9e77c00018d2ed6' }
    ];
    expect(component.breadcrumbsData).toEqual(existingCoupRes);

    component['setBreadcrumbsData'](true);
    const addCoupRes = [
      { label: 'Coupon Segments', url: '/football-coupon/coupon-segments' },
      { label: 'New Segment', url: '/football-coupon/coupon-segments/add' }
    ];
    expect(component.breadcrumbsData).toEqual(addCoupRes);
  });

  it('#saveChanges should save coupon', () => {
    component['updateCouponSegment'] = jasmine.createSpy('updateCouponSegment');
    component['setCouponSegmentExt'] = jasmine.createSpy('setCouponSegmentExt');

    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };

    component.couponSegment = couponSegment;

    component['saveChanges']();

    expect(component['updateCouponSegment']).toHaveBeenCalled();
    expect(apiClientService.footballCoupon().edit).toHaveBeenCalledWith(component.couponSegment);
    expect(component['setCouponSegmentExt']).toHaveBeenCalledWith(component.couponSegment);
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
      {
        title: `Football Coupon ${component.couponSegment.title}`,
        message: `Football Coupon ${component.couponSegment.title} is Saved.`
      }
    );
  });

  it('#createSegmen should show dialog and send request', () => {
    component.couponSegment = {
      title: 'test title'
    } as any;
    component['updateCouponSegment'] = jasmine.createSpy('updateCouponSegment');
    component['sendNewSegmentInformation'] = jasmine.createSpy('sendNewSegmentInformation');

    component.createSegment();
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: `Create Segment: ${component.couponSegment.title}`,
      message: `Do You Want to Create a Segment?`,
      yesCallback: jasmine.any(Function)
    });

    expect(component['updateCouponSegment']).toHaveBeenCalled();
    expect(component['sendNewSegmentInformation']).toHaveBeenCalled();
  });

  it('#sendNewSegmentInformation should send new info and show notification', () => {
    component.couponSegment = couponSegment;

    component.sendNewSegmentInformation();
    expect(apiClientService.footballCoupon().add).toHaveBeenCalledWith(component.couponSegment);
    expect(component.couponSegment.id).toEqual('testid');
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Creating Completed',
      message: 'The Segment is Successfully Created.'
    });
    expect(router.navigate).toHaveBeenCalledWith([
      `/football-coupon/coupon-segments/${component.couponSegment.id}`
    ]);
  });

  it('#isValidModel should validate coupon segment', () => {
    expect(component.isValidModel(component.couponSegment)).toBeFalsy();
    component.couponSegment = {
      title: 'test title',
      couponKeys: 'keys'
    } as any;
    expect(component.isValidModel(component.couponSegment)).toBeFalsy();

    component.couponSegment.scheduleType = scheduleType.DatesPeriod;
    expect(component.isValidModel(component.couponSegment)).toBeTruthy();

    component.couponSegment.scheduleType = scheduleType.DaysOfWeek;
    expect(component.isValidModel(component.couponSegment)).toBeFalsy();

    component.couponSegment.dayOfWeekArr = [{
      dayName: 'MONDAY',
      checked: true
    }];
    expect(component.isValidModel(component.couponSegment)).toBeTruthy();
  });

  it('#actionHandler should call correct method', () => {
    spyOn(component, 'removeSegment');
    component.actionsHandler('remove');
    expect(component.removeSegment).toHaveBeenCalled();

    spyOn(component, 'saveChanges');
    component.actionsHandler('save');
    expect(component.saveChanges).toHaveBeenCalled();

    spyOn(component, 'revertChanges');
    component.actionsHandler('revert');
    expect(component.revertChanges).toHaveBeenCalled();
  });

  it('#actionHandler should do nothing if wrong event', () => {
    spyOn(component, 'removeSegment');
    spyOn(component, 'saveChanges');
    spyOn(component, 'revertChanges');

    component.actionsHandler('test-event');
    expect(component.removeSegment).not.toHaveBeenCalled();
    expect(component.saveChanges).not.toHaveBeenCalled();
    expect(component.revertChanges).not.toHaveBeenCalled();
  });

  it('handleDateUpdate should segment date', () => {
    const startDate = '2018-09-12T02:42:01+03:00',
      endDate = '2019-09-12T02:42:01+03:00';
    component.couponSegment = couponSegment;
    component.handleDateUpdate({
      startDate: startDate,
      endDate: endDate
    });
    expect(component.couponSegment.from).toEqual(startDate);
    expect(component.couponSegment.to).toEqual(endDate);
  });

  it('#removeSegment should call remove and update navigation', () => {
    component.couponSegment = couponSegment;
    component.removeSegment();
    expect(apiClientService.footballCoupon().remove).toHaveBeenCalledWith(component.couponSegment.id);
    expect(router.navigate).toHaveBeenCalledWith(['/football-coupon/coupon-segments']);
  });

  it('#revertChanges should call #loadInitData', () => {
    component['loadInitData'] = jasmine.createSpy('loadInitData');
    component.revertChanges();
    expect(component['loadInitData']).toHaveBeenCalled();
  });

});
