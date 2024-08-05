import { Component } from '@angular/core';
import { DatePickerComponent as CoralDatePickerComponent } from '@app/shared/components/datePicker/date-picker.component';

@Component({
  selector: 'date-picker',
  templateUrl: 'date-picker.component.html',
  styleUrls: ['date-picker.component.scss']
})

export class DatePickerComponent extends CoralDatePickerComponent {}
