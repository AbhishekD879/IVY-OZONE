import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { TimeService } from '@core/services/time/time.service';
import { IDateRangeErrors } from '../../models/date-range-errors.model';
import { IDatePickerDate, IDatePickerMinMaxDates } from '../../models/date-picker-date.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { DatePipe } from '@angular/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class DatepickerValidatorService {

  constructor(
    private timeService: TimeService,
    private cmsService: CmsService,
    private datePipe: DatePipe) {
  }

  getDefaultErrorsState(): IDateRangeErrors {
    return {
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
  }

  updateErrorsState(errorsState: IDateRangeErrors, datePickerErrors: IDateRangeErrors,
                    startDate: IDatePickerDate, endDate: IDatePickerDate) {
    _.extend(errorsState, datePickerErrors);
    this.addCustomErrors(errorsState, startDate, endDate);
  }

  /** Check if DatePicker error
   * @return {boolean}
   */
  isDatePickerError(errorsState: IDateRangeErrors): boolean {
    return this.isDateRangeError(errorsState) || !this.isValidDatesEntered(errorsState);
  }

  /**
   * Check if date range error
   * @return {boolean}
   */
  private isDateRangeError(errorsState: IDateRangeErrors): boolean {
    return errorsState.startDateInFuture
      || errorsState.moreThanThreeMonthRange
      || errorsState.endDateLessStartDate
      || errorsState.moreThanOneYear;
  }
  /** Check if DatePicker error for Cashout and Openbets
   * @return {boolean}
   */
  isFourYearsDatePickerError(errorsState: IDateRangeErrors): boolean {
    return this.isFourYearsDateRangeError(errorsState) || !this.isValidDatesEntered(errorsState);
  }
  /**
   * Check if date range error for Cashout and Openbets
   * @return {boolean}
   */
  private isFourYearsDateRangeError(errorsState: IDateRangeErrors): boolean {
    return errorsState.startDateInFuture
      || errorsState.moreThanFourYearsRange
      || errorsState.endDateLessStartDate
      || errorsState.moreThanFourYears;
  }
  private isValidDatesEntered(errorsState: IDateRangeErrors): boolean {
    return errorsState.isValidendDate && errorsState.isValidstartDate;
  }

  private addCustomErrors(errorsState: IDateRangeErrors, startDate, endDate): void {
    if (!startDate || !endDate) {
      return;
    }
    errorsState.endDateLessStartDate = startDate.value > endDate.value;
    errorsState.moreThanOneYear = this.timeService.moreThanYears(startDate.value, 12);
    errorsState.moreThanFourYears = this.timeService.moreThanYears(startDate.value, 48);

    errorsState.moreThanThreeMonthRange = errorsState.moreThanOneYear
      ? true
      : this.timeService.getFullMonthRange(startDate.value, endDate.value) >= 12;
    errorsState.moreThanFourYearsRange = errorsState.moreThanFourYears
      ? true
      : this.timeService.getFullMonthRange(startDate.value, endDate.value) >= 48;
  }
  /**
   * Init Datepicker range
   */
   initSystemConfig(selectedTab: string): Observable<IDatePickerMinMaxDates> {
    let minDate = '', maxDate = '';
    return this.cmsService.getSystemConfig().pipe(
      map((config: ISystemConfig) => {
      if (config?.MyBetsDateLimit?.maxValue && config.MyBetsDateLimit[selectedTab]) {
        const dateLimit = config.MyBetsDateLimit[selectedTab];
        const maxValue = config.MyBetsDateLimit.maxValue; 
        if (dateLimit > 0 && dateLimit <= maxValue) {
          minDate = this.datePipe.transform(new Date().setFullYear(new Date().getFullYear() - dateLimit), 'yyyy-MM-dd');
          maxDate = this.datePipe.transform(new Date().setFullYear(new Date().getFullYear() + dateLimit), 'yyyy-MM-dd');
        }
      }
      return { minDate, maxDate };
    })); 
  }
}
