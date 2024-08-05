import { DatePipe } from '@angular/common';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { DAYS, MONTHS, DAYVALUE } from '../../constants/time.constant';
import { ICountDownTimer, IDateRange, IRacingDateRange, ITimeStampDateRange } from './time-service.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ITimeHydraModel } from '@core/services/timeSync/timeModel';
import { TIME_SERVICE_ENUM } from '@core/services/time/time.service.enum';
import { interval, Observable, Subscription } from 'rxjs';
import { map } from 'rxjs/internal/operators/map';

@Injectable()
export class TimeService {
  additionalTimeForSteamStartEnd: number = 900000; // 15 min
  oneDayInMiliseconds: number = 86400000;
  oneSecond: number = 1000;
  fiveMinutsInMiliseonds: number = 300000;
  threeMinutsInMiliseonds: number = 180000;
  refreshInterval: number = 60000 * 60; // 1 hour.
  eventPollingInterval: number = 6000; // 6 sec.
  eventOngoingGuess: number = 45000; // 45 sec.
  goForNextVsEvent: number = 15000;
  oneHourInSeconds: number = 3600;
  fiveSeconds: number = 5000;
  animationDelay: number = 5000; // BMA-39095 animation delay for goal alert
  timeOutregExpDate: RegExp = /(\d{4})\-(\d{1,2})\-(\d{1,2})\s(\d{1,2})\:(\d{1,2})\:(\d{1,2})/m;

  /**
   * Time after wich class given to price-odds-button after live Update should be removed
   */
  hideLiveUpdateClassTime: number = 2000;

  sec: number = 1000;
  min: number = 60000;

  /**
   * This structure dictates cache update intervals,
   * separately for each service.
   *
   * @type {
   * {featuredEvents: number, eventsList: number,
   * eventsByClasses: number, event: number, liveEvents: number,
   * couponsByClasses: number}}
   */
  apiDataCacheInterval: any = {
    event: this.min,
    events: this.min,
    liveEventsStream: 30 * this.sec, // stream widget event to stream
    multiplesEvents: 5 * this.min,
    inPlayWidget: this.min,
    LSWidget: this.min,
    coupons: 5 * this.min,
    ribbonEvents: this.min,
    connectRibbonEvents: 5 * this.min,
    privateMarkets: 5 * this.sec,
    currentMatches: this.min,
    favouritesMatches: 5 * this.sec,
    toteEvents: 60 * this.sec,
    nextRacesHome: 5 * this.min,
    nextRaces: 1 * this.min
  };

  private sixHoursInMisiseconds: number = 60000 * 60 * 6; // 6 hours.
  private eventsBackwardRange: number = 60000 * 60; // 1 hour.
  private timezoneOffset: number = new Date().getTimezoneOffset() * 60000;
  private readonly ukTimeZone: string = 'GMT';
  private timerIdHour: Subscription;

  /**
   * Seconds to round for SS requests
   *
   * @type {number}
   */
  private SSRequestsSecondsToRoundValue: number = 30;

  constructor(private locale: LocaleService,
              private datePipe: DatePipe,
              private filter: FiltersService,
              private timeSyncService: TimeSyncService,
              private windowRefService: WindowRefService) {
    this.dateTimeOfDayInISO = this.dateTimeOfDayInISO.bind(this);
  }

  /**
   * Format the date to the local format `04/12/2018, 10:46:18` from
   * ['2018-04-12 09:11:34', '2018', '12', '04', '09', '11', '34']
   * @params {string[]} [fulldate, year, month, day, hours, minutes, sec]
   * @return {string} formatted date
   */
  formatToLocaleDate([fulldate, year, month, day, hours, minutes, sec]: string[]): string {
    if (_.indexOf([fulldate, year, month, day, hours, minutes, sec], undefined) === -1) {
      const d = new Date(
        Date.UTC(+year, +month - 1, +day, +hours - 1, +minutes, +sec) // BMA-41373: date from openapi in UK time, not UTC.
      );
      return this.dateToString(d);
    }
  }

  dateToString(date: Date): string {
    return this.datePipe.transform(date, 'yyyy-MM-dd HH:mm:ss');
  }

  /**
   * Return date and time of the day by the name in ISO8601 format.
   *
   * @param day {string} - e.g. 'tomorrow', 'today'
   * @returns {string} date in ISO8601 format
   */
  dateTimeOfDayInISO(day: string): string {
    let ourDate;

    switch (day) {
      case 'twoWeeksAgo':
        ourDate = this.dateTimeInISO(-336, 0, 0, 0);
        break;
      case 'weekAgo':
        ourDate = this.dateTimeInISO(-168, 0, 0, 0);
        break;
      case 'yesterday':
        ourDate = this.dateTimeInISO(-24, 0, 0, 0);
        break;
      case 'today':
        ourDate = this.dateTimeInISO(0, 0, 0, 0);
        break;
      case 'tomorrow':
        ourDate = this.dateTimeInISO(24, 0, 0, 0);
        break;
      case 'afterTomorrow':
        ourDate = this.dateTimeInISO(48, 0, 0, 0);
        break;
      case 'post48h':
        const currentDateTime = new Date();
        const h = currentDateTime.getHours();
        const m = currentDateTime.getMinutes();
        ourDate = this.dateTimeInISO(h + 48, m, 0, 0);
        break;
      case '6days':
          ourDate = this.dateTimeInISO(144, 0, 0, 0);
          break;
      default:
        ourDate = this.dateTimeInISO(0, 0, 0, 0);
        break;
    }

    return ourDate;
  }

