import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { TimeService } from '@core/services/time/time.service';
import { IDateRangeErrors } from '@app/betHistory/models/date-range-errors.model';
import * as _ from 'underscore';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'date-picker',
  templateUrl: 'date-picker.component.html',
  styleUrls: ['date-picker.component.scss']
})

export class DatePickerComponent implements OnInit {
  @Input() date: { value: Date | null | undefined };
  @Input() dateType: string;
  @Input() label: string = '';
  @Input() minDate: string;
  @Input() maxDate: string;

  @Output() readonly errorStateData: EventEmitter<IDateRangeErrors> = new EventEmitter();

  isDatePickerOpened: boolean;

  private errorState: IDateRangeErrors = {} as IDateRangeErrors;

  constructor(
    private timeService: TimeService,
    private rendererService: RendererService
  ) { }

  ngOnInit(): void {
    this.setDate();
  }

  /**
   * Set and Validate Date on Change
   */
  onChange(date: string): void {
    if (date) {
      const dateParts = date.split('/');
      this.date.value = date.indexOf('/') === -1 ? new Date(date) :
        new Date(+dateParts[2], Number(dateParts[1]) - 1, +dateParts[0]);
      this.setDate();
      this.validateDate();
      this.setInactive();
    }
  }

  /**
   * Set open-state for Date Picker
   */
  setActive(): void {
    this.isDatePickerOpened = true;
  }

  /**
   * Set close-state for Date Picker
   */
  setInactive(): void {
    this.isDatePickerOpened = false;
  }

  /**
   * Formats date to DD/MM/YYYY.
   */
  formatDate(date = new Date(), format: string = 'dd/MM/yyyy'): string {
    return this.timeService.formatByPattern(date, format);
  }

  /**
   * Checks whether browser supports <input type="date">.
   * @private
   */
  get isDateSupports(): boolean {
    const input: { value: any } = this.rendererService.renderer.createElement('input');
    const notADateValue: string = 'not-a-date';
    this.rendererService.renderer.setAttribute(input, 'type', 'date');
    this.rendererService.renderer.setAttribute(input, 'value', notADateValue);

    return (input.value !== notADateValue);
  }
  set isDateSupports(value:boolean){}

  private setDate(): void {
    const date: Date = this.date.value;
    this.date.value = (date === null || date === undefined) ? new Date() : date;
    if (date) {
      this.date.value = this.dateType === 'startDate' ?
      new Date(date.setHours(0, 0, 0, 0))
      : new Date(date.setHours(23, 59, 59, 999));
    }
  }

  private validateDate(): void {
    const today: number = (new Date()).setHours(23, 59, 59, 999);
    const date: number = this.date.value.getTime();
    this.errorState[`${this.dateType}InFuture`] = Boolean(date > today);
    this.errorState[`isValid${this.dateType}`] = _.isNumber(date);
    this.errorStateData.emit(this.errorState);
  }
}
