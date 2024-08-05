import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'live-label',
  template: `<span [i18n]="'app.live'" data-crlat="liveLabel"></span>`,
  styleUrls: ['./live-label.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LiveLabelComponent {}