  /**
   * Return date object for 'tomorrow', 'today', 'future' day.
   *
   * @param day {string} - e.g. 'tomorrow', 'today'
   * @returns {number} - date object???
   */
  incrementDateDay(day: string): number {
    const getDate = new Date();
    let dayAdd;

    switch (day) {
      case 'today':
        dayAdd = 0;
        break;

      case 'tomorrow':
        dayAdd = 1;
        break;

      case 'future':
        dayAdd = 2;
        break;

      default:
        dayAdd = 0;
        break;
    }

    return getDate.setDate(getDate.getDate() + dayAdd);
  }

  /**
   * Return date range object {startDate, endDate} in ISO8601 format.
   * @param dateRange {string} or {object}
   * @returns {object}
   */
  createTimeRange(dateRange: string | IRacingDateRange): IRacingDateRange {
    let returnRange = {};

    if (typeof dateRange === 'object' && dateRange !== null) {
      returnRange = dateRange;
    } else {
      switch (dateRange) {
        case 'featured':
          returnRange = {
            startDate: this.dateTimeOfDayInISO('today'),
            endDate: this.dateTimeOfDayInISO('6days')
          };
          break;
          
        case 'antepost':
        case 'allEvents':
        case 'matchesTab':
          returnRange = {
            startDate: this.dateTimeOfDayInISO('today')
          };
          break;

        case 'today':
          returnRange = {
            startDate: this.dateTimeOfDayInISO('today'),
            endDate: this.dateTimeOfDayInISO('tomorrow')
          };
          break;

        case 'tomorrow':
          returnRange = {
            startDate: this.dateTimeOfDayInISO('tomorrow'),
            endDate: this.dateTimeOfDayInISO('afterTomorrow')
          };
          break;
        case 'todayAndTomorrow':
          returnRange = {
            startDate: this.dateTimeOfDayInISO('today'),
            endDate: this.dateTimeOfDayInISO('afterTomorrow')
          };
          break;
        case 'future':
          returnRange = {
            startDate: this.dateTimeOfDayInISO('afterTomorrow')
          };
          break;

        case 'pre48h':
          returnRange = {
            startDate: this.dateTimeOfDayInISO('today'),
            endDate: this.dateTimeOfDayInISO('post48h')
          };
          break;

        default:
          return {};
      }
    }

    return returnRange;
  }

  /**
   * Get current year => 2016
   * @returns {number}
   */
  getFullYear(): number {
    return new Date().getFullYear();
  }

  /**
   * Get current month number (December => 1)
   * @returns {number}
   */
  getMonthNumber(): number {
    return new Date().getMonth() + 1;
  }

  /**
   * Return value of MONTHS array in two types short or full.
   *
   * @param oldDate {date}
   * @param isFull {Boolean}
   * @returns {string}
   */
  getMonthI18nValue(oldDate: Date, isFull: boolean): string {
    const oldDates = new Date(oldDate);
    return isFull ? MONTHS.full[oldDates.getMonth()] : MONTHS.short[oldDates.getMonth()];
  }

  /**
   * Return value of DAYS array.
   *
   * @param oldDate {date}
   * @returns {string}
   */
  getDayI18nValue(oldDate: string): string {
    const oldDates = new Date(oldDate);
    return DAYS[oldDates.getDay()];
  }

  /**
   * Return value of DAYS array in UTC timezone.
   *
   * @param oldDate {date}
   * @returns {string}
   */
  getUTCDay(oldDate: Date): string {
    const oldDates = new Date(oldDate);
    return DAYS[oldDates.getUTCDay()];
  }

  /**
   * Returns the Day Value
   *
   * @param timeStamp
   * @returns {string}
   */
  getUTCDayValue(timeStamp: number): string {
    const racetimeValue = new Date(timeStamp).getUTCDate();
    let dayValue: string = DAYS[new Date(timeStamp).getUTCDay()];
    const today = new Date().getDate();
    const tomorrow = new Date(new Date().setDate(new Date().getDate() + 1)).getDate();
    if (racetimeValue === today) {
      dayValue = DAYVALUE.today;
    }
    if (racetimeValue === tomorrow) {
      dayValue = DAYVALUE.tomorrow;
    }
    return dayValue;
  }

