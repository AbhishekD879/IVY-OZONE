import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges, ChangeDetectorRef, Output, EventEmitter } from '@angular/core';
import { TimeService } from '@core/services/time/time.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'betpack-expiresin-timer',
  templateUrl: './betpack-expiresin-timer.component.html',
  styleUrls: ['./betpack-expiresin-timer.component.scss']
})
export class BetpackExpiresinTimerComponent implements OnInit, OnDestroy, OnChanges {


  @Input() utc: string | boolean;
  @Input() timer: string;
  @Input() displayTime: boolean;
  @Input() displayCountdown: boolean;
  @Input() betpackReview? : boolean;
  @Input() signPost? : string;
  @Output() EmitTimer: EventEmitter<boolean> = new EventEmitter();

  postpone: number;
  nextTick: number;
  countdown: number;
  brand: string = environment.brand;

  private readonly DURATION: number = 3600000*24; // 60 min * 60 sec * 1000 ms
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
    if (changes.timer) {
      this.init();
    }
  }

  ngOnDestroy(): void {
    this.clearTimers();
  }

  init(): void {
    // clear previous timers because init() may be called twice
    this.clearTimers();

    if (this.timer) {
      this.utc = this.utc ? 'UTC' : undefined;
      this.displayTime = !_.isUndefined(this.displayTime) ? this.displayTime : true;
      this.displayCountdown = !_.isUndefined(this.displayCountdown) ? this.displayCountdown : true;
      this.startTime = new Date(this.timer).getTime();
      this.startTimeStr = this.timeService.formatByPattern(this.timer, 'HH:mm', this.utc);
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

  /**
   * Check if can display timer
   * @returns {boolean}
   */
  isCountdown(): boolean {
    if (!this.displayCountdown) {
      return false;
    }
    const diff = this.getDiff();
    this.EmitTimer.emit(diff > 0 && diff < this.DURATION)
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
    return value < 10 && !this.betpackReview ? `0${value}` : value;
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

  formatTimebtHrs(hh, mm): string {
    return `${this.format(hh)}${'h'}${' '}${this.format(mm)}${'m'}`;
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
    if(!this.betpackReview){
      const diff = Math.round(this.getDiff() / 1000),
      min = Math.floor(diff / 60),
      sec = diff % 60;
    return this.formatTime(min, sec);
    } else {
      // const diff = Math.round(this.getDiff() / 1000),
      const min = Math.floor((this.getDiff()  / (1000 * 60)) % 60);
      const hrs = Math.floor((this.getDiff()  / (1000 * 60 * 60)) % 24);
      return this.formatTimebtHrs(hrs,min);
    }

  }
/**
   * Clear the timer
   * @returns {void}
   * @private
   */
  private clearTimers(): void {
    this.nextTick && this.windowRef.nativeWindow.clearTimeout(this.nextTick);
    this.postpone && this.windowRef.nativeWindow.clearTimeout(this.postpone);
  }

}
