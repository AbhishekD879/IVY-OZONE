import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';

import { DialogService } from '../../shared/dialog/dialog.service';
import { CouponSegment, CouponSegmentExt, DayOfWeek, ScheduleType } from '../../client/private/models/footballcoupon.model';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http';
import { DateRange } from '../../client/private/models/dateRange.model';
import { Breadcrumb } from '../../client/private/models/breadcrumb.model';
import * as _ from 'lodash';
import { BrandService } from '../../client/private/services/brand.service';
import { WEEKDAYS } from '../../core/constants/date-time.constant';
import { HttpResponse } from '@angular/common/http';

@Component({
  templateUrl: './coupon-segment.component.html',
  styleUrls: ['./coupon-segment.component.scss'],
  providers: [
    DialogService
  ]
})
export class CouponSegmentComponent implements OnInit {
  public isLoading: boolean = false;
  public pageType: string;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  public couponSegment: CouponSegmentExt;
  public scheduleType = ScheduleType;

  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private brandService: BrandService) { }

  ngOnInit(): void {
    this.form = new FormGroup({
      couponName: new FormControl('', [Validators.required]),
      couponKeys: new FormControl('', [Validators.required]),
      couponSheduleType: new FormControl(''),
      daysWeek: new FormGroup({})
    });
    WEEKDAYS.forEach(dayName => {
      (this.form.controls['daysWeek'] as FormGroup).addControl(dayName, new FormControl(false));
    });
    this.loadInitData();
  }

  public get couponKeys(): AbstractControl {
    return this.form.get('couponKeys');
  }

  public daysOfWeekValid(): boolean {
    return this.couponSegment.scheduleType === ScheduleType.DaysOfWeek && _.some(this.couponSegment.dayOfWeekArr, (day => day.checked)) ||
      this.couponSegment.scheduleType === ScheduleType.DatesPeriod;
  }

  createEmptySegment(): void {
    const temp: DayOfWeek[] = [];
    WEEKDAYS.forEach(dayName => {
      temp.push(new DayOfWeek(dayName, false));
    });
    this.couponSegment = {
      id: null,
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: this.brandService.brand,

      title: '',
      couponKeys: '',
      scheduleType: ScheduleType.DaysOfWeek,
      dayOfWeekArr: temp,
      dayOfWeek: null,
      from: null,
      to: null
    };
  }

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;

    this.activatedRoute.params.subscribe((params: Params) => {
      this.pageType = params.id ? 'edit' : 'add';
      if (this.pageType === 'edit') {
        this.apiClientService
            .footballCoupon()
            .getById(params['id'])
            .map((couponSegment: HttpResponse<CouponSegment>) => {
              return couponSegment.body;
            }).subscribe((couponSegment: CouponSegment) => {
              this.setCouponSegmentExt(couponSegment);
              this.setBreadcrumbsData();
              this.globalLoaderService.hideLoader();
              this.isLoading = false;
            }, () => {
              this.globalLoaderService.hideLoader();
              this.isLoading = false;
            });
      } else {
        this.setBreadcrumbsData(true);
        this.createEmptySegment();
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      }
    });
  }

  /**
   * Assigning input data to couponSegment and
   * extend the couponSegment with scheduleType and dayOfWeekArr properties
   * UI model (CouponSegmentExt) differs from backend model (CouponSegment)
   */
  private setCouponSegmentExt(couponSegment: CouponSegment): void {
    this.couponSegment = couponSegment as CouponSegmentExt;
    this.couponSegment.scheduleType = this.couponSegment.dayOfWeek ? ScheduleType.DaysOfWeek : ScheduleType.DatesPeriod;
    this.setDayOfWeekArr();
  }

  /**
   * Updating CouponSegment before saving:
   * - The segment can have either DaysOfWeek or two period dates
   * - Update couponSegment.dayOfWeek
   */
  private updateCouponSegment(): void {
    if (this.couponSegment.scheduleType === ScheduleType.DaysOfWeek) {
      this.updateDayOfWeek();
      this.couponSegment.from = this.couponSegment.to = null;
    } else {
      this.couponSegment.dayOfWeek = null;
      this.couponSegment.from = new Date(this.couponSegment.from).toISOString();
      this.couponSegment.to = new Date(this.couponSegment.to).toISOString();
    }
  }

  /**
   *  Create DayOfWeek[] from string[]:
   *  Set couponSegment.dayOfWeekArr from couponSegment.dayOfWeek
   */
  private setDayOfWeekArr(): void {
    const res: DayOfWeek[] = [];
    WEEKDAYS.forEach(dayName => {
      if (_.indexOf(this.couponSegment.dayOfWeek, dayName) === -1) {
        res.push(new DayOfWeek(dayName, false));
      } else {
        res.push(new DayOfWeek(dayName, true));
      }
    });
    this.couponSegment.dayOfWeekArr = res;
  }

  /**
   *  Create string[] from DayOfWeek[]:
   *  Set couponSegment.dayOfWeek from couponSegment.dayOfWeekArr
   */
  private updateDayOfWeek(): void {
    this.couponSegment.dayOfWeek = this.couponSegment.dayOfWeekArr
      .filter(day => day.checked)
      .map(day => day.dayName);
  }

  private setBreadcrumbsData(isNewCoupon: boolean = false): void {
    this.breadcrumbsData = [];
    this.breadcrumbsData.push({
      label: `Coupon Segments`,
      url: `/football-coupon/coupon-segments`
    });
    if (isNewCoupon) {
      this.breadcrumbsData.push({
        label: `New Segment`,
        url: `/football-coupon/coupon-segments/add`
      });
    } else {
      this.breadcrumbsData.push({
        label: this.couponSegment.title,
        url: `/football-coupon/coupon-segments/${this.couponSegment.id}`
      });
    }
  }

  saveChanges(): void {
    this.updateCouponSegment();
    this.apiClientService
      .footballCoupon()
      .edit(this.couponSegment as CouponSegment)
      .map((response: HttpResponse<CouponSegment>) => {
        return response.body;
      })
      .subscribe((coupon: CouponSegment) => {
        this.setCouponSegmentExt(coupon);
        this.actionButtons.extendCollection(this.couponSegment);
        this.dialogService.showNotificationDialog({
          title: `Football Segment`,
          message: `Football Segment is Saved.`
        });
      });

    this.dialogService.showNotificationDialog({
      title: `Football Coupon ${this.couponSegment.title}`,
      message: `Football Coupon ${this.couponSegment.title} is Saved.`
    });
  }

  /**
   * Confirmation dialog showing, data preprocessing, data saving.
   */
  createSegment(): void {
    this.dialogService.showConfirmDialog({
      title: `Create Segment: ${this.couponSegment.title}`,
      message: `Do You Want to Create a Segment?`,
      yesCallback: () => {
        this.updateCouponSegment();
        this.sendNewSegmentInformation();
      }
    });
  }

  public sendNewSegmentInformation(): void {
    this.apiClientService
      .footballCoupon()
      .add(this.couponSegment)
      .subscribe(data => {
        this.couponSegment.id = data.body.id;

        this.dialogService.showNotificationDialog({
          title: 'Creating Completed',
          message: 'The Segment is Successfully Created.'
        });
        this.router.navigate([`/football-coupon/coupon-segments/${this.couponSegment.id}`]);
      });
  }

  public isValidModel(couponSegment: CouponSegmentExt): boolean {
    return couponSegment && couponSegment.title && couponSegment.title.length > 0 && couponSegment.couponKeys &&
      ( couponSegment.scheduleType === ScheduleType.DatesPeriod ||
        couponSegment.scheduleType === ScheduleType.DaysOfWeek && _.some(couponSegment.dayOfWeekArr, (day => day.checked)) );
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeSegment();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  handleDateUpdate(data: DateRange): void {
    this.couponSegment.from = data.startDate;
    this.couponSegment.to = data.endDate;
  }

  removeSegment(): void {
    this.router.navigate(['/football-coupon/coupon-segments']);
    this.apiClientService
      .footballCoupon()
      .remove(this.couponSegment.id)
      .subscribe(() => {
        this.router.navigate(['/football-coupon/coupon-segments']);
      });
  }

  revertChanges(): void {
    this.loadInitData();
  }

}