  /**
   * Returns difference in days between requested date and current time.
   *
   * @param {string} date requested date.
   * @returns {number} difference in days.
   */
  compareDate(date: string): number {
    const currentDate = new Date(),
      compareDateValue = new Date(date.replace(/-/g, '/')),
      timeDiff = Math.abs(currentDate.getTime() - compareDateValue.getTime());

    return Math.ceil(timeDiff / (1000 * 3600 * 24));
  }

  /**
   * Return value of day or value from DAYS array if
   * this in not today or tomorrow.
   *
   * @param oldDate {number|string}
   * @returns {string}
   */
  getCorrectDay(oldDate: string): string {
    let dayName;

    const oldDates = new Date(oldDate).toISOString(),
      today = this.dateTimeOfDayInISO('today'),
      tomorrow = this.dateTimeOfDayInISO('tomorrow'),
      afterTomorrow = this.dateTimeOfDayInISO('afterTomorrow');

    if ((oldDates > today) && (oldDates < tomorrow)) {
      dayName = 'sb.today';
    } else if ((oldDates > tomorrow) && (oldDates < afterTomorrow)) {
      dayName = 'sb.tomorrow';
    } else {
      dayName = this.getDayI18nValue(oldDates);
    }

    return dayName;
  }

  /**
   * Return value of day or value from DAYS array if
   * this in not today or tomorrow or yesterday.
   *
   * @param {number|string} date - oldDate
   * @param {boolean} timeZone
   * @param {boolean} withPrefix
   * @returns {string}
   */
  getTodayTomorrowOrDate(date: string | Date,
    timeZone: boolean = true,
    withPrefix: boolean = true,
    format: string = 'yyyy-MM-dd'): string {
    const timeOffsetInMS = new Date().getTimezoneOffset() * 60000,
      oldDate = _.isString(date) ? new Date((date).replace(/-/g, '/')) : new Date(date);
    let dayName;

    if (timeZone) {
      oldDate.setTime(oldDate.getTime() - timeOffsetInMS);
    }

    const oldDates = new Date(oldDate).toISOString(),
      today = this.dateTimeOfDayInISO('today'),
      tomorrow = this.dateTimeOfDayInISO('tomorrow'),
      afterTomorrow = this.dateTimeOfDayInISO('afterTomorrow'),
      yesterday = new Date(),
      afterYesterday = new Date();

    yesterday.setDate(yesterday.getDate() - 1);
    yesterday.setHours(23, 59, 59, 0);
    afterYesterday.setDate(afterYesterday.getDate() - 2);
    afterYesterday.setHours(23, 59, 59, 0);

    if ((oldDates > today) && (oldDates < tomorrow)) {
      dayName = this.locale.getString('sb.today');
    } else if ((oldDates > tomorrow) && (oldDates < afterTomorrow)) {
      dayName = this.locale.getString('sb.tomorrow');
    } else if ((new Date(oldDates) < yesterday) && (new Date(oldDates) > afterYesterday)) {
      dayName = this.locale.getString('sb.yesterday');
    } else {
      dayName = this.datePipe.transform(oldDate, (withPrefix ? 'd MMM' : 'd MMM yyyy'));
    }

    return withPrefix ? `${dayName} ${this.datePipe.transform(oldDate, format)}` : dayName;
  }

  /**
   * Returns formatted date according to provided pattern
   * @param {Object} date
   * @param {String} pattern, example 'dd/MM/yyyy'
   * @returns {string}
   */
  formatByPattern(date: Date | string, pattern: string, utc?: string, ukTimeZone?: boolean, locale?: string): string {
    if (ukTimeZone) {
      utc = this.ukTimeZone;
    }

    // locale is needed for some places where date formatting includes Abbreviations
    // some envs get locale based on where server is located. So, this is a hack: used where needed
    return this.datePipe.transform(date, pattern, utc, locale);
  }

  /**
   *
   * @param {Date | String} dateA
   * @param {Date | String} dateB
   * @param {String} pattern
   * @param {Boolean} ukTimeZone
   * @returns {Boolean}
   */
  isEqualDatesByPattern(dateA: Date | string, dateB: Date | string, pattern: string, ukTimeZone?: boolean): boolean {
    return this.formatByPattern(dateA, pattern, null, ukTimeZone) === this.formatByPattern(dateB, pattern, null, ukTimeZone);
  }

  /**
   * Determine time period
   *
   * @param {string} startTime
   * @param {boolean} isRacing
   * @returns {string}
   */
  determineDay(startTime: string, isRacing: boolean): string {
    const startTimes = new Date(startTime).toISOString(),
      today = this.format('today', isRacing),
      tomorrow = this.format('tomorrow', isRacing),
      afterTomorrow = this.format('afterTomorrow', isRacing);
    let time;
    if (startTimes < today) {
      time = 'past';
    }
    if ((startTimes >= today) && (startTimes < tomorrow)) {
      time = 'today';
    }
    if ((startTimes >= tomorrow) && (startTimes < afterTomorrow)) {
      time = 'tomorrow';
    }
    if (startTimes > afterTomorrow) {
      time = 'future';
    }
    return time;
  }

