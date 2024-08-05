import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'live-label-updated',
  template: `<div class="live-label"><svg class="inplay-icon"><use xlink:href="#live-icon"></use></svg><div class="live" [i18n]="'app.live'" data-crlat="liveLabel"></div></div>`,
  styleUrls: ['./live-label-updated.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LiveLabelUpdatedComponent { }

