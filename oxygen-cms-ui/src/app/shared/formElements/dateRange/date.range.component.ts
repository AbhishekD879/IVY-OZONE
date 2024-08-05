import { Component, EventEmitter, Input, Output, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { DateRange } from '@app/client/private/models/dateRange.model';

@Component({
  selector: 'date-range',
  templateUrl: './date.range.component.html',
  styleUrls: ['./date.range.component.scss']
})
export class DateRangeComponent implements OnInit, OnChanges {
  @Input() isSetDateButtons: boolean;
  @Input() startPlaceholder?: string;
  @Input() endPlaceholder?: string;
  @Input() placeholderColumn?: boolean;
  @Input() startDate?: string;
  @Input() endDate?: string;
  @Input() isSecondsEnabled?: boolean = true;
  @Input() isStartDateEnable?: boolean = false;
  @Input() isEndDateEnable?: boolean = false;
  @Input() checkEndDateEnable?: boolean = false;


  minEndDate: Date;
  maxStartDate: Date;
  errorMessage: string;

  @Output() onDateUpdate: EventEmitter<DateRange> = new EventEmitter();
  @Output() onEndDateUpdate: EventEmitter<string> = new EventEmitter();

  constructor() {}

  handleDateChange(date: string, timeType: string) {
    if (timeType === 'start') {
      this.startDate = date;
      this.minEndDate = this.getConvertedDate(date);
    }

    if (timeType === 'end') {
      this.endDate = date;
      this.maxStartDate = this.getConvertedDate(date);
    }

    this.onDateUpdate.emit({
      startDate: this.startDate,
      endDate: this.endDate
    });
  }

  getConvertedDate(date) {
    const dateNow = new Date();
    return new Date(new Date(date).getTime() + (dateNow.getTimezoneOffset() * 60000));
  }

  /**
   * Create default today values because we need to control start/end date ranges.
   */
  createInitialDate() {
    const today = new Date();
    const tomorrow = new Date(new Date().setDate(new Date().getDate() + 1));

    if (!this.isSecondsEnabled) {
      today.setUTCSeconds(0);
      tomorrow.setUTCSeconds(0);
    }

    if (!this.startDate) { this.startDate = today.toISOString(); }
    if (!this.endDate) { this.endDate = tomorrow.toISOString(); }

    setTimeout(() => {
      this.onDateUpdate.emit({
        startDate: this.startDate,
        endDate: this.endDate
      });
    });
  }

  ngOnInit() {
    if (!this.startDate || !this.endDate) {
      this.createInitialDate();
    }

    if (new Date(this.endDate) < new Date(this.startDate)) {
      this.endDate = this.startDate;
    }

    this.minEndDate = new Date(this.startDate);
    this.maxStartDate = new Date(this.endDate);

    if (this.checkEndDateEnable) {
      this.setEndDateNull();
    }
  }

  setEndDateNull(): void {
    this.maxStartDate = null;
    this.endDate = '';
  }

  setEndateToCurrentDate(): void {
    if (!this.endDate || this.startDate > this.endDate) {
      this.endDate = new Date(new Date().setDate(new Date(this.startDate).getDate() + 1)).toISOString();
    }
    this.maxStartDate = new Date(this.endDate);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if(changes.checkEndDateEnable) {
      changes.checkEndDateEnable.currentValue ? this.setEndDateNull() : this.setEndateToCurrentDate();
      this.onEndDateUpdate.emit(this.endDate);
    }
  }

}
