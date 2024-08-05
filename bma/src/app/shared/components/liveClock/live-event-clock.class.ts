import { ILiveClock } from '@core/models/live-clock.model';

export default class LiveEventClock {
  period_code: string;
  enabled: boolean;
  liveTime: string;

  /**
   * Event Id
   * @member {number}
   */
  ev_id: number;

  /**
   * sport name
   * @member {string}
   */
  sport: string;

  /**
   * Half-time/Full-time identificator
   * @member {string}
   */
  matchTime: string = null;

  /**
   * Local time could be different from "real" time.
   * count delta to show real time duration time
   * @member {number}
   */
  private readonly localTimeDelta: number;

  /**
   * total match duration
   * @member {number}
   */
  private seconds: number = null;

  /**
   * Current match time duration
   * @member {number}
   */
  private clockTimeSeconds: number = 0;

  /**
   * Last clocks update time
   * @member {number}
   */
  private clockTimeLastUpdateSeconds: number = 0;

  /**
   * @param {number} serverTimeDelta
   * @param {string} sportName
   * @param {number} eventId
   */
  constructor(serverTimeDelta: number, clockData: ILiveClock) {
    this.localTimeDelta = serverTimeDelta;
    if (clockData) {
      this.ev_id = Number(clockData.ev_id);
      this.sport = clockData.sport;
      this.refresh(clockData);
    }
  }

  /**
   * Refreshes clockData and checks if clock update needed
   * @param clockData
   */
  public refresh(clockData?: ILiveClock): void {
    if (clockData) {
      this.period_code = clockData.period_code;
      this.clockTimeSeconds = parseInt(clockData.clock_seconds, 10);
      this.clockTimeLastUpdateSeconds = parseInt(clockData.last_update_secs, 10);
    }

    this.checkPeriod();
    this.update();
  }

  /**
   * Update clock seconds and minutes
   * only if clock is enabled
   */
  public update(): void {
    if (!this.enabled) {
      return;
    }

    const currTimeSeconds = Math.floor((new Date().getTime() + this.localTimeDelta) / 1000);
    const lastTimeUpdateDeltaSeconds = currTimeSeconds - this.clockTimeLastUpdateSeconds;

    this.seconds = lastTimeUpdateDeltaSeconds + this.clockTimeSeconds;
    this.matchTime = `${Math.floor(this.seconds / 60)}'`;

    this.liveTime = this.getFavMatchTimeFromSecs(this.seconds);
  }

  /**
   * Check period time, stop clocks for Half and Full time and Penalties
   * @private
   */
  private checkPeriod(): void {
    switch (this.period_code) {
      case 'HALF_TIME':
      case 'EXTRA_TIME_HALF_TIME':
        this.matchTime = 'HT';
        this.enabled = false;
        this.liveTime = null;
        break;
      case 'PENALTIES':
        this.matchTime = 'PENS';
        this.enabled = false;
        this.liveTime = null;
        break;
      case 'FINISH':
        this.matchTime = 'FT';
        this.enabled = false;
        this.liveTime = null;
        break;
      default:
        this.enabled = true;
    }
  }

  /**
   * Get converted seconds in new format
   * @param {number} seconds
   * @returns {string}
   * @private
   */
  private getFavMatchTimeFromSecs(seconds: number): string {
    return isNaN(seconds) ? '' : this.convert(Math.abs(seconds));
  }

  /**
   * Converts seconds to mm:ss format
   * @param {number} totalSeconds
   */
  private convert(totalSeconds: number): string {
    let minutes: number | string = Math.floor(totalSeconds / 60);
    let seconds: number | string = totalSeconds - (minutes * 60);

    minutes = minutes < 10 ? `0${minutes}` : minutes;
    seconds = seconds < 10 ? `0${seconds}` : seconds;

    return `${minutes}:${seconds}`;
  }
}
