import { Injectable } from '@angular/core';
import { ILiveClock } from '@core/models/live-clock.model';
import LiveEventClock from './live-event-clock.class';

@Injectable()
export class LiveEventClockProviderService {

  create(serverTimeDelta: number, clockData: ILiveClock): LiveEventClock {
    return new LiveEventClock(serverTimeDelta, clockData);
  }
}
