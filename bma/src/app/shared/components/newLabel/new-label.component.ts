import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'new-label',
  template: `<span [i18n]="'app.new'"></span>`,
  styleUrls: ['./new-label.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class NewLabelComponent {}

