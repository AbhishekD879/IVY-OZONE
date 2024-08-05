import LiveEventClock from '@shared/components/liveClock/live-event-clock.class';
import { ILiveClock } from '@core/models/live-clock.model';

describe('LiveEventClock', () => {
  let model,
    serverTimeDelta: number,
    clockData: ILiveClock,
    currentDate: Date;

  beforeEach(() => {
    currentDate = new Date();
    serverTimeDelta = 3600;
    clockData = {
      clock_seconds: '2791',
      ev_id: 91,
      last_update: currentDate.toString(),
      last_update_secs: Math.floor(currentDate.getTime() / 1000).toString(),
      offset_secs: 'offset_secs',
      period_code: 'SECOND_HALF',
      sport: 'football',
      start_time_secs: '20',
      state: 'R'
    };
    model = new LiveEventClock(serverTimeDelta, clockData);
  });

  it('should create and set initial value', () => {
    expect(model).toBeTruthy();
    expect(model.localTimeDelta).toEqual(3600);
    expect(model.ev_id).toEqual(91);
    expect(model.sport).toEqual('football');
    expect(model.period_code).toEqual('SECOND_HALF');
    expect(model.clockTimeSeconds).toEqual(2791);
    expect(model.clockTimeLastUpdateSeconds).toEqual(Math.floor(currentDate.getTime() / 1000));
  });

  it('should set initial value when clockData undefined', () => {
    model = new LiveEventClock(serverTimeDelta, undefined);
    expect(model.localTimeDelta).toEqual(3600);
  });

  describe('@refresh', () => {
    it('should check period and set enable = true', () => {
      spyOn(model, 'update');
      model.refresh(undefined);

      expect(model.enabled).toEqual(true);
      expect(model.matchTime).toEqual('46\'');
      expect(model['update']).toHaveBeenCalled();
    });

    it('should check period and set enable = true', () => {
      spyOn(model, 'update');
      const newClockData = {
        last_update: '4123',
        last_update_secs: '9876',
        period_code: 'SECOND_HALF'
      } as any;
      model.refresh(newClockData);

      // set data
      expect(model.enabled).toEqual(true);
      expect(model.update).toHaveBeenCalled();
    });

    it('should check period and set enable = false', () => {
      spyOn(model, 'update');
      const newClockData = {
        last_update: '4123',
        last_update_secs: '9876',
        period_code: 'EXTRA_TIME_HALF_TIME'
      } as any;
      model.refresh(newClockData);

      // set data
      expect(model.enabled).toEqual(false);
      expect(model.matchTime).toEqual('HT');
      expect(model.liveTime).toEqual(null);
      expect(model.update).toHaveBeenCalled();
    });

    it('should check period = PENALTIES and set enabled = false', () => {
      const newClockData = {
        period_code: 'PENALTIES'
      } as any;
      model.refresh(newClockData);

      expect(model.enabled).toEqual(false);
      expect(model.matchTime).toEqual('PENS');
      expect(model.liveTime).toEqual(null);
    });

    it('should check period = FINISH and set enabled = false', () => {
      const newClockData = {
        period_code: 'FINISH'
      } as any;
      model.refresh(newClockData);

      expect(model.enabled).toEqual(false);
      expect(model.matchTime).toEqual('FT');
      expect(model.liveTime).toEqual(null);
    });
  });

  it('@getFavMatchTimeFromSecs should return empty string', () => {
    expect(model.getFavMatchTimeFromSecs('test')).toEqual('');
  });

  it('@convert should add zero char before seconds and minutes', () => {
    expect(model.convert(4)).toEqual('00:04');
  });
});
