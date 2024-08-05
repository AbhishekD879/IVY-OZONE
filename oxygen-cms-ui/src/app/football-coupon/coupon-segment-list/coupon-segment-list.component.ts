import * as _ from 'lodash';

import { Component, OnInit } from '@angular/core';

import { TableColumn } from '../../client/private/models/table.column.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DayOfWeek, CouponSegment, CouponSegmentExt, ScheduleType } from '../../client/private/models/footballcoupon.model';
import { DialogService } from '../../shared/dialog/dialog.service';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http';
import { HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { WEEKDAYS } from '../../core/constants/date-time.constant';
import { AppConstants } from '../../app.constants';
import { Order } from '@app/client/private/models/order.model';

@Component({
  templateUrl: './coupon-segment-list.component.html',
  styleUrls: ['./coupon-segment-list.component.scss'],
  providers: [
    DialogService
  ]
})
export class CouponSegmentListComponent implements OnInit {

  public isLoading: boolean = false;
  public couponSegments: CouponSegmentExt[];
  public searchField: string = '';

  dataTableColumns: Array<TableColumn> = [
    {
      name: 'Segment Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Coupon IDs',
      property: 'couponKeys'
    },
    {
      name: 'Period Start',
      property: 'from',
      type: 'date-no-time'
    },
    {
      name: 'Period End',
      property: 'to',
      type: 'date-no-time'
    },
    {
      name: 'Days of Week',
      property: 'dayOfWeekArr',
      type: 'array'
    }
  ];

  filterProperties: Array<string> = [
    'title'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private snackBar: MatSnackBar,
    private router: Router,
    private globalLoaderService: GlobalLoaderService
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService
      .footballCoupon()
      .findAllByBrand()
      .map((response: HttpResponse<CouponSegment[]>) => {
        return response.body;
      })
      .subscribe((data: CouponSegment[]) => {
        this.couponSegments = data as CouponSegmentExt[];
        this.setCouponSegmentExt();
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      }, error => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
  }

  /**
   *  Extend every football coupon with scheduleType and dayOfWeekArr properties
   *  UI model (CouponSegmentExt) differs from backend model (CouponSegment)
   */
  private setCouponSegmentExt(): void {
    if (this.couponSegments) {
      this.couponSegments.forEach(couponSegment => {
        if (couponSegment.dayOfWeek) {
          couponSegment.scheduleType = ScheduleType.DaysOfWeek;
          this.setDayOfWeekArr(couponSegment);
        } else {
          couponSegment.scheduleType = ScheduleType.DatesPeriod;
        }
      });
    }
  }

  /**
   *  Create DayOfWeek[] from string[]:
   *  Set couponSegment.dayOfWeekArr from couponSegment.dayOfWeek
   */
  private setDayOfWeekArr(couponSegment: CouponSegmentExt): void {
    const res: DayOfWeek[] = [];
    WEEKDAYS.forEach(dayName => {
      if (_.indexOf(couponSegment.dayOfWeek, dayName) === -1) {
        res.push(new DayOfWeek(dayName, false));
      } else {
        res.push(new DayOfWeek(dayName, true));
      }
    });
    couponSegment.dayOfWeekArr = res;
  }

  /**
   *  Search for Football Coupon as filtering data in array
   */
  public get data(): CouponSegmentExt[] {
    if (this.searchField.length > 0) {
      return this.couponSegments.filter(item => {
        return ~item.title.toLowerCase().indexOf(this.searchField.toLowerCase());
      });
    } else {
      return this.couponSegments;
    }
  }

  public removeCouponSegment(coupon: CouponSegmentExt): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Segment',
      message: `Are You Sure You Want to Remove ${coupon.title} Segment`,
      yesCallback: () => {
        this.apiClientService
          .footballCoupon()
          .remove(coupon.id)
          .subscribe(() => {
            _.remove(this.couponSegments, {id: coupon.id});
          });
      }
    });
  }

  public addNewSegment(): void {
    this.router.navigate([`/football-coupon/coupon-segments/add`]);
  }

  reorderHandler(order: Order): void {
    this.apiClientService
      .footballCoupon()
      .reorder(order)
      .subscribe(() => {
        this.snackBar.open(`Segments order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

}