  /**
   * Get date and return start of the day and next day range,
   * for example ({ from: 2018-01-01 00:00:00, to: 2018-01-02 00:00:00})
   * @param timeStamp
   * @returns {{timeStampFrom: number, timeStampTo: number}}
   */
  determineCurrentAndNextDayRange(timeStamp: number): ITimeStampDateRange {
    const currDate = new Date(timeStamp),
      timeStampFrom = currDate.setUTCHours(0, 0, 0, 0),
      timeStampTo = currDate.setUTCHours(24, 0, 0, 0);
    return { timeStampFrom, timeStampTo };
  }

  /**
   * Return the number of milliseconds
   * since 1 January 1970 00:00:00 UTC for
   * the current date and time according to system settings.
   *
   * @returns {number}
   */
  getCurrentTime(): number {
    return new Date().getTime();
  }

  /** Return date according to timezone.
   *
   * @param datetime {Date}
   * @returns {Date}
   */
  getLocalDate(datetime: Date): Date {
    const zoneOffset = (new Date().getTimezoneOffset() * -1) * 60000,
      date = zoneOffset > 0 ? new Date(datetime.getTime() + zoneOffset) : new Date(datetime.getTime() - zoneOffset);

    if (date.getHours().toString() === '00' && date.getMinutes().toString() === '00') {
      date.setDate(date.getDate() - 1);
    }

    // check for summertime due to the openbet is workin in +1 hour timezone.
    if (this.summerTimeStatus(datetime)) {
      date.setHours(date.getHours() - 1);
    }

    return date;
  }

  /**
   * Converts date string to local date object
   * @param {string} dateString
   * @returns {Date}
   */
  getLocalDateFromString(dateString: string): Date {
    const replaceChars: {[key: string]: string} = {'T':' ','-':'/'};
    return dateString ?
     this.getLocalDate(new Date(dateString.replace(/[-T]/gi, m => replaceChars[m]))) : null;
  }

  selectTimeRangeStartDelta(deltaTimeNowUnix: number): string {
    const time = this.getCurrentTime() +
      deltaTimeNowUnix +
      this.sixHoursInMisiseconds -
      this.refreshInterval +
      this.timezoneOffset;

    return this.formatTime(time);
  }

  selectTimeRangeEndDelta(deltaTimeNowUnix: number): string {
    const time = this.getCurrentTime() +
      deltaTimeNowUnix +
      this.sixHoursInMisiseconds +
      this.timezoneOffset;

    return this.formatTime(time);
  }

  selectTimeRangeStart(): string {
    const time = this.getCurrentTime() +
      this.timezoneOffset -
      this.eventsBackwardRange;
    const roundedTime = this.roundSeconds(new Date(time), this.SSRequestsSecondsToRoundValue).getTime();

    return this.formatTime(roundedTime);
  }

  selectTimeRangeEnd(): string {
    const time = this.getCurrentTime() +
      this.sixHoursInMisiseconds +
      this.timezoneOffset;
    const roundedTime = this.roundSeconds(new Date(time), this.SSRequestsSecondsToRoundValue).getTime();

    return this.formatTime(roundedTime);
  }

  /**
   * Subtract given amount of days from current time.
   * @param  {Number} days - number of days to be subtracted from current time.
   * @return {string} - time string received after subtraction.
   */
  getTimeWithDelta(days: number): string {
    const time = this.getCurrentTime() -
      (days * 24 * 60 * 60 * 1000) +
      this.timezoneOffset;
    return this.formatTime(time);
  }

  /**
   * Convert minutes to miliseconds
   * @param  {Number} minutes - number of minutes to be converted
   * @return {Number} miliseconds - minutes in miliseconds
   */
  minutesToMiliseconds(minutes: number): number {
    return minutes * 60 * 1000;
  }

  secondsToMiliseconds(seconds: number): number {
    return seconds * 1000;
  }

  /**
   * Convert timestamp to 'h:mm' local time string
   * @param  {Number} startTime (timestamp)
   * @return {String} hour and min
   */
  getLocalHourMin(startTime: string | number): string {
    return this.datePipe.transform(startTime, 'h:mm');
  }

  /**
   * Convert timestamp to 'HH:mm' local time string to military time
   * @param  {Number} startTime (timestamp)
   * @return {String} hour and min (24:00)
   */
  getLocalHourMinInMilitary(startTime: number): string {
    return this.datePipe.transform(startTime, 'HH:mm');
  }

