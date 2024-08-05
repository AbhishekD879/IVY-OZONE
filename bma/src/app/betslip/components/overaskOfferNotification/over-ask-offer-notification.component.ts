import { ChangeDetectionStrategy, Component, Input, OnDestroy, OnInit } from '@angular/core';
import { interval, timer, Subscription } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';

@Component({
  selector: 'over-ask-offer-notification',
  styleUrls: ['over-ask-offer-notification.component.scss'],
  templateUrl: 'over-ask-offer-notification.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OveraskOfferNotificationComponent implements OnInit, OnDestroy {
  @Input() isTimerShown: boolean;

  offerTimer: string = '';
  traderOfferNotificationMessage: string;
  traderOfferExpiresMessage: string;

  private intervalTimer: Subscription;
  private expiredTime: number;
  private secondsToFinish: number;
  private featureConfigSubscription: Subscription;

  constructor(
    private overAskService: OverAskService,
    private cmsService: CmsService
  ) {}

  ngOnInit(): void {
    this.featureConfigSubscription = this.cmsService.getFeatureConfig('Overask').subscribe(
      (config: ISystemConfig) => {
        this.traderOfferNotificationMessage = config.traderOfferNotificationMessage;
        this.traderOfferExpiresMessage = config.traderOfferExpiresMessage;
      });

    if (this.overAskService.offerExpiresAt) {
      this.expiredTime = new Date(this.overAskService.offerExpiresAt).getTime();
      const dueTime = this.expiredTime - Date.now();

      if (dueTime >= 0) {
        this.countdownTimer();

        this.intervalTimer = interval(1000).pipe(
          takeUntil(timer(dueTime))
        ).subscribe( () => {
          this.countdownTimer();
        });
      }
    }
  }

  ngOnDestroy(): void {
    this.clearTimer();
    this.featureConfigSubscription && this.featureConfigSubscription.unsubscribe();
  }

  /**
   * Countdown Timer for UI
   */
  private countdownTimer(): void {
    // needed sync with current time in the sleep mode
    this.secondsToFinish = Math.floor((this.expiredTime - Date.now()) / 1000);

    if (this.secondsToFinish < 0) {
      this.clearTimer();
      return;
    }

    const minutes = Math.floor(this.secondsToFinish / 60);
    const seconds = this.secondsToFinish - minutes * 60;
    this.offerTimer = `${this.formatTime(minutes)}:${this.formatTime(seconds)}`;
  }

  /**
   * Format number to string like minutes/hours 0 => 00
   *
   * @params number {value}
   * @returns string {value}
   */
  private formatTime(value: number): string {
    if (!value) {
      return '00';
    } else if (value < 10) {
      return `0${value}`;
    }

    return value.toString();
  }

  /**
   * Clear rxjs interval subscriptions
   */
  private clearTimer(): void {
    this.intervalTimer && this.intervalTimer.unsubscribe();
  }
}
