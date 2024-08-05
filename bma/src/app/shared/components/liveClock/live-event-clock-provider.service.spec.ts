import { LiveEventClockProviderService } from '@shared/components/liveClock/live-event-clock-provider.service';
import { ILiveClock } from '@core/models/live-clock.model';
import LiveEventClock from '@shared/components/liveClock/live-event-clock.class';

describe('LiveEventClockProviderService', () => {
  let service;

  beforeEach(() => {
    service = new LiveEventClockProviderService();
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  it('@create should return LiveEventClock', () => {
    const serverTimeDelta: number = 312;
    const clockData: ILiveClock = {
      clock_seconds: '2',
      ev_id: 123,
      last_update: '5',
      last_update_secs: '8',
      offset_secs: '31',
      period_code: 'HT',
      sport: '99',
      start_time_secs: '52',
      state: 'state'
    };
    expect(service.create(serverTimeDelta, clockData) instanceof LiveEventClock).toEqual(true);
  });
});