  /**
   * Return time range for query
   * @param  {string} date timestamp
   * @return {String} hour and min
   */
  getTimeRangeForRequest(date: string): IRacingDateRange {
    const range: any = this.createTimeRange(date || 'today');
    return _.isEmpty(range) ? {} : { startTime: range.startDate, endTime: range.endDate };
  }

  /**
   * Return time range for query (Do not include user localization)
   * @param  {string} date timestamp
   * @return {String} hour and min
   */
  getRacingTimeRangeForRequest(date: string): IRacingDateRange {
    const range: any = this.createTimeRange(date || 'today');
    const startTime = range.startDate && this.removeTimezoneOffSet(range.startDate);
    const endTime = range.endDate && this.removeTimezoneOffSet(range.endDate);

    return _.isEmpty(range) ? {} : { startTime, endTime };
  }

  /**
   * returns DATE NOW in ISO format with MILLISECONDS = 0 and rounded seconds - SSRequestsSecondsToRoundValue
   * @returns {string}
   */
  getSuspendAtTime(randomMillis: boolean = false): string {
    const dateNow = new Date();
    return this.roundDateTo30Seconds(dateNow, randomMillis);
  }

  /**
   * Format datetime in ISO format with MILLISECONDS = 0 and rounded seconds - SSRequestsSecondsToRoundValue
   * @param time {string}
   * @returns {string}
   */
  roundTo30seconds(time: string): string {
    const dateTime = new Date(time);
    return this.roundDateTo30Seconds(dateTime);
  }

  /**
   * Format Date in ISO format with MILLISECONDS and rounded seconds - SSRequestsSecondsToRoundValue
   * @param date {Date}
   * @param randomMillis {boolean}
   * @returns {string}
   */
  roundDateTo30Seconds(date: Date, randomMillis?: boolean): string {
    date.setMilliseconds(randomMillis ? (Math.round(Math.random() * 1000) - 1) : 0);

    return this.roundSeconds(date, this.SSRequestsSecondsToRoundValue).toISOString();
  }

  /**
   * Return date range based on start - Date Now and end - date Now + hours
   *
   * @param {number} hours
   * @returns {DateRange}
   */
  getHoursRageFromNow(hours: number): IDateRange {
    const dateNow = this.roundSeconds(new Date(), this.SSRequestsSecondsToRoundValue);
    dateNow.setMilliseconds(0);
    const nowEnd = new Date(dateNow);
    nowEnd.setHours(nowEnd.getHours() + hours);
    return {
      start: dateNow.toISOString(),
      end: nowEnd.toISOString()
    };
  }

  /**
   * Returns difference in days between requested date and current time.
   *
   * @param {string} date - requested date.
   * @returns {number} difference in days.
   */
  daysDifference(date: string): number {
    const now = new Date().getTime();
    const checkedDate = new Date(date).getTime();

    return ((Number(now) - Number(checkedDate)) / (1000 * 60 * 60 * 24));
  }

  /**
   * Returns difference in days between requested date and current hydra time.
   * @param {string} date - requested date.
   * @returns {number} difference in days.
   */
  getHydraDaysDifference(date: string): Observable<number> {
    return (this.timeSyncService.getUserSessionTime(true, false) as Observable<ITimeHydraModel>).pipe(map((timeHydraModel: ITimeHydraModel) => {
      const now = new Date(timeHydraModel.timestamp).getTime();
      const checkedDate = new Date(date).getTime();
      return (Number(now) - Number(checkedDate)) / (1000 * 60 * 60 * 24);
    }));
  }

  /**
   * Checks whether given date is in the range from now until the next 24 hours.
   *
   * @param {number|string|Date} date
   * @return {boolean}
   */
  isInNext24HoursRange(date: Date): boolean {
    const difference = new Date(date).getTime() - this.getCurrentTime();
    return difference > 0 && difference <= this.oneDayInMiliseconds;
  }

  parseDateInLocalFormat(date: string): Date {
    return this.getLocalDate(this.parseDateTime(date));
  }

  /**
   * Check if is today date
   * @param {Date} date
   * @returns {boolean}
   */
  isTodayDate(date: Date): boolean {
    const nowDate = new Date();
    return nowDate.toDateString() === date.toDateString();
  }

  /**
   * Checks date range to be more than no. of YEAR BEFORE.
   * @param {date} start
   * @param {number} months
   * @returns {boolean}
   */
  moreThanYears(start: Date, months: number): boolean {
    const currentDate = new Date();
    const yearsAgo = currentDate.setMonth(currentDate.getMonth() - months);
    return start.getTime() < yearsAgo;
  }

  /**
   * Return Full months range between dates.
   * @param {date} start date
   * @param {date} end date
   * @returns {boolean}
   */
  getFullMonthRange(startDate: Date, endDate: Date): number {
    let fullMonths = (endDate.getFullYear() - startDate.getFullYear()) * 12 + (endDate.getMonth() - startDate.getMonth());

    if (endDate.getDate() < startDate.getDate()) {
      fullMonths--;
    }

    return fullMonths;
  }

