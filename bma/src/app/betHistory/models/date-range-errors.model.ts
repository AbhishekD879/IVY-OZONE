export interface IDateRangeErrors {
  startDateInFuture: boolean;
  endDateInFuture: boolean;
  moreThanOneYear: boolean;
  moreThanThreeMonthRange: boolean;
  moreThanFourYears: boolean;
  moreThanFourYearsRange: boolean;
  endDateLessStartDate: boolean;
  isValidstartDate: boolean;
  isValidendDate: boolean;
}


