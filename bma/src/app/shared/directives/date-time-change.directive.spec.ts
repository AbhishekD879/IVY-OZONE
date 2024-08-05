
import { DateTimeChangeDirective } from './date-time-change.directive';

describe('DateTimeChangeDirective', () => {
  let directive: DateTimeChangeDirective;

  let timeService;
  beforeEach(() => {

    timeService = {
    convertDateStr: jasmine.createSpy('convertDateStr'),
    formatByPattern: jasmine.createSpy('formatByPattern'),
    getDatetimeWithFormatSuffix: jasmine.createSpy('getDatetimeWithFormatSuffix').and.returnValue(new Date())
    };
    directive = new DateTimeChangeDirective(timeService);
  });

  it('should call the innerText method for today date', () => {
    const date = new Date().toLocaleDateString();
    directive.dateTimeFmt = new Date().toLocaleDateString();
    directive.showTime = true;
    timeService.convertDateStr.and.returnValue(date);
    timeService.formatByPattern.and.returnValue(date);
    timeService.getDatetimeWithFormatSuffix.and.returnValue(date);
    const val = directive.innerText;
    expect(val).toEqual(date);
  });
});