  /**
   * Returns beginning of the day of chosen date
   * @param {Date} dateObject for which beginning of the day should be calculated
   * @returns {Date} - Date which is beginning of the day for chosen date
   * @private
   */
  getStartOfTheDay(dateObject: Date): Date {
    return new Date(dateObject.setHours(0, 0, 0, 0));
  }

  /**
   * Returns end of the day of chosen date
   * @param {Date} dateObject for which end of the day should be calculated
   * @returns {Date} - Date which is end of the day for chosen date
   * @private
   */
  getEndOfTheDay(dateObject): Date {
    return new Date(dateObject.setHours(23, 59, 59, 999));
  }

  /**
   * return formated event start time
   *
   * @param {date} date
   * @param {string} date
   * @returns {string}
   */
  getEventTime(date: string): string {
    const today = this.determineDay(date, false) === 'today';

    return today ? `${this.datePipe.transform(date, 'HH:mm')}, Today` : this.datePipe.transform(date, 'HH:mm, dd MMM');
  }

  /*
   * return formated event start time
   * Return time for (race-)event in format HH:mm, e.g. 2:00 -> 02:00
   * @param {string} localTime
   * @returns {string}
   */
  formatHours(localTime: string): string {
    const localTimeSplit = localTime.split(':');
    if (localTimeSplit.length === 2 && localTimeSplit[0].length === 1) {
      return `0${localTime}`;
    }
    return localTime;
  }

  /**
   * Return date object from string for browsers like safari
   * @param parseDate {string} - string example 2019-01-25 13:34:27.000
   * @returns {Date} - date object
   */
  parseDateTime(parseDate: string): Date {
    const date = parseDate.split(/[^0-9]/).map(chunk => parseInt(chunk, 10));
    return new Date(date[0], date[1] - 1, date[2], date[3], date[4], date[5]);
  }

  /**
   * return formated event start time
   * Example 'Friday 25th January 2019'
   * @param {string} localTime
   * @returns {string}
   */
  getFullDateFormatSufx(date: Date): string {
    const [ week, day, month, year ] = this.datePipe.transform(date, 'EEEE d MMMM y').split(' ');
    return `${week} ${day}${this.locale.getString(this.filter.numberSuffix(day))} ${month} ${year}`;
  }

  /**
   * return formated event start time
   * Example '23:30 16 Jan'
   * @param {Date} localTime
   * @returns {string}
   */
  getDateTimeFormat(date: Date): string {
    const [time, day, month ] = this.datePipe.transform(date, TIME_SERVICE_ENUM.DATE_TIME_MONTH).split(' ');
    return `${time} ${day} ${month}`;
  }

  /**
   * return formated event start time with year
   * Example '23:30 16th January 2019'
   * @param {date} localDate
   * @returns {string}
   */
  getFullDateTimeFormatSufx(localDate: Date): string {
    const [time, day, month, year] = this.datePipe.transform(localDate, TIME_SERVICE_ENUM.DATE_TIME_MONTH_YEAR).split(' ');
    return `${time} ${day}${this.locale.getString(this.filter.numberSuffix(day))} ${month} ${year}`;
  }

  /**
   * Launches the countdown timer.
   *
   * Usage:
   *  localTimer = countDownTimer();
   *  {{localTimer.value}}
   *  localTimer.stop();
   *
   * @param {number} seconds - amount of seconds to count down, defaults to 5
   * @return {ICountDownTimer} - timer object
   */
  countDownTimer(seconds: number = 5): ICountDownTimer {
    let
      timerId = null,
      countDownValue = seconds;

    if (seconds > 119) {
      countDownValue = 119;
      console.warn(`Resetting countdown timer to ${countDownValue} seconds. Greater values are not supported.`);
    }

    const
      getMinutesValue = () => {
        return `0${Math.trunc(countDownValue / 60)}`;
      },

      getSecondsValue = () => {
        return `0${parseInt(((countDownValue % 3600) % 60).toFixed(), 10)}`.slice(-2);
      },

      getTimerValue = () => {
        return countDownValue !== null ? `${getMinutesValue()}:${getSecondsValue()}` : '';
      },

      stopTimer = () => {
        timerId && this.windowRefService.nativeWindow.clearInterval(timerId);
        countDownValue = timerId = null;
        timerEntity.value = getTimerValue();
      };

    const timerEntity: ICountDownTimer = {
      value: getTimerValue(),
      stop: () => stopTimer()
    };

    timerId = this.windowRefService.nativeWindow.setInterval(() => {
      if (!countDownValue) {
        stopTimer();
        return;
      }

      countDownValue--;
      timerEntity.value = getTimerValue();
    }, 1000);

    return timerEntity;
  }

