import { Component, Input, OnDestroy, OnInit, ViewChild, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';

import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

enum BUTTONS {
  OK = 'Ok,Thanks',
  DEPOSIT = 'Deposit'
}

@Component({
  selector: 'video-stream-error-dialog',
  styleUrls: ['./video-stream-error-dialog.component.scss'],
  templateUrl: './video-stream-error-dialog.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class VideoStreamErrorDialogComponent extends AbstractDialogComponent implements OnInit, OnDestroy {
  @Input() eventEntity: ISportEvent;

  @ViewChild('videoStreamErrorDialog', {static: true}) dialog;

  params: { [key: string]: any};
  countDown: string;
  countDownInterval: number;

  private lastButtonClicked: string = BUTTONS.OK; // default value to cover outside click condition;

  constructor(
    private windowRefService: WindowRefService,
    public device: DeviceService,
    private timeSyncService: TimeSyncService,
    private router: Router,
    private changeDetectorRef: ChangeDetectorRef,
    private gtmService: GtmService,
    private infoDialog: InfoDialogService,
    private pubsub: PubSubService
  ) {
    super(device, windowRefService);
  }

  ngOnDestroy(): void {
    clearInterval(this.countDownInterval);
  }

  close(): void {
    this.pubsub.publish(this.pubsub.API.VIDEO_STREAM_ERROR_DIALOG_CLOSED);
    this.changeDetectorRef.markForCheck();
    this.windowRefService.nativeWindow.clearInterval(this.countDownInterval);
    this.countDown = null;
    this.lastButtonClicked = BUTTONS.OK;
    this.closeDialog();
  }

  open(): void {
    super.open();
    this.changeDetectorRef.markForCheck();

    if (this.isCountTimerAvailable()) {
      this.setCountDownValue(this.params.eventEntity.startTime);
      this.countDownIntervalSetup(this.params.eventEntity.startTime);
    }

    this.onBeforeCloseHandler();
  }

  isCountTimerAvailable(): boolean {
    return this.params.eventEntity &&
      this.isStartTimeToday(this.params.eventEntity.startTime) &&
      this.params.eventEntity.startTime > +(new Date()) &&
        this.params.eventEntity.isResulted !== 'true' &&
          this.params.eventEntity.isStarted !== 'true';
  }

  /**
   * Will show countdown for today streams
   * @param startTime
   */
  isStartTimeToday(startTime: string): boolean {
    const today = new Date().getDate();
    const startTimeDay = new Date(startTime).getDate();

    return today === startTimeDay;
  }

  countDownIntervalSetup(eventStartTime: number): void {
    // Set Time we're counting down to
    // Update the count down every 1 second
    this.countDownInterval = this.windowRefService.nativeWindow.setInterval(() => {
      this.setCountDownValue(eventStartTime);
    }, 1000);
  }

  /**
   * Update stratTime timer
   * @param eventStartTime
   */
  setCountDownValue(eventStartTime: number | string): void {
    let validTypeStartTime: number = eventStartTime as number;
    const serverTimeDelta = this.timeSyncService.getTimeDelta();

    if (typeof eventStartTime === 'string') {
      validTypeStartTime = (new Date(eventStartTime)).getTime();
    }

    const timeToStart = validTypeStartTime - (+(new Date()) + serverTimeDelta);


    // Time calculations for days, hours, minutes and seconds
    const hours = Math.floor((timeToStart % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes: any = Math.floor((timeToStart % (1000 * 60 * 60)) / (1000 * 60));
    let seconds: any = Math.floor((timeToStart % (1000 * 60)) / 1000);

    if (seconds < 10) {
      seconds = `0${seconds}`;
    }

    if (minutes < 10) {
      minutes = `0${minutes}`;
    }

    // Output the result in an element with id="demo"
    this.countDown = `${hours}:${minutes}:${seconds}`;
    this.changeDetectorRef.markForCheck();

    // If the count down is over, write some text
    if (timeToStart < 0) {
      clearInterval(this.countDownInterval);
      this.countDown = null;
    }
  }

  /**
   * Navigate to deposit page
   */
  openDeposit(): void {
    this.changeDetectorRef.markForCheck();

    this.lastButtonClicked = BUTTONS.DEPOSIT;

    if (this.device.isOnline()) {
      this.router.navigate(['deposit']);
      this.closeDialog();
    } else {
      this.infoDialog.openConnectionLostPopup();
    }
  }

  /**
   * Decorate onBeforeClose event listener
   * as it's the last place where close action could be held
   */
  private onBeforeCloseHandler(): void {
    const originalOnBeforeClose = this.params.onBeforeClose && this.params.onBeforeClose.bind(this.params);

    this.params.onBeforeClose = (): void => {
      this.pubsub.publish(this.pubsub.API.VIDEO_STREAM_ERROR_DIALOG_CLOSED);

      // GA for number of clicks on Pop-up message is tracked
      // either on Greyhounds or Horse Racing EDP on error dialogs
      if (this.params.isInactivePopup) {
        this.trackPopUpButtonClick();
      }

      originalOnBeforeClose && originalOnBeforeClose();
    };
  }

  /**
   * GA tracking about outside modal or modal buttons clicks
   */
  private trackPopUpButtonClick(): void {
    const event = this.params && this.params.eventEntity;

    this.gtmService.push('trackEvent', {
      eventCategory: 'streaming',
      eventAction: 'pop up',
      eventLabel: this.lastButtonClicked,
      sportID: event.categoryId,
      typeID: event.typeId,
      eventID: event.id
    });
  }
}
