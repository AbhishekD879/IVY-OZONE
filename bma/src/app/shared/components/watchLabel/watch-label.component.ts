import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'watch-label',
  template: `<svg class="watch-icon-stream"><use xlink:href="#stream"></use></svg>
			       <span class="watch-live" data-crlat="watchLive" [i18n]="'app.watchLive'"></span>`,
  styleUrls: ['./watch-label.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class WatchLabelComponent {}

