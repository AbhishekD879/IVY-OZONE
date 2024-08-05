import { Router } from '@angular/router';
import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { CouponsListService } from '@sb/components/couponsList/coupons-list.service';
import { BetFilterParamsService } from '@app/retail/services/betFilterParams/bet-filter-params.service';

import { ICoupon } from '@sb/components/couponsListSportTab/coupons.model';
import { ICouponSegment } from '@sb/components/couponsList/coupons-list.model';

@Component({
  selector: 'coupons-list',
  styleUrls: ['./coupons-list.component.scss'],
  templateUrl: './coupons-list.component.html',
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class CouponsListComponent implements OnInit {
  @Input() couponsList: ICoupon[];

  couponSegments:  ICouponSegment[];

  constructor(
    private betFilterParamsService: BetFilterParamsService,
    private couponsListService: CouponsListService,
    private routingHelperService: RoutingHelperService,
    private router: Router
  ) { }

  ngOnInit(): void {
    if (this.couponsList && this.couponsList.length) {
      this.couponsListService.getCouponSegment().subscribe((segments: ICouponSegment[]) => {
        this.couponSegments = this.couponsListService.groupCouponBySegment(this.couponsList, segments);
      }, () => {
        this.couponSegments = this.couponsListService.groupCouponBySegment(this.couponsList, []);
      });
    }
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {ICoupon} coupon
   * @return {string}
   */
  trackById(index: number, coupon: ICoupon): string {
    return coupon.id ? `${index}${coupon.id}` : index.toString();
  }

  /**
   * couponUrl()
   * @param {ICoupon} coupon
   * @returns {string}
   */
  couponUrl(coupon: ICoupon): string {
    const couponName = this.routingHelperService.encodeUrlPart(coupon.name);
    return `/coupons/football/${couponName}/${coupon.id}`;
  }

  /**
   * goToBetFilter()
   */
  goToBetFilter(): void {
    this.betFilterParamsService.chooseMode().subscribe(betFilterParams => {
      if (!betFilterParams.cancelled) {
        this.router.navigate(['bet-filter', 'filters', 'your-teams']);
      }
    });
  }
}
