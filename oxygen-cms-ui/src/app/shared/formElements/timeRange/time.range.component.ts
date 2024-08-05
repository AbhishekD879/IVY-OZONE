import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'time-range',
  templateUrl: './time.range.component.html',
  styleUrls: ['./time.range.component.scss']
})
export class TimeRangeComponent implements OnInit {
  @Input() set startTime(value: string) {
    this.setDayTime(value, 'start');
  };
  @Input() set endTime(value: string) {
    this.setDayTime(value, 'end');
  };
  @Output() onTimeUpdate: EventEmitter<any> = new EventEmitter();
  disableFlag?: boolean = false;
  errorTimeoutId: number;

  defaultPlaceholder: string = 'Choose Date';
  chosenDate: any;
  chosenStartTime: any = {
    hh: '00',
    mm: '00',
    ss: '00'
  };

  chosenEndTime: any = {
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

    this.handleTimeChange()
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

  ngOnInit() { }
  setDayTime(value, type) {
    if (type == 'start') {
      this.chosenStartTime.hh = value?.hh || '00';
      this.chosenStartTime.mm = value?.mm || '00';
      this.chosenStartTime.ss = value?.ss || '00';
    }

    if (type == 'end') {
      this.chosenEndTime.hh = value?.hh || '00';
      this.chosenEndTime.mm = value?.mm || '00';
      this.chosenEndTime.ss = value?.ss || '00';
    }
  }

  handleTimeChange() {
    this.onTimeUpdate.emit({
      startTime: this.chosenStartTime,
      endTime: this.chosenEndTime
    });
  }
}