  /**
   * Launches the countdown HH:MM timer.
   *
   * Usage:
   *  localTimer = countDownTimerForHours();
   *  {{localTimer.value}}
   *  localTimer.stop();
   *
   * @param {number} seconds - amount of seconds to count down, defaults to 5
   * @return {ICountDownTimer} - timer object
   */
  countDownTimerForHours(seconds: number): ICountDownTimer {
    let
      countDownValue = seconds;
    const
      getHoursValue = () => {
        return `${Math.floor(countDownValue / (60 * 60))}`.slice(-2);
      },
      getMinutesValue = () => {
        return `0${Math.ceil(countDownValue % (60 * 60) / 60)}`.slice(-2);
      },
      getTimerValue = () => {
        return countDownValue > 0 ? this.formatHours(`${getHoursValue()}:${getMinutesValue()}`) : '00:00';
      },
      stopTimer = () => {
        this.timerIdHour && this.timerIdHour.unsubscribe();
        countDownValue = this.timerIdHour = null;
        timerEntity.value = getTimerValue();
      };
    const timerEntity: ICountDownTimer = {
      value: getTimerValue(),
      stop: () => stopTimer()
    };
    const subscribe = interval(1000);
    this.timerIdHour =  subscribe.subscribe( () => {
      if (countDownValue && countDownValue <= 0) {
        stopTimer();
        return timerEntity.value = TIME_SERVICE_ENUM.DEFAULT_TIMER;
      }
      countDownValue--;
      timerEntity.value = getTimerValue();
    });
    if (seconds < TIME_SERVICE_ENUM.INITIAL_VALUE) {
      timerEntity.value = TIME_SERVICE_ENUM.DEFAULT_TIMER;
    }
    return timerEntity;
  }

  reduceByCurrentTime(dateTime: string | number): number {
    const currentDateTime = new Date();
    const localDateTime = new Date(dateTime);
      localDateTime.setHours(
        localDateTime.getHours() - currentDateTime.getHours(),
        localDateTime.getMinutes() - currentDateTime.getMinutes(),
        localDateTime.getSeconds() - currentDateTime.getSeconds());
    return localDateTime.getTime();
  }

  /**
   * return rounded GMT time
   * @returns {String}
   */
  getGmtTime(): string {
    const date = new Date();
    const gmtDate = new Date(date.valueOf() + (date.getTimezoneOffset() * this.min));
    const roundedGmtTime = this.roundSeconds(new Date(gmtDate), this.SSRequestsSecondsToRoundValue).getTime();

    return this.formatTime(roundedGmtTime);
  }

  /**
   * return formated event start time
   * Example 'Friday 25th January'
   * @param {string} localTime
   * @returns {string}
   */
   getFullDateFormatSuffixWithDay(date: Date): string {
    const [ week, day, month ] = this.datePipe.transform(date, 'EEEE d MMMM').split(' ');
    return `${week} ${day}${this.locale.getString(this.filter.numberSuffix(day))} ${month}`;
  }

  /**
   * Schedule time should be in present time range
   * @param displayFrom in format HH:mm a, string e.g.: 03:00 AM, 03:00am
   * @param displayTo in format HH:mm a, string e.g.: 10:00PM, 10:00 pm
   */
  isActiveRangeForCustomTime(displayFrom: string, displayTo: string): boolean {
    const currentTime = this.getCurrentTime();

    const startTime = this.getDateTimeWithCustomTime(displayFrom);
    const endTime = this.getDateTimeWithCustomTime(displayTo);

    if (!startTime || !endTime || startTime > endTime) {
      return true;
    }

    return startTime < currentTime && endTime > currentTime;
  }

  /**
   * return formated event start time
   * Example '25th January 2019'
   * @param {string} localTime
   * @returns {string}
   */
  getOnlyFullDateFormatSuffix(date: Date): string {
    const [ day, month, year ] = this.datePipe.transform(date, 'd MMMM y').split(' ');
    return `${day}${this.locale.getString(this.filter.numberSuffix(day))} ${month} ${year}`;
  }

  /**
   * 
   * @param date format "2023-04-17 12:50:00" change to "2023-04-17T12:50:00Z"
   * @returns 
   */
  convertDateStr(date: string): string {
    return date.replace(' ', 'T') + (date.endsWith('Z') ? '' : 'Z');
  }

