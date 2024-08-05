import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges, ChangeDetectorRef, ViewEncapsulation } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { TimeService } from '@core/services/time/time.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'race-timer',
  templateUrl: 'race-timer.component.html',
  styleUrls: ['race-timer.component.scss'],
  encapsulation: ViewEncapsulation.None


})
export class RaceTimerComponent implements OnInit, OnDestroy, OnChanges {

  @Input() utc: string | boolean;
  @Input() event: ISportEvent;
  @Input() displayTime: boolean;
  @Input() displayCountdown: boolean;

  postpone: number;
  nextTick: number;
  countdown: number;
  brand: string = environment.brand;
  
  private readonly DURATION: number = 2700000; // 45 min * 60 sec * 1000 ms
  private startTimeStr: string;
  private startTime: number;
  private timeDelta: number;
  private wCountdown: string;

  constructor(
    private timeSyncService: TimeSyncService,
    private timeService: TimeService,
    private windowRef: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    this.tick = this.tick.bind(this);
    this.timeDelta = this.timeSyncService.getTimeDelta();
  }

  ngOnInit(): void {
    this.init();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.event) {
      this.init();
    }
  }

  ngOnDestroy(): void {
    this.clearTimers();
  }

  init(): void {
    // clear previous timers because init() may be called twice
    this.clearTimers();

    if (this.event && this.event.startTime) {
      this.utc = this.utc ? 'UTC' : undefined;
      this.displayTime = !_.isUndefined(this.displayTime) ? this.displayTime : true;
      this.displayCountdown = !_.isUndefined(this.displayCountdown) ? this.displayCountdown : true;
      this.startTime = new Date(this.event.startTime).getTime();
      this.startTimeStr = this.timeService.formatByPattern(new Date(this.event.startTime), 'HH:mm', this.utc);
      if (this.getDiff() > this.DURATION) {
        this.postpone = this.windowRef.nativeWindow.setTimeout(this.tick, this.getDiff() - this.DURATION);
      } else {
        this.tick();
      }
      this.changeDetectorRef.markForCheck();
    }
  }

  /**
   * get countdown
   * @returns {string}
   */
  get raceCountdown(): string {
    return this.wCountdown;
  }
  set raceCountdown(value:string){}

  /**
   * get start time
   * @returns {string}
   */
  get raceStartTime(): string {
    return this.startTimeStr;
  }
  set raceStartTime(value:string){}

  /**
   * Get event status code
   * @returns {string}
   */
  get status(): string {
    return this.event.raceStage;
  }
  set status(value:string){}

  /**
   * Get status css class
   * @returns {string}
   */
  get statusCssClass(): string {
    return `status-${this.status.toLowerCase()}`;
  }
  set statusCssClass(value:string){}

  /**
   * Check if can display time
   * @returns {boolean}
   */
  isTime(): boolean {
    if (!this.displayTime) {
      return false;
    }
    return this.getDiff() > this.DURATION;
  }

  /**
   * Check if can display timer
   * @returns {boolean}
   */
  isCountdown(): boolean {
    if (!this.displayCountdown) {
      return false;
    }
    const diff = this.getDiff();
    return diff > 0 && diff < this.DURATION;
  }

  /**
   * Check if race has started
   * @returns {boolean}
   */
  isOff(): boolean {
    return this.getDiff() < 0;
  }

  /**
   * Initiate next timer tick
   */
  initTimeout(): void {
    if (this.isOff()) {
      return;
    }
    this.nextTick = this.windowRef.nativeWindow.setTimeout(this.tick, 1000);
  }

  /**
   * Perform next timer tick
   */
  tick(): void {
    this.wCountdown = this.getCountdown();
    this.initTimeout();
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Format time to have start zero
   * @param value
   * @returns {string}
   * @private
   */
  format(value): string {
    return value < 10 ? `0${value}` : value;
  }

  /**
   * Format time string
   * @param mm
   * @param ss
   * @param delimeter
   * @returns {string}
   * @private
   */
  formatTime(mm, ss, delimeter = ':'): string {
    return `${this.format(mm)}${delimeter}${this.format(ss)}`;
  }

  /**
   * Get correct user local time
   * @returns {number}
   * @private
   */
  private getCurrentTime(): number {
    return Date.now() + this.timeDelta;
  }

  /**
   * Get interval from now to start time
   * @returns {number}
   * @private
   */
  private getDiff(): number {
    return this.startTime - this.getCurrentTime();
  }

  /**
   * Render countdown string
   * @returns {string}
   * @private
   */
  private getCountdown(): string {
    const diff = Math.round(this.getDiff() / 1000),
      min = Math.floor(diff / 60),
      sec = diff % 60;
    return this.formatTime(min, sec);
  }

  private clearTimers(): void {
    this.nextTick && this.windowRef.nativeWindow.clearTimeout(this.nextTick);
    this.postpone && this.windowRef.nativeWindow.clearTimeout(this.postpone);
  }
}
