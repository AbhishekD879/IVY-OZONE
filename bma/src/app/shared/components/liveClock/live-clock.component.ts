import { ChangeDetectionStrategy, Component, Input, Output, EventEmitter } from '@angular/core';
import { interval, Observable } from 'rxjs';

import { ISportEvent } from '@core/models/sport-event.model';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { LiveEventClockProviderService } from '@shared/components/liveClock/live-event-clock-provider.service';
import { map } from 'rxjs/operators';

@Component({
  selector: 'live-clock',
  templateUrl: 'live-clock.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class LiveClockComponent {

  public liveTime: Observable<string> = null;
  @Output() public readonly clockUpdated: EventEmitter<null>;

  private _event: ISportEvent = null;

  @Input() public set event(event: ISportEvent) {
    this._event = event;

    if (this.event && this.event.initClock) {
      const serverTimeDelta = this.timeSyncService.getTimeDelta();
      this.event.clock = this.liveEventClockProviderService.create(serverTimeDelta, this.event.initClock);
    }

    if (this.event && this.event.clock) {
      this.startTimer();
    }
  }

  public get event(): ISportEvent {
    return this._event;
  }

  constructor(
    private timeSyncService: TimeSyncService,
    private liveEventClockProviderService: LiveEventClockProviderService
  ) {
    this.clockUpdated = new EventEmitter();
  }

  private startTimer(): void {
    this.liveTime = interval(1000).pipe(
      map(_ => {
        this.event.clock.update();
        return {
          liveTime: this.event.clock.liveTime,
          matchTime: this.event.clock.matchTime
        };
      }),
      map((val) => {
        this.clockUpdated.emit();
        return val.liveTime;
      })
    );
  }
}
