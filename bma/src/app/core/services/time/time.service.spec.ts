import { TimeService } from './time.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

describe('TimeService', () => {
  let service: TimeService;

  let locale;
  let datePipe;
  let filterService;
  let timeSyncService;
  let windowRefService;

  const timeStamp = '1549407300000';
  const timeStampPattern = 'dd/MM/yyyy HH:mm';

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy().and.returnValue('string')
    };
    datePipe = {
      transform: jasmine.createSpy().and.returnValue('string')
    };
    filterService = {
      numberSuffix: jasmine.createSpy().and.returnValue('th')
    };
    windowRefService = {
      nativeWindow: jasmine.createSpyObj(['setInterval', 'clearInterval'])
    };
    timeSyncService = {
      getUserSessionTime: jasmine.createSpy().and.returnValue(of({
          'timestamp': 1642393233124,
          'x-forward-for': '103.115.128.202'
      }))
  };
    jasmine.clock().uninstall();
    jasmine.clock().install();

    service = new TimeService(locale, datePipe, filterService as any, timeSyncService, windowRefService);
  });

  it('isTodayDate - should check if is today date = true', () => {
    expect(service.isTodayDate(new Date())).toEqual(true);
  });

  it('isTodayDate - should check if is today date = false', () => {
    expect(service.isTodayDate(new Date('Mon Nov 19 3018 15:00:00'))).toEqual(false);
  });

  it('dateToString', () => {
    const date = new Date();
    service.dateToString(date);
    expect(datePipe.transform).toHaveBeenCalledTimes(1);
    expect(datePipe.transform).toHaveBeenCalledWith(date, 'yyyy-MM-dd HH:mm:ss');
  });

  describe('formatByPattern', () => {
    it('formatByPattern', () => {
      const date: Date = new Date();
      service.formatByPattern(date, 'yyyy-MM-dd HH:mm:ss', '+1');
      expect(datePipe.transform).toHaveBeenCalledTimes(1);
      expect(datePipe.transform).toHaveBeenCalledWith(date, 'yyyy-MM-dd HH:mm:ss', '+1', undefined);
    });

    it(`should use UK timezone if 'ukTimeZone' equal true`, () => {
      service.formatByPattern(timeStamp, timeStampPattern, null, true);

      expect(service['datePipe'].transform).toHaveBeenCalledWith(timeStamp, timeStampPattern, service['ukTimeZone'], undefined);
    });

    it('should use locale if provided', () => {
      service.formatByPattern(timeStamp, timeStampPattern, null, null, 'en-GB');

      expect(service['datePipe'].transform).toHaveBeenCalledWith(timeStamp, timeStampPattern, null, 'en-GB');
    });
  });
  

  describe('isEqualDatesByPattern', () => {
    it('should return True if dates are equal', () => {
      spyOn(service, 'formatByPattern').and.returnValues('1', '1');

      expect(service.isEqualDatesByPattern('1', '1', timeStampPattern)).toBeTruthy();
    });

    it('should return Frue if dates are Not equal', () => {
      spyOn(service, 'formatByPattern').and.returnValues('1', '2');

      expect(service.isEqualDatesByPattern('1', '2', timeStampPattern)).toBeFalsy();
    });

    it(`should call 'formatByPattern' with correct arguments`, () => {
      spyOn(service, 'formatByPattern');

      service.isEqualDatesByPattern('1', '2', timeStampPattern, true);

      expect(service.formatByPattern['calls'].argsFor(0)).toEqual(['1', timeStampPattern, null, true]);
      expect(service.formatByPattern['calls'].argsFor(1)).toEqual(['2', timeStampPattern, null, true]);
    });
  });

  describe('dateTimeOfDayInISO', () => {
    it('twoWeeksAgo', () => {
      expect(service.dateTimeOfDayInISO('twoWeeksAgo')).toEqual(dateTimeInISO(-336, 0, 0, 0));
    });
    it('weekAgo', () => {
      expect(service.dateTimeOfDayInISO('weekAgo')).toEqual(dateTimeInISO(-168, 0, 0, 0));
    });
    it('yesterday', () => {
      expect(service.dateTimeOfDayInISO('yesterday')).toEqual(dateTimeInISO(-24, 0, 0, 0));
    });
    it('today', () => {
      expect(service.dateTimeOfDayInISO('today')).toEqual(dateTimeInISO(0, 0, 0, 0));
    });
    it('tomorrow', () => {
      expect(service.dateTimeOfDayInISO('tomorrow')).toEqual(dateTimeInISO(24, 0, 0, 0));
    });
    it('afterTomorrow', () => {
      expect(service.dateTimeOfDayInISO('afterTomorrow')).toEqual(dateTimeInISO(48, 0, 0, 0));
    });
    it('post48h', () => {
      const currentDateTime = new Date(2019, 10, 19, 11, 12, 13);
      jasmine.clock().mockDate(currentDateTime);
      expect(service.dateTimeOfDayInISO('post48h')).toEqual(dateTimeInISO(11 + 48, 12, 0, 0));
    });
    it('6days', () => {
      expect(service.dateTimeOfDayInISO('6days')).toEqual(dateTimeInISO(144, 0, 0, 0));
    });
    it('default', () => {
      expect(service.dateTimeOfDayInISO('unknown')).toEqual(dateTimeInISO(0, 0, 0, 0));
    });
  });

  describe('getLocalDate', () => {
    beforeEach(() => {
      spyOn(Date.prototype, 'getTimezoneOffset').and.returnValue(1);
      spyOn(Date.prototype, 'getHours').and.returnValue('00' as any);
      spyOn(Date.prototype, 'getMinutes').and.returnValue('00' as any);
    });

    it('should return date to string', () => {
      const day = new Date('2020-04-16');
      day.setHours(23, 59, 0o0, 0o0);
      const result = service.getLocalDate(day);
      expect(result.getFullYear()).toEqual(day.getFullYear());
      expect(result.getMonth()).toEqual(day.getMonth());
      expect(result.getDate()).toEqual(day.getDate());
    });
  });


  describe('incrementDateDay', () => {
    it('today', () => {
      const date = new Date().getTime();
      const srvDate: number = service.incrementDateDay('today');
      expect(srvDate + 2 > date).toBeTruthy();
    });

    it('tomorrow', () => {
      const date = new Date();
      const tomorrowDate = new Date(service.incrementDateDay('tomorrow'));
      date.setDate(date.getDate() + 1);
      expect(tomorrowDate.getDay()).toEqual(date.getDay());
    });

    it('future', () => {
      const date = new Date();
      const futureDate = new Date(service.incrementDateDay('future'));

      date.setDate(date.getDate() + 2);
      expect(futureDate.getDay()).toEqual(date.getDay());
    });

    it('yesterday', () => {
        const date = new Date().getTime();
        const srvDate: number = service.incrementDateDay('yesterday');
        expect(srvDate + 2 > date).toBeTruthy();
    });


  });

  describe('createTimeRange', () => {
    it('object', () => {
      expect(service.createTimeRange(<any>{})).toEqual(<any>{});
    });

    it('featured', () => {
      expect(service.createTimeRange('featured')).toEqual({
        startDate: service.dateTimeOfDayInISO('today'),
        endDate: service.dateTimeOfDayInISO('6days')
      });
    });

    it('featured', () => {
      expect(service.createTimeRange('pre48h')).toEqual({
        startDate: service.dateTimeOfDayInISO('today'),
        endDate: service.dateTimeOfDayInISO('post48h')
      });
    });

    it('antepost', () => {
      expect(service.createTimeRange('antepost')).toEqual({
        startDate: service.dateTimeOfDayInISO('today')
      });
    });

    it('matchesTab', () => {
      expect(service.createTimeRange('matchesTab')).toEqual({
        startDate: service.dateTimeOfDayInISO('today')
      });
    });

    it('allEvents', () => {
      expect(service.createTimeRange('allEvents')).toEqual({
        startDate: service.dateTimeOfDayInISO('today')
      });
    });

    it('today', () => {
      expect(service.createTimeRange('today')).toEqual({
        startDate: service.dateTimeOfDayInISO('today'),
        endDate: service.dateTimeOfDayInISO('tomorrow')
      });
    });

    it('tomorrow', () => {
      expect(service.createTimeRange('tomorrow')).toEqual({
        startDate: service.dateTimeOfDayInISO('tomorrow'),
        endDate: service.dateTimeOfDayInISO('afterTomorrow')
      });
    });

    it('future', () => {
      expect(service.createTimeRange('future')).toEqual({
        startDate: service.dateTimeOfDayInISO('afterTomorrow')
      });
    });

    it('uknown', () => {
      expect(service.createTimeRange('')).toEqual({});
    });

    it('todayAndTomorrow', () => {
      expect(service.createTimeRange('todayAndTomorrow')).toEqual({
        startDate: service.dateTimeOfDayInISO('today'),
        endDate: service.dateTimeOfDayInISO('afterTomorrow')
      });
    });
  });

  it('getFullYear', () => {
    expect(service.getFullYear()).toEqual(new Date().getFullYear());
  });

  it('getMonthNumber', () => {
    expect(service.getMonthNumber()).toEqual(new Date().getMonth() + 1);
  });

  it('getMonthI18nValue', () => {
    const date = new Date(1541512386029);
    expect(service.getMonthI18nValue(date, true)).toEqual('sb.monthNovember');
  });

  it('getMonthI18nValue', () => {
    const date = new Date(1541512386029);
    expect(service.getMonthI18nValue(date, false)).toEqual('sb.monNovember');
  });

  it('getDayI18nValue', () => {
    const date = new Date(1541512386029).toString();
    expect(service.getDayI18nValue(date)).toEqual('sb.dayTuesday');
  });

  it('getUTCDay', () => {
    const date = new Date(1541512386029);
    expect(service.getUTCDay(date)).toEqual('sb.dayTuesday');
  });

  it('compareDate', () => {
    expect(service.compareDate('2018-11-04')).toEqual(compareDate('2018-11-04'));
  });

  it('getEventTime today', () => {
    const today = new Date();
    spyOn(service, 'determineDay').and.returnValue('today');

    service.getEventTime(`${today}`);
    expect(datePipe.transform).toHaveBeenCalledWith(`${today}`, 'HH:mm');
  });

  it('getEventTime future', () => {
    const future = new Date();
    spyOn(service, 'determineDay').and.returnValue('tomorrow');
    future.setDate(future.getDate() + 1);

    service.getEventTime(`${future}`);
    expect(datePipe.transform).toHaveBeenCalledWith(`${future}`, 'HH:mm, dd MMM');
  });

  it('formatHours', () => {
    expect(service.formatHours('2:00')).toEqual('02:00');
    expect(service.formatHours('12:22')).toEqual('12:22');
    expect(service.formatHours('Mon, 31 Dec 2018 14:20:01 GMT')).toEqual('Mon, 31 Dec 2018 14:20:01 GMT');
    expect(service.formatHours('1546266055065')).toEqual('1546266055065');
  });

  describe('getCorrectDay', () => {

    it('today', () => {
      service['dateTimeOfDayInISO'] = jasmine.createSpy('dateTimeOfDayInISO').and.callFake((p1) => {
        if (p1  === 'today') {
          return '2020-04-17T21:00:00.000Z';
        } else if (p1 ==='tomorrow') {
          return '2020-04-19T00:00:00.000Z';
        } else if (p1 ==='afterTomorrow') {
          return '2020-04-20T21:00:00.000Z';
        }
      });
      const result = service.getCorrectDay('2020-04-18');
      expect(result).toEqual('sb.today');
    });

    it('tomorrow', () => {
      service['dateTimeOfDayInISO'] = jasmine.createSpy('dateTimeOfDayInISO').and.callFake((p1) => {
        if (p1  === 'today') {
          return '2020-04-17T21:00:00.000Z';
        } else if (p1 ==='tomorrow') {
          return '2020-04-18T00:00:00.000Z';
        } else if (p1 ==='afterTomorrow') {
          return '2020-04-20T21:00:00.000Z';
        }
      });
      expect(service.getCorrectDay('2020-04-19')).toEqual('sb.tomorrow');
    });

    it('date string', () => {
      const date: Date = new Date('2018-11-04');
      expect(service.getCorrectDay(date.toISOString().substring(0, 10))).toEqual('sb.daySunday');
    });
  });

  describe('getUTCDayValue', () => {
    it('today', () => {
      const today = new Date().getTime();
      const result = service.getUTCDayValue(today);
      expect(result).toBeDefined();
    });

    it('tomorrow', () => {
      const today = new Date();
		  const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      const result = service.getUTCDayValue(tomorrow.getTime());
      expect(result).toBeDefined();
    });
  });

  describe('determineCurrentAndNextDayRange', () => {
    it('return Current And Next Day Range ', () => {
      const timestamp = 1587081600;
      const result = service.determineCurrentAndNextDayRange(timestamp);

      expect(result).toEqual({
          timeStampFrom: 1555200000,
          timeStampTo: 1641600000
      });
    });
  });

  describe('getLocalDateFromString', () => {
    it('should return date to string', () => {
      const day = '2020-04-16';
      const result = service.getLocalDateFromString(day);

      expect(result.toISOString().substring(0, 10)).toEqual('2020-04-16');
    });

    it('should return null', () => {
      const result = service.getLocalDateFromString('');

      expect(result).toEqual(null);
    });

    it('should return date to string (To replace T and -)', () => {
      const day = '2020-12-08T11:39:36.000Z';
      const result = service.getLocalDateFromString(day);

      expect(result.toISOString().substring(0, 10)).toEqual('2020-12-08');
    });
  });

  describe('minutesToMiliseconds and secondsToMiliseconds ', () => {
    it('should seconds from 20 minutes', () => {
      const result = service.minutesToMiliseconds(20);

      expect(result).toEqual(1200000);
    });

    it('should miliseconds from 20 seconds', () => {
      const result = service.secondsToMiliseconds(20);
      expect(result).toEqual(20000);
    });
  });

  describe('getLocalHourMin and getLocalHourMinInMilitary', () => {
    it('getLocalHourMin', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        return  '14:20:01';
      });
      const result = service.getLocalHourMin('Mon, 31 Dec 2018 14:20:01 GMT');

      expect(result).toEqual('14:20:01');
    });

    it('getLocalHourMinInMilitary', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        return  '23:00';
      });

      const result = service.getLocalHourMinInMilitary(23);

      expect(result).toEqual('23:00');
    });
  });

  describe('format', () => {
    it('should return time with this format yyyy-MM-dd h:mm:ss ', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        return  'Mon, 31 Dec 2018 14:20:01 GM';
      });

      const result = service['format']('2018-12-31', true);
      expect(result).toEqual('Mon, 31 Dec 2018 14:20:01 GM');
    });

    it('should call dateTimeOfDayInISO', () => {
      service.dateTimeOfDayInISO = jasmine.createSpy().and.returnValue('2020-04-16T21:00:00.000Z');
      const result = service['format']('2020-04-16', false);

      expect(result).toEqual('2020-04-16T21:00:00.000Z');
    });
  });

  describe('getEndOfTheDay and getStartOfTheDay', () => {
    it('getEndOfTheDay should return end of the day', () => {
      const resData: Date = new Date('2020-04-15');
      const result = service['getEndOfTheDay'](resData);

      resData.setHours(23, 59, 59, 999);

      expect(result).toEqual(resData);
    });

    it('getStartOfTheDay should return start of the day', () => {
      const resData: Date = new Date('2020-04-15');
      const result = service['getStartOfTheDay'](resData);

      resData.setHours(0, 0, 0, 0);

      expect(result).toEqual(resData);
    });
  });

  describe('moreThanOneYear', () => {
    it('moreThanOneYear should return true', () => {
      const resData: Date = new Date('2020-01-15');
      const result = service['moreThanYears'](resData, 12);

      expect(result).toBe(true);
    });
  });

  describe('moreThanFourYears', () => {
    it('moreThanFourYears should return true', () => {
      const resData: Date = new Date('2017-01-15');
      const result = service['moreThanYears'](resData, 48);

      expect(result).toBe(true);
    });
  });

  describe('isInNext24HoursRange', () => {
    it('moreThanOneYear should return false', () => {
      const resData: Date = new Date('2020-01-15');
      const result = service['isInNext24HoursRange'](resData);

      expect(result).toBe(false);
    });

    it('moreThanOneYear should return true', () => {
      const today: Date = new Date();
      today.setHours(23, 59, 59, 999);
      const result = service['isInNext24HoursRange'](today);

      expect(result).toBe(true);
    });
  });

  describe('getTimeRangeForRequest', () => {
    it('service createTimeRange should been called with date', () => {
      service.createTimeRange = jasmine.createSpy('createTimeRange').and.callFake((date) => {
        return  {
          startDate: '2020-01-15',
          endDate:'2020-01-16'
        };
      });

      const result = service['getTimeRangeForRequest']('2020-01-15');
      expect(result).toEqual({
        startTime: '2020-01-15',
        endTime: '2020-01-16'
      });
    });

    it('should return obj', () => {
      service.createTimeRange = jasmine.createSpy('createTimeRange').and.callFake((date) => {
        return  {};
      });
      const result = service['getTimeRangeForRequest']('');
      expect(result).toEqual({});
    });
  });

  describe('getRacingTimeRangeForRequest', () => {
    it('should return obj', () => {
      const result = service['getRacingTimeRangeForRequest']('2020-01-15');
      expect(result).toEqual({});
    });

    it('service createTimeRange should been called with date', () => {
      service.createTimeRange = jasmine.createSpy('createTimeRange').and.callFake((date) => {
        const today: Date = new Date('2020-01-15');
        return  {
          startDate: today.setHours(7, 0, ),
          endDate: today.setHours(23, 50, )
        };
      });

      const result = service['getRacingTimeRangeForRequest']('2020-01-15');
      expect(result).toEqual({
        startTime: '2020-01-15T07:00:00.000Z',
        endTime: '2020-01-15T23:50:00.000Z'
      });
    });

    it('service createTimeRange should been called with today', () => {
      service.createTimeRange = jasmine.createSpy('createTimeRange').and.callFake((date) => {
        const today: Date = new Date('2021-12-17');
        return  {
          startDate: today.setHours(7, 0, ),
          endDate: today.setHours(23, 50, )
        };
      });

      const result = service['getRacingTimeRangeForRequest']('');
      expect(result).toEqual({
        startTime: '2021-12-17T07:00:00.000Z',
        endTime: '2021-12-17T23:50:00.000Z'
      });
    });
  });

  describe('getHoursRageFromNow', () => {
    it('should have been called', () => {
      service['getHoursRageFromNow'](23);
      expect(service['getHoursRageFromNow']).toBeTruthy();
    });
  });

  describe('daysDifference', () => {
    it('moreThanOneYear should return false', () => {
      service['daysDifference']('2020-01-15');
      expect(service['daysDifference']).toBeTruthy(); 
    });
  });

  it('moreThanOneYear should return false', done => {
      const result = service['getHydraDaysDifference']('2020-01-15');
      result.subscribe(data => {
        expect(data).toBeTruthy();
        done();
      });
  });

  describe('getTodayTomorrowOrDate', () => {
    beforeEach(() => {
      service['dateTimeOfDayInISO'] = jasmine.createSpy('dateTimeOfDayInISO').and.callFake((p1) => {
        if (p1  === 'today') {
          return '2020-04-16';
        } else if (p1 ==='tomorrow') {
          return '2020-04-17';
        } else if (p1 ==='afterTomorrow') {
          return '2020-04-18';
        } else {
          return '2020-04-15';
        }
      });
    });

    it('getTodayTomorrowOrDate should return today', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        return  date.toISOString().substring(0, 10);
      });

      (locale.getString as jasmine.Spy).and.callFake((date) => {
            return 'today';
      });
      const result = service.getTodayTomorrowOrDate('2020-04-16');

      expect(result).toEqual('today 2020-04-16');
    });

    it('getTodayTomorrowOrDate should return  day without prefix', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        date.setHours(12, 30, 30, 99);
       return  date.toISOString().substring(0, 10);
      });

      const result = service.getTodayTomorrowOrDate('2020-04-15', false, false);

      expect(result).toEqual('2020-04-15');
    });

    it('getTodayTomorrowOrDate should return day with prefix', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        date.setHours(12, 30, 30, 99);
        return  date.toISOString().substring(0, 10);
      });

      const result = service.getTodayTomorrowOrDate('2020-04-15', false, true);

      expect(result).toEqual('2020-04-15 2020-04-15');
    });

    it('getTodayTomorrowOrDate should return tomorrow', () => {
      (locale.getString as jasmine.Spy).and.callFake((date) => {
        return '2020-04-18';
      });
      const result = service.getTodayTomorrowOrDate('"2020-04-17"', true, false);

      expect(result).toEqual('2020-04-18');
    });
    it('getTodayTomorrowOrDate should return yesterday', () => {
      const reqDate: Date = new Date();
      reqDate.setDate(reqDate.getDate() - 1);
        (datePipe.transform as jasmine.Spy).and.callFake((date) => {
         return  reqDate;
        });
      (locale.getString as jasmine.Spy).and.callFake((date) => {
        return reqDate.toISOString().substring(0, 10);
      });
      const result = service.getTodayTomorrowOrDate(reqDate, false, false, 'YY-MM-DD');
      expect(result).toEqual(reqDate.toISOString().substring(0, 10));
    });
  });

  describe('determineDay', () => {
    beforeEach(() => {
      service['format'] = jasmine.createSpy('format').and.callFake((p1) => {
        if (p1  === 'today') {
          return '2020-04-16';
        } else if (p1 ==='tomorrow') {
          return '2020-04-17';
        } else if (p1 ==='afterTomorrow') {
          return '2020-04-18';
        } else {
          return '2020-04-15';
        }
      });
    });

    it('past', () => {
      const result = service.determineDay('2020-04-14', true);
      expect(result).toEqual('past');
    });

    it('today', () => {
      const result = service.determineDay('2020-04-16', true);
      expect(result).toEqual('today');
    });

    it('tomorrow', () => {
      const result = service.determineDay('2020-04-17', true);
      expect(result).toEqual('tomorrow');
    });

    it('afterTomorrow', () => {
      const result = service.determineDay('2020-04-18', true);
      expect(result).toEqual('future');
    });

  });

  function dateTimeInISO(h: number, m: number, s: number, ms: number): string {
    const d = new Date();
    d.setHours(h, m, s, ms);
    const day: string = d.toISOString();
    return day;
  }

  function compareDate(date: string): number {
    const currentDate = new Date(),
      compareDateValue = new Date(date.replace(/-/g, '/')),
      timeDiff = Math.abs(currentDate.getTime() - compareDateValue.getTime());

    return Math.ceil(timeDiff / (1000 * 3600 * 24));
  }

  describe('Format date in error message', () => {
    it('should replace date in UTC to local one', () => {
      const dateArray = ['2018-04-12 09:11:34', '2018', '12', '04', '09', '11', '34'];
      const result = service.formatToLocaleDate(dateArray);
      expect(result).toEqual(jasmine.any(String));
    });

    it('should not format date and replace date in UTC to local one', () => {
      const dateArray = [undefined];
      const result = service.formatToLocaleDate(dateArray);
      expect(result).toEqual(undefined);
    });

  });

  describe('parseDateTime', () => {
    it('should return date object', () => {
      const date = '2019-01-25 13:34:27.000';
      const result = service.parseDateTime(date);
      expect(result instanceof Date).toBe(true);
    });
  });

  it('getFullDateFormatSufx should get full date format', () => {
    const date = new Date('2019-02-11T13:02:00Z');
    (locale.getString as jasmine.Spy).and.callFake(data => data);
    (datePipe.transform as jasmine.Spy).and.returnValue('Wed 2 11 2019');
    expect(service.getFullDateFormatSufx(date)).toEqual('Wed 2th 11 2019');
  });

  it('getOnlyFullDateFormatSuffix should get full date format without week', () => {
    const date = new Date('2019-02-11T13:02:00Z');
    (locale.getString as jasmine.Spy).and.callFake(data => data);
    (datePipe.transform as jasmine.Spy).and.returnValue('2 11 2019');
    expect(service.getOnlyFullDateFormatSuffix(date)).toEqual('2th 11 2019');
  });

  it('getFullDateFormatSuffixWithDay should get full date format without year', () => {
    const date = new Date('2019-02-11T13:02:00Z');
    (locale.getString as jasmine.Spy).and.callFake(data => data);
    (datePipe.transform as jasmine.Spy).and.returnValue('Wed 2 11');
    expect(service.getFullDateFormatSuffixWithDay(date)).toEqual('Wed 2th 11');
  });

  it('getDateTimeFormat should get date time format', () => {
    const date = new Date('2021-02-17T18:00:00Z');
    (locale.getString as jasmine.Spy).and.callFake(data => data);
    (datePipe.transform as jasmine.Spy).and.returnValue('23:30 17 Feb');
    expect(service.getDateTimeFormat(date)).toEqual('23:30 17 Feb');
  });

  it('getFullDateTimeFormatSufx should get date time format', () => {
    const date = new Date('2021-02-17T18:00:00Z');
    (locale.getString as jasmine.Spy).and.callFake(data => data);
    (datePipe.transform as jasmine.Spy).and.returnValue('23:30 17 February 2021');
    expect(service.getFullDateTimeFormatSufx(date)).toEqual('23:30 17th February 2021');
  });

  it('getSuspendAtTime', () => {
    service['roundSeconds'] = jasmine.createSpy().and.returnValue(new Date());
    service.getSuspendAtTime();
    service.getSuspendAtTime(true);
    expect(service['roundSeconds']).toHaveBeenCalledTimes(2);
  });

  it('should parseDateInLocalFormat', () => {
    expect(service.parseDateInLocalFormat('2019-01-25 13:34:27') instanceof Date).toEqual(true);
  });

  describe('getFullMonthRange', () => {
    const startDate = new Date('01.05.2000');
    let endDate;

    it(`should return 3`, () => {
      endDate = new Date('04.05.2000');

      expect(service.getFullMonthRange(startDate, endDate)).toEqual(3);
    });

    it(`should return 2`, () => {
      endDate = new Date('04.04.2000');

      expect(service.getFullMonthRange(startDate, endDate)).toEqual(2);
    });

    it(`should return 122`, () => {
      endDate = new Date('04.04.2010');

      expect(service.getFullMonthRange(startDate, endDate)).toEqual(122);
    });

    it(`should return 0`, () => {
      endDate = new Date('01.05.2000');

      expect(service.getFullMonthRange(startDate, endDate)).toEqual(0);
    });
  });

  describe('@countDownTimer', () => {

    it('result value', () => {
      const result = service.countDownTimer();

      expect(result).toEqual(jasmine.any(Object));
      expect(result.value).toEqual(jasmine.any(String));
      expect(result.stop).toEqual(jasmine.any(Function));
      expect(result.value.indexOf(':')).toBe(2);
    });

    it('should use default timer value', () => {
      const result = service.countDownTimer();

      expect(result.value).toBe('00:05');
    });

    it('should convert timer value', () => {
      const result = service.countDownTimer(70);

      expect(result.value).toBe('01:10');
    });

    it('should decrease timer value down to allowed', () => {
      const result = service.countDownTimer(120);

      expect(result.value).toBe('01:59');
    });

    it('should start timer at first run', () => {
      service.countDownTimer();

      expect(windowRefService.nativeWindow.setInterval).toHaveBeenCalledWith(jasmine.any(Function), 1000);
    });

    it('half a way of timer', fakeAsync(() => {
      windowRefService.nativeWindow.setInterval = cb => {
        cb();
        return 123;
      };
      const result = service.countDownTimer(2);

      tick();

      expect(result.value).toBe('00:01');
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));

    it('should end the timer', fakeAsync(() => {
      windowRefService.nativeWindow.setInterval = cb => {
        cb(); cb();
        return 123;
      };
      const result = service.countDownTimer(2);

      tick();

      expect(result.value).toBe('00:00');
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    }));

    it('should stop the timer after finished countdown', fakeAsync(() => {
      let cb;
      windowRefService.nativeWindow.setInterval = _cb => {
        cb = _cb;
        return 123;
      };
      const result = service.countDownTimer(2);
      cb(); cb(); cb();

      tick();

      expect(result.value).toBe('');
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    }));

    it('should stop the timer on demand', fakeAsync(() => {
      windowRefService.nativeWindow.setInterval = cb => {
        cb();
        return 123;
      };
      const result = service.countDownTimer(2);

      tick();

      expect(result.value).toBe('00:01');
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();

      result.stop();

      expect(result.value).toBe('');
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    }));
  });

  describe('Time zones & daylight saving time (DST)', () => {
    const timeZonesDiff = [];
    const anyDate = new Date(Date.now());

    beforeEach(() => {
      for (let i = 0; i < 12; i++) {
        timeZonesDiff[i] = (i < 4 || i > 9) ? 60 : 120;
      }
      let j = 0;
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return timeZonesDiff[j++];
      });
    });

    it('getTimezones should return min max zones for DST', () => {
      expect(service['getTimezones'](anyDate)).toEqual([60, 120]);
    });

    it('summerTimeStatus no DST', () => {
      for (let i = 0; i < 12; i++) {
        timeZonesDiff[i] = 60;
      }
      expect(service['summerTimeStatus'](anyDate)).toBe(false);
    });

    it('summerTimeStatus return summertime status true', () => {
      service['getTimezones'] = jasmine.createSpy('getTimezones').and.returnValue([0, 60]);
      (Date.prototype.getTimezoneOffset as jasmine.Spy).and.returnValue(0);
      expect(service['summerTimeStatus'](anyDate)).toBe(true);
    });

    it('summerTimeStatus return summertime status false', () => {
      service['getTimezones'] = jasmine.createSpy('getTimezones').and.returnValue([60, 120]);
      (Date.prototype.getTimezoneOffset as jasmine.Spy).and.returnValue(240);
      expect(service['summerTimeStatus'](anyDate)).toBe(false);
    });
  });

  describe('@reduceByCurrentTime', () => {
    it('should reduce time for date by current local time', () => {
      const currentDateTime = new Date(2019, 10, 19, 22, 0, 0);
      const dateIn48h = new Date(2019, 10, 21, 11, 0, 0);
      jasmine.clock().mockDate(currentDateTime);
      const result = service.reduceByCurrentTime(dateIn48h.getTime());
      expect(result).toEqual(new Date(2019, 10, 20, 13, 0, 0).getTime());
    });
  });

  it('should return formatted start delta time', () => {
    service['formatTime'] = jasmine.createSpy('roundSeconds').and.returnValue(jasmine.any(String));
    service.selectTimeRangeStartDelta(1586433460);

    expect(service['formatTime']).toHaveBeenCalledWith(jasmine.any(Number));
  });

  it('should return formatted end delta time', () => {
    service['formatTime'] = jasmine.createSpy('roundSeconds').and.returnValue(jasmine.any(String));
    service.selectTimeRangeEndDelta(1586433460);

    expect(service['formatTime']).toHaveBeenCalledWith(jasmine.any(Number));
  });

  it('should return formatted time with delta', () => {
    service['formatTime'] = jasmine.createSpy('roundSeconds').and.returnValue(jasmine.any(String));
    service.getTimeWithDelta(1);

    expect(service['formatTime']).toHaveBeenCalledWith(jasmine.any(Number));
  });

  it('should return rounded start time range', () => {
    service['formatTime'] = jasmine.createSpy('roundSeconds').and.returnValue(jasmine.any(String));
    const actualResult = service.selectTimeRangeStart();

    expect(actualResult).toEqual(jasmine.any(String));
    expect(service['formatTime']).toHaveBeenCalledWith(jasmine.any(Number));
  });

  it('should return rounded end time range', () => {
    service['formatTime'] = jasmine.createSpy('roundSeconds').and.returnValue(jasmine.any(String));
    const actualResult = service.selectTimeRangeEnd();

    expect(actualResult).toEqual(jasmine.any(String));
    expect(service['formatTime']).toHaveBeenCalledWith(jasmine.any(Number));
  });

  describe('@roundTo30seconds', () => {
    it('should return format datetime in ISO format with MILLISECONDS = 0 and rounded seconds - 30', () => {
      const actualResult = service.roundTo30seconds('2019-02-11T13:02:33.123Z');

      expect(actualResult).toBe('2019-02-11T13:02:30.000Z');
    });
  });

  describe('@roundDateTo30Seconds', () => {
    it('should return format datetime in ISO format with MILLISECONDS = 0 and rounded seconds = 30', () => {
      const date = new Date('2019-02-11T13:02:25.123Z');
      const actualResult = service.roundDateTo30Seconds(date);

      expect(actualResult).toBe('2019-02-11T13:02:00.000Z');
    });

    it('should return format datetime in ISO format with random MILLISECONDS and rounded seconds = 30', () => {
      const date = new Date('2019-02-11T13:02:33.123Z');
      const actualResult = service.roundDateTo30Seconds(date, true);

      expect(actualResult.includes('2019-02-11T13:02:30')).toBeTruthy();
    });
  });

  describe('removeTimezoneOffSet and roundSeconds', () => {
    it('should return time with this format yyyy-MM-dd h:mm:ss ', () => {
      const newDate = new Date('2020-12-31');
      Date.prototype.setMinutes = jasmine.createSpy().and.callFake(p1 => {
        return newDate.toISOString();
      });
      const result = service['removeTimezoneOffSet']('2020-12-31');
      expect(result).toEqual(newDate.toISOString());
    });

    it('roundSeconds should return current date', () => {
      const today: Date = new Date();
      const result = service['roundSeconds'](today, 0);

      expect(result).toEqual(today);
    });
  });

  describe('isActiveRangeForCustomTime', () => {
    it('should return true', () => {
      service.getCurrentTime = jasmine.createSpy('getCurrentTime').and.returnValue(1593581977027);
      service['getDateTimeWithCustomTime'] = jasmine.createSpy('getDateTimeWithCustomTime');

      const result = service.isActiveRangeForCustomTime('03:00am', '11:59pm');

      expect(service.getCurrentTime).toHaveBeenCalled();
      expect(service['getDateTimeWithCustomTime']).toHaveBeenCalledWith('03:00am');
      expect(service['getDateTimeWithCustomTime']).toHaveBeenCalledWith('11:59pm');
      expect(result).toEqual(true);
    });
  });

  describe('getDateTimeWithCustomTime', () => {
    it('should return undefined', () => {
      expect(service['getDateTimeWithCustomTime']('')).toBeUndefined();
    });

    it('should return undefined', () => {
      expect(service['getDateTimeWithCustomTime']('03:00')).toBeUndefined();
    });

    it('should return undefined', () => {
      expect(service['getDateTimeWithCustomTime']('0300pm')).toBeUndefined();
    });

    it('should return undefined', () => {
      expect(service['getDateTimeWithCustomTime']('23:00pm')).toBeUndefined();
    });

    it('should return time for am', () => {
      const resData = new Date();
      jasmine.clock().mockDate(resData);
      const result = service['getDateTimeWithCustomTime']('03:00AM');

      resData.setHours(3, 0);

      expect(result).toEqual(resData.getTime());
    });

    it('should return time for pm', () => {
      const resData = new Date();
      jasmine.clock().mockDate(resData);
      const result = service['getDateTimeWithCustomTime']('03:00pm');

      resData.setHours(15, 0);

      expect(result).toEqual(resData.getTime());
    });
  });

  it('should return GMT date string', () => {
    service['roundSeconds'] = jasmine.createSpy('roundSeconds').and.returnValue(new Date());
    service['formatTime'] = jasmine.createSpy('roundSeconds').and.returnValue(jasmine.any(String));
    const actualResult = service.getGmtTime();

    expect(actualResult).toEqual(jasmine.any(String));
    expect(service['roundSeconds']).toHaveBeenCalled();
    expect(service['formatTime']).toHaveBeenCalledWith(jasmine.any(Number));
  });

  it('should format time',  () => {
    const actualResult = service['formatTime'](1586424330263);

    expect(actualResult).toEqual('stringZ');
  });

  describe('@countDownTimerForHours', () => {

    it('result value', () => {
      const result = service.countDownTimerForHours(0);
      expect(result).toEqual(jasmine.any(Object));
      expect(result.value).toEqual(jasmine.any(String));
      expect(result.stop).toEqual(jasmine.any(Function));
      expect(result.value.indexOf(':')).toBe(2);
    });

    it('should use default timer value', () => {
      const result = service.countDownTimerForHours(300);
      expect(result.value).toBe('00:05');
    });

    it('should use null timer value for negative condition', () => {
      const result = service.countDownTimerForHours(null);
    });

    it('should use null timer value for 0 condition', () => {
      const result = service.countDownTimerForHours(0);
      expect(result.value).toBe('00:00');
    });

    it('should convert timer value', () => {
      const result = service.countDownTimerForHours(600);
      expect(result.value).toBe('00:10');
    });

    it('should decrease timer value down to allowed', () => {
      const result = service.countDownTimerForHours(7140);
      expect(result.value).toBe('01:59');
    });

    it('should call countdownTimer once', fakeAsync(() => {
      service.countDownTimerForHours(0);
      tick(5000);
    }));

    it('should call countdownTimer once', fakeAsync(() => {
      service.countDownTimerForHours(-1);
      tick(5000);
    }));

  });

  describe('convertTimeAndCreateDateUTC', () => {
    it('should convert date to UTC String', () => {
      const dateStr = "2023-04-17 12:50:00";
      expect(service.convertDateStr(dateStr)).toEqual("2023-04-17T12:50:00Z");
    });

    it('should return type as Object', () => {
      expect(typeof service.createDateAsUTC(new Date())).toBe('object');
    });

    it('should return same date when UTC date is passed', () => {
      const dateStr = "2023-04-17T12:50:00Z";
      expect(service.convertDateStr(dateStr)).toEqual("2023-04-17T12:50:00Z");
    });
  });

  describe('getDatetimeWithFormatSuffix', () => {
    it('should execute Yesterday logic', () => {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate()-1);
      const val = service.getDatetimeWithFormatSuffix(yesterday, true);
      expect(val).toContain('Yesterday');
    });

    it('should execute Today logic', () => {
      const today = new Date();
      const val = service.getDatetimeWithFormatSuffix(today, true);
      expect(val).toContain('Today');
    });

    it('should execute tomorrow logic', () => {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate()+1);
      const val = service.getDatetimeWithFormatSuffix(tomorrow, true);
      expect(val).toContain('Tomorrow');
    });

    it('should execute otherDay logic', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        return 'Sunday (02 April) 05:53';
      });
      (locale.getString as jasmine.Spy).and.callFake((date) => {
        return 'nd';
      });
      const otherDay = new Date("Sun, 2 Apr 2023 05:53:51 GMT");
      const val = service.getDatetimeWithFormatSuffix(otherDay, false);
      expect(val).toContain('Sunday (02nd April) - 05:53');
    });

    it('should execute otherDay logic', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        return 'Sunday (02 April) 05:53';
      });
      (locale.getString as jasmine.Spy).and.callFake((date) => {
        return 'nd';
      });
      const otherDay = new Date("Sun, 2 Apr 2023 05:53:51 GMT");
      const val = service.getDatetimeWithFormatSuffix(otherDay, true);
      expect(val).toContain('Sunday (02nd April)');
    });

    it('should convert date based upon UTC/BST time zone', () => {
      (datePipe.transform as jasmine.Spy).and.callFake((date) => {
        return 'Sunday (25 June) 20:00';
      });
      (locale.getString as jasmine.Spy).and.callFake((date) => {
        return 'th';
      });
      service['findDifferenceBetweenUTCAndBST'] = jasmine.createSpy('findDifferenceBetweenUTCAndBST').and.returnValue(2);
      const otherDay = new Date("2023-06-25 20:00:00");
      const val = service.getDatetimeWithFormatSuffix(otherDay, false, true);
      expect(val).toEqual('Sunday (25th June) - 20:00');
    });
  });

  it('should return time difference', () => {
    const value = service['findDifferenceBetweenUTCAndBST']();
    expect(value).not.toBeNaN();
  });

  it('should return time difference', () => {
    service.formatDateByTimeZone = jasmine.createSpy('NaN');
    const value = service['findDifferenceBetweenUTCAndBST']();
    expect(value).toBe(0);
  });

  afterEach(() => {
    jasmine.clock().uninstall();
  });
});
