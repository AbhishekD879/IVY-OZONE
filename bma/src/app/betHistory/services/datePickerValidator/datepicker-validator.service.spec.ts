import { DatepickerValidatorService } from '@app/betHistory/services/datePickerValidator/datepicker-validator.service';
import { of } from 'rxjs';
describe('test DatepickerValidatorService', () => {
  let timeService, cmsService, datePipe;
  let service: DatepickerValidatorService;
  let errorState;

  beforeEach(() => {
    errorState = {
      startDateInFuture: false,
      endDateInFuture: false,
      moreThanOneYear: false,
      moreThanThreeMonthRange: false,
      moreThanFourYears: false,
      moreThanFourYearsRange: false,
      endDateLessStartDate: false,
      isValidstartDate: true,
      isValidendDate: true
    };

    timeService = {
      moreThanYears: jasmine.createSpy(),
      getFullMonthRange: jasmine.createSpy(),
      moreThanFourYearsRange: jasmine.createSpy()
    } as any;

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({}))
    } as any;

    datePipe = {
      transform: jasmine.createSpy().and.returnValue('2019-04-26')
    } as any;
    
    service = new DatepickerValidatorService(timeService, cmsService, datePipe);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#getDefaultErrorsState should return default error Object', () => {
    expect(service.getDefaultErrorsState()).toEqual(errorState);
  });

  it('#isDateRangeError should update values in error Object', () => {
    const datePickError = errorState;
    datePickError.isValidstartDate = false;
    service.updateErrorsState(errorState, datePickError, { value: new Date }, { value: new Date });
    expect(errorState).toEqual(jasmine.objectContaining({
      isValidstartDate: false
    }));
  });
  describe('isDateRangeError', () => {
    describe('should return True if', () => {
      beforeEach(() => {
        expect(service['isDateRangeError'](errorState)).toBeFalsy();
        expect(service['isDatePickerError'](errorState)).toBeFalsy();
      });

      it(`startDateInFuture error`, () => {
        errorState.startDateInFuture = true;
      });

      it(`moreThanThreeMonthRange error`, () => {
        errorState.moreThanThreeMonthRange = true;
      });

      it(`endDateLessStartDate error`, () => {
        errorState.endDateLessStartDate = true;
      });

      it(`moreThanOneYear error`, () => {
        errorState.moreThanOneYear = true;
      });

      afterEach(() => {
        expect(service['isDateRangeError'](errorState)).toBeTruthy();
        expect(service['isDatePickerError'](errorState)).toBeTruthy();
      });
    });
  });
  
  describe('initSystemConfig', () => {
    it('#config with true values', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        MyBetsDateLimit: {
          cashout: 50,
          maxValue: 50
        }
      }));
      service.initSystemConfig('cashout').subscribe((result) => {
        expect(result).toEqual({minDate: '2019-04-26', maxDate: '2019-04-26'});
      });
    });
    it('#config with null values', () => {
      cmsService.getSystemConfig.and.returnValue(of(undefined));
      service.initSystemConfig('cashout').subscribe(() => {
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
      });
    });
  });
  describe('isFourYearsDateRangeError', () => {
    describe('should return True if', () => {
      beforeEach(() => {
        expect(service['isFourYearsDateRangeError'](errorState)).toBeFalsy();
        expect(service['isFourYearsDatePickerError'](errorState)).toBeFalsy();
      });

      it(`startDateInFuture error`, () => {
        errorState.startDateInFuture = true;
      });

      it(`moreThanFourYearsRange error`, () => {
        errorState.moreThanFourYearsRange = true;
      });

      it(`endDateLessStartDate error`, () => {
        errorState.endDateLessStartDate = true;
      });

      it(`moreThanFourYears error`, () => {
        errorState.moreThanFourYears = true;
      });

      afterEach(() => {
        expect(service['isFourYearsDateRangeError'](errorState)).toBeTruthy();
        expect(service['isFourYearsDatePickerError'](errorState)).toBeTruthy();
      });
    });
  });

  it('#isDateRangeError should check input dates range condition', () => {
    expect(service['isDateRangeError'](errorState)).toBeFalsy();
    errorState.startDateInFuture = true;
    expect(service['isDateRangeError'](errorState)).toBeTruthy();
  });

  it('#isFourYearsDateRangeError should check input dates range condition', () => {
    expect(service['isFourYearsDateRangeError'](errorState)).toBeFalsy();
    errorState.startDateInFuture = true;
    expect(service['isFourYearsDateRangeError'](errorState)).toBeTruthy();
  });

  it('#isValidDatesEntered should check input dates for valid format', () => {
    expect(service['isValidDatesEntered'](errorState)).toBeTruthy();
    errorState.isValidstartDate = false;
    expect(service['isValidDatesEntered'](errorState)).toBeFalsy();

  });

  describe('addCustomErrors', () => {
    const date = new Date;

    it('#addCustomErrors when stardate and endDate are null', () => {
      errorState.endDateLessStartDate = true;
      service['addCustomErrors'](errorState, null, null);
  
      expect(timeService.moreThanYears).not.toHaveBeenCalledWith(date, 12);
      expect(timeService.moreThanYears).not.toHaveBeenCalledWith(date, 48);
    });

    it('#addCustomErrors clarify properties for errors object', () => {
      errorState.endDateLessStartDate = true;
      service['addCustomErrors'](errorState, { value: date }, { value: date });
      expect(errorState).toEqual(jasmine.objectContaining({
        endDateLessStartDate: false
      }));
      expect(timeService.moreThanYears).toHaveBeenCalledWith(date, 12);
      expect(timeService.moreThanYears).toHaveBeenCalledWith(date, 48);
    });

    it(`moreThanThreeMonthRange should equal true if  moreThanOneYear equal true`, () => {
      timeService.moreThanYears.and.returnValue(true);
      timeService.moreThanYears.and.returnValue(true);

      service['addCustomErrors'](errorState, { value: date }, { value: date });

      expect(errorState.moreThanThreeMonthRange).toBeTruthy();
      expect(timeService.getFullMonthRange).not.toHaveBeenCalled();
    });

    describe('moreThanThreeMonthRange should equal True if getFullMonthRange return value >= 3', () => {
      beforeEach(() => {
        timeService.moreThanYears.and.returnValue(false);
      });

      it(`getFullMonthRange return`, () => {
        timeService.getFullMonthRange.and.returnValue(12);
      });

      it(`getFullMonthRange return`, () => {
        timeService.getFullMonthRange.and.returnValue(13);
      });

      afterEach(() => {
        service['addCustomErrors'](errorState, { value: date }, { value: date });

        expect(errorState.moreThanThreeMonthRange).toBeTruthy();
        expect(timeService.getFullMonthRange).toHaveBeenCalled();
      });
    });

    describe('moreThanFourYearsRange should equal True if getFullMonthRange return value >= 48', () => {
      beforeEach(() => {
        timeService.moreThanYears.and.returnValue(false);
      });

      it(`getFullMonthRange return`, () => {
        timeService.getFullMonthRange.and.returnValue(48);
      });

      it(`getFullMonthRange return`, () => {
        timeService.getFullMonthRange.and.returnValue(49);
      });

      afterEach(() => {
        service['addCustomErrors'](errorState, { value: date }, { value: date });

        expect(errorState.moreThanThreeMonthRange).toBeTruthy();
        expect(timeService.getFullMonthRange).toHaveBeenCalled();
      });
    });

    it(`moreThanThreeMonthRange should equal True if getFullMonthRange return value < 3`, () => {
      timeService.moreThanYears.and.returnValue(false);
      timeService.getFullMonthRange.and.returnValue(0);

      service['addCustomErrors'](errorState, { value: date }, { value: date });

      expect(errorState.moreThanThreeMonthRange).toBeFalsy();
      expect(timeService.getFullMonthRange).toHaveBeenCalled();
    });

    it(`moreThanFourYearsRange should equal True if getFullMonthRange return value < 3`, () => {
      timeService.moreThanYears.and.returnValue(false);
      timeService.getFullMonthRange.and.returnValue(0);

      service['addCustomErrors'](errorState, { value: date }, { value: date });

      expect(errorState.moreThanFourYearsRange).toBeFalsy();
      expect(timeService.getFullMonthRange).toHaveBeenCalled();
    });
  });
});
