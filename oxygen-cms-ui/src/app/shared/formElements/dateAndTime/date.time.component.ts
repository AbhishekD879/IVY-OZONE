import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';

@Component({
  selector: 'date-time-inputs',
  templateUrl: './date.time.component.html',
  styleUrls: ['./date.time.component.scss']
})
export class DateAndTimeComponent implements OnInit {
  @Input() isSetDateButtons?: boolean;
  @Input() validationError?: string;
  @Input() placeholder?: string;
  @Input() placeholderColumn?: boolean;
  @Input() set initialDate(value:string){
    this.setDayTime(value);
  };
  @Input() max?: Date;
  @Input() min?: Date;
  @Input() required: boolean = false;
  @Input() isSecondsEnabled?: boolean = true;
  @Input() disableFlag?: boolean = false;
  @Output() outputIsoTime: EventEmitter<any> = new EventEmitter();
  @Input() disabled?: boolean = false;

  errorTimeoutId: number;

  defaultPlaceholder: string = 'Choose Date';
  chosenDate: any;
  chosenTime: any = {
    hh: '00',
    mm: '00',
    ss: '00'
  };

  /**
   * Properties for setting today/tomorrow dates via today/tomorrow buttons.
   * @type {Date}
   */
  todayInitialDate: Date = new Date();
  tomorrowInitialDate: Date;

  constructor() {
    const clonedTodayDate = new Date(this.todayInitialDate.getTime());

    // set tomorrow date strictly from today`s date to fit in day range;
    this.tomorrowInitialDate = new Date(new Date(clonedTodayDate).setDate(new Date(clonedTodayDate).getDate() + 1));
  }

  /**
   * Validate Hours and minutes values.
   * @param {Event} event
   */
  validateTime(event: any) {
    const maxValue = +event.target.max;
    const currentValue = +event.target.value;

    if (currentValue > maxValue) {
      event.target.value = maxValue;
    }

    event.target.value = this.transformTimeNumber(event.target.value);

    this.reCalculateDate();
  }

  reCalculateDate() {
    this.outputIsoTime.emit(this.getISODate());
  }


  /**
   * Use initial dates to set today/tomorrow dates via buttons
   * @param {string} day
   */
  setDate(day: string): void {
    switch (day) {
      case 'today':
        if ((!this.max || this.todayInitialDate <= this.max) && (!this.min || this.todayInitialDate >= this.min)) {
          this.validationError = undefined;
          this.chosenDate = this.todayInitialDate;
        } else {
          this.validationError = 'Can`t set Today`s date, wrong date range.';
        }
        break;
      case 'tomorrow':
        if ((!this.max || this.tomorrowInitialDate <= this.max) && (!this.min || this.tomorrowInitialDate >= this.min)) {
          this.chosenDate = this.tomorrowInitialDate;
        } else {
          this.validationError = 'Can`t set Tomorrow`s date, wrong date range.';
        }
        break;
    }

    if (this.validationError) {
      clearTimeout(this.errorTimeoutId);
      this.errorTimeoutId = window.setTimeout(() => this.validationError = undefined, 3000);
    }

    this.reCalculateDate();
  }

  /**
   * add Zero to numbers less that 10
   * @param number
   * @returns {string}
   */
  transformTimeNumber(number) {
    const parsedNumber = parseInt(number, 10);
    return parsedNumber < 10 ? '0' + parsedNumber : parsedNumber;
  }

   getISODate() {
    if (this.chosenDate.toString() === 'Invalid Date') {
      return;
    }
    const transformedYear = this.transformTimeNumber(this.chosenDate.getFullYear());
    const transformedMonth = this.transformTimeNumber(this.chosenDate.getMonth() + 1);
    const transformedDay = this.transformTimeNumber(this.chosenDate.getDate());
    const transformedHours = this.transformTimeNumber(this.chosenTime.hh);
    const transformedMinutes = this.transformTimeNumber(this.chosenTime.mm);
    const transformedSeconds = this.transformTimeNumber(this.chosenTime.ss);

    const currentZoneDate = `${transformedYear}-${transformedMonth}-${transformedDay}`;
    const timeZoneOffset = (this.chosenDate).getTimezoneOffset(); // user is setting time in local time zone
    const positiveOffset = Math.abs(timeZoneOffset);
    const timeOffsetInHours = -(timeZoneOffset / 60);
    const minutesOffset = (positiveOffset - Math.floor(timeOffsetInHours) * 60);
    const symbolOffset = timeZoneOffset >= 0 ? '-' : '+';

    const transformedOffsetHours = this.transformTimeNumber(timeOffsetInHours);
    const transformedOffsetMinutes = this.transformTimeNumber(minutesOffset);

    const currentZoneTime = `${transformedHours}:${transformedMinutes}:${transformedSeconds}`;
    const identifierTZD = `${symbolOffset}${transformedOffsetHours}:${transformedOffsetMinutes}`;

    return `${currentZoneDate}T${currentZoneTime}${identifierTZD}`;
  }

  setDayTime(dayTime) {
    const date = new Date(dayTime);
    this.chosenDate = date;
    this.chosenTime.hh = (date && date.getHours()) || 0;
    this.chosenTime.mm = (date && date.getMinutes()) || 0;
    this.chosenTime.ss = (date && date.getSeconds()) || 0;
  }

  ngOnInit() {}
}
