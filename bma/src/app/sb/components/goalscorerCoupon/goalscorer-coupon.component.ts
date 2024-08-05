import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { Component, Input, OnInit } from '@angular/core';
import { IGoalscorerCoupon } from '@core/models/goalscorer-coupon.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { TimeService } from '@core/services/time/time.service';
import { GoalscorerCouponService } from '@sb/components/goalscorerCoupon/goalscorer-coupon.service';

@Component({
  selector: 'goalscorer-coupon',
  templateUrl: './goalscorer-coupon.component.html',
  styleUrls: ['./goalscorer-coupon.component.scss']
})
export class GoalscorerCouponComponent implements OnInit {

  @Input() couponEvents: IGoalscorerCoupon[];
  @Input() eventIdFromEDP: number;

  goalScorersToShow: number;
  goalScorersLimit: number;
  ycIconDisplay = 'general';
  customStylesClass = "['show-all-button-light']";
  couponEventsWithGoalScorers: IGoalscorerCoupon[];

  constructor(
    private goalscorerCouponService: GoalscorerCouponService,
    private routingHelperService: RoutingHelperService,
    private timeService: TimeService,
    private gtmService: GtmService,
    private datePipe: DatePipe,
    private router: Router
  ) {
  }

  ngOnInit() {
    this.couponEventsWithGoalScorers = this.goalscorerCouponService.formGoalScorers(this.couponEvents);
    this.goalScorersToShow = this.goalscorerCouponService.goalScorersToShow;
    this.goalScorersLimit = this.goalscorerCouponService.goalScorersLimit;
  }

  /**
   * getStartTime()
   * @param {number} startTime
   * @returns {string}
   */
  getStartTime(startTime: number): string {
    return this.timeService.getLocalHourMinInMilitary(startTime);
  }

  /**
   * goToEvent()
   * @param {ISportEvent} event
   */
  goToEvent(event: ISportEvent): void {
    const edpUrl = this.routingHelperService.formResultedEdpUrl(event);

    this.router.navigateByUrl(edpUrl);
    this.trackGoToEDP(event.name);
  }

  getEventUrl(event: ISportEvent): string {
    return `/${this.routingHelperService.formEdpUrl(event)}`;
  }

  /**
   * trackGoToEDP()
   * @param {string} eventName
   */
  trackGoToEDP(eventName: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'goalscorer coupon',
      eventAction: 'go to event',
      eventLabel: eventName
    });
  }

  /**
   * trackShowAll()
   * @param eventEntity
   */
  trackShowAll(eventEntity: ISportEvent): void {
    if (eventEntity.goalScorersShowAll) {
      this.gtmService.push('trackEvent', {
        eventCategory: 'goalscorer coupon',
        eventAction: 'show all',
        eventLabel: eventEntity.name
      });
      eventEntity.goalScorersToShow = eventEntity.goalScorers.length;
    } else {
      eventEntity.goalScorersToShow = this.goalscorerCouponService.goalScorersToShow;
    }
  }

  /**
   * getHeaderTime()
   * @param {ISportEvent} eventEntity
   * @returns {string}
   */
  getHeaderTime(eventEntity: ISportEvent): string {
    return this.datePipe.transform(eventEntity.startTime, 'dd MMM');
  }

  /**
   * isExpandedEvent()
   * @param {number} goalScorerEventsIndex
   * @param {number} couponEventsIndex
   * @returns {boolean}
   */
  isExpandedEvent(goalScorerEventsIndex: number, couponEventsIndex: number, eventId: number): boolean {
    return (goalScorerEventsIndex === 0) && (couponEventsIndex === 0) || eventId === this.eventIdFromEDP;
  }

  /**
   * Toggle "Show More"/"Show less"
   * @param {ISportEvent} eventEntity
   */
  showMoreClick(eventEntity: ISportEvent): void {
    eventEntity.goalScorersShowAll = !eventEntity.goalScorersShowAll;
    this.trackShowAll(eventEntity);
  }
}