   createDateAsUTC(date: Date): Date {
    return new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()));
  }

  getDatetimeWithFormatSuffix(date: Date, showTime?: boolean, isMyBets?: boolean): string {
    let value = '';
    const yesterday = new Date();
    const today = new Date();
    const tomorrow = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    tomorrow.setDate(tomorrow.getDate() + 1);
    if(isMyBets) {
    date.setHours(date.getHours() - this.findDifferenceBetweenUTCAndBST());
    }
    if (yesterday.getDate() == date.getDate() && yesterday.getMonth() == date.getMonth()) {
      value = '(Yesterday)';
    } else if (today.getDate() == date.getDate() && today.getMonth() == date.getMonth()) {
      value = '(Today)';
    } else if (tomorrow.getDate() == date.getDate() && tomorrow.getMonth() == date.getMonth()) {
      value = '(Tomorrow)';
    }
    const [week, day, Month, time] = this.datePipe.transform(date, 'EEEE (dd MMMM) HH:mm').split(' ');
    if (value) {
      value = `${week} ${value} - ${time}`;
    } else {
      value = `${week} ${day}${this.locale.getString(this.filter.numberSuffix(day.slice(1,)))} ${Month} - ${time}`;
    }
    return showTime ? value.split('-')[0].trim() : value;
  }

  /**
   * 
   * @returns number with utc/uk time hours difference
   */
  findDifferenceBetweenUTCAndBST() {
    const UKHours = this.formatDateByTimeZone('Europe/London');
    const UTCHours = this.formatDateByTimeZone('UTC');
    return !isNaN(UKHours) && !isNaN(UTCHours) && (UKHours != UTCHours) ? 1 : 0;
  }

  /**
   * format date to timezone
   * @param timezone string 'Europe/London, UTC'
   */
  formatDateByTimeZone(timezone) {
   return Number(new Date().toLocaleString('en-GB', { hour: '2-digit', hour12: false, timeZone: timezone }));
  }
  /**
   * Return the number of milliseconds
   * since 1 January 1970 00:00:00 UTC for
   * the current date and time according to system settings and input parameter.
   * @param {string} time in format HH:mm a, string e.g.: 03:00 AM, 03:00am
   * @returns {number}
   */
  private getDateTimeWithCustomTime(time: string): number {
    if (!time) {
      return;
    }

    const now = new Date();
    const timeArray = time.match(/(([01][0-9]):([0-5][0-9])(([AaPp][Mm])| ([AaPp][Mm])))/);

    if (timeArray) {
      const ampm = timeArray[4].toLowerCase();
      const hours = ampm.indexOf('am') !== -1 ? Number(timeArray[2]) : Number(timeArray[2]) + 12;
      const minutes = Number(timeArray[3]);

      return now.setHours(hours, minutes);
    }
  }

  /**
   * return date with rounded Seconds in Date to seconds value or 0
   *
   * @param {date} date
   * @param {number} seconds
   * @returns {Date}
   */
  private roundSeconds(date: Date, seconds: number): Date {
    if (seconds) {
      const secs = date.getSeconds() < seconds ? 0 : seconds;
      date.setSeconds(secs);
    }
    return date;
  }

  /**
   * Returns Date witOut TimeZone Offset and in ISO format;
   *
   * @param dateInISOformat
   * @returns {string}
   */
  private removeTimezoneOffSet(dateInISOformat: string): string {
    const newDate = new Date(dateInISOformat);
    newDate.setMinutes(newDate.getMinutes() - newDate.getTimezoneOffset());
    return newDate.toISOString();
  }

  /**
   * Return winter and summer timezone.
   *
   * @param {Date} date
   * @return {Number}
   */
  private getTimezones(date): number[] {
    const timeZones = [];
    for (let i = 0; i < 12; i++) {
      timeZones.push(new Date(date.getFullYear(), i, 1).getTimezoneOffset());
    }
    return [Math.min.apply(null, timeZones), Math.max.apply(null, timeZones)];
  }

  /**
   * Return summertime status
   * or return true, if client timezone don't observe Daylight Saving Time
   *
   * @param {Date} date
   * @return {Boolean}
   */
  private summerTimeStatus(date: Date): boolean {
    const winterTimezone = this.getTimezones(date);
    return date.getTimezoneOffset() < winterTimezone[1];
  }

  /**
   * Returns date and time in correct format
   * @param {string} day
   * @param {boolean} isRacing
   * @return {string}
   */
  private format(day: string, isRacing: boolean): string {
    if (isRacing) {
      return this.datePipe.transform(this.dateTimeOfDayInISO(day), 'yyyy-MM-dd h:mm:ss ');
    }
    return this.dateTimeOfDayInISO(day);
  }

  /**
   *  Return date and time of the day in ISO8601 format.
   *
   * @param h {number} - hours
   * @param m {number} - minuets
   * @param s {number} - seconds
   * @param ms {number} - milliseconds
   * @returns {Date} - date in ISO8601 format
   */
  private dateTimeInISO(h: number, m: number, s: number, ms: number): string {
    const date = new Date();

    date.setHours(h, m, s, ms);
    const day = date.toISOString();

    return day;
  }

  /**
   *  Return date in yyyy-MM-ddTHH:mm:ss formatt.
   *
   * @param time {number}
   * @returns {String}
   */
  private formatTime(time: number): string {
    return `${this.datePipe.transform(time, 'yyyy-MM-ddTHH:mm:ss')}Z`;
  }
}
