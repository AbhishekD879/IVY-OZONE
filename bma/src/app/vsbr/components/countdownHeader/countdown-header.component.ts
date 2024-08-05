import {
  Component,
  Input,
  OnChanges,
  SimpleChanges,
  ChangeDetectionStrategy,
  OnDestroy,
  ChangeDetectorRef,
} from '@angular/core';
import { Subscription } from 'rxjs';
import { VirtualSportsService } from '../../services/virtual-sports.service';
import { TimeService } from '@core/services/time/time.service';

@Component({
  selector: 'countdown-header',
  templateUrl: './countdown-header.component.html',
  styleUrls: ['./countdown-header.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CountdownHeaderComponent implements OnChanges, OnDestroy {
  @Input() eventName: string;
  @Input() startTimeUnix: number;
  timeLeft: string;
  countdownTrigger: number = 30;
  fillDeg: number = 0;
  liveEventText = 'LIVE';

  private timerSubscription: Subscription;

  constructor(
    private changeDetectorRef: ChangeDetectorRef,
    private virtualSportsService: VirtualSportsService,
    private timeService: TimeService
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.eventName) {
      this.eventName = changes.eventName.currentValue;
    }
    if (changes.startTimeUnix) {
      this.startTimeUnix = changes.startTimeUnix.currentValue;
      this.initTimer();
    }
  }

  ngOnDestroy(): void {
    if(this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
  }

  fillStroke(date:number): number {
    const fullFilledValue = 180;
    const tickValue = 6; // fullFilledValue / countdownTrigger;
    const secondsLeft = parseInt(
      ((this.startTimeUnix - date) / 1000).toFixed(),
      10
    );
    if (secondsLeft > this.countdownTrigger) {
      return 0;
    } else if (secondsLeft >= 0 && secondsLeft <= this.countdownTrigger) {
      return (
        (this.countdownTrigger - secondsLeft) * tickValue
      );
    }
    return fullFilledValue;
  }

  getTimeLeft(date: number): string {
    const milisecondsLeft = this.startTimeUnix - date;

    if (milisecondsLeft >= 0) {
      const hours = Math.floor((milisecondsLeft % (this.timeService.min * 60 * 24)) / (this.timeService.min * 60));
      let minutes = Math.floor((milisecondsLeft % (this.timeService.min * 60)) / this.timeService.min);
      const seconds = Math.floor((milisecondsLeft % (this.timeService.min)) / 1000);
      if (hours) {
        minutes = minutes + (hours * 60);
      }
      return `${minutes < 10 ? `0${minutes}` : minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
    } else {
      return this.liveEventText;
    }
  }

  private initTimer(): void {
    this.timerSubscription = this.virtualSportsService.time.subscribe((date: number) => {
      this.timeLeft = this.getTimeLeft(date);
      this.fillDeg = this.fillStroke(date);
      this.changeDetectorRef.detectChanges();
    });
  }
}
