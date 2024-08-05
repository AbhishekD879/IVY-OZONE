import { DateAgoPipe } from '@lazy-modules/timeline/pipes/dateAgo/date-ago.pipe';
import { of as observableOf } from 'rxjs';

describe('DateAgoPipe', () => {
  let pipe;

  const timeService = {
    getEventTime: jasmine.createSpy('getEventTime').and.returnValue('>1 hour')
  } as any;

  const changeDetectorRef = {
    detectChanges: jasmine.createSpy('detectChanges'),
    markForCheck: jasmine.createSpy('markForCheck'),
    detach: jasmine.createSpy('detach'),
  } as any;

  beforeEach(() => {
    pipe = new DateAgoPipe(changeDetectorRef, timeService);
    jasmine.clock().mockDate(new Date('2020-01-01T12:00:00.976Z'));
  });

  it('should return \'just now\'', () => {
    const result = pipe.transform(new Date());
    expect(result).toBe('Just now');
  });

  it('should return \'1 minute\'', () => {
    const result = pipe.transform('2020-01-01T11:59:00.976Z');
    expect(result).toBe('1 minute');
  });

  it('should return \'2 minutes\'', () => {
    const result = pipe.transform('2020-01-01T11:58:00.976Z');
    expect(result).toBe('2 minutes');
  });

  it('should return full date', () => {
    const result = pipe.transform('2020-01-01T11:00:00.976Z');
    expect(result).toBe('>1 hour');
  });

  it('should return full date #2', () => {
    const result = pipe.transform('2020-01-01T10:00:00.976Z');
    expect(result).toBe('>1 hour');
  });
  it('should return undefined', () => {
    const result = pipe.transform(undefined);
    expect(result).toBe(undefined);
  });
  it('should return undefined if timer was not defined', () => {
    pipe['timer'] = observableOf(undefined);
    const result = pipe.transform('2020-01-01T10:00:00.976Z');
    expect(result).toBeUndefined();
  });
  it('should return Just now if minutes < 0', () => {
    pipe['timer'] = observableOf(undefined);
    const result = pipe.transform('2020-01-01T11:59:30.976Z');
    expect(result).toBeUndefined('Just now');
  });
  it('ngOnDestroy', () => {
    const parentngOnDestroy = spyOn(DateAgoPipe.prototype['__proto__'], 'ngOnDestroy');
    pipe.ngOnDestroy();
    expect(parentngOnDestroy).toHaveBeenCalled();
  });
});
