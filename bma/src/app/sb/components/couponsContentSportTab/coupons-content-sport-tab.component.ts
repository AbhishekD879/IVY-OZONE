import { from as observableFrom, Subject } from 'rxjs';
import { Component, Input, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';

import { ICoupon, ICouponWithEvents } from '@sb/components/couponsListSportTab/coupons.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { finalize, takeUntil } from 'rxjs/operators';
import { SlpSpinnerStateService } from '@core/services/slpSpinnerState/slpSpinnerState.service';
import { GamingService } from '@core/services/sport/gaming.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'coupons-content-sport-tab',
  templateUrl: 'coupons-content-sport-tab.component.html'
})
export class CouponsContentSportTabComponent implements OnInit, OnDestroy {
  @Input() sport: GamingService;

  coupons: ICouponWithEvents[];
  isLoaded: boolean = false;
  isResponseError: boolean = false;
  isExpanded: boolean = false;

  private subscribedCoupons: { [key: string]: boolean } = {};
  private readonly tagName: string = 'CouponsContentTab';
  private unsubscribe$ = new Subject<void>();

  constructor(
    private slpSpinnerStateService: SlpSpinnerStateService,
    private pubSubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    if (this.unsubscribe$.isStopped) {
      this.unsubscribe$ = new Subject<void>();
    }
    this.sport.extendRequestConfig('coupons');
    this.loadCouponsData();
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
    // unSubscribe LS Updates via liveServe PUSH updates (iFrame)!
    for (const couponId in this.subscribedCoupons) {
      if (Object.prototype.hasOwnProperty.call(this.subscribedCoupons, couponId) && this.subscribedCoupons[couponId]) {
        this.sport.unSubscribeCouponsForUpdates(couponId);
      }
    }

    this.pubSubService.unsubscribe(this.tagName);

    this.subscribedCoupons = {};
  }

  trackById(index: number, coupon: ICouponWithEvents): number {
    return +coupon.id;
  }

  getCouponContent(coupon: ICouponWithEvents): void {
    const requestParams = this.sport.couponEventsRequestParams(coupon.id);

    if (!coupon.isExpanded) {
      this.unsubscribeForUpdates(coupon.id);

      observableFrom(this.sport.couponEventsByCouponId(_.extend({}, requestParams, { couponId: coupon.id })))
        .pipe(
          takeUntil(this.unsubscribe$),
          finalize(() => {
            this.changeDetectorRef.detectChanges();
          })
        )
        .subscribe((events: ISportEvent[]) => {
          coupon.isExpanded = true;
          coupon.isEventsLoaded = true;
          coupon.isEventsAvailable = !!(events && events.length);
          // Subscribe LS Updates via liveServe PUSH updates (iFrame)!
          if (coupon.isEventsAvailable) {
            this.subscribedCoupons[coupon.id] = true;
            this.sport.subscribeCouponsForUpdates(events, coupon.id);
          }
          coupon.events = _.sortBy(events, 'typeDisplayOrder');
        }, error => {
          coupon.isEventsLoaded = true;
          coupon.isEventsAvailable = false;
          console.error('Sort Events Data:', error);
        });
    } else {
      coupon.isExpanded = false;
      this.unsubscribeForUpdates(coupon.id);
    }
    this.changeDetectorRef.detectChanges();
  }

  reloadComponent(): void {
    this.isLoaded = false;
    this.isResponseError = false;
    this.isExpanded = false;
    this.coupons = [];
    this.ngOnDestroy();
    this.ngOnInit();
  }

  private addListeners(): void {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.LIVE_SERVE_UPDATE, () => {
      this.changeDetectorRef.detectChanges();
    });
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, (eventId: number) => {
      this.deleteEvent(eventId);
    });
  }

  /**
   * unSubscribe LS Updates via liveServe PUSH updates (iFrame)!
   */
  private unsubscribeForUpdates(id: string) {
    if (!this.subscribedCoupons[id]) {
      return;
    }

    this.subscribedCoupons[id] = false;
    this.sport.unSubscribeCouponsForUpdates(id);
  }

  /**
   * Load Coupons Data
   */
  private loadCouponsData(): void {
    this.isLoaded = false;
    this.isResponseError = false;

    observableFrom(this.sport.coupons())
      .pipe(
        takeUntil(this.unsubscribe$),
        finalize(() => {
          this.slpSpinnerStateService.handleSpinnerState();
          this.isLoaded = true;
          this.changeDetectorRef.detectChanges();
        })
      )
    .subscribe((coupons: ICoupon[]) => {
      this.coupons = <ICouponWithEvents[]>coupons.slice();
      this.addListeners();
      this.isResponseError = false;
    }, error => {
      this.coupons = [];
      this.isResponseError = true;
      console.warn('Coupons Data:', error && error.error || error);
    });
  }

  /**
   * @param {number} eventId
   */
  private deleteEvent(eventId: number): void {
    this.coupons.forEach((coupon: ICouponWithEvents, i: number) => {
      this.deleteIndex(coupon, eventId, i);
    });
  }

  private deleteIndex(coupon: ICouponWithEvents, eventId: number, index: number): void {
    if (!coupon.events) {
      return;
    }
    const eventIndex = coupon.events.findIndex((event: ISportEvent) => Number(event.id) === Number(eventId));
    if (eventIndex !== -1) {
      coupon.events.splice(eventIndex, 1);
    }
    if (!coupon.events.length) {
      this.coupons.splice(index, 1);
    }
  }
}
